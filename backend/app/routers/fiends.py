# backend/app/routers/fiends.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.creation_conditions import CreationConditions
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/fiends",
    tags=["Fiends"]
)

logger = logging.getLogger(__name__)


# Rotta per ottenere l'elenco di tutti i mostri
@router.get("/", response_model=list[schemas.Fiend])
def get_all_fiends(db: Session = Depends(get_db)):
    """
    Recupera l'elenco completo di tutti i mostri.

    :param db: Sessione del database ottenuta tramite dependency injection.
    :return: Lista di tutti i mostri.
    """
    return db.query(models.Fiend).all()


# Rotta per ottenere un singolo mostro specificato tramite il suo ID
@router.get("/{fiend_id}", response_model=schemas.Fiend)
def get_fiend(fiend_id: int, db: Session = Depends(get_db)):
    """
    Recupera un mostro specifico dal database in base al suo ID.

    :param fiend_id: L'ID del mostro da recuperare.
    :param db: Sessione del database ottenuta tramite dependency injection.
    :raises HTTPException: Se il mostro non viene trovato, lancia un'eccezione HTTP 404.
    :return: Dati del mostro trovato.
    """
    fiend = db.query(models.Fiend).filter(models.Fiend.id == fiend_id).first()
    if not fiend:
        raise HTTPException(status_code=404, detail="Mostro non trovato")
    return fiend


# Rotta per aggiornare il numero di catture dei mostri
@router.post("/update_captures")
def update_fiend_captures(request: schemas.FiendCapturesUpdateRequest, db: Session = Depends(get_db)):
    """
    Aggiorna il numero di catture dei mostri indicati nella richiesta.

    :param request: Richiesta contenente una lista di mostri e le variazioni di cattura.
    :param db: Sessione del database ottenuta tramite dependency injection.
    :raises HTTPException: Se un mostro non viene trovato o i dati non sono validi, lancia un'eccezione HTTP.
    :return: Un messaggio di conferma o errore.
    """
    logger.info("Richiesta di aggiornamento ricevuta: updates=%s", request.updates)

    captured_fiends: list[models.Fiend] = db.query(models.Fiend).filter(models.Fiend.id.in_([
        update.fiend_id for update in request.updates
    ])).all()

    logger.info("Mostri catturati trovati nel database: %s", [fiend.name for fiend in captured_fiends])

    deltas = [update.delta for update in request.updates]
    logger.info("Variazioni di cattura (deltas): %s", deltas)

    for captured_fiend, delta in zip(captured_fiends, deltas):
        new_capture_count = captured_fiend.was_captured + delta
        logger.info(
            "Controllo cattura per %s: catture attuali=%d, delta=%d, nuovo conteggio=%d",
            captured_fiend.name, captured_fiend.was_captured, delta, new_capture_count
        )

        if new_capture_count < 0:
            raise HTTPException(status_code=403,
                                detail=f"{captured_fiend.name} non può avere un numero di catture minore di 0 ({new_capture_count})")
        elif new_capture_count > 10:
            raise HTTPException(status_code=403,
                                detail=f"{captured_fiend.name} non può essere catturato più di 10 volte ({new_capture_count})")

    feedback = []

    # Se tutti i controlli passano, esegui gli aggiornamenti effettivi
    for captured_fiend, delta in zip(captured_fiends, deltas):
        captured_fiend.was_captured += delta
        db.add(captured_fiend)  # Aggiungi l'oggetto alla sessione per il commit successivo
        feedback.append((captured_fiend.name, delta))
        logger.info("Aggiornamento effettivo per %s: nuovo numero di catture=%d", captured_fiend.name, captured_fiend.was_captured)

    db.flush()
    logging.info("Flash del database per controllare nuove creazioni")

    # Ora verificare le condizioni per campioni e prototipi
    conquests = CreationConditions(
        db=db,
        captured_fiends=captured_fiends,
        negative_check=any(delta < 0 for delta in deltas)
    ).check()

    logger.info("Conquiste verificate: %s", conquests)

    # Prova a fare il commit delle modifiche tutte insieme
    try:
        db.commit()
        logger.info("Commit del database eseguito con successo")
    except Exception as e:
        db.rollback()
        logger.error("Errore durante il commit del database: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    response = {
        "message": "Aggiornamento delle catture completato con successo",
        "captures": feedback,
        **conquests
    }
    logger.info("Risposta restituita: %s", response)

    return response

# Rotta per resettare il numero di catture di tutti i mostri
@router.post("/reset")
def reset_fiends(db: Session = Depends(get_db)):
    for fiend in db.query(models.Fiend).all():
        fiend.was_captured = 0

    for model_conquest in [models.AreaConquest, models.SpeciesConquest, models.OriginalCreation]:
        conquests = db.query(model_conquest).all()

        for conquest in conquests:
            conquest.created = False
            conquest.defeated = False

    # Prova a fare il commit delle modifiche
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    return {"message": "Il database è stato inizializzato con successo"}
