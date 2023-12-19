from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson import Binary


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/imagenes'
mongo = PyMongo(app)

# Agregar mensajes de depuración
print("Conexión a MongoDB establecida con éxito") if mongo else print("Error al conectarse a MongoDB")
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image found', 400

    image = request.files['image']
    filename = image.filename

    # Convertir la imagen a formato binario para guardarla en MongoDB
    image_binary = Binary(image.read())

    # Guardar la imagen en la base de datos
    inserted_image = mongo.db.images.insert_one({'filename': filename, 'image': image_binary})
    
    if inserted_image:
        return 'Image uploaded successfully', 200
    else:
        return 'Failed to upload image', 500

if __name__ == "__main__":
    app.run(debug=True)
