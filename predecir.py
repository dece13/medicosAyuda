from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
 
model = load_model(r'C:\\Users\\57301\\Desktop\\Universidad\\ino2\\medicosAyuda\\model_savede.h5')
 
image = load_img(r'C:\\Users\\57301\\Desktop\\Universidad\\ino2\\medicosAyuda\\static\\css\\uploads\\piernarota.jpg', target_size=(224, 224))  # Carga una imagen desde la ruta
img = img_to_array(image)  # Convierte la imagen cargada en un array
img = img / 255.0  # Normaliza los valores de los píxeles
img = np.expand_dims(img, axis=0)  # Expande las dimensiones del array para que sea una muestra
label = model.predict(img)  # Realiza la predicción
print("Predicted Class (0 - Cars , 1- Planes): ", label[0][0])
