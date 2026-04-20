from werkzeug.security import generate_password_hash

from app.database import get_connection


def run_seed():
    usuarios = [
        ("admin@gmail.com", generate_password_hash("123"), "ADMIN"),
        ("prof@gmail.com", generate_password_hash("123"), "PROFESSOR"),
        ("aluno@gmail.com", generate_password_hash("123"), "ALUNO"),
    ]

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios")
            cursor.executemany(
                "INSERT INTO usuarios (email, senha, tipo) VALUES (%s, %s, %s)", usuarios
            )

    print("Usuários criados com sucesso!")


if __name__ == "__main__":
    run_seed()
