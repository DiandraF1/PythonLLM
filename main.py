 # Punctul de intrare pentru chatbot CLI sau Streamlit

from chatbot import ask_chatbot

while True:
    query = input("Tu: ")
    if query.lower() in ["exit", "quit"]:
        break
    print("\nAI:\n", ask_chatbot(query), "\n")
