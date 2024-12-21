import streamlit as st
from src.retrievers.models.chat_history import ChatHistory
from src.embedding.embeddings_logic import EmbeddingManager
from src.commons.enums.type_message import TypeMessage
from src.retrievers.retrievers_logic import Retrievers
from src.query_rewriting.query_rewriting_logic import QueryRewriting

# Título de la aplicación
st.title("Advance vector retriever")
embedding = EmbeddingManager()
retriever = Retrievers()
query_rewriter = QueryRewriting()
rewrited_query = ""
# Inicializar chat history si no está en el estado
if "advance_chat_history" not in st.session_state:
    st.session_state.advance_chat_history = []

# Entrada del usuario para consultas
user_prompt = st.chat_input("Escribe tu consulta")

# Procesar la consulta del usuario
if user_prompt:
    rewrited_query = query_rewriter.rewriting(user_prompt)
    st.session_state.advance_chat_history.append(
        ChatHistory(role="user", message=rewrited_query.rewriting_query)
    )
    st.session_state.advance_chat_history.append(ChatHistory(role="bot", message="..."))

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
    .no-response {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Mostrar el historial del chat
if st.session_state.advance_chat_history:
    for i, chat in enumerate(st.session_state.advance_chat_history):
        if chat.role == "user":
            st.markdown(
                f'<div class="chat-container"><div class="user-message">{chat.message}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            if (
                i == len(st.session_state.advance_chat_history) - 1
                and chat.message == "..."
            ):
                with st.spinner("..."):
                    top_k = 3
                    bot_response = retriever.advance_query_retrieval(
                        query=rewrited_query.rewriting_query
                    )
                    if bot_response.type_message == TypeMessage.INFO:
                        chat.message = bot_response.response
                    else:
                        chat.message = bot_response.message
            st.markdown(
                f'<div class="chat-container"><div class="bot-message">{chat.message}</div></div>',
                unsafe_allow_html=True,
            )
