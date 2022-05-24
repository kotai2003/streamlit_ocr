import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import av  # strealing video library
import easyocr
from OCR_class import OCR_engine

st.title('Streamlit App Test')
st.write('Real Time OCR Test')

# OCR
ocr_instance = OCR_engine.my_ocr(lang_list=['en'])


# Class
class VideoProcessor:

    def __init__(self) -> None:
        self.test_state = None

    def recv(self, frame):

        img = frame.to_ndarray(format='bgr24')

        if self.test_state == True:

            # 処理をここに入れる。
            result = ocr_instance.ocr_read(img=img)
            img = ocr_instance.draw_boxes(img=img, result=result)

            img = av.VideoFrame.from_ndarray(img, format='bgr24')

        else:
            # そのまま流す。
            img = av.VideoFrame.from_ndarray(img, format='bgr24')

        return img


ctx = webrtc_streamer(key='example', video_processor_factory=VideoProcessor)

if ctx.video_processor:
    ctx.video_processor.test_state = st.checkbox('OCR')
