from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

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
    username = db.Column(db.String(50))
    message = db.Column(db.String(200))
    image = db.Column(db.String(100))

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

        # Crear un nuevo mensaje y guardarlo en la base de datos
        new_message = Message(username=username, message=message, image=filename)
        db.session.add(new_message)
        db.session.commit()

        # Actualizar la lista de mensajes en la página
        messages = Message.query.all()
        return render_template('index.html', messages=messages)

    else:
        return "Error: Archivo no válido"

# Función para verificar la extensión del archivo permitida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
