from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    return SessionLocal()


def init_db():
    Base.metadata.create_all(bind=engine)
    _ensure_schema_updates()


def _ensure_schema_updates():
    inspector = inspect(engine)
    if "alunos" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("alunos")}
    if "cpf" in columns:
        return

    # Atualiza bancos antigos sem exigir ferramenta de migracao para a busca por CPF do aluno.
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE alunos ADD COLUMN cpf VARCHAR(14) NULL"))
