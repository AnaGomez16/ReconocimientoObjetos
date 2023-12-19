from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS  

#Aqui la conección a mongo
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost/imagenes'
mongo = PyMongo(app)

print("Conexión a MongoDB establecida con éxito") if mongo else print("Error al conectarse a MongoDB")


@app.route('/upload_videos', methods=['POST'])
def upload_video():
    data = request.json  #Se Obtienen los datos enviados desde Streamlit

    # Procesa los datos y se guardan en MongoDB
    if data and 'video_url' in data:
        # Aquí puedes realizar la lógica para procesar los datos del video
        # y guardar la información relevante en tu base de datos MongoDB

        #guardar la URL del video
        inserted_video = mongo.db.videos.insert_one({'video_url': data['video_url']})
            #se agrega la funcion que agrega el diccionario 
        if inserted_video:
            return 'Video guardado exitosamente en MongoDB', 200
        else:
            return 'Error al guardar el video', 500
    else:
        return 'Datos no válidos', 400

if __name__ == "__main__":
    app.run(debug=True)



