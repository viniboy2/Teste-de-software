from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth import generate_token, normalize_role
from app.database import get_session
from app.models import AlunoModel, ProfessorModel, UsuarioModel


def login_usuario(data):
    if not data:
        return {"erro": "Dados nao informados"}, 400

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return {"erro": "E-mail e senha sao obrigatorios"}, 400

    session = get_session()
    try:
        user = session.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    finally:
        session.close()

    if not user:
        return {"erro": "Usuario nao encontrado"}, 404

    if not check_password_hash(user.senha, senha):
        return {"erro": "Senha invalida"}, 401

    role = normalize_role(user.tipo)

    return {
        "id": user.id,
        "email": user.email,
        "tipo": role.upper(),
        "role": role,
        # O JWT tambem inclui a role para o front enviar nas proximas chamadas protegidas.
        "token": generate_token(user),
    }, 200


def _parse_date(value):
    if not value:
        return None

    return datetime.strptime(value, "%Y-%m-%d").date()


def cadastrar_usuario(data):
    if not data:
        return {"erro": "Dados nao informados"}, 400

    tipo = normalize_role(data.get("tipo") or data.get("role"))
    email = data.get("email")
    senha = data.get("senha")
    nome = data.get("nome")

    if tipo not in {"professor", "aluno"}:
        return {"erro": "Tipo de usuario deve ser professor ou aluno"}, 400

    if not email or not senha or not nome:
        return {"erro": "E-mail, senha e nome sao obrigatorios"}, 400

    session = get_session()
    try:
        if session.query(UsuarioModel).filter(UsuarioModel.email == email).first():
            return {"erro": "E-mail ja cadastrado"}, 409

        usuario = UsuarioModel(
            email=email,
            senha=generate_password_hash(senha),
            # O cadastro agora grava a role do usuario para refletir professor/aluno no JWT.
            tipo=tipo,
        )
        session.add(usuario)
        session.flush()

        if tipo == "professor":
            cpf = data.get("cpf")
            if not cpf:
                session.rollback()
                return {"erro": "CPF e obrigatorio para professor"}, 400

            session.add(
                ProfessorModel(
                    usuario_id=usuario.id,
                    nome=nome,
                    cpf=cpf,
                    telefone=data.get("telefone"),
                )
            )
        else:
            cpf = data.get("cpf")
            matricula = data.get("matricula")
            if not matricula:
                session.rollback()
                return {"erro": "Matricula e obrigatoria para aluno"}, 400

            session.add(
                AlunoModel(
                    usuario_id=usuario.id,
                    nome=nome,
                    cpf=cpf,
                    matricula=matricula,
                    data_nascimento=_parse_date(data.get("data_nascimento")),
                )
            )

        session.commit()
        return {
            "id": usuario.id,
            "email": usuario.email,
            "tipo": tipo.upper(),
            "role": tipo,
        }, 201
    except ValueError:
        session.rollback()
        return {"erro": "Data de nascimento deve estar no formato YYYY-MM-DD"}, 400
    except IntegrityError:
        session.rollback()
        return {"erro": "Dados duplicados: verifique CPF, matricula ou e-mail"}, 409
    finally:
        session.close()


def buscar_alunos(termo):
    termo = (termo or "").strip()
    if not termo:
        return {"erro": "Informe um termo de busca"}, 400

    session = get_session()
    try:
        alunos = (
            session.query(AlunoModel)
            # Busca por nome parcial ou CPF exato/parcial para apoiar a tela do professor.
            .filter(or_(AlunoModel.nome.ilike(f"%{termo}%"), AlunoModel.cpf.ilike(f"%{termo}%")))
            .limit(20)
            .all()
        )

        return {
            "alunos": [
                {
                    "id": aluno.id,
                    "usuario_id": aluno.usuario_id,
                    "nome": aluno.nome,
                    "cpf": aluno.cpf,
                    "matricula": aluno.matricula,
                    "data_nascimento": (
                        aluno.data_nascimento.isoformat()
                        if aluno.data_nascimento
                        else None
                    ),
                }
                for aluno in alunos
            ]
        }, 200
    finally:
        session.close()
