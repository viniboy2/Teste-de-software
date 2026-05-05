import os

from flask import Blueprint, current_app, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from app.auth import jwt_required, professor_required
from app.controllers.auth_controller import buscar_alunos, cadastrar_usuario, login_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response, status = login_usuario(data)
    return jsonify(response), status


@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    response, status = cadastrar_usuario(data)
    return jsonify(response), status


@auth_bp.route('/professor/teste', methods=['GET'])
@professor_required
def teste_professor():
    # Rota simples para validar se o JWT pertence a um professor.
    return jsonify({"mensagem": "Permissao de professor validada"}), 200


@auth_bp.route('/alunos/busca', methods=['GET'])
@professor_required
def alunos_busca():
    termo = request.args.get("termo") or request.args.get("q") or request.args.get("cpf")
    response, status = buscar_alunos(termo)
    return jsonify(response), status


@auth_bp.route('/arquivos/upload', methods=['POST'])
@professor_required
def upload_arquivo():
    if "arquivo" not in request.files:
        return jsonify({"erro": "Arquivo nao enviado"}), 400

    arquivo = request.files["arquivo"]
    if not arquivo.filename:
        return jsonify({"erro": "Nome do arquivo nao informado"}), 400

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    # Estrutura inicial: salva o arquivo fisico e devolve o nome para download posterior.
    filename = secure_filename(arquivo.filename)
    arquivo.save(os.path.join(upload_folder, filename))

    return jsonify({"mensagem": "Arquivo enviado", "arquivo": filename}), 201


@auth_bp.route('/arquivos/download/<path:filename>', methods=['GET'])
@jwt_required
def download_arquivo(filename):
    # Download exige JWT valido, mas pode ser usado por professor ou aluno autenticado.
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, secure_filename(filename), as_attachment=True)
