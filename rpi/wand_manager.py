import paho.mqtt.client as mqtt
import time
import CNN

message = ""

#Sequence of data
sequence = []
onSequence = False




def on_message(client, userdata, message):
    global onSequence, sequence

    message = str(message.payload.decode("utf-8"))
    print("message received ", message)
    #TODO: Mirar si era mayus
    if message == "sequence":
        if not onSequence: 
            onSequence = True
        else: print("Error sequence received while on sequence")

    elif onSequence:

        if len(sequence) == 20:
            onSequence = False
            print("#######  e ha completado una secuencia  #######")
            result = CNN.processData(sequence)
            print("NEURAL NETWORK RESULT: ", result)
            sequence.clear()
        else:
            #Unpack values
            try:
                values = message.split(", ")
                aX = float(values[0]);
                aY = float(values[1])
                aZ = float(values[2])
                rX = float(values[3])
                rY = float(values[4])
                rZ = float(values[5])

                
                #Append values to sequence
                sequence.append([aX,aY,aZ,rX,rY,rZ])

            except Exception as e:
                print("There was an error unpacking or getting values")

    else:
        #TODO: another handling method?
        print("error")



    message_received = True
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        global connected
        connected = True
        print("Connected")
        print("..........")
    else:
        print("Unable To Connect")
        
connected = False
message_received = False
#TODO: CHANGE TO 192.168.1.120
broker_address = "localhost"

print("Creating new instance")
client = mqtt.Client("MQTT")

client.on_message = on_message
client.on_connect = on_connect

print("Connecting to broker")
client.connect(broker_address, port=1883)

client.loop_start()

print("Subscribing to topic", "wand_sensor")
client.subscribe("wand_sensor")

while connected != True or message_received != True:
    time.sleep(0.2)

client.loop_forever()
