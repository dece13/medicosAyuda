from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
 

def predecir(rutaImagen):
    model = load_model(r'C:\\Users\\57301\\Desktop\\Universidad\\ino2\\medicosAyuda\\model_savede.h5')
    image = load_img(rutaImagen, target_size=(224, 224))  # Carga una imagen desde la ruta
    img = img_to_array(image)  # Convierte la imagen cargada en un array
    img = img / 255.0  # Normaliza los valores de los píxeles
    img = np.expand_dims(img, axis=0)  # Expande las dimensiones del array para que sea una muestra
    label = model.predict(img)  # Realiza la predicción
    if label[0][0]>0.75:
        return 1
    else:
        return 0
    

