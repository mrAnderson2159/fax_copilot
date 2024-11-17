from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.functions import get_one, get_all, repr, defeated, undefeated, full_details

router = APIRouter(
    prefix="/species_conquests",
    tags=["Species Conquests"]
)


@router.get("/", response_model=list[schemas.SpeciesConquest])
def get_all_species_conquests(db: Session = Depends(get_db)):
    return get_all(db, models.SpeciesConquest)


@router.get("/repr")
def get_species_conquest_repr(db: Session = Depends(get_db)):
    return repr(db, models.SpeciesConquest, 'unioculum', 'Campioni di Specie', 'species_conquests')


@router.get("/{species_conquest_id}", response_model=schemas.SpeciesConquest)
def get_species_conquest(species_conquest_id: int, db: Session = Depends(get_db)):
    return get_one(db, models.SpeciesConquest, species_conquest_id)


@router.post("/{species_conquest_id}/defeated", response_model=schemas.SpeciesConquest)
def defeated_species_conquest(species_conquest_id: int, db: Session = Depends(get_db)):
    return defeated(db, models.SpeciesConquest, species_conquest_id)


@router.post("/{species_conquest_id}/undefeated", response_model=schemas.SpeciesConquest)
def undefeated_species_conquest(species_conquest_id: int, db: Session = Depends(get_db)):
    return undefeated(db, models.SpeciesConquest, species_conquest_id)


@router.get("/{species_conquest_id}/full_details")
def get_species_conquest_full_details(species_conquest_id: int, db: Session = Depends(get_db)):
    """
    Recupera i dettagli completi di un campione di specie.
    """
    species_conquest: models.SpeciesConquest = get_one(db, models.SpeciesConquest, species_conquest_id)

    required_fiends = [(fiend.id, fiend.name) for fiend in species_conquest.fiends]
    required_fiends = sorted(required_fiends, key=lambda x: x[0])

    return full_details(
        species_conquest,
        required_fiends_amount=species_conquest.required_fiends,
        required_fiends=required_fiends,
    )
