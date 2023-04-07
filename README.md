# Project Report

# Smart House and Pattern Recognition based on RPI and ESP8266.

## Introduction

In this report I want to showcase a recent project I did to test some practical and not so practical applications on Machine Learning and real world interactions. 

The inspiration for this project came to me when I saw on an online video a Harry Potter’s wand made by Warner Bros, which you could use to perform some “spells” with and it would connect to your smarthome to, for instance, turn on you lights or audio.

I thought the idea was pretty interesting, but I didn’t know the technology they were using to detect the gestures and transform them into orders. 

Still without any knowledge at all about the insights of the wand I supposed It had to use some kind of data gathering and some machine learning algorithm to infer the gestures.

I looked back to a module I had been meaning to use for another project, the MP6050.  The MP6050 is an IMU (Inertial Measurement Unit), which can provide data such as acceleration and angular velocity. 

I thought maybe there was a chance that if a collected the data from the IMU and run it through a Machine Learning Algorithm it could give me back information about which kind of gesture was made.

## Overview of the plan

The basic idea was to stuff some electronics in a custom made wand, so I could transmit wirelessly data from the MP6050 to some kind of server and process that data.

The first challenge was the size of the wand. I have some prior experience with electronics and circuits but none of the kind of making custom PCBs with integrated circuits, so I had to think of the smallest components I could use to get this working. The list is as follows:

- Arduino nano
- ESP8266 - 01 Wifi Module
- On/Off Switch
- 3.7V Lipo Battery
- RGB LED
- LM 1117 (for current reduction to 3.3V)
- 4 330 Ohms Resistors
- Different color cables
- Small Button
- TP4056 (for Lipo charging and discharging)
- 16V 1000**μF** Capacitor

One I had the list of components I made some schematics for the circuit:

![Untitled](Project%20Report%202bc13acfc28a4a3c82e0ae88a6d2ab34/Untitled.png)

Having all those components at hand I figured a common size wand from the Harry Potter’s Universe wasn’t going to cut it for the size, so with the help of **Blender** ( 3D Modeling tool) , and a base model I took from a 3D printing website, I altered the model so everything could fit inside nicely.

![Untitled](Project%20Report%202bc13acfc28a4a3c82e0ae88a6d2ab34/Untitled%201.png)

![Untitled](Project%20Report%202bc13acfc28a4a3c82e0ae88a6d2ab34/Untitled%202.png)

## Wireless Transmission System

The second challenge was to transmit all the data gathered by the wand trough my home wifi network into my **Raspberry Pi**, which would act as a server to manage al the data, and probably host a small webserver in the future. 

### Data format

Most Machine Learning algorithms work best with a fixed size input, so I had to think of a way to always have the same “amount” of data coming out of the ESP8266. The simplest solution to this was to have a button you would press in the wand so that it would start recording a particular amount of values. I estimated that a sequence of 20, 6 value vectors would suit my needs.

In the end I had sequenced that looked something like this:

 

|  | AccelerationX | AccelerationY | AccelerationZ | AngularX | AngularY | AngularZ |
| --- | --- | --- | --- | --- | --- | --- |
| t0 | 1.2234 | 9.862 | 4.5123 | 0.3523 | 12.903 | 1.643 |
| t1 | 2.2234 | 9.334 | 6.3456 | 0.3236 | 13.347 | 1.393 |
| t2 | 3.2345 | 9.646 | 7.2134 | 0.5523 | 14.384 | 2.234 |
| t3 | 2.2345 | 9.123 | 6.2345 | 0.6553 | 15.522 | 1.931 |
| t4 | 1.7856 | 9.002 | 5.3234 | 0.5563 | 16.332 | 1.000 |
| …. | ….. | …. | …. | … | … | … |
| t19 | 1.2345 | 9.005 | 6.2342 | 0.5523 | 16.342 | 1.123 |

### Setting up de Raspberry Pi

As mentioned earlier, the choice of “server” was the **Raspberry Pi 3B,** I decided to install Raspbian and run a MQTT mosquitto server on it. MQTT is a protocol used for machine-to-machine communication commonly seen in SmartHome applications.