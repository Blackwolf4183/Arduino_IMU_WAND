#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <arduino-timer.h>

#define STACK_SIZE 20

const int buttonPin = 2;
const int ledPin = 3;
String stack[STACK_SIZE];

int top = -1;
int buttonState = 0;
//Timer to control recording time of movement
auto timer = timer_create_default();

Adafruit_MPU6050 mpu;

SoftwareSerial mySerial(10, 11); // RX, TX

void setup(void) {

  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);

  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens


  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  //Stablish ranges
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  //21 Khz bandwitdh
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  delay(100);


  //Serial Comunication with esp8266
  mySerial.begin(115200);
  mySerial.println("Comenzando conexion");
}

bool send = true;

void loop() {

  //Timer tick
  timer.tick();

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  String values = "";
  values = String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z) + "," + String(g.gyro.x) + "," + String(g.gyro.y) +"," + String(g.gyro.z) ;
  
  //detectar si hacemos un movimiento que pueda ser un gesto (quizas luego se implemente con un boton)
  if(a.acceleration.x > 15 || a.acceleration.y > 15 || a.acceleration.z > 15){
    if(send){
      //Serial.println("Se ha iniciado un movimiento");
      send = false;
      //dejamos solo 4 secuencias en el buffer
      while(top > 4){
        pop();
      }
    }

  }


  if(top == STACK_SIZE - 1){
    //que sigan pudiendo entrar valores 
    pop();
  }
  //colocamos nuevo valor al principio
  push_at_beginning(values);

  if(!send && top == STACK_SIZE - 1){

    Serial.println("Logeando movimiento");
    Serial.println("Valor antes top: " + top);
    //TODO: tenemos que enviar lo que tengamos en el buffer
    //de momento lo printeamos
    for(int i = 0;i<20;i++){
      String val = pop();
      mySerial.println(val);
      Serial.println(val);
    }

    send = true;
    Serial.println("Valor de top: " + top);
    delay(1000);
  }

  /* //mandamos al serial del esp8266 01
  mySerial.println(values);
  //printeamos por nuestro serial
  Serial.println(values); */

  //boton
  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) {
    Serial.println("Boton pulsado");
  } 


  delay(100);
}


//Toggle LED
bool toggle_led(void *) {
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN)); // toggle the LED
  return true; // keep timer active? true
}

//metodos para el stack
void push(String item) {
  if (top == STACK_SIZE - 1) {
    Serial.println("Error: Stack overflow");
    return;
  }
  stack[++top] = item;
}

void push_at_beginning(String item) {
  if (top == STACK_SIZE - 1) {
    Serial.println("Error: Stack overflow");
    return;
  }
  memmove(stack+1, stack, sizeof(String)*(top+1));
  stack[0] = item;
  top++;
}

String pop() {
  if (top == -1) {
    Serial.println("Error: Stack underflow");
    return "";
  }
  return stack[top--];
}