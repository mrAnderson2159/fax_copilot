from fastapi import APIRouter, Depends, HTTPException  # Importa i moduli necessari da FastAPI
from app import models, schemas  # Importa i modelli e gli schemi per il database e la serializzazione
from sqlalchemy.orm import Session  # Importa la sessione per interagire con il database
from app.database import get_db  # Importa la funzione per ottenere una connessione al database
from app.routers.functions import get_one, get_all, try_except  # Importa le funzioni di utilità per ottenere oggetti dal database

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
    # zones = db.query(models.Zone).order_by(models.Zone.id).all()
    zones = get_all(db, models.Zone)

    for zone in zones:
        if all([fiend.was_captured == 10 for fiend in zone.fiends]):
            zone.status = "completed"
        elif all([fiend.was_captured for fiend in zone.fiends]):
            zone.status = "area_conquest_created"
        elif any([fiend.was_captured for fiend in zone.fiends]):
            zone.status = "just_started"
        else:
            zone.status = "fresh"

    return zones  # Restituisce tutte le zone presenti nel database



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
    # zone = db.query(models.Zone).filter(models.Zone.id == zone_id).first()
    return get_one(db, models.Zone, zone_id)    # Restituisce la zona trovata o lancia un errore HTTP 404 se non esiste


# Definisce un endpoint GET per ottenere i mostri in una zona specificata tramite il suo ID
@router.get("/{zone_id}/fiends", response_model=list[schemas.Fiend])
def get_zone_fiends(zone_id: int, db: Session = Depends(get_db)):
    # zone = db.query(models.Zone).filter(models.Zone.id == zone_id).first()
    # if not zone:
    #     # Se la zona non esiste, lancia un errore HTTP 404
    #     raise HTTPException(status_code=404, detail="Zona non trovata")

    zone = get_one(db, models.Zone, zone_id)
    fiends = db.query(models.Fiend).filter(models.Fiend.zone_id == zone_id).order_by(models.Fiend.id).all()
    return fiends


@try_except
@router.get("/{zone_id}/fiends_with_found", response_model=schemas.FiendWithFound)
def get_zone_fiends_with_found(zone_id: int, db: Session = Depends(get_db)):
    """
    Ottieni tutti i mostri di una zona, suddivisi in:
    - `native`: mostri nativi della zona.
    - `others`: mostri trovabili in quella zona, ma nativi di altre zone.
    """
    # Recupera i mostri nativi della zona
    native_fiends = db.query(models.Fiend).filter(models.Fiend.zone_id == zone_id).order_by(models.Fiend.id).all()

    # Recupera i mostri trovabili tramite la relazione `CanBeFound`
    other_fiends = (
        db.query(models.Fiend)
        .join(models.CanBeFound, models.CanBeFound.fiend_id == models.Fiend.id)
        .filter(models.CanBeFound.zone_id == zone_id)
        .order_by(models.Fiend.id)
        .all()
    )

    return {"native": native_fiends, "others": other_fiends}
