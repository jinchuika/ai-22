# para ejecutar en windows
# $env:FLASK_APP = "main.py"
# flask run --host=0.0.0.0
# recuerde agregar el archivo "regresion.h5"

from flask import Flask, render_template, request, redirect, flash
from keras.models import load_model
import numpy as np
from flask import Flask

app = Flask(__name__)
# para subir archivos
app.secret_key = "test_key"


def get_model():
    global model
    model = load_model('regresion.h5')
    print(" * Modelo cargado!")

get_model()

def predecir(a, b):
    X = np.array([[a, b]])
    prediccion = model.predict(X)
    return prediccion


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        print(request.form['primero'], request.form['segundo'])
        if request.form['primero'] and request.form['segundo']:
            print('datos obtenidos')
            resultado = predecir(
                int(request.form['primero']),
                int(request.form['segundo'])
            )
            flash(str(resultado))
            return redirect('/')
        else:
            flash('Error al recibir los datos')
            return redirect(request.url)


if __name__ == "__main__":
    app.run()
