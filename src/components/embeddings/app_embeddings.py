import streamlit as st
from src.commons.models.chat_retriever.chat_history import ChatHistory
from src.retrievers.retrievers_logic import vector_retriever
from src.vector_store_client.vector_store_client_logic import VectorStoreManager
from src.commons.enums.type_message import TypeMessage
import time

# Inicializar VectorStoreManager
vectorStoreManager = VectorStoreManager()

# Título de la aplicación
st.title("Vector query")

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
                    time.sleep(5)
                    bot_response = vector_retriever(user_prompt)
                    if bot_response.typeMessage == TypeMessage.INFO:
                        chat.message = bot_response.response
                    else:
                        chat.message = bot_response.message
            st.markdown(
                f'<div class="chat-container"><div class="bot-message">{chat.message}</div></div>',
                unsafe_allow_html=True,
            )
