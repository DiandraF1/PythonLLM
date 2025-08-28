import streamlit as st
from chatbot import ask_chatbot
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv
import tempfile
import os
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_cover_image(prompt: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3", 
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print(" Eroare la generarea imaginii:", e)
        return None

#  Setări aplicație
st.set_page_config(page_title="Smart Librarian")
st.title(" Smart Librarian – RAG Chatbot")

#  Inițializare sesiune
if "last_response" not in st.session_state:
    st.session_state.last_response = None
if "last_image_url" not in st.session_state:
    st.session_state.last_image_url = None

#  Input întrebare
query = st.text_input("Ce fel de carte cauți?", placeholder="Ex: Vreau o carte despre magie și aventură")

#  Recomandare
if st.button(" Recomandă"):
    if query.strip() == "":
        st.warning("Te rog introdu o întrebare.")
    else:
        with st.spinner("Caut cea mai bună recomandare..."):
           
            response = ask_chatbot(query)
            st.session_state.last_response = response
            st.success("Gata! Iată recomandarea și rezumatul:")
            st.markdown(response)

           
            if " Rezumat complet:" in response:
                summary = response.split(" Rezumat complet:")[1].strip()
            else:
                summary = response  
        
        blocked_words = ["dictator", "supraveghere", "moarte", "ucidere", "politică", "viol", "tortură", "opresiune", "big brother"]
        clean_summary = summary

        for word in blocked_words:
           clean_summary = re.sub(rf"\b{word}\b", "", clean_summary, flags=re.IGNORECASE)

        image_prompt = f"Create an artistic and symbolic book cover based on this cleaned description: {clean_summary}"

       
        image_url = generate_cover_image(image_prompt)
        st.session_state.last_image_url = image_url


if st.button(" Ascultă recomandarea și rezumatul"):
    if st.session_state.last_response:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts = gTTS(st.session_state.last_response, lang="ro")   
            tts.save(tmpfile.name)

            with open(tmpfile.name, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')

            os.unlink(tmpfile.name)
    else:
        st.warning(" Nu există un text de redat. Generează mai întâi o recomandare.")


if "last_image_url" in st.session_state and st.session_state.last_image_url:
    st.image(
        st.session_state.last_image_url,
        caption="Imagine generată pentru cartea recomandată",
        use_container_width=True  
    )
