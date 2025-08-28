#  Smart Librarian – RAG Chatbot

Un chatbot AI care recomandă cărți în funcție de interesele utilizatorului, folosind GPT + RAG (ChromaDB) și funcționalități opționale precum Text-to-Speech și generare de imagini.

---

##  Funcționalități implementate

-  **Căutare semantică (RAG)** pe baza unui fișier `book_summaries.json`
-  **Generare de răspunsuri conversaționale** cu OpenAI GPT (`gpt-4o-mini`)
-  **Rezumat detaliat** oferit automat după recomandare
-  **Redare audio** a recomandării și rezumatului (cu `gTTS`)
-  **Generare imagine** de copertă pe baza rezumatului cărții (DALL·E)
-  **Filtru de limbaj ofensator** (răspunde politicos și nu trimite la GPT)

---

##  Instalare și rulare

### 1. navighează în folderul local
cd smart_librarian


### 2. Creează mediu virtual

python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows


### 3. Instalează dependențele

pip install -r requirements.txt

### 4.Creează fișier .env cu cheia ta OpenAI

echo "OPENAI_API_KEY=sk-..." > .env

### 5. Rulează aplicația

streamlit run app.py

Aplicația se va deschide în browser la:
http://localhost:8501

## Exemple de întrebări pentru testare

"Vreau o carte despre prietenie"
"Ce carte proasta imi recomanzi?"-pentru testarea limbajului
"Vreau o carte despre aventura?"
"Cine era Harry Potter?"

## Structura proiectului

smart_librarian/
├── app.py                  # Streamlit
├── chatbot.py              # Logica GPT + RAG
├── tools.py                # Tool: get_summary_by_title()
├── vector_store.py         # Inițializare ChromaDB
├── book_summaries.json     # Setul de cărți și rezumate
├── requirements.txt        # Pachete necesare
└── .env                    #  Cheia  OpenAI

## Tehnologii folosite

Streamlit

OpenAI API (GPT + DALL·E)

gTTS (Text to Speech)

ChromaDB (vector store)

Sentence Transformers

##  WSL (Am folosit  Windows Subsystem for Linux)

 Microfonul nu funcționează în WSL → Voice Input a fost dezactivat

 Toate celelalte funcții (TTS, RAG, imagine) funcționează perfect