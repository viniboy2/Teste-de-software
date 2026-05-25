from flask import Blueprint, jsonify, redirect, request, send_from_directory, session
from werkzeug.utils import secure_filename

from app.auth import decode_token_from_request, normalize_role
from app.controllers.document_controller import get_upload_folder, upload_documento
from app.database import get_session
from app.models import AlunoModel, DocumentoModel

document_bp = Blueprint("document", __name__)


@document_bp.route('/arquivos/upload', methods=['POST'])
def upload_arquivo():
    is_admin = normalize_role(session.get("user_role")) == "admin"
    jwt_payload = None
    if not is_admin:
        jwt_payload, error_response = decode_token_from_request()
        if error_response:
            return error_response

        role = normalize_role(jwt_payload.get("role") or jwt_payload.get("tipo"))
        if role != "professor":
            return jsonify({"erro": "Acesso permitido apenas para professores ou administradores"}), 403

    if "arquivo" not in request.files:
        return jsonify({"erro": "Arquivo nao enviado"}), 400

    response, status = upload_documento(
        request.form,
        request.files,
        current_user=jwt_payload,
        is_admin=is_admin,
    )

    redirect_to = request.form.get("redirect_to")
    if 200 <= status < 300 and redirect_to and redirect_to.startswith("/"):
        return redirect(redirect_to)

    return jsonify(response), status


@document_bp.route('/arquivos/download/<path:filename>', methods=['GET'])
def download_arquivo(filename):
    role = normalize_role(session.get("user_role"))
    safe_filename = secure_filename(filename)

    if role == "aluno":
        db = get_session()
        try:
            documento = (
                db.query(DocumentoModel)
                .join(AlunoModel, AlunoModel.id == DocumentoModel.aluno_id)
                .filter(
                    AlunoModel.usuario_id == session.get("user_id"),
                    DocumentoModel.caminho_arquivo == safe_filename,
                )
                .first()
            )
        finally:
            db.close()

        if not documento:
            return jsonify({"erro": "Arquivo nao encontrado para este aluno"}), 404
    elif role != "admin":
        _, error_response = decode_token_from_request()
        if error_response:
            return error_response

    return send_from_directory(get_upload_folder(), safe_filename, as_attachment=True)
