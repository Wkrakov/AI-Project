import streamlit as st
import easyocr
from PIL import Image
import numpy as np  # Добавляем импорт numpy
import io

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
if result:
    if img is not None:
        reader = easyocr.Reader(['en'])  # Создаем объект для распознавания текста на английском
        result = reader.readtext(np.array(img))  # Преобразуем PIL Image в numpy array
        text = ' '.join([item[1] for item in result])  # Извлекаем текст из результатов
        st.write('Результаты распознавания:')
        st.write(text)
    else:
        st.write("Пожалуйста, загрузите изображение.")
