"""Models da aplicacao."""

from .aluno_model import AlunoModel
from .aluno_disciplina_model import AlunoDisciplinaModel
from .comunicado_model import ComunicadoModel
from .disciplina_model import DisciplinaModel
from .documento_model import DocumentoModel
from .nota_model import NotaModel
from .professor_model import ProfessorModel
from .professor_disciplina_model import ProfessorDisciplinaModel
from .solicitacao_documento_model import SolicitacaoDocumentoModel
from .usuario_model import UsuarioModel

__all__ = [
    "UsuarioModel",
    "ProfessorModel",
    "ProfessorDisciplinaModel",
    "SolicitacaoDocumentoModel",
    "AlunoModel",
    "AlunoDisciplinaModel",
    "ComunicadoModel",
    "DisciplinaModel",
    "DocumentoModel",
    "NotaModel",
]
