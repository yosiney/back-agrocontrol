# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project (no pasa nada si luego lo montás con volume)
COPY . .

# Expose FastAPI port (internal = 6868)
EXPOSE 6868

# Default CMD (prod) 👉 el compose ya sobreescribe con --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6868"]
