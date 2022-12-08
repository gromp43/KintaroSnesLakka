#!/bin/bash

mkdir /storage/kintaro
cp -i pcb.py /storage/kintaro/pcb.py
chmod +x /storage/kintaro/pcb.py
cp -i kintaro.service /storage/.config/system.d/kintaro.service
systemctl enable kintaro.service
