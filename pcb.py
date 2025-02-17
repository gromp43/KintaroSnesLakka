#!/usr/bin/python3 -u
#Copyright 2017 Michael Kirsch

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import time
import os
import RPi.GPIO as GPIO

pcb_components={"LED":7,"FAN":8,"RESET":3,"POWER":5,"CHECK_PCB":10}

class path():
    kintaro_folder = "/storage/kintaro/"
    temp_command = 'vcgencmd measure_temp'

class vars():
    fan_hysteresis = 5
    fan_starttemp = 55
    reset_hold_short = 100
    reset_hold_long = 500
    debounce_time = 0.01
    counter_time = 0.01

GPIO.setmode(GPIO.BOARD) #Use the same layout as the pins
GPIO.setup(pcb_components["LED"], GPIO.OUT) #LED Output
GPIO.setup(pcb_components["FAN"], GPIO.OUT) #FAN Output
GPIO.setup(pcb_components["POWER"], GPIO.IN)  #set pin as input
GPIO.setup(pcb_components["RESET"], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin as input and switch on internal pull up resistor
GPIO.setup(pcb_components["CHECK_PCB"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

def temp(): #returns the gpu temoperature
    res = os.popen(path.temp_command).readline()
    return float((res.replace("temp=", "").replace("'C\n", "")))

class led:  #class to control the led
    def toggle(status):  #toggle the led on of off
        if status == 0:       #the led is inverted
            GPIO.output(pcb_components["LED"], GPIO.LOW)
        if status == 1:
            GPIO.output(pcb_components["LED"], GPIO.HIGH)

    def blink(amount,interval): #blink the led
        for x in range(amount):
            led.toggle(1)
            time.sleep(interval)
            led.toggle(0)
            time.sleep(interval)

def fan(status):  #switch the fan on or off
    if status == 1:
        GPIO.output(pcb_components["FAN"], GPIO.HIGH)
    if status == 0:
        GPIO.output(pcb_components["FAN"], GPIO.LOW)

def fancontrol(hysteresis,starttemp):  #read the temp and have a buildin hysteresis
    if temp() > starttemp:
        fan(1)
    if temp() < starttemp-hysteresis:
        fan(0)

def Falling_Power(channel):
    time.sleep(0.5)
    if (GPIO.input(pcb_components["POWER"]) == GPIO.HIGH) and GPIO.input(pcb_components["CHECK_PCB"]) == GPIO.LOW:  # shutdown funktion if the powerswitch is toggled
        led.toggle(0)
        fan(0)
        os.system("shutdown -h now")

def Falling_Reset(channel):
    if (GPIO.input(pcb_components["RESET"]) == GPIO.LOW):  # reset function
        time.sleep(vars.debounce_time)  # debounce time
        os.system("reboot")

def PCB_Pull(channel):
    GPIO.cleanup()

if (GPIO.input(pcb_components["POWER"]) == GPIO.HIGH) and GPIO.input(pcb_components["CHECK_PCB"]) == GPIO.LOW:
    os.system("shutdown -h now")

GPIO.add_event_detect(pcb_components["CHECK_PCB"],GPIO.RISING,callback=PCB_Pull)

time.sleep(1)

if GPIO.input(pcb_components["CHECK_PCB"])==GPIO.LOW: #check if there is an pcb and if there is then attach the interrupts
    led.toggle(0.5)
    GPIO.add_event_detect(pcb_components["RESET"], GPIO.FALLING, callback=Falling_Reset)
    time.sleep(0.5)
    GPIO.add_event_detect(pcb_components["POWER"], GPIO.FALLING, callback=Falling_Power)

while True:
    time.sleep(5)
    led.toggle(1)
    fancontrol(vars.fan_hysteresis , vars.fan_starttemp) # fan starts at 60 degrees and has a 5 degree hysteresis
