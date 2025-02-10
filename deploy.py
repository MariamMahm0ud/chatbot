

from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from main import store_book, search_book, generate_answer  # استيراد الفانكشنز من main.py
import os
import shutil

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API to upload files
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        response = store_book(file_location)  # استدعاء الدالة من main.py
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

# API for chatbot
@app.get("/chat/")
async def chat(question: str):
    relevant_texts = search_book(question)  # البحث عن المعلومات في الـ DB
    answer = generate_answer(question, relevant_texts)  # توليد الإجابة باستخدام Ollama
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
