from flask import Flask, json, render_template, request, redirect, url_for, jsonify
from flask_mqtt import Mqtt
import time

app = Flask(__name__)

# configurações do MQTT
app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt_client = Mqtt(app)

# variáveis globais
temperatura = 25.0
umidade = 60.0
led_status = 0
last_update = time.time()

topic_subscribe = "/aula_flask/#"

# rotas flask
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/tempo_real')
def tempo_real():
    global temperatura, umidade
    values = {"temperatura": temperatura, "umidade": umidade}
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
    
    # atualiza status do LED
    led_status = int(message)
    
    # publica via MQTT
    publish_result = mqtt_client.publish(topic, message)
    
    return jsonify({
        'led_status': led_status
    })

@app.route('/get_sensor_data')
def get_sensor_data():
    global temperatura, umidade, last_update
    return jsonify({
        'temperatura': temperatura,
        'umidade': umidade,
        'last_update': last_update
    })

# handlers MQTT
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('[MQTT] Conectado com sucesso ao broker!')
        mqtt_client.subscribe(topic_subscribe)
        print(f'[MQTT] Inscrito no tópico: {topic_subscribe}')
    else:
        print('[MQTT] Falha na conexão. Código:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("[MQTT] Desconectado do broker")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global temperatura, umidade, led_status, last_update
    try:
        payload = message.payload.decode()
        data = json.loads(payload)
        if data.get("sensor") == "/aula_flask/temperatura":
            temperatura = data["valor"]
        elif data.get("sensor") == "/aula_flask/umidade":
            umidade = data["valor"]
        last_update = time.time()
    except:
        # fallback para mensagem simples
        if message.topic == "/aula_flask/temperatura":
            temperatura = float(payload)
        elif message.topic == "/aula_flask/umidade":
            umidade = float(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
