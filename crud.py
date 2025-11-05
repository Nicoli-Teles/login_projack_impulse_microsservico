from sqlalchemy.orm import Session
from models import Usuario

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def criar_usuario(db: Session, email: str, senha_hash: str):
    usuario = Usuario(email=email, senha=senha_hash)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
