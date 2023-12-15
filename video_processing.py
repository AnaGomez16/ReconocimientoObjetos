import cv2
from pytube import YouTube
from transformers import DetrForObjectDetection, DetrImageProcessor
import supervision as sv
import matplotlib.pyplot as plt


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


def process_frames_with_model(frames, model):
    for frame in frames:
        # Lógica para procesar el cuadro con DETR y obtener detecciones
        with torch.no_grad():

        #load image and predict
        inputs = image_processor(images=frame, return_tensors='pt')
        outputs = model(**inputs)

        #post-process
        target_sizes = torch.tensor([frame.shape[:2]])
        results = image_processor.post_process_object_detection(outputs=outputs, threshold=0.25, target_sizes=target_sizes)[0]

        #annotations
        detections = sv.Detections.from_transformers(transformers_results=results)
        labels = [f'{id2label[class_id]} {confidence:.2f}' for _, confidence, class_id, _ in detections]
        box = box_annotator.annotate(scene=frame.copy(), detections=detections, labels=labels)

        %matplotlib inline
        sv.show_frame_in_notebook(box, (16, 16))
        
        # Lógica para dibujar las detecciones en el cuadro original
        frame_with_detections = frame.copy()
        for detection in detections:
            # Lógica para dibujar las cajas de detección en el cuadro
            cv2.rectangle(frame_with_detections, detection['bbox'], (0, 255, 0), 2)

        # Visualizar el resultado en el cuadro original
        cv2.imshow('Detected Objects', frame_with_detections)

        # Esperar 25 milisegundos entre cada cuadro (puedes ajustar esto según tu preferencia)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


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

    model = DetrForObjectDetection.from_pretrained('C:/Users/Ana Milena GOMEZ/Documents/Ana Milena GOMEZ/IA-School_Factoria-F5/ComputerVision/ReconocimientoObjetos/MODELO CARROS')

    image_processor = DetrImageProcessor.from_pretrained('facebook/detr-resnet-50')

    process_frames_with_model(frames, model)


if __name__ == "__main__":
    main()
