import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv(override=True)

st.set_page_config(page_title="TechNova Support", page_icon="🎧", layout="wide")

st.markdown("""
    <style>
        .stChatMessage { border-radius: 12px; }
        h1 { color: #10b981; }
    </style>
""", unsafe_allow_html=True)

if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

PROMPT_TEMPLATE = """
You are a friendly and professional customer support agent for TechNova.
Answer the customer's question using ONLY the information provided in the context below.

If the answer is not in the context, say exactly this:
"I don't have that information right now. Let me connect you with a human agent who can help. Please email support@technova.io or use the live chat inside the app."

Never make up answers. Never guess. If unsure, escalate.

Context:
{context}

Chat history:
{chat_history}

Customer question: {question}

Your answer:
"""

@st.cache_resource
def load_knowledge_base():
    loader = DirectoryLoader("docs", glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=".chroma"
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def ask_question(retriever, question, chat_history):
    history_text = ""
    for q, a in chat_history[-3:]:
        history_text += f"Customer: {q}\nAgent: {a}\n"
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
    parser = StrOutputParser()
    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
            "chat_history": lambda _: history_text
        }
        | prompt
        | llm
        | parser
    )
    return chain.invoke(question)

with st.sidebar:
    st.title("🎧 TechNova Support")
    st.markdown("*Powered by AI — here to help 24/7*")
    st.divider()
    st.markdown("### How can I help you?")
    st.markdown("""
    - Questions about your account
    - Billing and payments
    - Plan features and limits
    - Integrations and setup
    - Data and privacy
    """)
    st.divider()
    st.markdown("**Can't find your answer?**")
    st.markdown("📧 support@technova.io")
    st.markdown("💬 Live chat inside the app")
    if st.session_state.chat_history:
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

st.markdown("## 🎧 TechNova Support")
st.markdown("Hi there! I'm the TechNova support assistant. Ask me anything about your account, billing, or how the platform works.")
st.divider()

if st.session_state.retriever is None:
    with st.spinner("Loading knowledge base..."):
        st.session_state.retriever = load_knowledge_base()

for question, answer in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        st.write(answer)

user_question = st.chat_input("Type your question here...")

if user_question:
    with st.chat_message("user"):
        st.write(user_question)
    with st.chat_message("assistant"):
        with st.spinner("Looking that up..."):
            answer = ask_question(
                st.session_state.retriever,
                user_question,
                st.session_state.chat_history
            )
        st.write(answer)
    st.session_state.chat_history.append((user_question, answer))