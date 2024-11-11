from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/area_conquests",
    tags=["Area Conquests"]
)


def _get_area_conquest(area_conquest_id: int, db: Session) -> models.AreaConquest:
    """
    Recupera un campione di zona dal database.

    :param area_conquest_id: ID del campione di zona.
    :param db: Sessione del database.
    :raises HTTPException: Se il campione di zona non viene trovato.
    :return: Oggetto AreaConquest.
    """
    area_conquest = db.query(models.AreaConquest).filter(models.AreaConquest.id == area_conquest_id).first()
    if not area_conquest:
        raise HTTPException(status_code=404, detail="Campione di zona non trovato")
    return area_conquest


@router.get("/", response_model=list[schemas.AreaConquest])
def get_all_area_conquests(db: Session = Depends(get_db)):
    """
    Restituisce tutti i campioni di zona.

    :param db: Sessione del database.
    :return: Lista di campioni di zona.
    """
    return db.query(models.AreaConquest).order_by(models.AreaConquest.id).all()


@router.get("/created", response_model=list[schemas.AreaConquest])
def get_created_area_conquests(db: Session = Depends(get_db)):
    """
    Restituisce tutti i campioni di zona.

    :param db: Sessione del database.
    :return: Lista di campioni di zona.
    """
    return db.query(models.AreaConquest).filter(models.AreaConquest.created).order_by(models.AreaConquest.id).all()


@router.get("/repr", response_model=schemas.ConquestRepr)
def get_area_conquest_repr(db: Session = Depends(get_db)):
    name = 'don tomberry'
    conquest = db.query(models.AreaConquest).filter(models.AreaConquest.name == name).first()

    if not conquest:
        raise HTTPException(status_code=404, detail=f"{name} non trovato")

    return schemas.ConquestRepr(
        id=conquest.id,
        name="Campioni di Zona",
        image_url=conquest.image_url,
        destination='area_conquests'
    )

@router.get("/{area_conquest_id}", response_model=schemas.AreaConquest)
def get_area_conquest(area_conquest_id: int, db: Session = Depends(get_db)):
    """
    Recupera un singolo campione di zona.

    :param area_conquest_id: ID del campione di zona.
    :param db: Sessione del database.
    :raises HTTPException: Se il campione di zona non viene trovato.
    :return: Oggetto AreaConquest.
    """
    return _get_area_conquest(area_conquest_id, db)


@router.post("/{area_conquest_id}/defeated", response_model=schemas.AreaConquest)
def defeated_area_conquest(area_conquest_id: int, db: Session = Depends(get_db)):
    """
    Segna un campione di zona come sconfitto.

    :param area_conquest_id: ID del campione di zona.
    :param db: Sessione del database.
    :raises HTTPException: Se il campione di zona non viene trovato.
    :return: Oggetto aggiornato del campione di zona.
    """
    area_conquest = _get_area_conquest(area_conquest_id, db)
    area_conquest.defeated = True

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    return area_conquest


@router.post("/{area_conquest_id}/undefeated", response_model=schemas.AreaConquest)
def undefeated_area_conquest(area_conquest_id: int, db: Session = Depends(get_db)):
    """
    Segna un campione di zona come non sconfitto.

    :param area_conquest_id: ID del campione di zona.
    :param db: Sessione del database.
    :raises HTTPException: Se il campione di zona non viene trovato.
    :return: Oggetto aggiornato del campione di zona.
    """
    area_conquest = _get_area_conquest(area_conquest_id, db)
    area_conquest.defeated = False

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    return area_conquest
