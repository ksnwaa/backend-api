# Gunakan image Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Ekspos port 8080
EXPOSE 8080

# Jalankan aplikasi
CMD ["python", "/app/app.py"]

