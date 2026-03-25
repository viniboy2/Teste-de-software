from models.usuario_model import Usuario
from werkzeug.security import check_password_hash

def login_usuario(data):
    user = Usuario.query.filter_by(email=data.get('email')).first()

    if not user:
        return {"erro": "Usuário não encontrado"}, 404

    if not check_password_hash(user.senha, data.get('senha')):
        return {"erro": "Senha inválida"}, 401

    return {
        "id": user.id,
        "email": user.email,
        "tipo": user.tipo
    }, 200