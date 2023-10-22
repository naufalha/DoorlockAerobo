Creating a Raspberry Pi door lock system with a web interface and using MQTT (Mosquitto) for communication can be a fun and useful project. This project assumes you have basic knowledge of Raspberry Pi, Python, HTML, and MQTT. Here's a step-by-step guide to get you started:

**Requirements:**

1. Raspberry Pi (with Raspbian OS)
2. A servo motor or solenoid lock
3. Mosquitto MQTT broker installed on your Raspberry Pi
4. Python and Flask for the web interface
5. HTML, CSS, and JavaScript for the webpage
6. MQTT client libraries (paho-mqtt) for Python

**Step 1: Set up Mosquitto MQTT Broker**

Install and configure Mosquitto on your Raspberry Pi. You can install it using:

```bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

Start the Mosquitto broker and enable it to start on boot:

```bash
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

**Step 2: Hardware Setup**

Connect your servo motor or solenoid lock to the GPIO pins on your Raspberry Pi. You may need to use a motor driver or relay, depending on the type of lock you are using. Make sure to power the lock properly.

**Step 3: Web Interface**

1. Create a new directory for your project and navigate to it:

```bash
mkdir door_lock_project
cd door_lock_project
```

2. Create a Python script for your web interface. This script should use Flask to create a simple web application. You can use the example below as a starting point and customize it to your needs.

```python
from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/unlock')
def unlock():
    # Send an MQTT message to trigger the door unlock
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.publish("door/lock", "unlock")
    client.disconnect()
    return "Door unlocked"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

3. Create an HTML template for your webpage (e.g., `templates/index.html`). This is a simple example with a button to unlock the door:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Door Lock Control</title>
</head>
<body>
    <h1>Door Lock Control</h1>
    <button onclick="unlockDoor()">Unlock</button>
    <script>
        function unlockDoor() {
            fetch('/unlock')
                .then(response => response.text())
                .then(message => alert(message));
        }
    </script>
</body>
</html>
```

**Step 4: MQTT Integration**

You'll need to create a Python script to subscribe to MQTT messages and control the door lock. This script should run continuously and listen for unlock commands.

```python
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
```

**Step 5: Run the System**

Start your web interface and MQTT script on the Raspberry Pi. You can access the web interface from any device on your local network.

```bash
python web_interface.py
python mqtt_door_lock.py
```

Now, when you click the "Unlock" button on the web page, it will send an MQTT message to the Raspberry Pi, which will trigger the door unlock process.

This is a basic implementation, and you can expand it by adding authentication, security measures, and more features to suit your specific requirements.