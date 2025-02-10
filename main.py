
import chromadb
import os
import fitz  # PyMuPDF for PDF text extraction
import ollama
from sentence_transformers import SentenceTransformer
import re
import hashlib
import time
import gc

# 🔹 Database Setup
DB_PATH = "chatbot_db"
os.makedirs(DB_PATH, exist_ok=True)

# Initialize ChromaDB Client
chroma_client = chromadb.PersistentClient(path=DB_PATH)

# Ensure Collection Exists
db = chroma_client.get_or_create_collection("books")

# 🔹 Load Semantic Search Model
search_model = SentenceTransformer("all-MiniLM-L6-v2")

# 📝 Extract and Clean Text from PDF
def extract_text_from_pdf(pdf_path, max_pages=10):
    """ Extract text from the first max_pages of a PDF file and clean it """
    try:
        doc = fitz.open(pdf_path)
        text_list = []

        for page_num in range(min(max_pages, len(doc))):
            text = doc[page_num].get_text("text")
            text = re.sub(r'\s+', ' ', text).strip()
            text_list.extend(re.split(r'\n+', text))

        return [p for p in text_list if len(p) > 30]  # Remove short sentences
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return []

# 🏛️ Store Book in Database Efficiently
def store_book(file_path):
    """ Store book content in ChromaDB while avoiding duplicates """
    try:
        paragraphs = extract_text_from_pdf(file_path) if file_path.endswith(".pdf") else []

        if not paragraphs:
            print("⚠️ No text extracted from the file.")
            return "⚠️ No text extracted from the file."

        stored_data = db.get(include=["documents"])
        stored_paragraphs = set(stored_data.get("documents", []))

        for idx, paragraph in enumerate(paragraphs):
            hash_id = hashlib.md5(paragraph.encode()).hexdigest()
            if hash_id in stored_paragraphs:  # Skip if already exists
                print(f"⚠️ Skipping duplicate paragraph: {idx + 1}")
                continue

            embedding = search_model.encode(paragraph).tolist()
            db.add(
                ids=[hash_id], 
                documents=[paragraph],
                metadatas=[{"paragraph_title": f"Paragraph {idx + 1}", "chunk_id": idx}],
                embeddings=[embedding]
            )

        print("✅ Book stored in the database.")
        return "✅ Book successfully stored!"
    except Exception as e:
        print(f"❌ Error storing book: {e}")
        return f"❌ Error storing book: {e}"

# 🔍 Search for Relevant Paragraphs
def search_book(question, top_n=3):
    """ Search for the most relevant paragraphs to the question """
    try:
        stored_data = db.get(include=["documents"])
        total_docs = len(stored_data.get("documents", []))

        if total_docs == 0:
            return []

        adjusted_n_results = min(top_n, total_docs)
        print(f"🔍 Searching for: {question}")
        question_embedding = search_model.encode(question).tolist()
        results = db.query(query_embeddings=[question_embedding], n_results=adjusted_n_results)

        return results.get("documents", [[]])[0] if results else []
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

# 🤖 Generate Answer Using Ollama
def generate_answer(question, relevant_texts):
    """ Generate an answer using Ollama based only on retrieved texts """
    if not relevant_texts:
        return "❌ No sufficient information available."

    context = "\n\n".join(relevant_texts)
    prompt = f"""***Important:***
    You have only the following information to answer the question. ***Do not add extra details or make assumptions.***

    **Question:** {question}

    **Available Information:**
    {context}

    ***Your answer must be strictly based on the above information.*** If no clear answer is found, respond with: "❌ No sufficient information available."
    """

    retries = 3
    for attempt in range(retries):
        try:
            print("⚡ Sending request to Ollama...")
            #you can use another models like gemma , Mistral ,TinyLlama ,LLaMA3 
            response = ollama.chat(model="phi", messages=[{"role": "user", "content": prompt}])
            gc.collect()
            print("✅ Response received from Ollama.")

            answer = response["message"]["content"].strip()
            if "sorry" in answer.lower() or "i don't know" in answer.lower():
                return "❌ No sufficient information available."

            return answer
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    return "⚠️ Error calling the model. Ensure it is running correctly."

# 🏁 Chatbot Interaction
def chatbot():
    """ Start chatbot interaction """
    print("\n🤖 Welcome! Type your question or 'exit' to quit.")

    while True:
        question = input("\n📌 Ask a question: ").strip()
        if question.lower() == "exit":
            print("👋 Goodbye!")
            break

        relevant_texts = search_book(question)
        answer = generate_answer(question, relevant_texts)
        print("\n🔍 Answer:\n", answer)
        gc.collect()

# 🏁 Start Chatbot if run directly
if __name__ == "__main__":
    chatbot()
