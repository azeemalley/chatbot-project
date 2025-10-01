import os
import streamlit as st
from openai import OpenAI
import faiss
import tempfile
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="Super AI Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Super AI Chatbot")
st.write("Chat with GPT‑3.5 or upload a PDF for Q&A 📄")

# Select personality
personality = st.selectbox(
    "🔹 Choose Personality Mode:",
    ["Professional Job Mentor", "Polite Teacher", "Motivational Coach", "Sarcastic Pirate"]
)

system_prompts = {
    "Professional Job Mentor": "You are a job interview mentor. Give clear, practical advice.",
    "Polite Teacher": "You are a patient teacher. Explain things step by step in simple words.",
    "Motivational Coach": "You are an inspiring motivational coach. Encourage the user with energy.",
    "Sarcastic Pirate": "You are a funny pirate. Reply like a pirate with jokes and 'Arrr!'."
}

# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- 📄 PDF Upload Section ---------------- #
st.sidebar.header("📄 Document Q&A Mode")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")
pdf_text = ""

if uploaded_file:
    # Extract text
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    # Split into small chunks
    docs = pdf_text.split(". ")
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(docs)
    faiss_index = faiss.IndexFlatL2(vectors.shape[1])
    faiss_index.add(vectors.toarray().astype("float32"))

    st.sidebar.success("✅ PDF uploaded and processed!")

# ---------------- Chat Section ---------------- #
user_input = st.chat_input("Type your message...")

if user_input:
    if uploaded_file and pdf_text.strip() != "":
        # --- PDF Q&A mode ---
        user_vec = vectorizer.transform([user_input]).toarray().astype("float32")
        D, I = faiss_index.search(user_vec, k=2)  # Top 2 matches
        context = " ".join([docs[i] for i in I[0]])

        messages = [
            {"role": "system", "content": "You are a helpful assistant for PDF Q&A."},
            {"role": "user", "content": f"Context from PDF:\n{context}\n\nQuestion: {user_input}"}
        ]

    else:
        # --- Normal chatbot mode ---
        messages = [{"role": "system", "content": system_prompts[personality]}] + st.session_state.messages
        messages.append({"role": "user", "content": user_input})

    # GPT Response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response.choices[0].message.content

    # Save conversation if not PDF mode
    if not uploaded_file:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display response
    st.markdown(f"**🤖 Bot ({personality if not uploaded_file else 'PDF Assistant'}):** {reply}")

# ---------------- Display History ---------------- #
if not uploaded_file:
    st.write("### 💬 Conversation History")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**👤 You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**🤖 Bot ({personality}):** {msg['content']}")