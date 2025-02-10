# Use the official Python image as a base
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY requirements.txt .
COPY main.py ./
COPY streamlit_ui.py ./

# Install dependencies
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --prefer-binary sentence-transformers

# Expose necessary ports
EXPOSE 8000 8501

# Start both FastAPI and Streamlit
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_ui.py --server.port 8501 --server.address 0.0.0.0
