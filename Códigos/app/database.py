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
    table_names = set(inspector.get_table_names())

    if "alunos" in table_names:
        _add_missing_columns(
            inspector,
            "alunos",
            {
                "cpf": "VARCHAR(14) NULL",
                "curso_serie": "VARCHAR(80) NULL",
                "status_matricula": "VARCHAR(20) NULL",
            },
        )

    if "professores" in table_names:
        _add_missing_columns(
            inspector,
            "professores",
            {
                "disciplina_principal": "VARCHAR(80) NULL",
                "formacao_academica": "VARCHAR(120) NULL",
                "regime_trabalho": "VARCHAR(50) NULL",
                "data_admissao": "DATE NULL",
            },
        )

    if "documentos" in table_names:
        _make_nullable_if_needed(inspector, "documentos", "professor_id", "INTEGER NULL")


def _add_missing_columns(inspector, table_name, columns_to_add):
    columns = {column["name"] for column in inspector.get_columns(table_name)}
    missing_columns = [
        (column_name, column_definition)
        for column_name, column_definition in columns_to_add.items()
        if column_name not in columns
    ]
    if not missing_columns:
        return

    # Atualiza bancos antigos sem exigir ferramenta de migracao neste projeto.
    with engine.begin() as connection:
        for column_name, column_definition in missing_columns:
            connection.execute(
                text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
            )


def _make_nullable_if_needed(inspector, table_name, column_name, column_definition):
    columns = {column["name"]: column for column in inspector.get_columns(table_name)}
    column = columns.get(column_name)
    if not column or column.get("nullable"):
        return

    if engine.dialect.name != "mysql":
        return

    with engine.begin() as connection:
        connection.execute(
            text(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {column_definition}")
        )
