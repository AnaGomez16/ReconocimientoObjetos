from ultralytics import YOLO
import cv2
from pytube import YouTube
from decouple import config


def download_video(youtube_url, output_path):
    '''
    Downloads a video from YouTube.
    Args:
        youtube_url (str): The YouTube video URL.
        output_path (str): The path to the folder where the video will be saved.
    Returns:
        str: The filename of the downloaded video.
    '''
    yt = YouTube(youtube_url)
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path)
    return ys.default_filename


def process_video_with_model(video_path, model):
    '''
    Processes a video using a YOLOv8 model and displays real-time inference results.
    Args:
        video_path (str): The path to the video file.
        model: The YOLOv8 model object.
    Returns:
        None
    This function displays the video frames with the inference results 
    until the user presses 'q'.
    '''
    cap = cv2.VideoCapture(video_path)

    #Loop through the video frames
    while cap.isOpened():
        #Read a frame from the video
        success, frame = cap.read()

        if success:
            #Run YOLOv8 inference on the frame
            results = model(frame)

            #Visualize the results on the frame
            annotated_frame = results[0].plot()

            #Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            #Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            #Break the loop if the end of the video is reached
            break

    #Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()


def main():

    youtube_url = 'https://www.youtube.com/watch?v=IXFFhtD8lhk'

    output_folder = config('VIDEO_FOLDER')
   
    video_filename = download_video(youtube_url, output_folder)

    #Obtains the full path of the downloaded video
    video_path = f"{output_folder}/{video_filename}"

    model_path = config('YOLO_PATH')

    model = YOLO(model_path)

    process_video_with_model(video_path, model)


if __name__ == "__main__":
    main()