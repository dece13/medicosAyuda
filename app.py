from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from predecir import predecir
import os
import random
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/chat_app'
db = SQLAlchemy(app)

# Configuración de la carpeta de carga de archivos
app.config['UPLOAD_FOLDER'] = 'static/css/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# Modelo de mensaje
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(100))
    hueso_roto = db.Column(db.Boolean, default=False)

# Ruta de la página principal
@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

# Ruta para la carga de mensajes e imágenes
@app.route('/upload', methods=['POST'])
def upload():
    username = request.form['username']
    message = request.form['message']
    image_file = request.files['image']

    if image_file and allowed_file(image_file.filename):
        # Construir la ruta al archivo de imagen en el directorio static/uploads
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        # Simulación de la detección de hueso roto (valor aleatorio)
        predicc = predecir(image_path)  # Llamada a la función predecir desde predecir.py
        hueso_roto = False if predicc == 1 else True

        # Actualizar el campo 'hueso_roto' en la base de datos
        new_message = Message(username=username, message=message, image=filename, hueso_roto=hueso_roto)
        db.session.add(new_message)
        db.session.commit()

        # Crear mensaje sobre hueso roto o no
        response_message = 'Hueso roto' if hueso_roto else 'No roto'

        # Retornar solo el mensaje de respuesta (sin HTML completo)
        return response_message

    else:
        return "Error: Archivo no válido"

# Función para verificar la extensión del archivo permitida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
