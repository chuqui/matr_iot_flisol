import Adafruit_BBIO.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import os
import json
import Adafruit_DHT
 
host = "a2sq3y7mdrjtom.iot.us-east-1.amazonaws.com"
certPath = os.getcwd() + '/certificates/'
clientId = "bbb"
topic = "d87dec59"
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)

#dht_sensor = Adafruit_DHT.DHT11
#dht_pin = 'P8_10'
#GPIO.setup("P8_10", GPIO.IN)

GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_12", GPIO.IN)

def customPubackCallback(mid):
    pass

def customSubackCallback(mid, data):
    print data

def customOnMessage(message):
    print json.loads(message.payload)

def publishButtonPress():
    print "Publishing button press"
    myAWSIoTMQTTClient.publishAsync(topic, """{"type": "button", "data": "button pressed"}""", 1, ackCallback=customPubackCallback)

# def publishDHT(hum, temp):
#     print "Publishing DHT Sensor data"
#     myAWSIoTMQTTClient.publishAsync(topic, """{"type": "dht", "data": "Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, hum)}""", 1, ackCallback=customPubackCallback)

def setup_mqtt():
    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials("{}rootCA.pem".format(certPath), "{}BeagleBoneBlack.private-key.txt".format(certPath), "{}BeagleBoneBlack.certificate.pem".format(certPath))

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    myAWSIoTMQTTClient.onMessage = customOnMessage
    
    myAWSIoTMQTTClient.connect()
    print "MQTT Connected"
    time.sleep(5)

    myAWSIoTMQTTClient.subscribeAsync(topic, 1, ackCallback=customSubackCallback)


setup_mqtt()

while True:
    # Read DHT11 sensor
    # humidity, temperature = Adafruit_DHT.read(dht_sensor, dht_pin)
    # if humidity is not None and temperature is not None:
    #     publishDHT(humidity, temperature)
    # time.sleep(2)

    # Read button state
    btn = GPIO.input("P8_12")
    if btn == 0:
	publishButtonPress()
	time.sleep(2)


#    GPIO.output("P8_10", GPIO.HIGH)
#    time.sleep(1)
#    GPIO.output("P8_10", GPIO.LOW)
#    time.sleep(1)
