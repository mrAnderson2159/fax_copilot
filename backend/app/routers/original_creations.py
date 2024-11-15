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
    return db.query(models.OriginalCreation).order_by(models.OriginalCreation.id).all()

@router.get("/created", response_model=list[schemas.OriginalCreation])
def get_created_original_creations(db: Session = Depends(get_db)):
    """
    Restituisce tutti i campioni di specie creati.

    :param db: Sessione del database.
    :return: Lista di campioni di zona.
    """
    return db.query(models.OriginalCreation).filter(models.OriginalCreation.created).order_by(models.OriginalCreation.id).all()


@router.get("/repr", response_model=schemas.ConquestRepr)
def get_original_creation_repr(db: Session = Depends(get_db)):
    name = 'gasteropodos'
    conquest = db.query(models.OriginalCreation).filter(models.OriginalCreation.name == name).first()

    if not conquest:
        raise HTTPException(status_code=404, detail=f"{name} non trovato")

    return schemas.ConquestRepr(
        id=conquest.id,
        name="Prototipi Zoolab",
        image_url=conquest.image_url,
        destination='original_creations'
    )



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


@router.get("/{original_creation_id}/full_details")
def get_original_creation_full_details(original_creation_id: int, db: Session = Depends(get_db)):
    """
    Restituisce i dettagli completi di una creazione originale.

    :param original_creation_id: ID della creazione originale.
    :param db: Sessione del database.
    :raises HTTPException: Se la creazione originale non viene trovata.
    :return: Oggetto FullDetailsResponse.
    """
    original_creation = _get_original_creation(original_creation_id, db)

    rewards_dict = {reward.reward_type: reward for reward in original_creation.rewards}
    creation_reward = rewards_dict.get('creation')
    battle_reward = rewards_dict.get('battle')
    common_steal = rewards_dict.get('common_steal')
    rare_steal = rewards_dict.get('rare_steal')
    original_creation_stats = next(stats for stats in original_creation.stats)

    return schemas.FullDetailsResponse(
        id=original_creation.id,
        name=original_creation.name,
        image_url=original_creation.image_url,
        created=original_creation.created,
        defeated=original_creation.defeated,
        creation_reward=(creation_reward.item.name, creation_reward.quantity),
        battle_reward=(battle_reward.item.name, battle_reward.quantity),
        common_steal=(common_steal.item.name, common_steal.quantity) if common_steal else None,
        rare_steal=(rare_steal.item.name, rare_steal.quantity),
        hp=original_creation_stats.stats.hp,
        mp=original_creation_stats.stats.mp,
        overkill=original_creation_stats.stats.overkill,
        ap=original_creation_stats.stats.ap,
        ap_overkill=original_creation_stats.stats.ap_overkill,
        guil=original_creation_stats.stats.guil,
        creation_rule=original_creation.creation_rule,


    )