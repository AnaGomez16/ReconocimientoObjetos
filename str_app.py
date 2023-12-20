import streamlit as st
from decouple import config
from video_processing.video_processing_YOLOv8 import download_video, process_video_with_model
from video_processing.video_processing_YOLOv8 import get_video_report, get_logo_report
from ultralytics import YOLO


#Function to check if the URL is a valid YouTube link
def valid_youtube_link(url):
    return "youtube.com" in url or "youtu.be" in url


st.title('Brand Logo Detection')

video_url = st.text_input('Insert video URL')

if video_url:
   if valid_youtube_link(video_url):
      st.success("The link is valid.")
      st.video(video_url)
        
      output_folder = config('VIDEO_FOLDER')
      video_filename = download_video(video_url, output_folder)
      video_path = f"{output_folder}/{video_filename}"
        
      model_path = config('YOLO_PATH')
      model = YOLO(model_path)
      labels_list = list(model.names.values())
      detected_labels = process_video_with_model(video_path, model)

      duration, frame_rate, info_dict = get_video_report(video_path, video_filename)
      info_dict['detections'] = get_logo_report(labels_list, detected_labels, duration, frame_rate)
      print(info_dict)

   else:
      st.error("The link is not valid. Please, enter a valid YouTube link.")