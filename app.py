
# app.py
from flask import Flask, render_template, request,redirect, url_for,jsonify
from login import login
from sensores import  sensores
from atuadores import atuadores
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json

#https://wokwi.com/projects/322577683855704658

temperatura = 10
humidade = 10

atuadores_values = 1

app = Flask(__name__)
## __name__ is the application name

app.register_blueprint(login, url_prefix = '/')
app.register_blueprint(sensores, url_prefix = '/')
app.register_blueprint(atuadores, url_prefix = '/')


app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

mqtt_client = Mqtt()
mqtt_client.init_app(app)

topic_subscribe1 = "/aula/temperatura"
topic_subscribe2 = "/aula/humidade"

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/logoff')
def logoff():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/tempo_real')
def tempo_real():
    global temperatura, humidade
    values = {"temperatura" : temperatura, "humidade" : humidade}
    return render_template("tr.html", values = values)

@app.route('/publish')
def publish():
    return render_template('publish.html')

@app.route('/publish_message', methods = ['GET','POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
    return jsonify(publish_result)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_subscribe1) # subscribe topic
        mqtt_client.subscribe(topic_subscribe2) # subscribe topic
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    print(message.payload.decode())
    if(message.topic == topic_subscribe1):
        global temperatura
        temperatura = message.payload.decode()
    if(message.topic == topic_subscribe2):
        global humidade
        humidade = message.payload.decode()

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8080, debug = True) 