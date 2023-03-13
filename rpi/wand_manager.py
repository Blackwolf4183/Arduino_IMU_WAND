import paho.mqtt.client as mqtt
import time
import CNN
import DataProcessing

#TODO: CHANGE TO 192.168.1.120
# Mqtt server IP
broker_address = "192.168.1.120"

#Message string over mqtt
message = ""
#Sequence of data
sequence = []
#Checks if currently receiving sequence
onSequence = False


def on_message(client, userdata, message):
    global onSequence, sequence

    #Decode message
    message = str(message.payload.decode("utf-8"))
    message = message.strip()
    print("\tmessage received:", message)

    #Search for "sequence" word to start "recording" sequence
    if message == "Sequence":
        if not onSequence: 
            onSequence = True
            #Error if received two simultaneous sequences
        else: print("Error sequence received while on sequence") 
    #If we are already on a sequence
    elif onSequence:
        #All data sent (sequences of length 20) (19 is the last one received)
        if len(sequence) == 19:

            #TODO: add one more sequence?
            onSequence = False
            print("#######  Sequence completed  #######")
            #Process the data in the covolutional neural network

            #TODO: for now only
            DataProcessing.process_image(sequence)
            

            #result = CNN.processData(sequence)
            #TODO: print over mqtt channel the result 
            #print("NEURAL NETWORK RESULT: ", result) 

            time.sleep(1)

            client.publish("wand_sensor", "successful")


            #Clear sequence for incoming ones
            sequence.clear()
        else:
            #Unpack values
            try:
                values = message.split(",")
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
                client.publish("wand_sensor", "error")   
                onSequence = False

    else:
        if message == "Starting conexion":
            time.sleep(5)
            client.publish("wand_sensor", "successful")    
        elif message != "ESP8266 up and running" and message != "lumos" and message != "error" and message != "successful":
            print("error")


    message_received = True
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global connected
        connected = True
        print("Connected")
        print("#########")
    else:
        print("Unable To Connect")
        


# ------------- Connection with Mqtt server ----------------

connected = False
message_received = False

print("Creating new instance")
client = mqtt.Client("MQTT")

client.on_message = on_message
client.on_connect = on_connect

print("Connecting to broker: ", broker_address)
client.connect(broker_address, port=1883)

client.loop_start()

print("Subscribing to topic", "wand_sensor")
client.subscribe("wand_sensor")

while connected != True or message_received != True:
    time.sleep(0.2)

client.loop_forever()
