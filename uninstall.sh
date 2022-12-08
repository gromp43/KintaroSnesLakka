#!/bin/bash
systemctl stop kintaro.service
systemctl disable kintaro.service
rm -f /storage/.config/system.d/kintaro.service 
rm -Rf /storage/kintaro/
