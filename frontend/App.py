import streamlit as st
import pandas as pd
import numpy as np


st.title('Detección de logos/marcas')


DATE_COLUMN = 'date/time'  # Define el nombre de la columna que contiene la fecha/hora

DATA_URL = ('https://s3-us-west-2.amazonaws.com/'  # Define la URL del conjunto de datos
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Definir variables y funciones
DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'



def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)  # Carga el conjunto de datos desde la URL usando Pandas
    lowercase = lambda x: str(x).lower()  # Define una función lambda para convertir los nombres de las columnas a minúsculas
    data.rename(lowercase, axis='columns', inplace=True)  # Aplica la función lambda a los nombres de las columnas
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])  # Convierte la columna de fecha/hora a formato datetime
    return data  # Devuelve el conjunto de datos modificado

# Cargar el conjunto de datos
data_load_state = st.text('Cargando datos...')
data = load_data(10000)
data_load_state.text('Datos cargados correctamente!')

# Función para verificar si la URL es un enlace válido de YouTube
def es_enlace_youtube(url):
    return "youtube.com" in url or "youtu.be" in url

#sección para mostrar el video

st.subheader('Insertar URL del video')
video_url = st.text_input('Insertar URL del video')


if video_url and ("youtube.com" in video_url or "youtu.be" in video_url):
        if es_enlace_youtube(video_url):
         st.success("El enlace es válido.")
        # Aquí puedes realizar la lógica adicional que desees al tener un enlace de YouTube válido
else:

video_url = st.text_input('Insertar URL del video')


if video_url:
    if es_enlace_youtube(video_url):
        st.success("El enlace es válido.")
        st.video(video_url)
        # Aquí puedes realizar la lógica adicional que desees al tener un enlace de YouTube válido
    else:

        st.error("El enlace no es válido. Por favor, introduce un enlace válido de YouTube.")

if video_url:
    st.video(video_url)






