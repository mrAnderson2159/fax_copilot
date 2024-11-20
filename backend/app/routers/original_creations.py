from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.functions import get_one, get_all, repr, defeated, undefeated, full_details

router = APIRouter(
    prefix="/original_creations",
    tags=["Original Creations"]
)


@router.get("/", response_model=list[schemas.OriginalCreation])
def get_all_original_creations(db: Session = Depends(get_db)):
    """
    Restituisce tutte le creazioni originali.

    :param db: Sessione del database.
    :return: Lista di creazioni originali.
    """
    return get_all(db, models.OriginalCreation)


@router.get("/repr", response_model=schemas.ConquestRepr)
def get_original_creation_repr(db: Session = Depends(get_db)):
    """
    Restituisce un oggetto rappresentativo di una creazione originale.

    :param db: Sessione del database.
    :return: Oggetto ConquestRepr.
    """
    return repr(db, models.OriginalCreation, 'gasteropodos', 'Prototipi Zoolab', 'original_creations')


@router.get("/{original_creation_id}", response_model=schemas.OriginalCreation)
def get_original_creation(original_creation_id: int, db: Session = Depends(get_db)):
    return get_one(db, models.OriginalCreation, original_creation_id)


@router.post("/{original_creation_id}/defeated")
def defeated_original_creation(original_creation_id: int, db: Session = Depends(get_db)):
    return defeated(db, models.OriginalCreation, original_creation_id)


@router.post("/{original_creation_id}/undefeated")
def undefeated_original_creation(original_creation_id: int, db: Session = Depends(get_db)):
    return undefeated(db, models.OriginalCreation, original_creation_id)


@router.get("/{original_creation_id}/full_details")
def get_original_creation_full_details(original_creation_id: int, db: Session = Depends(get_db)):
    """
    Restituisce i dettagli completi di una creazione originale.

    :param original_creation_id: ID della creazione originale.
    :param db: Sessione del database.
    :raises HTTPException: Se la creazione originale non viene trovata.
    :return: Oggetto FullDetailsResponse.
    """
    original_creation: models.OriginalCreation = get_one(db, models.OriginalCreation, original_creation_id)

    return full_details(
        original_creation,
        creation_rule=original_creation.creation_rule,
    )
