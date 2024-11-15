from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    effect = Column(String, nullable=False)
    type = Column(String,
                  CheckConstraint("type IN ('common', 'offensive', 'support', 'special', 'curio', 'sphere_grid')"),
                  nullable=False)

    fiend_rewards = relationship("FiendReward", back_populates="item")
    area_conquest_rewards = relationship("AreaConquestReward", back_populates="item")
    species_conquest_rewards = relationship("SpeciesConquestReward", back_populates="item")
    original_creation_rewards = relationship("OriginalCreationReward", back_populates="item")


class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)

    fiends = relationship("Fiend", back_populates="zone")
    found_fiends = relationship("CanBeFound", back_populates="zone")
    area_conquests = relationship("AreaConquest", back_populates="zone")


class SpeciesConquest(Base):
    __tablename__ = "species_conquests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    required_fiends = Column(Integer, nullable=False)
    created = Column(Boolean, default=False, index=True)
    defeated = Column(Boolean, default=False, index=True)

    fiends = relationship("Fiend", back_populates="species_conquest")
    rewards = relationship("SpeciesConquestReward", back_populates="species_conquest")
    equipment_rewards = relationship("SpeciesConquestEquipmentReward", back_populates="species_conquest")
    weaknesses = relationship("SpeciesConquestWeakness", back_populates="species_conquest")
    resistances = relationship("SpeciesConquestResistance", back_populates="species_conquest")
    stats = relationship("SpeciesConquestStats", back_populates="species_conquest")


class Fiend(Base):
    __tablename__ = "fiends"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    was_captured = Column(Integer, default=0)
    zone_id = Column(Integer, ForeignKey("zones.id", onupdate="CASCADE"), nullable=False)
    image_url = Column(String, unique=True)
    species_conquest_id = Column(Integer, ForeignKey("species_conquests.id", onupdate="CASCADE"), nullable=True)

    zone = relationship("Zone", back_populates="fiends")
    species_conquest = relationship("SpeciesConquest", back_populates="fiends")
    found_zones = relationship("CanBeFound", back_populates="fiend")
    rewards = relationship("FiendReward", back_populates="fiend")
    equipment_rewards = relationship("FiendEquipmentReward", back_populates="fiend")
    weaknesses = relationship("FiendWeakness", back_populates="fiend")
    resistances = relationship("FiendResistance", back_populates="fiend")
    stats = relationship("FiendStats", back_populates="fiend")


class UniqueFiend(Base):
    __tablename__ = "unique_fiends"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)


class AreaConquest(Base):
    __tablename__ = "area_conquests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    zone_id = Column(Integer, ForeignKey("zones.id", onupdate="CASCADE"))
    created = Column(Boolean, default=False, index=True)
    defeated = Column(Boolean, default=False, index=True)

    zone = relationship("Zone", back_populates="area_conquests")
    rewards = relationship("AreaConquestReward", back_populates="area_conquest")
    equipment_rewards = relationship("AreaConquestEquipmentReward", back_populates="area_conquest")
    weaknesses = relationship("AreaConquestWeakness", back_populates="area_conquest")
    resistances = relationship("AreaConquestResistance", back_populates="area_conquest")
    stats = relationship("AreaConquestStats", back_populates="area_conquest")


class OriginalCreation(Base):
    __tablename__ = "original_creations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    created = Column(Boolean, default=False, index=True)
    creation_rule = Column(String)
    defeated = Column(Boolean, default=False, index=True)

    rewards = relationship("OriginalCreationReward", back_populates="original_creation")
    equipment_rewards = relationship("OriginalCreationEquipmentReward", back_populates="original_creation")
    weaknesses = relationship("OriginalCreationWeakness", back_populates="original_creation")
    resistances = relationship("OriginalCreationResistance", back_populates="original_creation")
    stats = relationship("OriginalCreationStats", back_populates="original_creation")


class CanBeFound(Base):
    __tablename__ = "can_be_found"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate='CASCADE'), primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey('zones.id', onupdate='CASCADE'), primary_key=True, index=True)

    fiend = relationship("Fiend", back_populates="found_zones")
    zone = relationship("Zone", back_populates="found_fiends")


class FiendReward(Base):
    __tablename__ = "fiend_rewards"
    reward_type = Column(String, CheckConstraint("reward_type IN ('battle', 'common_steal', 'rare_steal')",
                                                 name="valid_reward_type"), index=True, nullable=False,
                         primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", onupdate='CASCADE'), nullable=False, primary_key=True)
    fiend_id = Column(Integer, ForeignKey("fiends.id", onupdate='CASCADE'), nullable=False, primary_key=True)
    quantity = Column(Integer, nullable=False)

    item = relationship("Item", back_populates="fiend_rewards")
    fiend = relationship("Fiend", back_populates="rewards")


class AreaConquestReward(Base):
    __tablename__ = "area_conquest_rewards"
    reward_type = Column(String, CheckConstraint("reward_type IN ('creation', 'battle', 'common_steal', 'rare_steal')",
                                                 name="valid_reward_type"), index=True, nullable=False,
                         primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", onupdate='CASCADE'), nullable=False)
    area_conquest_id = Column(Integer, ForeignKey("area_conquests.id", onupdate='CASCADE'), nullable=False,
                              primary_key=True)
    quantity = Column(Integer, nullable=False)

    item = relationship("Item", back_populates="area_conquest_rewards")
    area_conquest = relationship("AreaConquest", back_populates="rewards")


class SpeciesConquestReward(Base):
    __tablename__ = "species_conquest_rewards"
    reward_type = Column(String, CheckConstraint("reward_type IN ('creation', 'battle', 'common_steal', 'rare_steal')",
                                                 name="valid_reward_type"), index=True, nullable=False,
                         primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", onupdate='CASCADE'), nullable=False)
    species_conquest_id = Column(Integer, ForeignKey("species_conquests.id", onupdate='CASCADE'), nullable=False,
                                 primary_key=True)
    quantity = Column(Integer, nullable=False)

    item = relationship("Item", back_populates="species_conquest_rewards")
    species_conquest = relationship("SpeciesConquest", back_populates="rewards")


class OriginalCreationReward(Base):
    __tablename__ = "original_creation_rewards"
    reward_type = Column(String, CheckConstraint("reward_type IN ('creation', 'battle', 'common_steal', 'rare_steal')",
                                                 name="valid_reward_type"), index=True, nullable=False,
                         primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", onupdate='CASCADE'), nullable=False)
    original_creation_id = Column(Integer, ForeignKey("original_creations.id", onupdate='CASCADE'), nullable=False,
                                  primary_key=True)
    quantity = Column(Integer, nullable=False)

    item = relationship("Item", back_populates="original_creation_rewards")
    original_creation = relationship("OriginalCreation", back_populates="rewards")


class Ability(Base):
    __tablename__ = "abilities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    effect = Column(String, nullable=False)
    equipment_type = Column(String,
                            CheckConstraint("equipment_type IN ('weapon', 'armor')", name="valid_equipment_type"),
                            nullable=False)

    fiend_equipment_rewards = relationship("FiendEquipmentReward", back_populates="ability")
    area_conquest_equipment_rewards = relationship("AreaConquestEquipmentReward", back_populates="ability")
    species_conquest_equipment_rewards = relationship("SpeciesConquestEquipmentReward", back_populates="ability")
    original_creation_equipment_rewards = relationship("OriginalCreationEquipmentReward", back_populates="ability")


class FiendEquipmentReward(Base):
    __tablename__ = "fiend_equipment_rewards"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate="CASCADE"), primary_key=True, index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)

    fiend = relationship("Fiend", back_populates="equipment_rewards")
    ability = relationship("Ability", back_populates="fiend_equipment_rewards")


class AreaConquestEquipmentReward(Base):
    __tablename__ = "area_conquest_equipment_rewards"
    area_conquest_id = Column(Integer, ForeignKey('area_conquests.id', onupdate="CASCADE"), primary_key=True,
                              index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)

    area_conquest = relationship("AreaConquest", back_populates="equipment_rewards")
    ability = relationship("Ability", back_populates="area_conquest_equipment_rewards")


class SpeciesConquestEquipmentReward(Base):
    __tablename__ = "species_conquest_equipment_rewards"
    species_conquest_id = Column(Integer, ForeignKey('species_conquests.id', onupdate="CASCADE"), primary_key=True,
                                 index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)

    species_conquest = relationship("SpeciesConquest", back_populates="equipment_rewards")
    ability = relationship("Ability", back_populates="species_conquest_equipment_rewards")


class OriginalCreationEquipmentReward(Base):
    __tablename__ = "original_creation_equipment_rewards"
    original_creation_id = Column(Integer, ForeignKey('original_creations.id', onupdate="CASCADE"), primary_key=True,
                                  index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)

    original_creation = relationship("OriginalCreation", back_populates="equipment_rewards")
    ability = relationship("Ability", back_populates="original_creation_equipment_rewards")


class WeaknessOrResistance(Base):
    __tablename__ = "weakness_or_resistance"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    fiend_weaknesses = relationship("FiendWeakness", back_populates="weakness")
    fiend_resistances = relationship("FiendResistance", back_populates="resistance")
    area_conquest_weaknesses = relationship("AreaConquestWeakness", back_populates="weakness")
    area_conquest_resistances = relationship("AreaConquestResistance", back_populates="resistance")
    species_conquest_weaknesses = relationship("SpeciesConquestWeakness", back_populates="weakness")
    species_conquest_resistances = relationship("SpeciesConquestResistance", back_populates="resistance")
    original_creation_weaknesses = relationship("OriginalCreationWeakness", back_populates="weakness")
    original_creation_resistances = relationship("OriginalCreationResistance", back_populates="resistance")


class FiendWeakness(Base):
    __tablename__ = "fiend_weakness"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate="CASCADE"), primary_key=True, index=True)
    weakness_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)
    percentage = Column(Integer, nullable=False)

    fiend = relationship("Fiend", back_populates="weaknesses")
    weakness = relationship("WeaknessOrResistance", back_populates="fiend_weaknesses")


class FiendResistance(Base):
    __tablename__ = "fiend_resistance"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate="CASCADE"), primary_key=True, index=True)
    resistance_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)

    fiend = relationship("Fiend", back_populates="resistances")
    resistance = relationship("WeaknessOrResistance", back_populates="fiend_resistances")


class AreaConquestWeakness(Base):
    __tablename__ = "area_conquest_weakness"
    area_conquest_id = Column(Integer, ForeignKey('area_conquests.id', onupdate="CASCADE"), primary_key=True, index=True)
    weakness_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)
    percentage = Column(Integer, nullable=False)

    area_conquest = relationship("AreaConquest", back_populates="weaknesses")
    weakness = relationship("WeaknessOrResistance", back_populates="area_conquest_weaknesses")


class AreaConquestResistance(Base):
    __tablename__ = "area_conquest_resistance"
    area_conquest_id = Column(Integer, ForeignKey('area_conquests.id', onupdate="CASCADE"), primary_key=True, index=True)
    resistance_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)

    area_conquest = relationship("AreaConquest", back_populates="resistances")
    resistance = relationship("WeaknessOrResistance", back_populates="area_conquest_resistances")


class SpeciesConquestWeakness(Base):
    __tablename__ = "species_conquest_weakness"
    species_conquest_id = Column(Integer, ForeignKey('species_conquests.id', onupdate="CASCADE"), primary_key=True,
                                 index=True)
    weakness_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)
    percentage = Column(Integer, nullable=False)

    species_conquest = relationship("SpeciesConquest", back_populates="weaknesses")
    weakness = relationship("WeaknessOrResistance", back_populates="species_conquest_weaknesses")


class SpeciesConquestResistance(Base):
    __tablename__ = "species_conquest_resistance"
    species_conquest_id = Column(Integer, ForeignKey('species_conquests.id', onupdate="CASCADE"), primary_key=True,
                                 index=True)
    resistance_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)

    species_conquest = relationship("SpeciesConquest", back_populates="resistances")
    resistance = relationship("WeaknessOrResistance", back_populates="species_conquest_resistances")


class OriginalCreationWeakness(Base):
    __tablename__ = "original_creation_weakness"
    original_creation_id = Column(Integer, ForeignKey('original_creations.id', onupdate="CASCADE"), primary_key=True,
                                  index=True)
    weakness_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)
    percentage = Column(Integer, nullable=False)

    original_creation = relationship("OriginalCreation", back_populates="weaknesses")
    weakness = relationship("WeaknessOrResistance", back_populates="original_creation_weaknesses")


class OriginalCreationResistance(Base):
    __tablename__ = "original_creation_resistance"
    original_creation_id = Column(Integer, ForeignKey('original_creations.id', onupdate="CASCADE"), primary_key=True,
                                  index=True)
    resistance_id = Column(Integer, ForeignKey('weakness_or_resistance.id', onupdate="CASCADE"), primary_key=True, index=True)

    original_creation = relationship("OriginalCreation", back_populates="resistances")
    resistance = relationship("WeaknessOrResistance", back_populates="original_creation_resistances")


class Stats(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, index=True)
    for_fiend = Column(String, nullable=False)
    hp = Column(Integer)
    mp = Column(Integer)
    overkill = Column(Integer)
    guil = Column(Integer)
    ap = Column(Integer)
    ap_overkill = Column(Integer)

    fiends = relationship("FiendStats", back_populates="stats")
    area_conquests = relationship("AreaConquestStats", back_populates="stats")
    species_conquests = relationship("SpeciesConquestStats", back_populates="stats")
    original_creations = relationship("OriginalCreationStats", back_populates="stats")


class FiendStats(Base):
    __tablename__ = "fiend_stats"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate="CASCADE"), primary_key=True, index=True)
    stats_id = Column(Integer, ForeignKey('stats.id', onupdate="CASCADE"), primary_key=True, index=True)

    fiend = relationship("Fiend", back_populates="stats")
    stats = relationship("Stats", back_populates="fiends")


class AreaConquestStats(Base):
    __tablename__ = "area_conquest_stats"
    area_conquest_id = Column(Integer, ForeignKey('area_conquests.id', onupdate="CASCADE"), primary_key=True, index=True)
    stats_id = Column(Integer, ForeignKey('stats.id', onupdate="CASCADE"), primary_key=True, index=True)

    area_conquest = relationship("AreaConquest", back_populates="stats")
    stats = relationship("Stats", back_populates="area_conquests")


class SpeciesConquestStats(Base):
    __tablename__ = "species_conquest_stats"
    species_conquest_id = Column(Integer, ForeignKey('species_conquests.id', onupdate="CASCADE"), primary_key=True, index=True)
    stats_id = Column(Integer, ForeignKey('stats.id', onupdate="CASCADE"), primary_key=True, index=True)

    species_conquest = relationship("SpeciesConquest", back_populates="stats")
    stats = relationship("Stats", back_populates="species_conquests")


class OriginalCreationStats(Base):
    __tablename__ = "original_creation_stats"
    original_creation_id = Column(Integer, ForeignKey('original_creations.id', onupdate="CASCADE"), primary_key=True,
                                  index=True)
    stats_id = Column(Integer, ForeignKey('stats.id', onupdate="CASCADE"), primary_key=True, index=True)

    original_creation = relationship("OriginalCreation", back_populates="stats")
    stats = relationship("Stats", back_populates="original_creations")
