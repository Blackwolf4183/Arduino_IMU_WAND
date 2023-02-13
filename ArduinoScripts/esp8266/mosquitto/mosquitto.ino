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

void setup() {
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
  client.publish(topic, "ESP8266 up and running");
}

void callback(char *topic_received, byte *payload, unsigned int length) {
  /* Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
      Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------"); */

  //Send callback info to arduino nano
  if (!strcmp(topic_received, topic)) {
        if (!strncmp((char *)payload, "successful", length)) {
          //server accepted instruction
          Serial.println("successful");
        } else if (!strncmp((char *)payload, "error", length)) {
          //something went wrong on server
          Serial.println("error");
        }else if (!strncmp((char *)payload, "lumos", length)) {
          //Server recognized lumos
          Serial.println("lumos");
        }
    }

}


void loop() {
  client.loop();

        
  if(Serial.available() > 0 ){
      
      String read = Serial.readStringUntil('\n');
      const char * values = read.c_str();
      client.publish(topic, values);
  }else{
      //si no hay datos esperamos 100msg a que vuelva a haber
      delay(100);
  }
}
