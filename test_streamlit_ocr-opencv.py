import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import av  # strealing video library
# import easyocr
from OCR_class import OCR_engine


st.title("Webcam Live Feed")
st.write('Real Time OCR Test')
run = st.checkbox('Run')

FRAME_WINDOW = st.image([])

# Webcam
video = cv2.VideoCapture(0)
print(f'frame rate : {video.get(cv2.CAP_PROP_FPS)}')

frame_rate_new = 10
video.set(cv2.CAP_PROP_FPS, frame_rate_new)
# OCR
ocr_instance = OCR_engine.my_ocr(lang_list=['en'])

while run:
    _,img = video.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_copy = img.copy()
    # OCR
    result = ocr_instance.ocr_read(img=img_copy)
    # Result 集計+ Box Plotting
    img_return, _, _ = ocr_instance.draw_boxes(img=img, result=result)

    FRAME_WINDOW.image(img)
else:
    st.write('Stopped')
