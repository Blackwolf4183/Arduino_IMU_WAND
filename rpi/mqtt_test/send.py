import paho.mqtt.publish as publish

broker_address = "192.168.1.120"

print("sending message")
publish.single("wand_sensor", "error", hostname=broker_address)
