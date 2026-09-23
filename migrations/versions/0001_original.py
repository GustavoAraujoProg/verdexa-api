from alembic import op
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Numeric
)

from sqlalchemy.sql import func

from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=False,
        unique=True
    )

    senha_hash = Column(
        String(255),
        nullable=False
    )

    data_criacao = Column(
        DateTime,
        default=func.now()
    )


class Planta(Base):
    __tablename__ = "plantas"

    id = Column(Integer, primary_key=True, index=True)

    nome_popular = Column(
        String(150),
        nullable=False
    )

    nome_cientifico = Column(
        String(150)
    )

    descricao = Column(
        Text
    )


class Doenca(Base):
    __tablename__ = "doencas"

    id = Column(Integer, primary_key=True, index=True)

    planta_id = Column(
        Integer,
        ForeignKey("plantas.id"),
        nullable=False
    )

    nome_doenca = Column(
        String(150),
        nullable=False
    )

    sintomas = Column(
        Text
    )

    causas = Column(
        Text
    )

    prevencao = Column(
        Text
    )

    tratamento_recomendado = Column(
        Text
    )


class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    url_imagem = Column(
        String(255),
        nullable=False
    )

    data_analise = Column(
        DateTime,
        default=func.now()
    )


class ResultadoAnalise(Base):
    __tablename__ = "resultados_analise"

    id = Column(Integer, primary_key=True, index=True)

    analise_id = Column(
        Integer,
        ForeignKey("analises.id"),
        nullable=False
    )

    doenca_id = Column(
        Integer,
        ForeignKey("doencas.id"),
        nullable=False
    )

    precisao_ia = Column(
        Numeric(5, 2)
    )


class HistoricoCuidados(Base):
    __tablename__ = "historico_cuidados"

    id = Column(Integer, primary_key=True, index=True)

    analise_id = Column(
        Integer,
        ForeignKey("analises.id"),
        nullable=False
    )

    observacao = Column(
        Text
    )

    status_planta = Column(
        String(100)
    )

    data_registro = Column(
        DateTime,
        default=func.now()
    )

def upgrade():
    Base.metadata.create_all(op.get_bind())

def downgrade():
    raise RuntimeError("Downgrade destrutivo desabilitado; restaure um backup.")
