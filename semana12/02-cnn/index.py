# para ejecutar en windows
# $env:FLASK_APP = "index.py"
# flask run --host=0.0.0.0
# necesario descargar el modelo
# disponible para descargar en
# https://drive.google.com/file/d/1Egvh2LM0vGEY9Jp8kuh1Kn0_vk1zFQlW/view?usp=sharing

from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os

from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input

app = Flask(__name__)
app.secret_key = "test_key"
app.config['UPLOAD_FOLDER'] = 'uploads'

def get_model():
    global model
    model = load_model('VGG16_cats_and_dogs.h5')
    print(" * Model loaded!")

get_model()

def predecir(model, filename):
    image = load_img('uploads/'+ filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    clases = model.predict(image)
    return clases[0]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No existe el archivo')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No hay archivo seleccionado')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            perro, gato = predecir(model, filename)
            flash(str(perro))
            flash(str(gato))
            return redirect('/')


if __name__ == "__main__":
    app.run()
