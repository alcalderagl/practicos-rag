import streamlit as st
from typing import List
from qdrant_client.conversions import common_types as types
from src.retrievers.models.chat_history import ChatHistory
from src.embedding.embeddings_logic import EmbeddingManager
from src.commons.enums.type_message import TypeMessage
from src.retrievers.retrievers_logic import Retrievers
from src.query_rewriting.query_rewriting_logic import QueryRewriting

# Título de la aplicación
st.title("Vector retriever")
embedding = EmbeddingManager()
retriever = Retrievers()
query_rewriter = QueryRewriting()
rewrited_query = ""

option = st.selectbox(
    "Selected a vector retrieval?",
    ("🧩Naive", "📡Advance", "⚖️Compare"),
    key="vector_retrieval_option",
    on_change=lambda: st.session_state.update({"chat_history": []}),
)


# Inicializar chat history si no está en el estado
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Entrada del usuario para consultas
user_prompt = st.chat_input("Write your question")

# Procesar la consulta del usuario
if user_prompt:
    if option == "📡Advance":
        rewrited_query = query_rewriter.rewriting(user_prompt).rewriting_query
        st.session_state.chat_history.append(
            ChatHistory(role="user", message=rewrited_query)
        )
    elif option == "🧩Naive":
        st.session_state.chat_history.append(
            ChatHistory(role="user", message=user_prompt)
        )
    else:
        rewrited_query = query_rewriter.rewriting(user_prompt).rewriting_query
        st.session_state.chat_history.append(
            ChatHistory(
                role="user",
                message=f"user question ->{user_prompt} <br/> rewrited question -> {rewrited_query}",
            )
        )
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
    .no-response {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initial_retrieval(user_prompt: str) -> str:
    top_k = 3
    bot_response = retriever.initial_query_retrieval(
        query_text=user_prompt, top_k=top_k
    )
    if bot_response.type_message == TypeMessage.INFO:
        best_resp = []
        response: List[types.ScoredPoint] = bot_response.response
        for index, resp in enumerate(response):
            page_content = resp.payload.get("page_content", "")
            best_resp.append(
                f'<span class="no-response">Resultado {index + 1} - {round(resp.score * 100, 2) }%</span> <br/> {page_content} <br/> <br/>'
            )
        return (
            f'<span class="no-response">Te comparto los {top_k} resultados similares a tu pregunta:</span><br/><br/>'
            + " ".join(best_resp)
        )
    else:
        return bot_response.message


def advance_retrieval(user_prompt: str) -> str:
    bot_response = retriever.advance_query_retrieval(query=user_prompt)
    if bot_response.type_message == TypeMessage.INFO:
        return bot_response.response
    else:
        return bot_response.message


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
                    if option == "🧩Naive":
                        chat.message = initial_retrieval(user_prompt=user_prompt)
                    elif option == "📡Advance":
                        chat.message = advance_retrieval(user_prompt=rewrited_query)
                    else:
                        # compare
                        naive_bot_response = initial_retrieval(user_prompt=user_prompt)
                        advance_bot_response = advance_retrieval(
                            user_prompt=rewrited_query
                        )
                        chat.message = (
                            naive_bot_response
                            + '<br/> <span class="no-response">Respuesta resumida</span><br/>'
                            + advance_bot_response
                        )
            st.markdown(
                f'<div class="chat-container"><div class="bot-message">{chat.message}</div></div>',
                unsafe_allow_html=True,
            )
