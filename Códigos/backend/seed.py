from app import app
from database.db import db
from models.usuario_model import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    usuarios = [
        Usuario(email="admin@gmail.com", senha=generate_password_hash("123"), tipo="ADMIN"),
        Usuario(email="prof@gmail.com", senha=generate_password_hash("123"), tipo="PROFESSOR"),
        Usuario(email="aluno@gmail.com", senha=generate_password_hash("123"), tipo="ALUNO"),
    ]

    db.session.add_all(usuarios)
    db.session.commit()

    print("Usuários criados com sucesso!")