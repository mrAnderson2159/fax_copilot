from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/original_creations",
    tags=["Original Creations"]
)


def _get_original_creation(original_creation_id: int, db: Session) -> models.OriginalCreation:
    """
    Recupera una singola creazione originale.

    :param original_creation_id: ID della creazione originale.
    :param db: Sessione del database.
    :raises HTTPException: Se la creazione originale non viene trovata.
    :return: Oggetto OriginalCreation.
    """
    original_creation = db.query(models.OriginalCreation).filter(
        models.OriginalCreation.id == original_creation_id
    ).first()
    if not original_creation:
        raise HTTPException(status_code=404, detail="Creazione originale non trovata")
    return original_creation


@router.get("/", response_model=list[schemas.OriginalCreation])
def get_all_original_creations(db: Session = Depends(get_db)):
    """
    Restituisce tutte le creazioni originali.

    :param db: Sessione del database.
    :return: Lista di creazioni originali.
    """
    return db.query(models.OriginalCreation).all()


@router.get("/{original_creation_id}", response_model=schemas.OriginalCreation)
def get_original_creation(original_creation_id: int, db: Session = Depends(get_db)):
    return _get_original_creation(original_creation_id, db)


@router.post("/{original_creation_id}/defeated", response_model=schemas.OriginalCreation)
def defeated_original_creation(original_creation_id: int, db: Session = Depends(get_db)):
    """
    Segna una creazione originale come sconfitta.

    :param original_creation_id: ID della creazione originale.
    :param db: Sessione del database.
    :raises HTTPException: Se la creazione originale non viene trovata.
    :return: L'oggetto aggiornato della creazione originale.
    """
    original_creation = _get_original_creation(original_creation_id, db)
    original_creation.defeated = True

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    return original_creation


@router.post("/{original_creation_id}/undefeated", response_model=schemas.OriginalCreation)
def undefeated_original_creation(original_creation_id: int, db: Session = Depends(get_db)):
    """
    Segna una creazione originale come non sconfitta.

    :param original_creation_id: ID della creazione originale.
    :param db: Sessione del database.
    :raises HTTPException: Se la creazione originale non viene trovata.
    :return: L'oggetto aggiornato della creazione originale.
    """
    original_creation = _get_original_creation(original_creation_id, db)
    original_creation.defeated = False

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    return original_creation
