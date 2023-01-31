#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SoftwareSerial.h>

#define STACK_SIZE 20

const int buttonPin = 2;
const int ledPin = 3;

//Counter for the amount of sequences sent
int counter = 0;
int buttonState = 0;
//Led to notify gesture recording
bool ledOn = false;
//Control wether pushing the button does anything at all
bool canPushButton = true;

Adafruit_MPU6050 mpu;

SoftwareSerial mySerial(10, 11);  // RX, TX

void setup(void) {

  Serial.println("Starting program...");

  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);

  Serial.begin(115200);
  while (!Serial)
    delay(10);  // will pause Zero, Leonardo, etc until serial console opens


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
  mySerial.println("Starting conexion");
}


void loop() {


  /* Get new sensor events with the readings */
  //if recording
  if (ledOn) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    String values = "";
    values = String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z) + "," + String(g.gyro.x) + "," + String(g.gyro.y) + "," + String(g.gyro.z);

    //Send over serial
    mySerial.println(values);
    counter++;

    Serial.println(counter);
    Serial.println(values);
    if (counter == STACK_SIZE) {
      //if buffer fills stop
      toggle_led();
      //restart counter
      counter = 0;
      //printStackToSerial();
    }
  }


  //Button
  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH && canPushButton) {
    Serial.println("Button has been pushed");
    toggle_led();
    mySerial.println("Sequence");
  }


  //Pick measurements each 100 ms
  delay(100);
}

//Toggle LED
void toggle_led() {
  ledOn = canPushButton;
  canPushButton = !canPushButton;
  digitalWrite(ledPin, ledOn);  // toggle the LED
}
