import cv2
from pytube import YouTube
from transformers import DetrForObjectDetection, DetrImageProcessor
import supervision as sv
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import torch


def get_model_and_image_processor():    
    MODEL_PATH = os.getenv('MODEL_PATH')
    CHECKPOINT = 'facebook/detr-resnet-50'

    image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT)
    model = DetrForObjectDetection.from_pretrained(MODEL_PATH)
    return image_processor, model


def download_video(youtube_url, output_path):
    yt = YouTube(youtube_url)
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path)
    return ys.default_filename


def process_video_with_model(video_path, image_processor, model):
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    frames_to_skip = 50

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1
        if frame_count % (frames_to_skip + 1) != 0:
            continue  # Salta frames_to_skip frames
        
        #Process the frame with DETR and obtain detections
        with torch.no_grad():
            
            inputs = image_processor(images=frame, return_tensors='pt')
            outputs = model(**inputs)
            
            # Post-process
            target_sizes = torch.tensor([frame.shape[:2]])
            results = image_processor.post_process_object_detection(outputs=outputs,
                                                                    threshold=0.40,
                                                                    target_sizes=target_sizes)[0]


            # Draw the detections on the frame
            detections = sv.Detections.from_transformers(transformers_results=results)
            labels = [f"{model.config.id2label[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]

            box_annotator = sv.BoxAnnotator()
            
            annotated_frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
            
            #Display the frame with detections
            cv2.imshow('Detected Objects', annotated_frame)

            # Wait for a key press or a short delay
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def main():

    load_dotenv()

    # Especifica la URL de YouTube y la carpeta de salida
    youtube_url = 'https://www.youtube.com/watch?v=G_-B8fPkgb0'
    output_folder = os.getenv('VIDEO_FOLDER')

    # Descarga el video desde YouTube
    video_filename = download_video(youtube_url, output_folder)

    # Obtiene el path completo del video descargado
    video_path = f"{output_folder}/{video_filename}"

    image_processor, model = get_model_and_image_processor()   

    process_video_with_model(video_path, image_processor, model)


if __name__ == "__main__":
    main()
