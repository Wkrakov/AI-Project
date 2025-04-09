import io
import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR

# Инициализация PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model


def load_image():
    uploaded_file = st.file_uploader(label='Выберите изображение для распознавания')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return Image.open(io.BytesIO(image_data))
    else:
        return None


st.title('Распознай английский текст с изображения!')
img = load_image()

result = st.button('Распознать изображение')
if result and img is not None:
    # Распознавание текста с использованием PaddleOCR
    result = ocr.ocr(img, cls=True)
    text = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text += line[1][0] + " "

    st.write('Результаты распознавания:')
    st.write(text)
elif result:
    st.write('Пожалуйста, загрузите изображение.')
