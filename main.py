import streamlit as st
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import requests
import tempfile

# ------------- OCR FUNCTION ----------------
@st.cache_resource
def load_paddle_model():
    return PaddleOCR(lang='en', use_angle_cls=True)

def ocr_with_paddle(img):
    ocr = load_paddle_model()
    result = ocr.ocr(np.array(img))

    final_text = ''
    for line in result[0]:
        text = line[1][0]
        final_text += text + ' '
    return final_text.strip()

# ------------- IMAGE LOADING ----------------
def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(response.raw).convert("RGB")
        return img
    except Exception as e:
        st.error(f"Ошибка загрузки изображения: {e}")
        return None

# ------------- MAIN APP ---------------------
st.set_page_config(page_title="OCR with Paddle", layout="centered")
st.title("📝 OCR: Распознавание текста с помощью PaddleOCR")

input_type = st.radio("Источник изображения", ["Загрузить файл", "Ввести URL"])

img = None

if input_type == "Загрузить файл":
    uploaded_file = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
elif input_type == "Ввести URL":
    url = st.text_input("Введите URL изображения (например, с GitHub)")
    if url:
        img = load_image_from_url(url)

if img:
    st.image(img, caption="Загруженное изображение", use_column_width=True)

    if st.button("🔍 Распознать текст"):
        with st.spinner("Распознавание текста..."):
            text = ocr_with_paddle(img)
            st.subheader("📋 Распознанный текст:")
            st.text_area("Результат", text, height=200)
else:
    st.info("Пожалуйста, загрузите изображение или введите URL выше.")
