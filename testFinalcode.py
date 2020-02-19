from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import json
import os
import RPi.GPIO as GPIO
import picamera
from time import sleep
import boto3
import argparse
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
camera = picamera.PiCamera()
GPIO.setwarnings(False)
def openDoor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(3,GPIO.OUT)
    pwm = GPIO.PWM(7,50)
    pwm.start(7.5)
    GPIO.output(3,True)
    sleep(2)
    GPIO.output(3,False)
    sleep(4)
    GPIO.output(3,True)
    duty = 10/18+2
    GPIO.output(7,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(7,False)
    pwm.ChangeDutyCycle(0)
    sleep(1)
    GPIO.output(3,False)
    print("Door is closed!!!")
    pwm.stop()
    GPIO.cleanup()
print("Scan your card")
#Take picture and send to S3
id,username = reader.read()
print(id)
if(id ==177115600747):
    print("Stand in front of camera to take the picture")
    sleep(2)
    camera.resolution = (600,600)
    camera.awb_mode = 'auto'
    camera.capture('door',format='jpeg')
    s3 = boto3.client('s3',region_name ='us-east-1')
    s3.upload_file('','','')#Upload your folder, name of bucket, image
    camera.close()
#Certificates and hostname
IoT_CLIENT = "" #Your client name here
HOST_NAME = "" #Your host name here
ROOT_CA = "" #Your root key here
PRIVATE_KEY = "" #Your private key here
CERT_FILE ="" #Your certificate file here
IoTThing_name = "" #Your thing name is here

#Custom MQTT message callback
def photoVerifiedcustomCallback(client,userdata,message):
    data = json.loads(message.payload)
    try:
        similarity = data[1][0]['Similarity']
        if(similarity >92):
            print("Welcome in ")
            openDoor()
            sleep(8)
    except:
        print("Not Today!!!")
        #pass
#For certificate based connection
myMQTTClient = AWSIoTMQTTClient(IoT_CLIENT)
myMQTTClient.configureEndpoint(HOST_NAME, ...) #Configure your end point
myMQTTClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
myMQTTClient.configureOfflinePublishQueueing(-1)

#Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) #Draining:2Hz
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
myMQTTClient.connect()
topic_name = "SmartDoorProject"
myMQTTClient.subscribe(topic_name, 1, photoVerifiedcustomCallback)
sleep(10)
exit()