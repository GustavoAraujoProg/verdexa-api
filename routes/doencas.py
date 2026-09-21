from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/doencas",
    tags=["Doenças"]
)

# LISTAR TODAS
@router.get("/", response_model=list[schemas.DoencaResponse])
def listar_doencas(
    db: Session = Depends(get_db)
):

    return db.query(models.Doenca).all()


# BUSCAR PELO ID
@router.get("/{doenca_id}", response_model=schemas.DoencaResponse)
def buscar_doenca(
    doenca_id: int,
    db: Session = Depends(get_db)
):

    doenca = (
        db.query(models.Doenca)
        .filter(models.Doenca.id == doenca_id)
        .first()
    )

    if not doenca:
        raise HTTPException(
            status_code=404,
            detail="Doença não encontrada"
        )

    return doenca


# CADASTRAR
@router.post("/", response_model=schemas.DoencaResponse)
def cadastrar_doenca(
    doenca: schemas.DoencaCreate,
    db: Session = Depends(get_db)
):

    planta = (
        db.query(models.Planta)
        .filter(models.Planta.id == doenca.planta_id)
        .first()
    )

    if not planta:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada"
        )

    nova_doenca = models.Doenca(
        planta_id=doenca.planta_id,
        nome_doenca=doenca.nome_doenca,
        sintomas=doenca.sintomas,
        causas=doenca.causas,
        prevencao=doenca.prevencao,
        tratamento_recomendado=doenca.tratamento_recomendado
    )

    db.add(nova_doenca)

    db.commit()

    db.refresh(nova_doenca)

    return nova_doenca


# ALTERAR
@router.put("/{doenca_id}", response_model=schemas.DoencaResponse)
def atualizar_doenca(
    doenca_id: int,
    dados: schemas.DoencaCreate,
    db: Session = Depends(get_db)
):

    doenca = (
        db.query(models.Doenca)
        .filter(models.Doenca.id == doenca_id)
        .first()
    )

    if not doenca:
        raise HTTPException(
            status_code=404,
            detail="Doença não encontrada"
        )

    planta = (
        db.query(models.Planta)
        .filter(models.Planta.id == dados.planta_id)
        .first()
    )

    if not planta:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada"
        )

    doenca.planta_id = dados.planta_id
    doenca.nome_doenca = dados.nome_doenca
    doenca.sintomas = dados.sintomas
    doenca.causas = dados.causas
    doenca.prevencao = dados.prevencao
    doenca.tratamento_recomendado = dados.tratamento_recomendado

    db.commit()

    db.refresh(doenca)

    return doenca


# EXCLUIR
@router.delete("/{doenca_id}")
def excluir_doenca(
    doenca_id: int,
    db: Session = Depends(get_db)
):

    doenca = (
        db.query(models.Doenca)
        .filter(models.Doenca.id == doenca_id)
        .first()
    )

    if not doenca:
        raise HTTPException(
            status_code=404,
            detail="Doença não encontrada"
        )

    db.delete(doenca)

    db.commit()

    return {
        "mensagem": "Doença excluída com sucesso"
    }