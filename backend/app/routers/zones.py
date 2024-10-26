from fastapi import APIRouter, Depends, HTTPException  # Importa i moduli necessari da FastAPI
from app import models, schemas  # Importa i modelli e gli schemi per il database e la serializzazione
from sqlalchemy.orm import Session  # Importa la sessione per interagire con il database
from app.database import get_db  # Importa la funzione per ottenere una connessione al database

# Crea un router per le API di FastAPI, con prefisso /zones e tag "Zones"
router = APIRouter(
    prefix="/zones",
    tags=["Zones"]
)


# Definisce un endpoint GET per ottenere tutte le zone
@router.get("/", response_model=list[schemas.Zone])
def get_zones(db: Session = Depends(get_db)):
    """
    Recupera tutte le zone dal database.

    :param db: Sessione del database ottenuta tramite dependency injection.
    :return: Lista di tutte le zone.
    """
    return db.query(models.Zone).all()


# Definisce un endpoint GET per ottenere una singola zona specificata tramite il suo ID
@router.get("/{zone_id}", response_model=schemas.Zone)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    """
    Recupera una zona specifica dal database in base al suo ID.

    :param zone_id: L'ID della zona da recuperare.
    :param db: Sessione del database ottenuta tramite dependency injection.
    :raises HTTPException: Se la zona non viene trovata, lancia un'eccezione HTTP 404.
    :return: Dati della zona trovata.
    """
    # Cerca la zona nel database con l'ID specificato
    zone = db.query(models.Zone).filter(models.Zone.id == zone_id).first()
    if not zone:
        # Se la zona non esiste, lancia un errore HTTP 404
        raise HTTPException(status_code=404, detail="Zona non trovata")
    return zone  # Restituisce la zona trovata


# Definisce un endpoint GET per ottenere i mostri in una zona specificata tramite il suo ID
@router.get("/{zone_id}/fiends", response_model=list[schemas.Fiend])
def get_zone_fiends(zone_id: int, db:Session = Depends(get_db)):
    zone = db.query(models.Zone).filter(models.Zone.id == zone_id).first()
    if not zone:
        # Se la zona non esiste, lancia un errore HTTP 404
        raise HTTPException(status_code=404, detail="Zona non trovata")

    fiends = db.query(models.Fiend).filter(models.Fiend.zone_id == zone_id).all()
    return fiends
