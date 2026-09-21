from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/plantas",
    tags=["Plantas"]
)

# LISTAR TODAS AS PLANTAS
@router.get("/", response_model=list[schemas.PlantaResponse])
def listar_plantas(db: Session = Depends(get_db)):

    plantas = db.query(models.Planta).all()

    return plantas

# BUSCAR PLANTA PELO ID
@router.get("/{planta_id}", response_model=schemas.PlantaResponse)
def buscar_planta(
    planta_id: int,
    db: Session = Depends(get_db)
):

    planta = (
        db.query(models.Planta)
        .filter(models.Planta.id == planta_id)
        .first()
    )

    if not planta:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada"
        )

    return planta


# CADASTRAR PLANTA
@router.post("/", response_model=schemas.PlantaResponse)
def cadastrar_planta(
    planta: schemas.PlantaCreate,
    db: Session = Depends(get_db)
):

    nova_planta = models.Planta(
        nome_popular=planta.nome_popular,
        nome_cientifico=planta.nome_cientifico,
        descricao=planta.descricao
    )

    db.add(nova_planta)

    db.commit()

    db.refresh(nova_planta)

    return nova_planta


# ALTERAR PLANTA
@router.put("/{planta_id}", response_model=schemas.PlantaResponse)
def atualizar_planta(
    planta_id: int,
    dados: schemas.PlantaCreate,
    db: Session = Depends(get_db)
):

    planta = (
        db.query(models.Planta)
        .filter(models.Planta.id == planta_id)
        .first()
    )

    if not planta:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada"
        )

    planta.nome_popular = dados.nome_popular
    planta.nome_cientifico = dados.nome_cientifico
    planta.descricao = dados.descricao

    db.commit()

    db.refresh(planta)

    return planta


# EXCLUIR PLANTA
@router.delete("/{planta_id}")
def excluir_planta(
    planta_id: int,
    db: Session = Depends(get_db)
):

    planta = (
        db.query(models.Planta)
        .filter(models.Planta.id == planta_id)
        .first()
    )

    if not planta:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada"
        )

    db.delete(planta)

    db.commit()

    return {
        "mensagem": "Planta excluída com sucesso"
    }


# MOSTRAR DOENCAS DE UMA PLANTA
@router.get("/{planta_id}/doencas")
def listar_doencas_planta(
    planta_id: int,
    db: Session = Depends(get_db)
):

    planta = (
        db.query(models.Planta)
        .filter(models.Planta.id == planta_id)
        .first()
    )

    if not planta:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada"
        )

    doencas = (
        db.query(models.Doenca)
        .filter(models.Doenca.planta_id == planta_id)
        .all()
    )

    return {
        "planta": planta.nome_popular,
        "nome_cientifico": planta.nome_cientifico,
        "doencas": doencas
    }