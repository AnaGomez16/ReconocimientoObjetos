import cv2
from pytube import YouTube

def download_video(youtube_url, output_path):
    yt = YouTube(youtube_url)
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path)
    return ys.default_filename

def split_video_to_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame_name = f"{output_folder}/frame_{count}.jpg"
        cv2.imwrite(frame_name, frame)

        count += 1

    cap.release()

def main():
    # Especifica la URL de YouTube y la carpeta de salida
    youtube_url = 'URL_DEL_VIDEO_EN_YOUTUBE'
    output_folder = 'carpeta_de_salida'

    # Descarga el video desde YouTube
    video_filename = download_video(youtube_url, output_folder)

    # Obtiene el path completo del video descargado
    video_path = f"{output_folder}/{video_filename}"

    # Divide el video en frames
    split_video_to_frames(video_path, output_folder)




if __name__ == "__main__":
    main()
