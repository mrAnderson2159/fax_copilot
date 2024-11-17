from pydantic import BaseModel
from typing import Optional


class BaseElement(BaseModel):
    """Represents the base structure for an element, with an ID, a name and an optional image URL."""
    id: int
    name: str
    image_url: Optional[str] = None


class Zone(BaseElement):
    """Represents a zone in the database, with BaseElement fields and a status field reflecting
    the completion status of the zone."""
    status: Optional[str] = None

    class Config:
        from_attributes = True


class Fiend(BaseElement):
    """Represents a fiend in the database, with BaseElement fields, a zone ID field and a was_captured field."""
    was_captured: Optional[int] = 0
    zone_id: int

    class Config:
        from_attributes = True


class FiendCaptureUpdate(BaseModel):
    """Represents an update to the number of captures of a fiend, with a fiend ID and a delta value."""
    fiend_id: int
    delta: int


class FiendCapturesUpdateRequest(BaseModel):
    """Request to update the captures of fiends."""
    updates: list[FiendCaptureUpdate]


class FiendWithFound(BaseModel):
    """Represents a group of fiends, with a list of native fiends and a list of other fiends that can be found
    in the same zone of the native fiends."""
    native: list[Fiend]
    others: list[Fiend]


class ConquestResponseBase(BaseElement):
    """Base for conquest responses, containing BaseElement fields, a created field, an optional defeated field and
    an optional reward field."""
    created: bool
    defeated: Optional[bool] = False
    reward: Optional[tuple[str, int]] = None


class AreaConquest(ConquestResponseBase):
    """Represents an area conquest, with ConquestResponseBase fields."""
    class Config:
        from_attributes = True


class AreaConquestResponse(ConquestResponseBase):
    """Represents an area conquest response, with ConquestResponseBase fields and
    a destination field set to 'area_conquests'."""
    destination: str = 'area_conquests'

    class Config:
        from_attributes = True


class SpeciesConquest(ConquestResponseBase):
    """Represents a species conquest, with ConquestResponseBase fields and a required_fiends field."""
    required_fiends: int

    class Config:
        from_attributes = True


class SpeciesConquestResponse(ConquestResponseBase):
    """Represents a species conquest response, with ConquestResponseBase fields and a destination field
    set to 'species_conquests'."""
    destination: str = 'species_conquests'

    class Config:
        from_attributes = True


class OriginalCreation(ConquestResponseBase):
    """Represents an original creation, with ConquestResponseBase fields and a creation_rule field."""
    creation_rule: str

    class Config:
        from_attributes = True


class OriginalCreationResponse(ConquestResponseBase):
    """Represents an original creation response, with ConquestResponseBase fields and a destination field
    set to 'original_creations'."""
    destination: str = 'original_creations'

    class Config:
        from_attributes = True


class ConquestRepr(BaseElement):
    """Represents a conquest, with BaseElement fields and a destination field."""
    destination: str


class FullDetailsResponse(BaseElement):
    """Represents a full details response, with BaseElement fields and other optional fields."""
    created: Optional[bool] = False
    defeated: Optional[bool] = False
    creation_reward: Optional[tuple[str, int]] = None
    zone_id: Optional[int] = None
    zone_name: Optional[str] = None
    required_fiends: Optional[list[tuple[int, str]]] = None
    required_fiends_amount: Optional[int] = None
    creation_rule: Optional[str] = None
    hp: Optional[int] = None
    mp: Optional[int] = None
    overkill: Optional[int] = None
    ap: Optional[int] = None
    ap_overkill: Optional[int] = None
    guil: Optional[int] = None
    battle_reward: Optional[tuple[str, int]] = None
    weakness: Optional[list[tuple[str, int]]] = None
    resistance: Optional[list[str]] = None
    common_steal: Optional[tuple[str, int]] = None
    rare_steal: Optional[tuple[str, int]] = None