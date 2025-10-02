from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mqtt import Mqtt
import json
import time

app = Flask(__name__)

# Configuração MQTT
app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'  # Ou '192.168.0.77' se for local
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5000
app.config['MQTT_TLS_ENABLED'] = False

# Inicialização MQTT
mqtt_client = Mqtt(app)

# Variáveis globais
temperature = 25.0
humidity = 60.0
led_status = 0
last_update = time.time()

topic_subscribe = "/aula_flask/#"

# Rotas principais
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/tempo_real')
def tempo_real():
    global temperature, humidity, last_update
    values = {"temperature": temperature, "humidity": humidity}
    return render_template("tr.html", values=values)

@app.route('/publish')
def publish():
    global led_status
    return render_template('publish.html', led_status=led_status)

@app.route('/publish_message', methods=['POST'])
def publish_message():
    global led_status
    request_data = request.get_json()
    
    topic = request_data.get('topic', '/aula_flask/led')
    message = request_data.get('message', '0')
    
    # Atualiza status do LED
    led_status = int(message)
    
    # Publica via MQTT
    publish_result = mqtt_client.publish(topic, message)
    
    return jsonify({
        'result': publish_result[0],
        'message_id': publish_result[1] if len(publish_result) > 1 else None,
        'led_status': led_status
    })

@app.route('/get_sensor_data')
def get_sensor_data():
    global temperature, humidity, last_update
    return jsonify({
        'temperature': temperature,
        'humidity': humidity,
        'last_update': last_update
    })

# Handlers MQTT
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_subscribe)
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")

@mqtt_client.on_message()
@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global temperature, humidity, led_status, last_update
    
    payload = message.payload.decode()
    topic = message.topic
    
    try:
        # Para números simples do Wokwi
        if topic == "/aula_flask/temperature":
            temperature = float(payload)
        elif topic == "/aula_flask/humidity":
            humidity = float(payload)
        elif topic == "/aula_flask/led":
            led_status = int(payload)
        
        last_update = time.time()
        print(f"[MQTT] {topic} = {payload}")
        
    except Exception as e:
        print(f"Erro ao processar mensagem: {payload} | {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)