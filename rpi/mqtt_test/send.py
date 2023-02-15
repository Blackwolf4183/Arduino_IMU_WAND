# Code Written By Tech Notebook
# youtube.com/technotebook

import paho.mqtt.client as mqtt
import time

connected = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        connected = True
        print("Connected")
    else:
        print("Not Able To Connect")

broker_address = "192.168.1.120"


client = mqtt.Client("P1") 
client.on_connect = on_connect

client.connect(broker_address)
time.sleep(0.4)
client.loop_start()
while True:
    client.publish("wand_sensor", "lumos")
    time.sleep(5)
    client.publish("wand_sensor", "successful")
    time.sleep(5)
    client.publish("wand_sensor", "error")
    time.sleep(5)
    
client.loop_stop()


# Code Written By Tech Notebook
# youtube.com/technotebook