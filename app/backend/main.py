import os
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/health")
def health():
    with engine.connect() as conn:
        versao = conn.execute(text("SELECT version()")).scalar()
    return {"status": "ok", "postgres": versao}

@app.post("/enviar")
def enviar(nome: str = Form(...), mensagem: str = Form(...)):
    # por enquanto só devolve; depois você grava no banco
    return {"recebido": {"nome": nome, "mensagem": mensagem}}

# Estáticos SEMPRE por último, senão o mount engole as rotas acima
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")