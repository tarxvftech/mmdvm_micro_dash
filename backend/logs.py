import sys
import json
import asyncio
from collections import deque
from typing import Dict, Deque, List

from paho.mqtt import client as mqtt_client

class LogMonitor:
    def __init__(self, log_files: List[str], history_size: int = 10000):
        self.log_files = log_files
        self.history_size = history_size
        self.queues: Dict[str, asyncio.Queue] = {file: asyncio.Queue() for file in log_files}
        self.history: Dict[str, Deque] = {file: deque(maxlen=history_size) for file in log_files}
        self.processes = {}
        self.tasks: List[asyncio.Task] = []
        self.stop_event = asyncio.Event()

    async def tail(self, file: str):
        cmd = "cmd://"
        if file.startswith(cmd):
            process = await asyncio.create_subprocess_exec(
                *(file[len(cmd):].split()),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        else:
            process = await asyncio.create_subprocess_exec(
                'tail', '-F', file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        self.processes[file] = process
        while not self.stop_event.is_set():
            line = await process.stdout.readline()
            if line:
                await self.queues[file].put(line.decode().strip())
            else:
                break

    async def consume_logs(self,cb=None):
        while not self.stop_event.is_set():
            for file, queue in self.queues.items():
                while not queue.empty():
                    line = await queue.get()
                    print(line)
                    self.history[file].append(line)
                    if cb:
                        print(cb,file)
                        # await cb(file,line)
                        asyncio.create_task(cb(file,line))
            await asyncio.sleep(0.01)

    async def start(self,cb=None):
        for file in self.log_files:
            task = asyncio.create_task(self.tail(file))
            self.tasks.append(task)
        consumer_task = asyncio.create_task(self.consume_logs(cb))
        self.tasks.append(consumer_task)
        print("started")

    async def stop(self):
        self.stop_event.set()
        for process in self.processes.values():
            process.terminate()
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def run(self,*args,**kwargs):
        await self.start(*args,**kwargs)
        await self.stop_event.wait()

with open("config.ini","r") as fd:
    config = json.load(fd)
MQTT_BROKER = config["mqtt"]["host"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_TOPIC_PRE = config["mqtt"]["prefix"]
MQTT_TOPIC_SUB = MQTT_TOPIC_PRE + "#"
mqtt_client_instance = mqtt_client.Client(client_id="log_tailer",callback_api_version=2)

async def pub(file,line):
    print("PUB",file,line)
    t = MQTT_TOPIC_PRE + file
    mqtt_client_instance.publish(t,line)

async def mqtt_loop():
    def on_message(client, userdata, msg):
        line = msg.payload.decode()
        print(client,userdata,msg,line)
        # asyncio.create_task(broadcast({msg.topic: line}))
    mqtt_client_instance.on_message = on_message
    mqtt_client_instance.connect(MQTT_BROKER, MQTT_PORT)
    # mqtt_client_instance.subscribe(MQTT_TOPIC_SUB)
    mqtt_client_instance.loop_start()
    print("Ready!")
    while True:
        await asyncio.sleep(1)


async def main():
    log_files = ["/var/log/X.0.log", "test.log"]
    log_files = ["test.log","/var/log/X.0.log","cmd://journalctl -f","cmd://dmesg -w"]
    monitor = LogMonitor(log_files)
    try:
        mr = asyncio.create_task(monitor.run(pub))
        mq = asyncio.create_task(mqtt_loop())
        await asyncio.gather(mr,mq)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    asyncio.run(main())


