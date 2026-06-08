from flask import abort, jsonify, session

from app.auth import normalize_role


def admin_required():
    if normalize_role(session.get("user_role")) != "admin":
        abort(403)


def admin_json_required():
    if normalize_role(session.get("user_role")) != "admin":
        return jsonify({"erro": "Acesso permitido apenas para administradores"}), 403

    return None


def aluno_required():
    if normalize_role(session.get("user_role")) != "aluno":
        abort(403)


def teacher_required():
    if normalize_role(session.get("user_role")) != "professor":
        abort(403)
