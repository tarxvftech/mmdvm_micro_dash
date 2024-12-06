import asyncio
from paho.mqtt import client as mqtt_client

async def broadcast(message):
    for client in clients:
        await client.send_json(message)

async def mqtt_loop():
    def on_message(client, userdata, msg):
        line = msg.payload.decode()
        asyncio.create_task(broadcast({msg.topic: line}))
    mqtt_client_instance.on_message = on_message
    mqtt_client_instance.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client_instance.subscribe(MQTT_TOPIC_SUB)
    mqtt_client_instance.loop_start()
    while True:
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(mqtt_loop())

mQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "logs/#"
MQTT_TOPIC_PUB = "logs/output"
mqtt_client_instance = mqtt_client.Client("log_tailer")

if __name__ == "__main__":
    mqtt_client_instance.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client_instance.subscribe(MQTT_TOPIC_SUB)
    mqtt_client_instance.loop_start()
