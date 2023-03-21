#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi
const char *ssid = "MOVISTAR_9770"; // Enter your WiFi name
const char *password = "fGYCSuPWiQdAvQvPfhLv";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "192.168.1.120";
const char *topic = "wand_sensor";
const char *mqtt_username = NULL;
const char *mqtt_password = NULL;
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

const int ledPin = 1; 

void setup() {
  pinMode (ledPin, OUTPUT);
  pinMode (0, OUTPUT);
  pinMode (2, OUTPUT);
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
  client.publish(topic, "ESP8266 LED up and running");
}



void callback(char *topic_received, byte *payload, unsigned int length) {


  //Send callback info to arduino nano
  if (!strcmp(topic_received, topic)) {
        if (!strncmp((char *)payload, "successful", length)) {
          //server accepted instruction
          digitalWrite(ledPin, HIGH); // LED on
          digitalWrite(0, HIGH); // LED on
          digitalWrite(2, HIGH); // LED on
          Serial.print("LED ON");
        } else if (!strncmp((char *)payload, "error", length)) {
          //something went wrong on server
          digitalWrite(ledPin, LOW); // LED OFF
          digitalWrite(0, LOW); // LED OFF
          digitalWrite(2, LOW); // LED OFF
          Serial.print("LED OFF");
        }
    }

}


void loop() {
  client.loop();     
  delay(100); 
  
}
