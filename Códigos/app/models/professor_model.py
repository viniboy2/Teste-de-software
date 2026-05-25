from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProfessorModel(Base):
    __tablename__ = "professores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    disciplina_principal: Mapped[str | None] = mapped_column(String(80), nullable=True)
    formacao_academica: Mapped[str | None] = mapped_column(String(120), nullable=True)
    regime_trabalho: Mapped[str | None] = mapped_column(String(50), nullable=True)
    data_admissao: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

    usuario = relationship("UsuarioModel", back_populates="professor")
    documentos = relationship("DocumentoModel", back_populates="professor")
    notas = relationship("NotaModel", back_populates="professor")
