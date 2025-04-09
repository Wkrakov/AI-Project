import io
import streamlit as st
from transformers import pipeline
from PIL import Image

# @st.cache_resource используется для кеширования ресурса (модели)
# Это позволяет загружать модель только один раз при первом запуске приложения
# или при обновлении кода, а не каждый раз, когда пользователь нажимает кнопку.
# Это значительно повышает производительность.
@st.cache_resource
def load_ocr_model():
    """Загружает OCR модель с Hugging Face."""
    try:
        # Используем pipeline "image-to-text", так как модель YaelSch/OCR-image-to-text-m
        # специально обучена для этой задачи.
        ocr_pipeline = pipeline("image-to-text", model="YaelSch/OCR-image-to-text-m")
        return ocr_pipeline
    except Exception as e:
        st.error(f"Не удалось загрузить OCR модель. Ошибка: {e}")
        return None

def load_image():
    """Загружает изображение, выбранное пользователем."""
    uploaded_file = st.file_uploader(label='Выберите изображение для распознавания', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        try:
            image_data = uploaded_file.getvalue()
            st.image(image_data, caption="Загруженное изображение", use_column_width=True)
            return Image.open(io.BytesIO(image_data)).convert("RGB") # Конвертируем в RGB на всякий случай
        except Exception as e:
            st.error(f"Не удалось загрузить изображение. Ошибка: {e}")
            return None
    else:
        return None

# Заголовок приложения
st.title('Распознавание текста с изображения с помощью OCR')
st.markdown('**Внимание:** Эта модель обучена в основном на английских текстах и может работать хуже с другими языками.')

# Загрузка изображения
img = load_image()

# Загрузка OCR модели (с кешированием)
ocr_model = load_ocr_model()

# Кнопка для запуска распознавания
result_button = st.button('Распознать текст')

# Обработка нажатия кнопки и распознавание текста
if result_button:
    if img is not None and ocr_model is not None:
        with st.spinner('Распознавание текста...'):
            try:
                # Вызываем пайплайн для распознавания текста
                ocr_result = ocr_model(img)

                st.subheader('Результаты распознавания:')
                if ocr_result and isinstance(ocr_result, list) and len(ocr_result) > 0 and "generated_text" in ocr_result[0]:
                    recognized_text = ocr_result[0]["generated_text"]
                    st.text_area("Распознанный текст:", recognized_text, height=200)
                else:
                    st.warning("Не удалось распознать текст или получен неожиданный формат результата.")
            except Exception as e:
                st.error(f"Произошла ошибка при распознавании текста: {e}")
    elif img is None:
        st.warning("Пожалуйста, загрузите изображение.")
    elif ocr_model is None:
        st.error("OCR модель не была загружена. Пожалуйста, проверьте подключение к Интернету и попробуйте еще раз.")
