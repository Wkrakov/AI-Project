import io
import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR

# Функция для загрузки изображения
def load_image():
    uploaded_file = st.file_uploader(label='Выберите изображение для распознавания')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None

# Функция для распознавания текста с помощью Paddle OCR
def ocr_with_paddle(img):
    ocr = PaddleOCR(lang='en', use_angle_cls=True)
    result = ocr.ocr(img)
    final_text = ''
    for item in result:
        final_text += ' ' + item[1][0]
    return final_text

st.title('Распознай английский текст с изображения!')
img = load_image()

if img is not None:
    result_button = st.button('Распознать изображение')
    if result_button:
        extracted_text = ocr_with_paddle(img)
        st.write('Результаты распознавания:')
        st.write(extracted_text)
