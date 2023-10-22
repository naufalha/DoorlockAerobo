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
