from pydantic import BaseModel, ConfigDict

# PLANTAS
class PlantaBase(BaseModel):
    nome_popular: str
    nome_cientifico: str | None = None
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
    planta_id: int
    nome_doenca: str
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