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
    type = Column(String, CheckConstraint("type IN ('common', 'offensive', 'support', 'special')"), nullable=False)


class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)

    fiends = relationship("Fiend", back_populates="zone")
    found_fiends = relationship("CanBeFound", back_populates="zone")


class SpeciesConquest(Base):
    __tablename__ = "species_conquests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    required_fiends = Column(Integer, nullable=False)
    created = Column(Boolean, default=False, index=True)
    defeated = Column(Boolean, default=False, index=True)

    fiends = relationship("Fiend", back_populates="species_conquest")


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


class SpecialFiend(Base):
    __tablename__ = "special_fiends"
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

    zone = relationship("Zone")


class OriginalCreation(Base):
    __tablename__ = "original_creations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    image_url = Column(String, unique=True)
    created = Column(Boolean, default=False, index=True)
    creation_rule = Column(String)
    defeated = Column(Boolean, default=False, index=True)


class CanBeFound(Base):
    __tablename__ = "can_be_found"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate='CASCADE'), primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey('zones.id', onupdate='CASCADE'), primary_key=True, index=True)

    fiend = relationship("Fiend", back_populates="found_zones")
    zone = relationship("Zone", back_populates="found_fiends")


class Reward(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True, index=True)
    reward_type = Column(String, CheckConstraint("reward_type IN ('creation', 'battle', 'common_steal', 'rare_steal')",
                                                 name="valid_reward_type"
                                                 ), index=True, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    item = relationship("Item")
    reward_associations = relationship("RewardAssociation", back_populates="reward")


class RewardAssociation(Base):
    __tablename__ = "reward_associations"
    id = Column(Integer, primary_key=True, index=True)
    reward_id = Column(Integer, ForeignKey("rewards.id", onupdate="CASCADE"), nullable=False)
    target_type = Column(String,
                         CheckConstraint(
                             "target_type IN ('area_conquest', 'species_conquest', 'original_creation')",
                             name="valid_target_type"
                         ),
                         nullable=False)
    target_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    reward = relationship("Reward", back_populates="reward_associations")


class Ability(Base):
    __tablename__ = "abilities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    effect = Column(String, nullable=False)
    equipment_type = Column(String, CheckConstraint(
        "equipment_type IN ('weapon', 'armor')", name="valid_equipment_type"), nullable=False)


class FiendEquipmentReward(Base):
    __tablename__ = "fiend_equipment_rewards"
    fiend_id = Column(Integer, ForeignKey('fiends.id', onupdate="CASCADE"), primary_key=True, index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)


class AreaConquestEquipmentReward(Base):
    __tablename__ = "area_conquest_equipment_rewards"
    area_conquest_id = Column(Integer, ForeignKey('area_conquests.id', onupdate="CASCADE"), primary_key=True,
                              index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)


class SpeciesConquestEquipmentReward(Base):
    __tablename__ = "species_conquest_equipment_rewards"
    species_conquest_id = Column(Integer, ForeignKey('species_conquests.id', onupdate="CASCADE"), primary_key=True,
                                 index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)


class OriginalCreationEquipmentReward(Base):
    __tablename__ = "original_creation_equipment_rewards"
    original_creations_id = Column(Integer, ForeignKey('original_creations.id', onupdate="CASCADE"), primary_key=True,
                                   index=True)
    ability_id = Column(Integer, ForeignKey('abilities.id', onupdate="CASCADE"), primary_key=True, index=True)
