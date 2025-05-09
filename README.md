
# 🤖 Chatbot with PDF Knowledge Base  
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/MariamMahm0ud/chatbot)

## 📌 Project Overview  
This project is an **AI-powered chatbot** capable of answering user queries based on the content of uploaded PDF books. It uses **ChromaDB** for storing and retrieving text, **Sentence Transformers** for semantic search, and **Ollama** for generating responses.

## 🚀 Features  
✅ Extracts and cleans text from PDFs  
✅ Stores data in a **vector database (ChromaDB)** for efficient retrieval  
✅ Performs **semantic search** using `all-MiniLM-L6-v2`  
✅ Generates responses using **Ollama AI models**  
✅ Supports multiple AI models (**Phi, Mistral, Gemma, TinyLlama, LLaMA3**)  
✅ Interactive **Streamlit UI** for easy usage  
✅ Deployment-ready with **Docker support**  

## 🛠️ Technologies Used  
- **Python 3.10+**  
- **ChromaDB** (for vector storage)  
- **PyMuPDF (fitz)** (for PDF text extraction)  
- **SentenceTransformers** (for embeddings)  
- **Ollama AI** (for generating answers)  
- **Streamlit** (for UI)  
- **Docker** (for deployment)  

## 📂 Project Structure  
```
📦 chatbot_project  
 ├── chatbot_db/        # Local ChromaDB database  
 ├── __pycache__/       # Python cache files  
 ├── deploy.py          # Deployment script  
 ├── dockerfile         # Docker configuration  
 ├── main.py            # Core chatbot logic  
 ├── streamlit_ui.py    # Streamlit-based web UI  
 ├── requirements.txt   # Required Python libraries  
 ├── Py-tutorial.pdf    # Example PDF document  
 └── README.md          # Project documentation  
```

## 🏗️ How to Set Up & Run  

### 🔹 1. Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### 🔹 2. Run the Chatbot in Terminal  
```bash
python main.py
```

### 🔹 3. Run the Web Interface (Streamlit UI)  
```bash
streamlit run streamlit_ui.py
```

### 🔹 4. Run with Docker (Optional)  
```bash
docker build -t chatbot-app .

```

## 💡 How It Works  
1. **Extracts text** from uploaded PDFs  
2. **Stores processed text** in a vector database (ChromaDB)  
3. **Searches for relevant sections** when a user asks a question  
4. **Generates an AI response** using Ollama (based only on retrieved content)  
5. **Displays the answer** in the terminal or web UI  

## 🎯 Example Usage  
- Upload a book (PDF)  
- Ask: *"What is loop in python?"*  
- The chatbot will retrieve relevant sections and generate an AI-powered response  

## 📌 Future Improvements  
- ✅ Support for **multi-document retrieval**  
- ✅ Integration with **LangChain** for advanced workflows  
- ✅ More **AI models** for response generation  
- ✅ **User authentication** for better security  


