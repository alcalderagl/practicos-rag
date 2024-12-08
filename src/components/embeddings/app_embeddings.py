import streamlit as st
from src.commons.models.chat_retriever.chat_history import ChatHistory
from src.embedding.embeddings_logic import EmbeddingManager
from src.commons.enums.type_message import TypeMessage

# Título de la aplicación
st.title("Vector query")
embedding = EmbeddingManager()
# Inicializar chat history si no está en el estado
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Entrada del usuario para consultas
user_prompt = st.chat_input("Escribe tu consulta")

# Procesar la consulta del usuario
if user_prompt:
    st.session_state.chat_history.append(ChatHistory(role="user", message=user_prompt))
    st.session_state.chat_history.append(ChatHistory(role="bot", message="..."))

# Estilo para los mensajes del chat
st.markdown(
    """
    <style>
    .user-message {
        color: black;
        background-color: #dcf8c6;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 10px;
        width: fit-content;
        align-self: flex-end;
    }
    .bot-message {
        color: black;
        background-color: #f1f0f0;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 10px;
        width: fit-content;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Mostrar el historial del chat
if st.session_state.chat_history:
    for i, chat in enumerate(st.session_state.chat_history):
        if chat.role == "user":
            st.markdown(
                f'<div class="chat-container"><div class="user-message">{chat.message}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            if i == len(st.session_state.chat_history) - 1 and chat.message == "...":
                with st.spinner("..."):
                    bot_response = embedding.query_qdrant(
                        query_text=user_prompt, top_k=5
                    )
                    if bot_response.type_message == TypeMessage.INFO:
                        # responses = [resp for resp in bot_response.response]
                        best_resp = []
                        for resp in bot_response.response:
                            best_resp.append(f"{resp.score} -> {resp.payload['text']}")
                            # print(resp.score, resp.payload['text'])
                        chat.message = "\n".join(best_resp)

                        #'These are the similarities to your query ' + ' '.join(responses)
                    else:
                        chat.message = bot_response.message
            st.markdown(
                f'<div class="chat-container"><div class="bot-message">{chat.message}</div></div>',
                unsafe_allow_html=True,
            )
