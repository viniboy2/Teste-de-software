from werkzeug.security import check_password_hash

from app.database import get_session
from app.models import UsuarioModel


def login_usuario(data):
    if not data:
        return {"erro": "Dados não informados"}, 400

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return {"erro": "E-mail e senha são obrigatórios"}, 400

    session = get_session()
    try:
        user = session.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    finally:
        session.close()

    if not user:
        return {"erro": "Usuário não encontrado"}, 404

    if not check_password_hash(user.senha, senha):
        return {"erro": "Senha inválida"}, 401

    return {
        "id": user.id,
        "email": user.email,
        "tipo": user.tipo,
    }, 200
