from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas
from security import verificar_senha, gerar_hash_senha
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Login Microservice - SQLite")

# Permitir que o HTML acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_email(db, email=usuario.email)
    if not db_usuario or not verificar_senha(usuario.senha, db_usuario.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    return {"mensagem": "Login bem-sucedido!", "usuario_id": db_usuario.id}

# rota opcional para criar usuário de teste (executar 1 vez)
@app.post("/criar_teste")
def criar_usuario_teste(db: Session = Depends(get_db)):
    email = "teste@exemplo.com"
    senha_hash = gerar_hash_senha("123456")
    existente = crud.get_usuario_by_email(db, email)
    if existente:
        return {"mensagem": "Usuário de teste já existe."}
    crud.criar_usuario(db, email, senha_hash)
    return {"mensagem": "Usuário de teste criado com sucesso!"}
