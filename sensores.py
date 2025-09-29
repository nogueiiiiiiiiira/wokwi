from flask import Blueprint, render_template, request, redirect, url_for

sensores = Blueprint("sensores", __name__, template_folder = "templates")

global sensores_lista
sensores_lista = {}

@sensores.route('/adicionar_sensor', methods = ['GET', 'POST'])
def adicionar_sensor():
    if request.method == 'POST':
        sensor = request.form['sensor']
        sensores_lista[sensor] = True
    else:
        sensor = request.args.get('sensor', None)
        if sensor:
            sensores_lista[sensor] = True

    return render_template("sensores.html", sensores_lista = sensores_lista)

@sensores.route('/deletar_sensor', methods = ['GET', 'POST'])
def deletar_sensor():
    if request.method == 'POST':
        sensor = request.form['sensor']
        if sensor in sensores_lista:
            sensores_lista.pop(sensor)
    else:
        sensor = request.args.get('sensor', None)
        if sensor and sensor in sensores_lista:
            sensores_lista.pop(sensor)

    return render_template("sensores.html", sensores_lista = sensores_lista)

if __name__ == "__main__":
    sensores.run(host = '0.0.0.0', port = 8080, debug = True)
