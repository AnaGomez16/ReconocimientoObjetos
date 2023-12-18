import streamlit as st

st.title('Brand Logo Detection')

#Function to check if the URL is a valid YouTube link
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
        st.error("El enlace no es válido. Por favor, introduce un enlace válido de YouTube.")

if video_url:
    st.video(video_url)