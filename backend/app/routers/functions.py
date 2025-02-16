# backend/app/routers/functions.py
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session  # Importa la sessione per interagire con il database
from app.database import Base
from app.schemas import ConquestRepr, FullDetailsResponse, NemesisResponse
from app.creation_conditions import CreationConditions


def try_except(func):
    """
    Decoratore per gestire le eccezioni nei metodi di questo modulo,
    distinguendo tra errori server-side e client-side.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            # Passa eccezioni HTTPException esistenti senza modificarle
            print(e)
            raise e
        except Exception as e:
            # Per altre eccezioni, restituisce un errore generico server-side
            print(e)
            raise HTTPException(status_code=500, detail=f"Errore interno: {str(e)}")
    return wrapper



@try_except
def get_one(db: Session, model: type[Base], obj_id: int) -> Base:
    """
    Recupera un oggetto di un modello dal database.

    :param db: Sessione del database.
    :param model: Modello da cui recuperare l'oggetto.
    :param obj_id: ID dell'oggetto da recuperare.
    :return: Oggetto del modello.
    """
    query = db.query(model).filter(model.id == obj_id).first()
    if not query:
        raise HTTPException(status_code=404, detail=f'"{model.__name__}" non trovato')
    return query


@try_except
def get_all(db: Session, model: type[Base]) -> list[Base]:
    """
    Recupera tutti gli oggetti di un modello dal database.

    :param db: Sessione del database.
    :param model: Modello da cui recuperare gli oggetti.
    :return: Lista di oggetti del modello.
    """
    query = db.query(model).order_by(model.id).all()
    if not query:
        raise HTTPException(status_code=404, detail=f'"{model.__name__}" non trovato')
    return query


@try_except
def repr(db: Session, model: type[Base], creation_name: str, category_name: str, destination: str) -> ConquestRepr:
    """
    Recupera un oggetto di un modello dal database.

    :param db: Sessione del database.
    :param model: Modello da cui recuperare l'oggetto.
    :param creation_name: Nome dell'oggetto da recuperare.
    :return: Oggetto del modello.
    """
    query = db.query(model).filter(model.name == creation_name).first()
    if not query:
        raise HTTPException(status_code=404, detail=f'"{creation_name}" non trovato')

    return ConquestRepr(
        id=query.id,
        name=category_name,
        image_url=query.image_url,
        destination=destination
    )


@try_except
def __defeat_func(db: Session, model: type[Base], obj_id: int, defeated: bool) -> Optional[NemesisResponse]:
    conquest = get_one(db, model, obj_id)
    conquest.defeated = defeated

    db.flush()
    db.refresh(conquest)

    il_supremo = CreationConditions(db).check_il_supremo()

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Errore durante l'aggiornamento: {str(e)}")

    if il_supremo:
        return NemesisResponse(
            id=il_supremo.id,
            name=il_supremo.name,
            image_url=il_supremo.image_url,
            created=il_supremo.created,
            reward=il_supremo.reward if il_supremo.reward else None,
            destination=il_supremo.destination,
            destination_name='Prototipi Zoolab',
            type='Prototipo'
        )


@try_except
def defeated(db: Session, model: type[Base], obj_id: int) -> Optional[NemesisResponse]:
    """
    Segna un oggetto come sconfitto.

    :param db: Sessione del database.
    :param model: Modello dell'oggetto da segnare come sconfitto.
    :param obj_id: ID dell'oggetto da segnare come sconfitto.
    :return: Oggetto aggiornato.
    """
    return __defeat_func(db, model, obj_id, True)


@try_except
def undefeated(db: Session, model: type[Base], obj_id: int) -> Optional[NemesisResponse]:
    """
    Segna un oggetto come non sconfitto.

    :param db: Sessione del database.
    :param model: Modello dell'oggetto da segnare come non sconfitto.
    :param obj_id: ID dell'oggetto da segnare come non sconfitto.
    :return: Oggetto aggiornato.
    """
    return __defeat_func(db, model, obj_id, False)


@try_except
def full_details(obj, **fields) -> FullDetailsResponse:
    """
    Recupera i dettagli completi di un oggetto.

    :param obj: Oggetto da cui recuperare i dettagli.
    """

    rewards_dict = {reward.reward_type: reward for reward in obj.rewards}
    creation_reward = rewards_dict.get('creation')
    battle_reward = rewards_dict.get('battle')
    common_steal = rewards_dict.get('common_steal')
    rare_steal = rewards_dict.get('rare_steal')
    obj_stats = next(stats for stats in obj.stats)

    return FullDetailsResponse(
        id=obj.id,
        name=obj.name,
        image_url=obj.image_url,
        created=obj.created,
        defeated=obj.defeated,
        creation_reward=(creation_reward.item.name, creation_reward.quantity),
        battle_reward=(battle_reward.item.name, battle_reward.quantity),
        common_steal=(common_steal.item.name, common_steal.quantity) if common_steal else None,
        rare_steal=(rare_steal.item.name, rare_steal.quantity),
        stats=obj_stats,
        hp=obj_stats.stats.hp,
        mp=obj_stats.stats.mp,
        ap=obj_stats.stats.ap,
        overkill=obj_stats.stats.overkill,
        ap_overkill=obj_stats.stats.ap_overkill,
        guild=obj_stats.stats.guil,
        **fields
    )
