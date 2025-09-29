from flask import Blueprint, render_template, request, redirect, url_for

atuadores = Blueprint("atuadores", __name__, template_folder = "templates")

global atuadores_lista
atuadores_lista = {}

@atuadores.route('/adicionar_atuador', methods = ['GET', 'POST'])
def adicionar_atuador():
    if request.method == 'POST':
        atuador = request.form['atuador']
        atuadores_lista[atuador] = True
    else:
        atuador = request.args.get('atuador', None)
        if atuador:
            atuadores_lista[atuador] = True

    return render_template("atuadores.html", atuadores_lista = atuadores_lista)

@atuadores.route('/deletar_atuador', methods = ['GET', 'POST'])
def deletar_atuador():
    if request.method == 'POST':
        atuador = request.form['atuador']
        if atuador in atuadores_lista:
            atuadores_lista.pop(atuador)
    else:
        atuador = request.args.get('atuador', None)
        if atuador and atuador in atuadores_lista:
            atuadores_lista.pop(atuador)

    return render_template("atuadores.html", atuadores_lista = atuadores_lista)

if __name__ == "__main__":
    atuadores.run(host = '0.0.0.0', port = 8080, debug = True)
