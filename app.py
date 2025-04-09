import streamlit as st
from PIL import Image
from transformers import AutoModelForImageToText, AutoTokenizer, pipeline

# Функция для загрузки модели и токенизатора
def load_model(model_name):
    try:
        model = AutoModelForImageToText.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        st.error(f"Ошибка при загрузке модели: {e}")
        return None, None

# Функция для преобразования изображения в текст
def image_to_text(image, model, tokenizer):
    try:
        # Создание пайплайна для преобразования изображения в текст
        captioner = pipeline("image-to-text", model=model, tokenizer=tokenizer)
        
        # Преобразование изображения в текст
        result = captioner(image)
        
        return result[0]['generated_text']
    except Exception as e:
        st.error(f"Ошибка при преобразовании изображения: {e}")
        return None

# Основная функция приложения
def main():
    st.title("Преобразование изображения в текст")
    
    # Загрузка модели
    model_name = "YaelSch/OCR-image-to-text-m"
    model, tokenizer = load_model(model_name)
    
    if model is None:
        return
    
    # Загрузка изображения
    uploaded_image = st.file_uploader("Загрузите изображение", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Загруженное изображение")
        
        # Преобразование изображения в текст
        text = image_to_text(image, model, tokenizer)
        
        if text is not None:
            st.write("Текст с изображения:")
            st.write(text)

if __name__ == "__main__":
    main()
