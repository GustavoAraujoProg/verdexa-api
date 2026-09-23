from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# PLANTAS
class PlantaBase(BaseModel):
    nome_popular: str = Field(min_length=1, max_length=150)
    nome_cientifico: str | None = Field(default=None, max_length=150)
    descricao: str | None = None


class PlantaCreate(PlantaBase):
    pass


class PlantaResponse(PlantaBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# DOENCAS
class DoencaBase(BaseModel):
    planta_id: int = Field(gt=0)
    nome_doenca: str = Field(min_length=1, max_length=150)
    sintomas: str | None = None
    causas: str | None = None
    prevencao: str | None = None
    tratamento_recomendado: str | None = None


class DoencaCreate(DoencaBase):
    pass


class DoencaResponse(DoencaBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )

class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    email: EmailStr = Field(max_length=150)
    senha: str = Field(min_length=8, max_length=128)


class UsuarioUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = Field(default=None, max_length=150)


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    email: str
    data_criacao: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class ResultadoResponse(BaseModel):
    id: int
    doenca: DoencaResponse
    confianca_modelo: float


class AnaliseResponse(BaseModel):
    id: int
    planta_id: int | None
    url_imagem: str
    status: str
    conclusao: str | None
    versao_modelo: str | None
    erro: str | None
    data_analise: datetime
    resultados: list[ResultadoResponse]


class CuidadoCreate(BaseModel):
    observacao: str = Field(min_length=1, max_length=5000)
    status_planta: Literal['em_tratamento', 'melhorando', 'estavel', 'piorando', 'recuperada']


class CuidadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    analise_id: int
    observacao: str | None
    status_planta: str | None
    data_registro: datetime
