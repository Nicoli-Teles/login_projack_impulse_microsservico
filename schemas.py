from pydantic import BaseModel

class UsuarioLogin(BaseModel):
    email: str
    senha: str
