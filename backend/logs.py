import asyncio
from collections import deque
from typing import Dict, Deque, List

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

    async def consume_logs(self):
        while not self.stop_event.is_set():
            for file, queue in self.queues.items():
                while not queue.empty():
                    line = await queue.get()
                    self.history[file].append(line)
                    #print(f"{file}: {line}")
            await asyncio.sleep(0.01)

    async def start(self):
        for file in self.log_files:
            task = asyncio.create_task(self.tail(file))
            self.tasks.append(task)
        consumer_task = asyncio.create_task(self.consume_logs())
        self.tasks.append(consumer_task)

    async def stop(self):
        self.stop_event.set()
        for process in self.processes.values():
            process.terminate()
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def run(self):
        await self.start()
        await self.stop_event.wait()

async def main():
    log_files = ["/var/log/X.0.log", "test.log"]
    monitor = LogMonitor(log_files)

    try:
        await monitor.run()
    except KeyboardInterrupt:
        await monitor.stop()

if __name__ == "__main__":
    asyncio.run(main())
