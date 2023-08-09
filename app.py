from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Obtener el mensaje de texto enviado en la solicitud
    message = request.form['message']

    # Obtener el archivo de imagen enviado en la solicitud
    image_file = request.files['image']

    # Aquí puedes procesar el mensaje de texto y la imagen según tus necesidades
    # Por ejemplo, puedes guardar la imagen en el servidor, realizar análisis, etc.

    # Devolver una respuesta al cliente (puedes personalizar esta respuesta)
    return 'Mensaje recibido: {}\nImagen recibida: {}'.format(message, image_file.filename)

if __name__ == '__main__':
    app.run()
