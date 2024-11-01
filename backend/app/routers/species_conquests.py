from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/species_conquests",
    tags=["Species Conquests"]
)


def _get_species_conquest(species_conquest_id: int, db: Session) -> models.SpeciesConquest:
    species_conquest = db.query(models.SpeciesConquest).filter(models.SpeciesConquest.id == species_conquest_id).first()
    if not species_conquest:
        raise HTTPException(status_code=404, detail="Campione di specie non trovato")
    return species_conquest


@router.get("/", response_model=list[schemas.SpeciesConquest])
def get_all_species_conquests(db: Session = Depends(get_db)):
    return db.query(models.SpeciesConquest).all()

@router.get("/created", response_model=list[schemas.SpeciesConquest])
def get_created_species_conquests(db: Session = Depends(get_db)):
    """
    Restituisce tutti i campioni di specie creati.

    :param db: Sessione del database.
    :return: Lista di campioni di zona.
    """
    return db.query(models.SpeciesConquest).filter(models.SpeciesConquest.created).order_by(models.SpeciesConquest.id).all()



@router.get("/{species_conquest_id}", response_model=schemas.SpeciesConquest)
def get_species_conquest(species_conquest_id: int, db: Session = Depends(get_db)):
    return _get_species_conquest(species_conquest_id, db)


@router.post("/{species_conquest_id}/defeated", response_model=schemas.SpeciesConquest)
def defeated_species_conquest(species_conquest_id: int, db: Session = Depends(get_db)):
    """
    Segna un campione di specie come sconfitto.
    """
    species_conquest = _get_species_conquest(species_conquest_id, db)
    species_conquest.defeated = True

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    return species_conquest


@router.post("/{species_conquest_id}/undefeated", response_model=schemas.SpeciesConquest)
def undefeated_species_conquest(species_conquest_id: int, db: Session = Depends(get_db)):
    """
    Segna un campione di specie come non sconfitto.
    """
    species_conquest = _get_species_conquest(species_conquest_id, db)
    species_conquest.defeated = False

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    return species_conquest
