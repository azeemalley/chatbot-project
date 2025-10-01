# 🤖 Super AI Chatbot

An advanced AI chatbot project built using **Python**, **Streamlit**, and **OpenAI GPT‑3.5**.  

This app allows interactive conversations, personality switching, and can even answer questions based on uploaded PDF documents.

## 🌍 Live Demo
👉 [Click here to try the chatbot](https://chatbot-project-fkts6jqxocoyyojuk9p6pj.streamlit.app/)

## ✨ Features
- 🔹 **Personality Selector** – switch between Job Mentor, Teacher, Motivational Coach, or even a Pirate 🏴‍☠️  
- 🔹 **Multi-turn Conversation** – chatbot remembers the discussion context during your session  
- 🔹 **PDF Q&A Assistant** – upload a PDF and ask questions directly from its content  
- 🔹 **Beautiful UI** – deployed on **Streamlit Cloud** and accessible anywhere  

## 🛠️ Tech Stack
- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) – front-end and live deployment  
- [OpenAI GPT-3.5](https://platform.openai.com/) – LLM backend for conversation  
- [FAISS](https://github.com/facebookresearch/faiss) + [scikit-learn](https://scikit-learn.org/) – to support PDF search with embeddings  
- [PyPDF2](https://pypi.org/project/PyPDF2/) – extract text from PDF documents  

## 🖥️ Run Locally
To run this app locally:

```bash
# Clone the repo
git clone https://github.com/azeemalley/chatbot-project.git
cd chatbot-project

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
