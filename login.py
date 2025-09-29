from flask import Blueprint, render_template, request, redirect, url_for

login = Blueprint("login", __name__, template_folder = "templates")

global usuarios

usuarios = {
    'usuario1@gmail.com' : '1234',
    'usuario2@gmail.com' : '1234'
}

@login.route('/validar_usuario', methods = ['POST'])
def validar_usuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        print(usuario, password)
        if usuario in usuarios and usuarios[usuario] == password:
            return render_template('home.html')
        else:
            return '<h1>Credenciais Inválidas!</h1>'
    else:
        return render_template('login.html')

@login.route('/adicionar_usuario', methods = ['GET', 'POST'])
def adicionar_usuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
    else:
        usuario = request.args.get('usuario', None)
        password = request.args.get('password', None)
    usuarios[usuario] = password
    return render_template("usuarios.html", usuarios = usuarios)

@login.route('/deletar_usuario', methods = ['GET', 'POST'])
def deletar_usuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        if usuario in usuarios:
            usuarios.pop(usuario)
    else:
        usuario = request.args.get('usuario', None)
        if usuario and usuario in usuarios:
            usuarios.pop(usuario)

    return render_template("usuarios.html", usuarios = usuarios)

if __name__ == "__main__":
    login.run(host = '0.0.0.0', port = 8080, debug = True)
