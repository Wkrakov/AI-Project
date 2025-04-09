import streamlit as st
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import requests

# --- Кэшируем модель, чтобы не загружалась каждый раз ---
@st.cache_resource
def load_ocr_model():
    return PaddleOCR(use_angle_cls=True, lang='en')  # только английский

# --- Функция для распознавания текста ---
def ocr_with_paddle(image: Image.Image) -> str:
    ocr = load_ocr_model()
    result = ocr.ocr(np.array(image), cls=True)

    extracted_text = ""
    for line in result[0]:
        text = line[1][0]
        extracted_text += text + " "
    return extracted_text.strip()

# --- Функция загрузки изображения по URL ---
def load_image_from_url(url: str):
    try:
        response = requests.get(url)
        img = Image.open(response.raw).convert("RGB")
        return img
    except Exception as e:
        st.error(f"Ошибка загрузки изображения: {e}")
        return None

# --- Интерфейс Streamlit ---
st.set_page_config(page_title="OCR with PaddleOCR", layout="centered")
st.title("📝 Распознавание текста (OCR) с помощью PaddleOCR")

input_method = st.radio("Источник изображения", ["📁 Загрузить файл", "🌐 Ввести URL"])

image = None

if input_method == "📁 Загрузить файл":
    uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

elif input_method == "🌐 Ввести URL":
    image_url = st.text_input("Введите URL изображения (например, с GitHub)")
    if image_url:
        image = load_image_from_url(image_url)

if image:
    st.image(image, caption="Загруженное изображение", use_column_width=True)

    if st.button("🔍 Распознать текст"):
        with st.spinner("Распознавание текста..."):
            result_text = ocr_with_paddle(image)
            st.subheader("📋 Распознанный текст:")
            st.text_area("Результат", result_text, height=200)
else:
    st.info("Пожалуйста, загрузите изображение или введите URL.")
