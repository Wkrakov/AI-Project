import io
import streamlit as st
from PIL import Image
import easyocr

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

if st.button('Распознать изображение'):
    if img is not None:
        reader = easyocr.Reader(['en'])  # Для английского языка
        result = reader.readtext(img)
        text = '\n'.join([item[1] for item in result])
        st.write('Результаты распознавания:')
        st.write(text)
    else:
        st.write("Пожалуйста, загрузите изображение.")
