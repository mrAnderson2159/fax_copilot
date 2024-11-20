from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.functions import get_one, get_all, repr, defeated, undefeated, full_details

router = APIRouter(
    prefix="/area_conquests",
    tags=["Area Conquests"]
)


@router.get("/", response_model=list[schemas.AreaConquest])
def get_all_area_conquests(db: Session = Depends(get_db)):
    """
    Restituisce tutti i campioni di zona.

    :param db: Sessione del database.
    :return: Lista di campioni di zona.
    """
    return get_all(db, models.AreaConquest)


@router.get("/repr", response_model=schemas.ConquestRepr)
def get_area_conquest_repr(db: Session = Depends(get_db)):
    return repr(db, models.AreaConquest, 'don tomberry', 'Campioni di Zona', 'area_conquests')


@router.get("/{area_conquest_id}", response_model=schemas.AreaConquest)
def get_area_conquest(area_conquest_id: int, db: Session = Depends(get_db)):
    """
    Recupera un singolo campione di zona.

    :param area_conquest_id: ID del campione di zona.
    :param db: Sessione del database.
    :raises HTTPException: Se il campione di zona non viene trovato.
    :return: Oggetto AreaConquest.
    """
    return get_one(db, models.AreaConquest, area_conquest_id)


@router.post("/{area_conquest_id}/defeated")
def defeated_area_conquest(area_conquest_id: int, db: Session = Depends(get_db)):
    """
    Segna un campione di zona come sconfitto.

    :param area_conquest_id: ID del campione di zona.
    :param db: Sessione del database.
    :raises HTTPException: Se il campione di zona non viene trovato.
    :return: Oggetto aggiornato del campione di zona.
    """
    return defeated(db, models.AreaConquest, area_conquest_id)


@router.post("/{area_conquest_id}/undefeated")
def undefeated_area_conquest(area_conquest_id: int, db: Session = Depends(get_db)):
    """
    Segna un campione di zona come non sconfitto.

    :param area_conquest_id: ID del campione di zona.
    :param db: Sessione del database.
    :raises HTTPException: Se il campione di zona non viene trovato.
    :return: Oggetto aggiornato del campione di zona.
    """
    return undefeated(db, models.AreaConquest, area_conquest_id)


@router.get("/{area_conquest_id}/full_details")
def get_area_conquest_full_details(area_conquest_id: int, db: Session = Depends(get_db)):
    area_conquest: models.AreaConquest = get_one(db, models.AreaConquest, area_conquest_id)
    required_fiends = [(fiend.id, fiend.name) for fiend in area_conquest.zone.fiends]
    required_fiends = sorted(required_fiends, key=lambda x: x[0])

    return full_details(
        area_conquest,
        zone_id=area_conquest.zone.id,
        zone_name=area_conquest.zone.name,
        required_fiends=required_fiends
    )
