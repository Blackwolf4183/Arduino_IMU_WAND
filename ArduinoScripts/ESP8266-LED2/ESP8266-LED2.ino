#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi
const char *ssid = "MOVISTAR_9770"; // Enter your WiFi name
const char *password = "fGYCSuPWiQdAvQvPfhLv";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "192.168.1.120";
const char *topic = "smart_switch";
const char *mqtt_username = NULL;
const char *mqtt_password = NULL;
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

const int switch1 = 0;
const int switch2 = 2;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT); 
  pinMode (switch1, OUTPUT);
  pinMode (switch2, OUTPUT);
  
  // Both outputs on high so the relays start disconnected
  digitalWrite(switch1, HIGH);
  digitalWrite(switch2, HIGH);

  // Set software serial baud to 115200;
  Serial.begin(115200);
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  //connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
      String client_id = "esp8266-client-";
      client_id += String(WiFi.macAddress());
      Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
      if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
          Serial.println("Public emqx mqtt broker connected");
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
      }
  }
  //subscribe and publish
  client.subscribe(topic);
  client.publish(topic, "ESP8266 Smart_switch up and running");
}



void callback(char *topic_received, byte *payload, unsigned int length) {


  //Send callback info to arduino nano
  if (!strcmp(topic_received, topic)) {
        if (!strncmp((char *)payload, "switch1-on", length)) {
          //server accepted instruction
          digitalWrite(switch1, LOW); //swich 1 on 
          Serial.print("Switch 1 ON");
        } else if (!strncmp((char *)payload, "switch2-on", length)) {
          //something went wrong on server
          digitalWrite(switch2, LOW); //swich 2 on 
          Serial.print("Switch 2 ON");
        } else if (!strncmp((char *)payload, "switch1-off", length)) {
          //something went wrong on server
          digitalWrite(switch1, HIGH); //swich 1 off
          Serial.print("Switch 1 OFF");
        } else if (!strncmp((char *)payload, "switch2-off", length)) {
          //something went wrong on server
          digitalWrite(switch2, HIGH); //swich 1 off 
          Serial.print("Switch 2 OFF");
        }
    }

}


void loop() {
  client.loop();     
  delay(100); 
  
}
