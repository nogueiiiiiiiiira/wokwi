from flask import Blueprint, render_template, request

login = Blueprint("login", __name__, template_folder="templates")

usuarios = {
    'usuario1@gmail.com': '1234',
    'usuario2@gmail.com': '1234'
}

@login.route('/login')
def login_page():
    return render_template('login.html', erro=False)

@login.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    usuario = request.form['usuario']
    password = request.form['password']
    print(usuario, password)
    
    if usuario in usuarios and usuarios[usuario] == password:
        return render_template('home.html')
    else:
        # renderiza o login novamente com a flag de erro
        return render_template('login.html', erro=True)

if __name__ == "__main__":
    login.run(host = '0.0.0.0', port = 8080, debug = True)