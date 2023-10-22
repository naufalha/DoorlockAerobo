import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Configure GPIO pins for the lock
LOCK_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_PIN, GPIO.OUT)

def on_message(client, userdata, message):
    if message.payload.decode() == "unlock":
        unlock_door()

def unlock_door():
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    time.sleep(2)  # Adjust the delay as needed
    GPIO.output(LOCK_PIN, GPIO.LOW)

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("door/lock")

client.loop_forever()
