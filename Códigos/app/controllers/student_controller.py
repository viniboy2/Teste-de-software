from datetime import datetime

from app.controllers.admin_controller import format_created_at
from app.database import get_session
from app.models import (
    AlunoModel,
    AlunoDisciplinaModel,
    DisciplinaModel,
    DocumentoModel,
    NotaModel,
    ProfessorDisciplinaModel,
    ProfessorModel,
    SolicitacaoDocumentoModel,
    UsuarioModel,
)


def get_student_by_user_id(user_id):
    db = get_session()
    try:
        row = (
            db.query(AlunoModel, UsuarioModel.email)
            .join(UsuarioModel, UsuarioModel.id == AlunoModel.usuario_id)
            .filter(AlunoModel.usuario_id == user_id)
            .first()
        )
        if not row:
            return None

        aluno, email = row
        return {
            "id": aluno.id,
            "nome": aluno.nome,
            "email": email,
            "matricula": aluno.matricula,
            "curso": aluno.curso_serie or "Nao informado",
            "status": aluno.status_matricula or "Nao informado",
        }
    finally:
        db.close()


def get_student_area_data(user_id):
    db = get_session()
    try:
        row = (
            db.query(AlunoModel, UsuarioModel.email)
            .join(UsuarioModel, UsuarioModel.id == AlunoModel.usuario_id)
            .filter(AlunoModel.usuario_id == user_id)
            .first()
        )
        if not row:
            return None

        aluno, email = row
        notas = (
            db.query(NotaModel, DisciplinaModel.nome)
            .join(DisciplinaModel, DisciplinaModel.id == NotaModel.disciplina_id)
            .filter(NotaModel.aluno_id == aluno.id)
            .order_by(DisciplinaModel.nome.asc())
            .all()
        )
        documentos = (
            db.query(DocumentoModel)
            .filter(DocumentoModel.aluno_id == aluno.id)
            .order_by(DocumentoModel.id.desc())
            .limit(12)
            .all()
        )
        solicitacoes = (
            db.query(SolicitacaoDocumentoModel)
            .filter(SolicitacaoDocumentoModel.aluno_id == aluno.id)
            .order_by(SolicitacaoDocumentoModel.id.desc())
            .limit(12)
            .all()
        )
        disciplinas = (
            db.query(DisciplinaModel)
            .join(
                AlunoDisciplinaModel,
                AlunoDisciplinaModel.disciplina_id == DisciplinaModel.id,
            )
            .filter(AlunoDisciplinaModel.aluno_id == aluno.id)
            .order_by(DisciplinaModel.nome.asc())
            .all()
        )

        disciplinas_map = {
            disciplina.id: {
                "nome": disciplina.nome,
                "codigo": disciplina.codigo,
                "carga_horaria": disciplina.carga_horaria,
                "professores": [],
            }
            for disciplina in disciplinas
        }

        if disciplinas_map:
            professor_links = (
                db.query(ProfessorDisciplinaModel.disciplina_id, ProfessorModel.nome)
                .join(ProfessorModel, ProfessorModel.id == ProfessorDisciplinaModel.professor_id)
                .filter(ProfessorDisciplinaModel.disciplina_id.in_(disciplinas_map.keys()))
                .order_by(ProfessorModel.nome.asc())
                .all()
            )
            for disciplina_id, professor_name in professor_links:
                if disciplina_id in disciplinas_map:
                    disciplinas_map[disciplina_id]["professores"].append(professor_name)

        return {
            "aluno": {
                "id": aluno.id,
                "nome": aluno.nome,
                "email": email,
                "matricula": aluno.matricula,
                "curso": aluno.curso_serie or "Nao informado",
                "status": aluno.status_matricula or "Nao informado",
            },
            "disciplinas": list(disciplinas_map.values()),
            "notas": [
                {
                    "disciplina": disciplina_nome,
                    "nota": nota.nota,
                    "observacao": nota.observacao or "-",
                    "data": format_created_at(nota.data_lancamento),
                }
                for nota, disciplina_nome in notas
            ],
            "documentos": [
                {
                    "titulo": documento.titulo,
                    "arquivo": documento.caminho_arquivo,
                    "data": format_created_at(documento.data_envio),
                }
                for documento in documentos
            ],
            "solicitacoes_documentos": [
                {
                    "id": solicitacao.id,
                    "titulo": solicitacao.titulo,
                    "mensagem": solicitacao.mensagem or "Envie o documento solicitado pela secretaria.",
                    "status": solicitacao.status,
                    "status_label": "Enviado" if solicitacao.status == "enviado" else "Pendente",
                    "data": format_created_at(solicitacao.created_at),
                }
                for solicitacao in solicitacoes
            ],
        }
    finally:
        db.close()


def get_student_document_request(solicitacao_id, aluno_id):
    db = get_session()
    try:
        solicitacao = (
            db.query(SolicitacaoDocumentoModel)
            .filter(
                SolicitacaoDocumentoModel.id == solicitacao_id,
                SolicitacaoDocumentoModel.aluno_id == aluno_id,
            )
            .first()
        )
        if not solicitacao:
            return None

        return {
            "id": solicitacao.id,
            "titulo": solicitacao.titulo,
            "status": solicitacao.status,
        }
    finally:
        db.close()


def mark_student_document_request_sent(solicitacao_id, aluno_id, documento_id):
    db = get_session()
    try:
        solicitacao = (
            db.query(SolicitacaoDocumentoModel)
            .filter(
                SolicitacaoDocumentoModel.id == solicitacao_id,
                SolicitacaoDocumentoModel.aluno_id == aluno_id,
            )
            .first()
        )
        if not solicitacao:
            return

        solicitacao.documento_id = documento_id
        solicitacao.status = "enviado"
        solicitacao.completed_at = datetime.now()
        db.commit()
    finally:
        db.close()
