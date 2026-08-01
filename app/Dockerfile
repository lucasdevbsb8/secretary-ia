FROM python:3.12-slim

# Nome do projeto como diretório de trabalho dentro do container
WORKDIR /secretary-ia

# Dependências primeiro (aproveita cache de camada)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o pacote da API e os estáticos do formulário
COPY backend/ ./backend/
COPY frontend/ ./frontend/

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]