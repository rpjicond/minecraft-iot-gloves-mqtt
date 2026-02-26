# ESP8266 Firmware – MQTT Button Controller

This folder contains the Arduino code used to run the IoT glove built with an **ESP8266 HUZZAH** board.

## Features
- Connects to WiFi
- Connects to MQTT broker with authentication
- Reads multiple push-buttons (GPIO)
- Publishes MQTT messages on button press
- Very low latency communication

## File
- `esp_gant1.ino` – main firmware
- `esp_gant2.ino` – main firmware

## Requirements
- Arduino IDE 1.8.x
- ESP8266 board package
- Libraries:
  - PubSubClient
  - ESP8266WiFi

## Uploading the Firmware
1. Open the `.ino` file
2. Select **Board: ESP8266 Feather HUZZAH**
3. Configure COM port
4. Upload

