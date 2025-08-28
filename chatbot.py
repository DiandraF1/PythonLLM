import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

from vector_store import create_chroma_collection
from tools import get_summary_by_title
from sentence_transformers import SentenceTransformer

load_dotenv()

BANNED_WORDS = ["idiot", "prost", "stupid", "nașpa", "urât", "dracu"]


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
collection = create_chroma_collection()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_chatbot(user_query: str) -> str:
    
    lowered = user_query.lower()
    if any(bad_word in lowered for bad_word in BANNED_WORDS):
        return " Te rog folosește un limbaj adecvat. Sunt aici să te ajut cât pot de bine. "

    
    query_embedding = embedding_model.encode([user_query])[0]

    
    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    retrieved_text = results["documents"][0][0]
    title = results["ids"][0][0]

    
    prompt = f"""
Utilizatorul a întrebat: "{user_query}"

Am găsit o potrivire bună: cartea **{title}**.

Scrie un mesaj scurt, conversațional, în care recomanzi această carte pe baza temelor implicite și contextului. Nu da încă un rezumat detaliat.
"""

    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    recommendation = response.choices[0].message.content.strip()

    
    summary = get_summary_by_title(title)

   
    full_response = f"{recommendation}\n\n **Rezumat complet:**\n{summary}"
    return full_response


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