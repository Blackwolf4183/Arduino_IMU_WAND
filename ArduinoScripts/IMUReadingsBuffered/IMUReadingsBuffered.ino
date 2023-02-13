#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SoftwareSerial.h>

#define STACK_SIZE 20

const int buttonPin = 2;
//RGB Led
const int redPin = 3;
const int greenPin = 4;
const int bluePin = 5;

//Counter for the amount of sequences sent
int counter = 0;

// Number of colors used for animating, higher = smoother and slower animation)
int numColors = 255;

//Counter to keep track of led color
int ledCounter = 0;
int buttonState = 0;
//Led to notify gesture recording
bool ledOn = false;
//Control wether pushing the button does anything at all
bool canPushButton = true;

Adafruit_MPU6050 mpu;

//Serial communication with Esp8266 Setup
SoftwareSerial mySerial(10, 11);  // RX, TX


//Timers
const unsigned long mainLoopInterval = 100;
const unsigned long rgbInterval = 8;

unsigned long mainLoopTimer;
unsigned long rgbTimer;

void setup(void) {

  Serial.println("Starting program...");

  //Timers
  mainLoopTimer = millis();
  rgbTimer = millis();

  //Pin outputs
  pinMode(buttonPin, INPUT);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

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


  if((millis() - mainLoopTimer) >= mainLoopInterval){

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
      }
      
    }

    //Button
    buttonState = digitalRead(buttonPin);

    if (buttonState == HIGH && canPushButton) {
      Serial.println("Button has been pushed");
      toggle_led();
      mySerial.println("Sequence");
    }


    //#########################################################
    //Serial reading
    char* espSerial = "";
    int size;
    while(size = mySerial.available() > 0 ){
      char c = mySerial.read();
      espSerial += c;
    }

    Serial.println(espSerial);

    /* if(!strncmp(espSerial, "successful",size)){
      for(int i = 0;i<4;i++){
        setColor(0, 255, 0);
        delay(500);
        setColor(0, 0, 0);
      }
  
    }else if(!strncmp(espSerial, "error",size)){
      for(int i = 0;i<4;i++){
        setColor(255, 0, 0);
        delay(500);
        setColor(0, 0, 0);
      }
    }else if(!strncmp(espSerial, "lumos",size)){
      setColor(255, 255, 255);
      delay(3000);
      setColor(0, 0, 0);
    } */
    //############################################

    mainLoopTimer = millis();
  }

  if((millis() - rgbTimer) >= rgbInterval){
    //RGB Led
    if(ledOn){
      float colorNumber = ledCounter > numColors ? ledCounter - numColors: ledCounter;
      
      //Led Brightness
      float brightness = 1; // Between 0 and 1 (0 = dark, 1 is full brightness)
      float saturation = 1; // Between 0 and 1 (0 = gray, 1 = full color)
      float hue = (colorNumber / float(numColors)) * 360; // Number between 0 and 360
      long color = HSBtoRGB(hue, saturation, brightness); 
      
      // Get the red, blue and green parts from generated color
      int red = color >> 16 & 255;
      int green = color >> 8 & 255;
      int blue = color & 255;

      setColor(red, green, blue);
      
      // Counter can never be greater then 2 times the number of available colors
      // the colorNumber = line above takes care of counting backwards (nicely looping animation)
      // when counter is larger then the number of available colors
      ledCounter = (ledCounter + 1) % (numColors * 2);
    }else{
      //If led not on just no color
      setColor(0,0,0);
    }

    rgbTimer = millis();
  }

  
}

//Toggle LED
void toggle_led() {
  ledOn = canPushButton;
  canPushButton = !canPushButton;
}

//Set RGB Led Color
void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin, redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin, blueValue);
}

long HSBtoRGB(float _hue, float _sat, float _brightness) {
    float red = 0.0;
    float green = 0.0;
    float blue = 0.0;
    
    if (_sat == 0.0) {
        red = _brightness;
        green = _brightness;
        blue = _brightness;
    } else {
        if (_hue == 360.0) {
            _hue = 0;
        }

        int slice = _hue / 60.0;
        float hue_frac = (_hue / 60.0) - slice;

        float aa = _brightness * (1.0 - _sat);
        float bb = _brightness * (1.0 - _sat * hue_frac);
        float cc = _brightness * (1.0 - _sat * (1.0 - hue_frac));
        
        switch(slice) {
            case 0:
                red = _brightness;
                green = cc;
                blue = aa;
                break;
            case 1:
                red = bb;
                green = _brightness;
                blue = aa;
                break;
            case 2:
                red = aa;
                green = _brightness;
                blue = cc;
                break;
            case 3:
                red = aa;
                green = bb;
                blue = _brightness;
                break;
            case 4:
                red = cc;
                green = aa;
                blue = _brightness;
                break;
            case 5:
                red = _brightness;
                green = aa;
                blue = bb;
                break;
            default:
                red = 0.0;
                green = 0.0;
                blue = 0.0;
                break;
        }
    }

    long ired = red * 255.0;
    long igreen = green * 255.0;
    long iblue = blue * 255.0;
    
    return long((ired << 16) | (igreen << 8) | (iblue));
}
