from ultralytics import YOLO
import cv2
from pytube import YouTube
import matplotlib.pyplot as plt


def download_video(youtube_url, output_path):
    yt = YouTube(youtube_url)
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path)
    return ys.default_filename


def process_video_with_model(video_path, model):
    cap = cv2.VideoCapture(video_path)

    #Loop through the video frames
    while cap.isOpened():
        #Read a frame from the video
        success, frame = cap.read()

        if success:
            #Run YOLOv8 inference on the frame
            results = model(frame)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()


def main():

    # load_dotenv()

    # Especifica la URL de YouTube y la carpeta de salida
    youtube_url = 'https://www.youtube.com/watch?v=IXFFhtD8lhk'

    # output_folder = os.getenv('VIDEO_FOLDER')
    output_folder = 'C:/Users/Ana Milena GOMEZ/Documents/Ana Milena GOMEZ/IA-School_Factoria-F5/ComputerVision/ReconocimientoObjetos/video_folder/'

    # Descarga el video desde YouTube
    video_filename = download_video(youtube_url, output_folder)

    # Obtiene el path completo del video descargado
    video_path = f"{output_folder}/{video_filename}"

    # Load the YOLOv8 model
    model_path = 'C:/Users/Ana Milena GOMEZ/Documents/Ana Milena GOMEZ/IA-School_Factoria-F5/ComputerVision/ReconocimientoObjetos/best_YOLO_model/best.pt'

    model = YOLO(model_path)

    process_video_with_model(video_path, model)


if __name__ == "__main__":
    main()
