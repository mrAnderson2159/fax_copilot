from pydantic import BaseModel
from typing import Optional


class ZoneBase(BaseModel):
    """Rappresenta la struttura base per una zona, con nome e URL opzionale dell'immagine."""
    name: str
    image_url: Optional[str] = None


class Zone(ZoneBase):
    """Rappresenta una zona nel database, con un ID per identificazione."""
    id: int

    class Config:
        orm_mode = True


class FiendBase(BaseModel):
    """Rappresenta la struttura base per un mostro, con nome, stato di cattura e URL opzionale dell'immagine."""
    name: str
    was_captured: Optional[int] = 0
    image_url: Optional[str] = None


class Fiend(FiendBase):
    """Rappresenta un mostro nel database, con un ID e il campo zone_id per la zona di appartenenza."""
    id: int
    zone_id: int

    class Config:
        orm_mode = True


class FiendCaptureUpdate(BaseModel):
    """Rappresenta l'aggiornamento del numero di catture di un mostro, con ID e variazione."""
    fiend_id: int
    delta: int


class FiendCapturesUpdateRequest(BaseModel):
    """Richiesta per aggiornare le catture dei mostri."""
    updates: list[FiendCaptureUpdate]


class FiendWithFound(BaseModel):
    native: list[Fiend]
    others: list[Fiend]


class ConquestResponseBase(BaseModel):
    """Base per la risposta delle conquiste, contenente il nome e lo stato di creazione."""
    name: str
    created: bool
    image_url: str


class AreaConquestBase(BaseModel):
    """Rappresenta la struttura base per una conquista di zona, con nome, immagine e stato di creazione."""
    name: str
    image_url: Optional[str] = None
    created: Optional[bool] = False


class AreaConquestResponse(ConquestResponseBase):
    """Risposta per una conquista di zona."""

    class Config:
        orm_mode = True


class AreaConquest(AreaConquestBase):
    """Rappresenta una conquista di zona nel database, con un ID per identificazione."""
    id: int

    class Config:
        orm_mode = True


class SpeciesConquestBase(BaseModel):
    """Rappresenta la struttura base per una conquista di specie, con nome, immagine, requisiti e stato."""
    name: str
    image_url: Optional[str] = None
    required_fiends: int
    created: Optional[bool] = False


class SpeciesConquestResponse(ConquestResponseBase):
    """Risposta per una conquista di specie."""

    class Config:
        orm_mode = True


class SpeciesConquest(SpeciesConquestBase):
    """Rappresenta una conquista di specie nel database, con un ID per identificazione."""
    id: int

    class Config:
        orm_mode = True


class OriginalCreationBase(BaseModel):
    """Rappresenta la struttura base per una creazione originale, con nome, immagine, regola e stato."""
    name: str
    image_url: Optional[str] = None
    created: Optional[bool] = False
    creation_rule: Optional[str] = None


class OriginalCreationResponse(ConquestResponseBase):
    """Risposta per una creazione originale."""

    class Config:
        orm_mode = True


class OriginalCreation(OriginalCreationBase):
    """Rappresenta una creazione originale nel database, con un ID per identificazione."""
    id: int

    class Config:
        orm_mode = True
