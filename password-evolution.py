import hashlib
import sqlite3
from flask import Flask, request

app = Flask(__name__)
DATABASE = 'database.db'

# Generaciòn de hash de contraseña
def generate_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verificaciòn de contraseña con hash
def verify_password(password, hashed_password):
    return generate_hash(password) == hashed_password

# Creacion de base de dato y usuarios
def create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.commit()
    conn.close()

# Agregar usuarios
def add_user(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    hashed_password = generate_hash(password)
    c.execute('INSERT INTO users VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

# Verificar usuario
def verify_user(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()

    if result:
        hashed_password = result[0]
        return verify_password(password, hashed_password)
    else:
        return False

# Ruta del sitio web
@app.route('/')
def index():
    return 'Sitio de prueba Evaluacion 3 '

# Registro de nuevo usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        return 'Usuario registrado con éxito'
    else:
        return '''
        <form method="POST" action="/register">
            <label>Usuario:</label>
            <input type="text" name="username" required><br>
            <label>Contraseña:</label>
            <input type="password" name="password" required><br>
            <input type="submit" value="Registrar">
        </form>
        '''
# Verificacion de usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            return 'Inicio de sesión exitoso'
        else:
            return 'Credenciales incorrectas'
    else:
        return '''
        <form method="POST" action="/login">
            <label>Usuario:</label>
            <input type="text" name="username" required><br>
            <label>Contraseña:</label>
            <input type="password" name="password" required><br>
            <input type="submit" value="Iniciar sesión">
        </form>
        '''

# Iniciar la aplicación en el puerto 9500
if __name__ == '__main__':
    create_database()
    # Agregar los integrantes del grupo 
    add_user("Antonio Pinto", "Duoc2023")
    add_user("Francisco Osorio", "Duoc2023")
    app.run(port=9500)
