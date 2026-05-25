from flask import Blueprint, abort, jsonify, redirect, render_template, request, session, url_for
from werkzeug.datastructures import MultiDict

from app.controllers.document_controller import upload_documento
from app.controllers.student_controller import (
    get_student_area_data,
    get_student_by_user_id,
    get_student_document_request,
    mark_student_document_request_sent,
)
from app.routes.guards import student_required

student_bp = Blueprint("student", __name__)


@student_bp.route("/aluno", methods=["GET"])
@student_bp.route("/aluno/dashboard", methods=["GET"])
def dashboard():
    student_required()
    data = get_student_area_data(session.get("user_id"))
    if not data:
        abort(404)

    return render_template("student_dashboard.html", **data)


@student_bp.route("/aluno/documentos/upload", methods=["POST"])
def upload_documento_aluno():
    student_required()
    aluno = get_student_by_user_id(session.get("user_id"))
    if not aluno:
        return jsonify({"erro": "Aluno nao encontrado"}), 404

    solicitacao_id = request.form.get("solicitacao_id", type=int)
    if not solicitacao_id:
        return jsonify({"erro": "Solicitacao de documento nao informada"}), 400

    solicitacao = get_student_document_request(solicitacao_id, aluno["id"])
    if not solicitacao:
        return jsonify({"erro": "Solicitacao de documento nao encontrada"}), 404

    upload_form = MultiDict(request.form)
    upload_form["titulo"] = solicitacao["titulo"]

    response, status = upload_documento(
        upload_form,
        request.files,
        is_admin=True,
        aluno_id_override=aluno["id"],
    )

    if 200 <= status < 300:
        mark_student_document_request_sent(
            solicitacao_id,
            aluno["id"],
            response["documento"]["id"],
        )
        return redirect(url_for("student.dashboard"))

    return jsonify(response), status
