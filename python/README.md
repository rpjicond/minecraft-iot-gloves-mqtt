# Python Scripts – Minecraft IoT Automation

This folder contains all Python programs used to automate events inside Minecraft based on MQTT messages.

## Scripts

### `main.py`
Subscribes to MQTT topics and triggers actions inside Minecraft.
Initializes the world, players, map, and diamond.
Detects the winner when a player grabs the diamond.


### `appel_pouvoirs.py`
Implements superpowers activated by IoT buttons.
Implements negative effects (lava, TNT, obstacles).

## Requirements

sudo apt install python3-pip
pip3 install paho-mqtt mcpi

Works on Raspberry Pi OS (Buster/Bullseye).
