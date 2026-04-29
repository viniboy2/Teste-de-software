"""Models da aplicacao."""

from .aluno_model import AlunoModel
from .disciplina_model import DisciplinaModel
from .documento_model import DocumentoModel
from .nota_model import NotaModel
from .professor_model import ProfessorModel
from .usuario_model import UsuarioModel

__all__ = [
    "UsuarioModel",
    "ProfessorModel",
    "AlunoModel",
    "DisciplinaModel",
    "DocumentoModel",
    "NotaModel",
]
