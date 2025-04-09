import io
import streamlit as st
from transformers import pipeline
from PIL import Image

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

if img is not None:
    result = st.button('Распознать изображение')
    if result:
        try:
            captioner = pipeline("image-to-text", model="YaelSch/OCR-image-to-text-m")
            text = captioner(img)
            st.write('Результаты распознавания:')
            st.write(text[0]["generated_text"])
        except ImportError as e:
            st.error(f"Ошибка импорта: {e}")
        except OSError as e:
            st.error(f"Ошибка загрузки модели: {e}")
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
