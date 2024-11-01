from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """
    Rappresenta un utente nel sistema.

    Attributi:
        id (int): L'ID univoco dell'utente.
        username (str): Nome utente univoco.
        hashed_password (str): La password dell'utente memorizzata in forma hashata.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Zone(Base):
    """
    Rappresenta una zona nel gioco, in cui può essere trovato una specifica quantità di mostri

    Attributi:
        id (int): L'ID univoco della zona.
        name (str): Nome univoco della zona.
        image_url (str): URL dell'immagine associata alla zona.
        fiends (list[Fiend]): Lista dei mostri nativi della zona.
        found_fiends (list[CanBeFound]): Lista di associazioni con mostri che possono essere trovati anche in questa zona.
    """
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)

    # Relazioni
    fiends = relationship("Fiend", back_populates="zone")
    found_fiends = relationship("CanBeFound", back_populates="zone")


class SpeciesConquest(Base):
    """
    Rappresenta un campione di specie, sbloccato catturando un numero specifico di mostri della stessa specie.

    Attributi:
        id (int): L'ID univoco della conquista di specie.
        name (str): Nome univoco della conquista di specie.
        image_url (str): URL dell'immagine associata alla conquista.
        required_fiends (int): Numero di mostri necessari per sbloccare la conquista.
        created (bool): Flag che indica se la conquista è stata generata.
        defeated (bool): Flag che indica se la conquista è stata sconfitta.
        fiends (list[Fiend]): Lista dei mostri che appartengono a questa specie.
    """
    __tablename__ = "species_conquests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    required_fiends = Column(Integer, nullable=False)
    created = Column(Boolean, default=False, index=True)
    defeated = Column(Boolean, default=False, index=True)

    # Relazione con Fiend
    fiends = relationship("Fiend", back_populates="species_conquest")


class Fiend(Base):
    """
    Rappresenta un mostro nel gioco.

    Attributi:
        id (int): L'ID univoco del mostro.
        name (str): Nome univoco del mostro.
        was_captured (int): Numero di volte che il mostro è stato catturato.
        zone_id (int): ID della zona nativa del mostro.
        image_url (str): URL dell'immagine del mostro.
        species_conquest_id (int): ID della conquista di specie a cui il mostro appartiene.
        zone (Zone): La zona nativa del mostro.
        species_conquest (SpeciesConquest): La conquista di specie associata al mostro.
        found_zones (list[CanBeFound]): Lista delle associazioni con le zone in cui il mostro può essere trovato.
    """
    __tablename__ = "fiends"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    was_captured = Column(Integer, default=0)
    zone_id = Column(Integer, ForeignKey("zones.id", onupdate="CASCADE"), nullable=False)
    image_url = Column(String, unique=True)
    species_conquest_id = Column(Integer, ForeignKey("species_conquests.id", onupdate="CASCADE"), nullable=True)

    # Relazioni
    zone = relationship("Zone", back_populates="fiends")
    species_conquest = relationship("SpeciesConquest", back_populates="fiends")
    found_zones = relationship("CanBeFound", back_populates="fiend")


class SpecialFiend(Base):
    """
    Rappresenta un mostro non catturabile, generalmente un Boss.

    Attributi:
        id (int): L'ID univoco del mostro speciale.
        name (str): Nome univoco del mostro speciale.
        image_url (str): URL dell'immagine del mostro speciale.
    """
    __tablename__ = "special_fiends"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)


class AreaConquest(Base):
    """
    Rappresenta un campione di zona, generato catturando tutti i mostri di una zona specifica.

    Attributi:
        id (int): L'ID univoco della conquista di zona.
        name (str): Nome univoco della conquista di zona.
        image_url (str): URL dell'immagine associata alla conquista.
        zone_id (int): ID della zona associata alla conquista.
        created (bool): Flag che indica se la conquista è stata generata.
        defeated (bool): Flag che indica se la conquista è stata sconfitta.
        zone (Zone): La zona associata alla conquista.
    """
    __tablename__ = "area_conquests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    zone_id = Column(Integer, ForeignKey("zones.id", onupdate="CASCADE"))
    created = Column(Boolean, default=False, index=True)
    defeated = Column(Boolean, default=False, index=True)

    zone = relationship("Zone")


class OriginalCreation(Base):
    """
    Rappresenta un prototipo zoolab nel gioco, generato in base a regole specifiche.

    Attributi:
        id (int): L'ID univoco della creazione originale.
        name (str): Nome univoco della creazione originale.
        image_url (str): URL dell'immagine associata alla creazione.
        created (bool): Flag che indica se la creazione è stata generata.
        creation_rule (str): La regola per generare la creazione.
        defeated (bool): Flag che indica se la creazione è stata sconfitta.
    """
    __tablename__ = "original_creations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    created = Column(Boolean, default=False, index=True)
    creation_rule = Column(String)
    defeated = Column(Boolean, default=False, index=True)


class CanBeFound(Base):
    """
    Rappresenta la relazione N:M tra mostri e zone aggiuntive in cui possono essere trovati.

    Attributi:
        fiend_id (int): L'ID del mostro associato.
        zone_id (int): L'ID della zona associata.
        fiend (Fiend): Il mostro che può essere trovato nella zona.
        zone (Zone): La zona in cui il mostro può essere trovato.
    """
    __tablename__ = "can_be_found"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate='CASCADE'), primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey('zones.id', onupdate='CASCADE'), primary_key=True, index=True)

    # Collegamenti per la relazione Many-to-Many
    fiend = relationship("Fiend", back_populates="found_zones")
    zone = relationship("Zone", back_populates="found_fiends")
