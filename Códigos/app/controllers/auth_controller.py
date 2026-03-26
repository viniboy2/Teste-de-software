from werkzeug.security import check_password_hash

from app.database import get_connection


def login_usuario(data):
    if not data:
        return {"erro": "Dados não informados"}, 400

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return {"erro": "E-mail e senha são obrigatórios"}, 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, email, senha, tipo FROM usuarios WHERE email = %s",
                (email,),
            )
            user = cursor.fetchone()

    if not user:
        return {"erro": "Usuário não encontrado"}, 404

    if not check_password_hash(user["senha"], senha):
        return {"erro": "Senha inválida"}, 401

    return {
        "id": user["id"],
        "email": user["email"],
        "tipo": user["tipo"],
    }, 200
