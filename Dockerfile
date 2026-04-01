# Stage 1: Build Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Backend & Final Image
FROM python:3.11-slim
WORKDIR /app

# Instalar dependências de sistema para o OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Configurar ambiente Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do backend
COPY backend/ .

# Copiar o build do frontend para a pasta static do backend
COPY --from=frontend-builder /app/frontend/dist ./static

# Expor a porta 8080 (padrão do Fly.io)
EXPOSE 8080

# Comando para iniciar o servidor com Uvicorn
# Importante: O Fly.io usa a porta 8080 por padrão
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
