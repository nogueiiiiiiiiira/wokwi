from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mqtt import Mqtt
import time
import json

app = Flask(__name__)

# configurações MQTT
app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt_client = Mqtt(app)

usuarios = {
    'usuario1@gmail.com': '1234',
    'usuario2@gmail.com': '1234',
}

# variáveis globais
temperatura = 25.0
umidade = 60.0
led_status = 0
last_update = time.time()
topic_subscribe = "/aula_flask/#"

# rotas de autenticação
@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html', erro=False)

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    usuario = request.form['usuario']
    password = request.form['password']
    print(f"Tentativa de login: {usuario}, {password}")
    
    if usuario in usuarios and usuarios[usuario] == password:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', erro=True)


# rotas principais
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

# mqtt
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
    global temperatura, umidade, last_update
    try:
        payload = message.payload.decode()
        data = json.loads(payload)
        
        if data.get("sensor") == "/aula_flask/temperatura":
            temperatura = float(data["valor"])
        elif data.get("sensor") == "/aula_flask/umidade":
            umidade = float(data["valor"])
            
        last_update = time.time()
        print(f'[MQTT] Dados atualizados - Temp: {temperatura}, Umidade: {umidade}')
        
    except Exception as e:
        print(f'[MQTT] Erro ao processar mensagem: {e}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)