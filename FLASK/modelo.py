from flask import Flask, render_template, request
import pickle

# Cargamos el modelo
with open('ruta_del_modelo.pkl', 'rb') as file:
    modelo = pickle.load(file)

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    prediccion = None
    if request.method == 'POST':
        # Aquí debes recoger todos los datos que necesita tu modelo para hacer una predicción
        dato1 = float(request.form['dato1'])
        dato2 = float(request.form['dato2'])
        # ... (todos los datos necesarios)

        datos = [dato1, dato2]  # etc
        prediccion = modelo.predict([datos])[0]
        
    return render_template('index.html', prediccion=prediccion)


if __name__ == '__main__':
    app.run(debug=True)
