import streamlit as st
from PIL import Image
import io
import paddleocr

# Загрузка модели PaddleOCR
ocr = paddleocr.PaddleOCR(lang='en', use_angle_cls=True)

def load_image():
    uploaded_file = st.file_uploader(label='Выберите изображение для распознавания')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None

def recognize_text(img):
    if img is not None:
        result = ocr.ocr(img)
        text = ''
        for item in result[0]:
            text += item[1][0] + ' '
        return text
    else:
        return None

st.title('Распознай английский текст с изображения!')
img = load_image()

if st.button('Распознать изображение'):
    recognized_text = recognize_text(img)
    if recognized_text:
        st.write('Результаты распознавания:')
        st.write(recognized_text)
    else:
        st.write("Пожалуйста, загрузите изображение.")
