import io
import streamlit as st

from transformers import pipeline
from PIL import Image
pip install --upgrade transformers
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
    captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    text = captioner(img)
    st.write('**Результаты распознавания:**')
    st.write(text[0]["generated_text"])
