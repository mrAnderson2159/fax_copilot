# backend/app/populate_data.py
import traceback
from sqlalchemy.exc import SQLAlchemyError
from app.database import SessionLocal
from app.models import *

# Inizializza la sessione di database come variabile globale
db = SessionLocal()


def lower_case(function):
    def wrapper(name: str, *args, **kwargs):
        return function(name.lower(), *args, **kwargs)

    return wrapper


def all_lower_case(function):
    def wrapper(*args):
        return function(*[arg.lower() if isinstance(arg, str) else arg for arg in args])

    return wrapper


def get_or_create(model, filter_key: str, **kwargs):
    global db

    # Se filter_key è '*', utilizza tutti i campi in kwargs per il filtro
    if filter_key == '*':
        filter_condition = kwargs
    else:
        # Gestisci più chiavi separate da virgole
        keys = [key.strip() for key in filter_key.split(',')]
        filter_condition = {key: kwargs[key] for key in keys if key in kwargs}

    instance = db.query(model).filter_by(**filter_condition).first()

    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.flush()  # Ottiene l'ID per l'istanza creata
        db.refresh(instance)
        return instance


@lower_case
def new_zone(zone_name: str) -> Zone:
    return get_or_create(Zone, 'name', name=zone_name, image_url=f"../images/zones/{zone_name}.webp")


@lower_case
def new_fiend(fiend_name: str, zone: Zone, species_conquest: SpeciesConquest = None) -> Fiend:
    return get_or_create(
        Fiend,
        'name',
        name=fiend_name,
        was_captured=0,
        zone_id=zone.id,
        species_conquest_id=(species_conquest.id if species_conquest else None),
        image_url=f"../images/fiends/{fiend_name}.webp"
    )


@lower_case
def new_area_conquest(fiend_name: str, zone: Zone) -> AreaConquest:
    return get_or_create(
        AreaConquest,
        'name',
        name=fiend_name,
        zone_id=zone.id,
        image_url=f"../images/area_conquests/{fiend_name}.webp"
    )


@lower_case
def new_species_conquest(fiend_name: str, required_fiends: int) -> SpeciesConquest:
    return get_or_create(
        SpeciesConquest,
        'name',
        name=fiend_name,
        required_fiends=required_fiends,
        image_url=f"../images/species_conquests/{fiend_name}.webp"
    )


@lower_case
def new_original_creation(fiend_name: str, creation_rule: str) -> OriginalCreation:
    return get_or_create(
        OriginalCreation,
        'name',
        name=fiend_name,
        creation_rule=creation_rule,
        image_url=f"../images/original_creations/{fiend_name}.webp"
    )


@all_lower_case
def new_can_be_found(fiend_name: str, zone_name: str) -> CanBeFound:
    fiend = db.query(Fiend).filter(Fiend.name == fiend_name).first()
    zone = db.query(Zone).filter(Zone.name == zone_name).first()
    if not fiend:
        raise ValueError(f"Il mostro '{fiend_name}' non è stato trovato nel database.")
    if not zone:
        raise ValueError(f"La zona '{zone_name}' non è stata trovata nel database.")
    return get_or_create(CanBeFound, '*', fiend_id=fiend.id, zone_id=zone.id)


@lower_case
def new_item(item_name: str, effect: str, item_type: str) -> Item:
    return get_or_create(Item, 'name', name=item_name, effect=effect, type=item_type)


@lower_case
def new_ability(ability_name: str, effect: str, equipment_type: str) -> Ability:
    return get_or_create(Ability, 'name', name=ability_name, effect=effect, equipment_type=equipment_type)


@all_lower_case
def new_fiend_reward(fiend_name: str, reward_type: str, item_name: str, quantity: int) -> FiendReward:
    fiend = db.query(Fiend).filter(Fiend.name == fiend_name).first()
    item = db.query(Item).filter(Item.name == item_name).first()
    if not fiend:
        raise ValueError(f"Il mostro '{fiend_name}' non è stato trovato nel database.")
    if not item:
        raise ValueError(f"L'item '{item_name}' non è stato trovato nel database.")
    return get_or_create(FiendReward, '*', fiend_id=fiend.id, reward_type=reward_type, item_id=item.id,
                         quantity=quantity)


@all_lower_case
def new_area_conquest_reward(area_conquest_name: str, reward_type: str, item_name: str,
                             quantity: int) -> AreaConquestReward:
    area_conquest = db.query(AreaConquest).filter(AreaConquest.name == area_conquest_name).first()
    item = db.query(Item).filter(Item.name == item_name).first()
    if not area_conquest:
        raise ValueError(f"L'area conquest '{area_conquest_name}' non è stata trovata nel database.")
    if not item:
        raise ValueError(f"L'item '{item_name}' non è stato trovato nel database.")
    return get_or_create(AreaConquestReward, '*', area_conquest_id=area_conquest.id, reward_type=reward_type,
                         item_id=item.id, quantity=quantity)


@all_lower_case
def new_species_conquest_reward(species_conquest_name: str, reward_type: str, item_name: str,
                                quantity: int) -> SpeciesConquestReward:
    species_conquest = db.query(SpeciesConquest).filter(SpeciesConquest.name == species_conquest_name).first()
    item = db.query(Item).filter(Item.name == item_name).first()
    if not species_conquest:
        raise ValueError(f"Il species conquest '{species_conquest_name}' non è stato trovato nel database.")
    if not item:
        raise ValueError(f"L'item '{item_name}' non è stato trovato nel database.")
    return get_or_create(SpeciesConquestReward, '*', species_conquest_id=species_conquest.id, reward_type=reward_type,
                         item_id=item.id, quantity=quantity)


@all_lower_case
def new_original_creation_reward(original_creation_name: str, reward_type: str, item_name: str,
                                 quantity: int) -> OriginalCreationReward:
    original_creation = db.query(OriginalCreation).filter(OriginalCreation.name == original_creation_name).first()
    item = db.query(Item).filter(Item.name == item_name).first()
    if not original_creation:
        raise ValueError(f"L'original creation '{original_creation_name}' non è stata trovata nel database.")
    if not item:
        raise ValueError(f"L'item '{item_name}' non è stato trovato nel database.")
    return get_or_create(OriginalCreationReward, '*', original_creation_id=original_creation.id, reward_type=reward_type,
                         item_id=item.id, quantity=quantity)


@all_lower_case
def new_fiend_equipment_reward(fiend_name: str, ability_name: str) -> FiendEquipmentReward:
    fiend = db.query(Fiend).filter(Fiend.name == fiend_name).first()
    ability = db.query(Ability).filter(Ability.name == ability_name).first()
    if not fiend:
        raise ValueError(f"Il mostro '{fiend_name}' non è stato trovato nel database.")
    if not ability:
        raise ValueError(f"L'abilità '{ability_name}' non è stata trovata nel database.")
    return get_or_create(FiendEquipmentReward, '*', fiend_id=fiend.id, ability_id=ability.id)


@all_lower_case
def new_area_conquest_equipment_reward(area_conquest_name: str, ability_name: str) -> AreaConquestEquipmentReward:
    area_conquest = db.query(AreaConquest).filter(AreaConquest.name == area_conquest_name).first()
    ability = db.query(Ability).filter(Ability.name == ability_name).first()
    if not area_conquest:
        raise ValueError(f"L'area conquest '{area_conquest_name}' non è stata trovata nel database.")
    if not ability:
        raise ValueError(f"L'abilità '{ability_name}' non è stata trovata nel database.")
    return get_or_create(AreaConquestEquipmentReward, '*', area_conquest_id=area_conquest.id, ability_id=ability.id)


@all_lower_case
def new_species_conquest_equipment_reward(species_conquest_name: str, ability_name: str) -> SpeciesConquestEquipmentReward:
    species_conquest = db.query(SpeciesConquest).filter(SpeciesConquest.name == species_conquest_name).first()
    ability = db.query(Ability).filter(Ability.name == ability_name).first()
    if not species_conquest:
        raise ValueError(f"Il species conquest '{species_conquest_name}' non è stato trovato nel database.")
    if not ability:
        raise ValueError(f"L'abilità '{ability_name}' non è stata trovata nel database.")
    return get_or_create(SpeciesConquestEquipmentReward, '*', species_conquest_id=species_conquest.id, ability_id=ability.id)


@all_lower_case
def new_original_creation_equipment_reward(
        original_creation_name: str,
        ability_name: str
) -> OriginalCreationEquipmentReward:
    original_creation = db.query(OriginalCreation).filter(OriginalCreation.name == original_creation_name).first()
    ability = db.query(Ability).filter(Ability.name == ability_name).first()
    if not original_creation:
        raise ValueError(f"L'original creation '{original_creation_name}' non è stata trovata nel database.")
    if not ability:
        raise ValueError(f"L'abilità '{ability_name}' non è stata trovata nel database.")
    return get_or_create(OriginalCreationEquipmentReward,
                         '*',
                         original_creation_id=original_creation.id,
                         ability_id=ability.id)


@lower_case
def new_weakness_or_resistance(name: str) -> WeaknessOrResistance:
    return get_or_create(WeaknessOrResistance, 'name', name=name)


@all_lower_case
def new_fiend_weakness(fiend_name: str, weakness_or_resistance_name: str, percentage: int) -> FiendWeakness:
    fiend = db.query(Fiend).filter(Fiend.name == fiend_name).first()
    weakness = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not fiend:
        raise ValueError(f"Il mostro '{fiend_name}' non è stato trovato nel database.")
    if not weakness:
        raise ValueError(f"La debolezza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(FiendWeakness, '*', fiend_id=fiend.id, weakness_id=weakness.id, percentage=percentage)


@all_lower_case
def new_fiend_resistance(fiend_name: str, weakness_or_resistance_name: str) -> FiendResistance:
    fiend = db.query(Fiend).filter(Fiend.name == fiend_name).first()
    resistance = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not fiend:
        raise ValueError(f"Il mostro '{fiend_name}' non è stato trovato nel database.")
    if not resistance:
        raise ValueError(f"La resistenza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(FiendResistance, '*', fiend_id=fiend.id, resistance_id=resistance.id)


@all_lower_case
def new_area_conquest_weakness(
        area_conquest_name: str,
        weakness_or_resistance_name: str,
        percentage: int
) -> AreaConquestWeakness:
    area_conquest = db.query(AreaConquest).filter(AreaConquest.name == area_conquest_name).first()
    weakness = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not area_conquest:
        raise ValueError(f"L'area conquest '{area_conquest_name}' non è stata trovata nel database.")
    if not weakness:
        raise ValueError(f"La debolezza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(AreaConquestWeakness,
                         '*',
                         area_conquest_id=area_conquest.id,
                         weakness_id=weakness.id,
                         percentage=percentage)


@all_lower_case
def new_area_conquest_resistance(area_conquest_name: str, weakness_or_resistance_name: str) -> AreaConquestResistance:
    area_conquest = db.query(AreaConquest).filter(AreaConquest.name == area_conquest_name).first()
    resistance = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not area_conquest:
        raise ValueError(f"L'area conquest '{area_conquest_name}' non è stata trovata nel database.")
    if not resistance:
        raise ValueError(f"La resistenza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(AreaConquestResistance,
                         '*',
                         area_conquest_id=area_conquest.id,
                         resistance_id=resistance.id)


@all_lower_case
def new_species_conquest_weakness(
        species_conquest_name: str,
        weakness_or_resistance_name: str,
        percentage: int
) -> SpeciesConquestWeakness:
    species_conquest = db.query(SpeciesConquest).filter(SpeciesConquest.name == species_conquest_name).first()
    weakness = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not species_conquest:
        raise ValueError(f"Il species conquest '{species_conquest_name}' non è stato trovato nel database.")
    if not weakness:
        raise ValueError(f"La debolezza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(SpeciesConquestWeakness,
                         '*',
                         species_conquest_id=species_conquest.id,
                         weakness_id=weakness.id,
                         percentage=percentage)


@all_lower_case
def new_species_conquest_resistance(species_conquest_name: str, weakness_or_resistance_name: str) -> SpeciesConquestResistance:
    species_conquest = db.query(SpeciesConquest).filter(SpeciesConquest.name == species_conquest_name).first()
    resistance = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not species_conquest:
        raise ValueError(f"Il species conquest '{species_conquest_name}' non è stato trovato nel database.")
    if not resistance:
        raise ValueError(f"La resistenza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(SpeciesConquestResistance,
                         '*',
                         species_conquest_id=species_conquest.id,
                         resistance_id=resistance.id)


@all_lower_case
def new_original_creation_weakness(
        original_creation_name: str,
        weakness_or_resistance_name: str,
        percentage: int
) -> OriginalCreationWeakness:
    original_creation = db.query(OriginalCreation).filter(OriginalCreation.name == original_creation_name).first()
    weakness = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not original_creation:
        raise ValueError(f"L'original creation '{original_creation_name}' non è stata trovata nel database.")
    if not weakness:
        raise ValueError(f"La debolezza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(OriginalCreationWeakness,
                         '*',
                         original_creation_id=original_creation.id,
                         weakness_id=weakness.id,
                         percentage=percentage)


@all_lower_case
def new_original_creation_resistance(original_creation_name: str, weakness_or_resistance_name: str) -> OriginalCreationResistance:
    original_creation = db.query(OriginalCreation).filter(OriginalCreation.name == original_creation_name).first()
    resistance = db.query(WeaknessOrResistance).filter(WeaknessOrResistance.name == weakness_or_resistance_name).first()
    if not original_creation:
        raise ValueError(f"L'original creation '{original_creation_name}' non è stata trovata nel database.")
    if not resistance:
        raise ValueError(f"La resistenza '{weakness_or_resistance_name}' non è stata trovata nel database.")
    return get_or_create(OriginalCreationResistance,
                         '*',
                         original_creation_id=original_creation.id,
                         resistance_id=resistance.id)


@lower_case
def new_stat(for_fiend: str, *, hp: int = None, mp: int = None, overkill: int = None, guil: int = None, ap: int = None,
              ap_overkill: int = None) -> Stats:
    return get_or_create(
        Stats,
        '*',
        for_fiend=for_fiend,
        hp=hp,
        mp=mp,
        overkill=overkill,
        guil=guil,
        ap=ap,
        ap_overkill=ap_overkill
    )


@lower_case
def new_fiend_stats(fiend_name: str) -> FiendStats:
    fiend = db.query(Fiend).filter(Fiend.name == fiend_name).first()
    stat = db.query(Stats).filter(Stats.for_fiend == fiend_name).first()
    if not fiend:
        raise ValueError(f"Il mostro '{fiend_name}' non è stato trovato nel database.")
    if not stat:
        raise ValueError(f"Le statistiche per '{fiend_name}' non sono state trovate nel database.")
    return get_or_create(FiendStats, '*', fiend_id=fiend.id, stats_id=stat.id)


@lower_case
def new_area_conquest_stats(area_conquest_name: str) -> AreaConquestStats:
    area_conquest = db.query(AreaConquest).filter(AreaConquest.name == area_conquest_name).first()
    stat = db.query(Stats).filter(Stats.for_fiend == area_conquest_name).first()
    if not area_conquest:
        raise ValueError(f"L'area conquest '{area_conquest_name}' non è stata trovata nel database.")
    if not stat:
        raise ValueError(f"Le statistiche per '{area_conquest_name}' non sono state trovate nel database.")
    return get_or_create(AreaConquestStats, '*', area_conquest_id=area_conquest.id, stats_id=stat.id)


@lower_case
def new_species_conquest_stats(species_conquest_name: str) -> SpeciesConquestStats:
    species_conquest = db.query(SpeciesConquest).filter(SpeciesConquest.name == species_conquest_name).first()
    stat = db.query(Stats).filter(Stats.for_fiend == species_conquest_name).first()
    if not species_conquest:
        raise ValueError(f"Il species conquest '{species_conquest_name}' non è stato trovato nel database.")
    if not stat:
        raise ValueError(f"Le statistiche per '{species_conquest_name}' non sono state trovate nel database.")
    return get_or_create(SpeciesConquestStats, '*', species_conquest_id=species_conquest.id, stats_id=stat.id)


@lower_case
def new_original_creation_stats(original_creation_name: str) -> OriginalCreationStats:
    original_creation = db.query(OriginalCreation).filter(OriginalCreation.name == original_creation_name).first()
    stat = db.query(Stats).filter(Stats.for_fiend == original_creation_name).first()
    if not original_creation:
        raise ValueError(f"L'original creation '{original_creation_name}' non è stato trovato nel database.")
    if not stat:
        raise ValueError(f"Le statistiche per '{original_creation_name}' non sono state trovate nel database.")
    return get_or_create(OriginalCreationStats, '*', original_creation_id=original_creation.id, stats_id=stat.id)




def populate_data():
    global db
    areas = [
        'besaid', 'kilika', 'via mihen', 'via micorocciosa', 'via djose',
        'piana dei lampi', 'macalania', 'bikanel', 'piana della bonaccia',
        'grotta del crepaccio', 'monte gagazet', 'dentro sin', 'rovine di omega'
    ]

    try:
        print("Popolamento del database in corso...")
        print("Creazione degli Item...", end=' ')
        items = [
            new_item("Pozione", "Fa recuperare 200HP ad un alleato", "common"),
            new_item("Granpozione", "Fa recuperare 1000HP ad un alleato", "common"),
            new_item("Extrapozione", "Fa recuperare 9999HP ad un alleato", "common"),
            new_item("Megapozione", "Fa recuperare 2000HP a tutto il party", "common"),
            new_item("Etere", "Fa recuperare 100MP ad un alleato", "common"),
            new_item("Turboetere", "Fa recuperare 500MP ad un alleato", "common"),
            new_item("Elisir", "Fa recuperare 9999HP e 999MP ad un alleato", "common"),
            new_item("Megaelisir", "Fa recuperare 9999HP e 999MP a tutto il party", "common"),
            new_item("Coda di Fenice", "Cura lo status K.O. di un alleato", "common"),
            new_item("Megafenice", "Cura lo status K.O. di tutto il party", "common"),
            new_item("Antidoto", "Cura lo status Veleno di un alleato", "common"),
            new_item("Ago Dorato", "Cura lo status Pietra di un alleato", "common"),
            new_item("Collirio", "Cura lo status Blind di un alleato", "common"),
            new_item("Erba dell'eco", "Cura lo status Mutismo di un alleato", "common"),
            new_item("Acquasanta", "Cura lo status Zombie e Maledizione di un alleato", "common"),
            new_item("Panacea", "Cura tutti gli status alterati di un alleato", "common"),
            new_item("Protoenergia", "Infligge lo status Protoenergia ad un nemico", "offensive"),
            new_item("Protomagia", "Infligge lo status Protomagia ad un nemico", "offensive"),
            new_item("Protorapidità", "Infligge lo status Protorapidità ad un nemico", "offensive"),
            new_item("Protoabilità", "Infligge lo status Protoabilità ad un nemico", "offensive"),
            new_item("Scheggia di Piros", "Causa danni di elemento Fuoco ad un nemico", "offensive"),
            new_item("Anima di Piros", "Causa danni di elemento Fuoco ad un nemico", "offensive"),
            new_item("Magmagilite", "Causa danni di elemento Fuoco a tutti i nemici", "offensive"),
            new_item("Razzo Elettrico", "Causa danni di elemento Tuono ad un nemico", "offensive"),
            new_item("Razzo Fulminante", "Causa danni di elemento Tuono ad un nemico", "offensive"),
            new_item("Elettromagilite", "Causa danni di elemento Tuono a tutti i nemici", "offensive"),
            new_item("Squama di Pesce", "Causa danni di elemento Acqua ad un nemico", "offensive"),
            new_item("Squama di Drago", "Causa danni di elemento Acqua ad un nemico", "offensive"),
            new_item("Idromagilite", "Causa danni di elemento Acqua a tutti i nemici", "offensive"),
            new_item("Vento Artico", "Causa danni di elemento Gelo ad un nemico", "offensive"),
            new_item("Vento Antartico", "Causa danni di elemento Gelo ad un nemico", "offensive"),
            new_item("Criomagilite", "Causa danni di elemento Gelo a tutti i nemici", "offensive"),
            new_item("Granata", "Causa danni a tutti i nemici", "offensive"),
            new_item("Blindogranata", "Causa danni e infligge lo status Antiscutum a tutti i nemici", "offensive"),
            new_item("Melatonina", "Causa danni e infligge lo status Sonno a tutti i nemici", "offensive"),
            new_item("Onirolina", "Causa danni e infligge lo status Sonno a tutti i nemici", "offensive"),
            new_item("Mina Tacet", "Causa danni e infligge lo status Mutismo a tutti i nemici", "offensive"),
            new_item("Lacrimogeno", "Causa danni e infligge lo status Blind a tutti i nemici", "offensive"),
            new_item("Neromagilite", "Dimezza gli HP di tutti i nemici", "offensive"),
            new_item("Eliomagilite", "Causa danni ad un nemico", "offensive"),
            new_item("Sacromagilite", "Causa danni a tutti i nemici", "offensive"),
            new_item("Examagilite", "Causa danni a tutti i nemici", "offensive"),
            new_item("Zanna Velenosa", "Causa danni e infligge lo status Veleno ad un nemico", "offensive"),
            new_item("Clessidra d'Argento", "Infligge lo status Lentezza a tutti i nemici", "offensive"),
            new_item("Clessidra d'Oro", "Causa danni e infligge lo status Lentezza a tutti i nemici", "offensive"),
            new_item("Candela della Vita", "Infligge lo status Sentenza ad un nemico", "offensive"),
            new_item("Granata Fossile", "Infligge lo status Pietra a tutti i nemici", "offensive"),
            new_item("Ombra d'Oltremondo", "Infligge lo status Morte ad un nemico", "offensive"),
            new_item("Vento d'Oltremondo", "Infligge lo status Morte a tutti i nemici", "offensive"),
            new_item("Materioscura", "Causa gravi danni a tutti i nemici", "offensive"),
            new_item("Albhedina", "Cura Veleno, Mutismo, Pietra e recupera 1000HP a tutto il party", "support"),
            new_item("Acqua Curativa", "Fa recuperare 9999HP a tutto il party", "support"),
            new_item("Coda di Chocobo", "Attiva lo status Haste su un alleato", "support"),
            new_item("Piuma di Chocobo", "Attiva lo status Haste su tutto il party", "support"),
            new_item("Cortina Lunare", "Attiva lo status Shell su un alleato", "support"),
            new_item("Cortina Luminosa", "Attiva lo status Protect su un alleato", "support"),
            new_item("Cortina Stellare", "Attiva lo status Reflex su un alleato", "support"),
            new_item("Fluido Rigenerante", "Attiva lo status Rigene su un alleato", "support"),
            new_item("Fluido Magico", "Assorbe MP da un nemico", "support"),
            new_item("Fluido Energetico", "Assorbe HP da un nemico", "support"),
            new_item("Fluido Vitale", "Assorbe HP ed MP da un nemico", "support"),
            new_item("Sale Purificatore", "Causa danni ed elimina la magia difensiva su un nemico", "support"),
            new_item("Nettare Energetico", "Raddoppia gli HP massimi di un alleato", "support"),
            new_item("Nettare Magico", "Raddoppia gli MP massimi di un alleato", "support"),
            new_item("Filtro Energetico", "Raddoppia gli HP massimi di tutto il party", "support"),
            new_item("Filtro Magico", "Raddoppia gli MP massimi di tutto il party", "support"),
            new_item("Duostella", "Azzera il consumo di MP di un alleato", "support"),
            new_item("Triostella", "Azzera il consumo di MP di tutto il party", "support"),
            new_item("stricnina", "Potrebbe essere utile!", "special"),
            new_item("hypellina", "Potrebbe essere utile!", "special"),
            new_item("portafoglio gonfio", "Potrebbe essere utile!", "special"),
            new_item("controchiave", "Potrebbe essere utile!", "special"),
            new_item("ali x l'ignoto", "Potrebbe essere utile!", "special"),
            new_item("spina iperica", "Potrebbe essere utile!", "special"),
            new_item("pendulum", "Potrebbe essere utile!", "special"),
            new_item("amuleto", "Potrebbe essere utile!", "special"),
            new_item("porta sul domani", "Potrebbe essere utile!", "special"),
            new_item("anima del baro", "Potrebbe essere utile!", "special"),
            new_item("equazione cubica", "Potrebbe essere utile!", "special"),

            new_item("mappa", "Mostra la mappa di Spira", "special"),
            new_item("carta d'identità", "Permette di cambiare il nome di un eone", "special"),

            new_item("corona di boccioli", "Rarità", "curio"),
            new_item("corona di fiori", "Rarità", "curio"),

            new_item("abilitosfera", "Permette di imparare un'abilità", "sphere_grid"),
            new_item("energosfera", "Attiva una somatosfera di HP, POT fisica e DIF fisica", "sphere_grid"),
            new_item("magicosfera", "Attiva una somatosfera di MP, POT magica e DIF magica", "sphere_grid"),
            new_item("velocisfera", "Attiva una somatosfera di Rapidità, Destrezza e Mira", "sphere_grid"),
            new_item("fatosfera", "Attiva una somatosfera di Fortuna", "sphere_grid"),

            new_item("accapisfera", "Converte una somatosfera vuota in HP +300", "sphere_grid"),
            new_item("emmepisfera", "Converte una somatosfera vuota in MP +40", "sphere_grid"),
            new_item("destrosfera", "Converte una somatosfera vuota in Destrezza +4", "sphere_grid"),
            new_item("difesfera fis", "Converte una somatosfera vuota in DIF Fisica +4", "sphere_grid"),
            new_item("difesfera mag", "Converte una somatosfera vuota in DIF Magica +4", "sphere_grid"),
            new_item("potesfera fis", "Converte una somatosfera vuota in POT Fisica +4", "sphere_grid"),
            new_item("potesfera mag", "Converte una somatosfera vuota in POT Magica +4", "sphere_grid"),
            new_item("fortunosfera", "Converte una somatosfera vuota in Fortuna +4", "sphere_grid"),
            new_item("mirasfera", "Converte una somatosfera vuota in Mira +4", "sphere_grid"),
            new_item("rapidosfera", "Converte una somatosfera vuota in Rapidità +4", "sphere_grid"),

            new_item("mastersfera", "Attiva qualsiasi somatosfera nella sferografia", "sphere_grid"),
            new_item("onnisfera", "Permette di spostarsi su qualsiasi somatosfera nella sferografia", "sphere_grid"),
            new_item("gamberosfera",
                     "Trasporta in una qualsiasi Somatosfera già attivata dal personaggio che ne fa uso",
                     "sphere_grid"),
            new_item("telesfera", "Trasporta in una qualsiasi Somatosfera già attivata da un altro personaggio",
                     "sphere_grid"),
            new_item("empatosfera", "Trasporta in una Somatosfera sulla quale si trova un alleato", "sphere_grid"),
            new_item("passosfera lv 1", "Sblocca una passosfera lv 1 nella sferografia", "sphere_grid"),
            new_item("passosfera lv 2", "Sblocca una passosfera lv 2 nella sferografia", "sphere_grid"),
            new_item("passosfera lv 3", "Sblocca una passosfera lv 3 nella sferografia", "sphere_grid"),
            new_item("passosfera lv 4", "Sblocca una passosfera lv 4 nella sferografia", "sphere_grid"),
        ]

        print('OK')

        print("Creazione delle Zone...", end=' ')
        zones = {area: new_zone(area) for area in areas}
        print('OK')

        print("Creazione delle AreaConquests...", end=' ')
        area_conquests = [
            new_area_conquest("Trusthevis", zones["besaid"]),
            new_area_conquest("Molboro Beta", zones["kilika"]),
            new_area_conquest("Kolossos", zones["via mihen"]),
            new_area_conquest("Iaguaro regina", zones["via micorocciosa"]),
            new_area_conquest("Yormungand", zones["via djose"]),
            new_area_conquest("Kyactus", zones["piana dei lampi"]),
            new_area_conquest("Espada", zones["macalania"]),
            new_area_conquest("Abyss Worm", zones["bikanel"]),
            new_area_conquest("Chimera X", zones["piana della bonaccia"]),
            new_area_conquest("Don Tomberry", zones["grotta del crepaccio"]),
            new_area_conquest("Catoblepas", zones["monte gagazet"]),
            new_area_conquest("Abadon", zones["dentro sin"]),
            new_area_conquest("Vorban", zones["rovine di omega"])
        ]
        print('OK')

        print("Creazione delle SpeciesConquests...", end=' ')
        class SpeciesConquestsData:
            def __init__(self):
                # Definiamo i dati dei conquest
                couples = [
                    ('fenril', 3),
                    ('ornitorestes', 3),
                    ('pterix', 4),
                    ('honet', 4),
                    ('vizalsha', 4),
                    ('unioculum', 4),
                    ('budino jumbo', 3),
                    ('elemento nega', 3),
                    ('tanket', 3),
                    ('fefnil', 4),
                    ('sonnellino', 5),
                    ('re piros', 5),
                    ('juggernaut', 5),
                    ("clod d'acciaio", 10)
                ]

                # Creiamo un dizionario per mappare i nomi ai `SpeciesConquest`
                self.species_conquests = {
                    name: new_species_conquest(name, required_fiends)
                    for name, required_fiends in couples
                }

            def __getitem__(self, name: str) -> SpeciesConquest:
                # Otteniamo il `SpeciesConquest` corrispondente al nome
                return self.species_conquests[name.lower()]

            def all(self) -> list[SpeciesConquest]:
                # Ritorna tutti i `SpeciesConquest` sotto forma di lista
                return list(self.species_conquests.values())

        species_conquests = SpeciesConquestsData()
        print('OK')

        print("Creazione degli OriginalCreations...", end=' ')
        original_creations = [
            new_original_creation('Mangiaterra', 'Generare 2 creature della categoria campioni di zona'),
            new_original_creation('Titanosfera', 'Generare 2 creature della categoria campioni di specie'),
            new_original_creation('Catastrophe', 'Generare 6 creature della categoria campioni di zona'),
            new_original_creation('Vlakorados', 'Generare 6 creature della categoria campioni di specie'),
            new_original_creation('Gasteropodos', 'Catturare un esemplare di ogni mostro'),
            new_original_creation('Ultima X', 'Catturare 5 esemplari di ogni mostro'),
            new_original_creation('Shinryu',
                                  'Catturare 2 esemplari di Splasher, Aquelous ed Echeneis nel Monte Gagazet'),
            new_original_creation('Il Supremo',
                                  'Catturare 10 esemplari di ogni mostro e sconfiggere tutti i '
                                  'campioni di zona, campioni di specie e prototipi zoolab almeno una volta')
        ]
        print('OK')

        print("Creazione dei Fiend...", end=' ')
        fiends = [
            new_fiend('dingo', zones['besaid'], species_conquests['fenril']),
            new_fiend('condor', zones['besaid'], species_conquests['pterix']),
            new_fiend("budino d'acqua", zones['besaid'], species_conquests['budino Jumbo']),

            new_fiend('Deinonychus', zones['kilika'], species_conquests['ornitorestes']),
            new_fiend('Ape Killer', zones['kilika'], species_conquests['honet']),
            new_fiend('Elemento Giallo', zones['kilika'], species_conquests['elemento Nega']),
            new_fiend('Balsamiko', zones['kilika']),

            new_fiend('Mihen Phang', zones['via mihen'], species_conquests['fenril']),
            new_fiend('Ipiria', zones['via mihen'], species_conquests['ornitorestes']),
            new_fiend('Occhio fluttuante', zones['via mihen'], species_conquests['unioculum']),
            new_fiend('Elemento Bianco', zones['via mihen'], species_conquests['elemento Nega']),
            new_fiend('Rarth', zones['via mihen'], species_conquests['tanket']),
            new_fiend('Vivre', zones['via mihen'], species_conquests['fefnil']),
            new_fiend('Piros', zones['via mihen'], species_conquests['re piros']),
            new_fiend('Bikorno', zones['via mihen'], species_conquests['juggernaut']),

            new_fiend('Raptor', zones['via micorocciosa'], species_conquests['ornitorestes']),
            new_fiend('Gandharva', zones['via micorocciosa'], species_conquests['vizalsha']),
            new_fiend('Budino di tuono', zones['via micorocciosa'], species_conquests['budino Jumbo']),
            new_fiend('Elemento rosso', zones['via micorocciosa'], species_conquests['elemento Nega']),
            new_fiend('Ramashut', zones['via micorocciosa'], species_conquests['fefnil']),
            new_fiend('Fungongo', zones['via micorocciosa'], species_conquests['sonnellino']),
            new_fiend('Garuda', zones['via micorocciosa']),

            new_fiend('Garm', zones['via djose'], species_conquests['fenril']),
            new_fiend('Simurgh', zones['via djose'], species_conquests['pterix']),
            new_fiend('Lesmathor', zones['via djose'], species_conquests['honet']),
            new_fiend('Budino di neve', zones['via djose'], species_conquests['budino Jumbo']),
            new_fiend('Bunyips', zones['via djose'], species_conquests['tanket']),
            new_fiend('Basilisk', zones['via djose']),
            new_fiend('Ochu', zones['via djose']),

            new_fiend('Meryujin', zones['piana dei lampi'], species_conquests['ornitorestes']),
            new_fiend('Aroj', zones['piana dei lampi'], species_conquests['vizalsha']),
            new_fiend('Buel', zones['piana dei lampi'], species_conquests['unioculum']),
            new_fiend('Elemento dorato', zones['piana dei lampi'], species_conquests['elemento Nega']),
            new_fiend('Kusarik', zones['piana dei lampi'], species_conquests['fefnil']),
            new_fiend('Larva', zones['piana dei lampi']),
            new_fiend('Thytan', zones['piana dei lampi'], species_conquests["clod d'acciaio"]),
            new_fiend('Kyactus?', zones['piana dei lampi']),

            new_fiend('Lupo delle nevi', zones['macalania'], species_conquests['fenril']),
            new_fiend('Shumelke', zones['macalania']),
            new_fiend('Vespa', zones['macalania'], species_conquests['honet']),
            new_fiend('Occhio diabolico', zones['macalania'], species_conquests['unioculum']),
            new_fiend('Budino di Ghiaccio', zones['macalania'], species_conquests['budino Jumbo']),
            new_fiend('Elemento Blu', zones['macalania'], species_conquests['elemento Nega']),
            new_fiend('Mulfus', zones['macalania'], species_conquests['tanket']),
            new_fiend('Mafut', zones['macalania'], species_conquests['tanket']),
            new_fiend('Kushipos', zones['macalania']),
            new_fiend('Chimera', zones['macalania']),

            new_fiend('Lupo del deserto', zones['bikanel'], species_conquests['fenril']),
            new_fiend('Alcione', zones['bikanel'], species_conquests['pterix']),
            new_fiend('Mushuhushu', zones['bikanel'], species_conquests['fefnil']),
            new_fiend('Zuu', zones['bikanel']),
            new_fiend('Anellidus', zones['bikanel']),
            new_fiend('Kyactus', zones['bikanel']),

            new_fiend('Scoor', zones['piana della bonaccia'], species_conquests['fenril']),
            new_fiend('Nebiros', zones['piana della bonaccia'], species_conquests['honet']),
            new_fiend('Budino di fiamme', zones['piana della bonaccia'], species_conquests['budino Jumbo']),
            new_fiend('Shred', zones['piana della bonaccia'], species_conquests['tanket']),
            new_fiend('Anacondar', zones['piana della bonaccia']),
            new_fiend('Hoga', zones['piana della bonaccia']),
            new_fiend('Iaguaro', zones['piana della bonaccia']),
            new_fiend('Chimera Brain', zones['piana della bonaccia']),
            new_fiend('Molboro', zones['piana della bonaccia']),

            new_fiend('Yowie', zones['grotta del crepaccio'], species_conquests['ornitorestes']),
            new_fiend('Galkimasela', zones['grotta del crepaccio'], species_conquests['vizalsha']),
            new_fiend('Elemento scuro', zones['grotta del crepaccio'], species_conquests['elemento Nega']),
            new_fiend('Heg', zones['grotta del crepaccio'], species_conquests['fefnil']),
            new_fiend('Son', zones['grotta del crepaccio'], species_conquests['sonnellino']),
            new_fiend('Varaha', zones['grotta del crepaccio'], species_conquests['juggernaut']),
            new_fiend('Epej', zones['grotta del crepaccio']),
            new_fiend('Fantasma', zones['grotta del crepaccio']),
            new_fiend('Tomberry', zones['grotta del crepaccio']),

            new_fiend('Mal Bernardo', zones['monte gagazet'], species_conquests['fenril']),
            new_fiend('Alyman', zones['monte gagazet'], species_conquests['unioculum']),
            new_fiend('Budino oscuro', zones['monte gagazet'], species_conquests['budino Jumbo']),
            new_fiend('Granad', zones['monte gagazet'], species_conquests['re piros']),
            new_fiend('Grat', zones['monte gagazet']),
            new_fiend('Grendel', zones['monte gagazet'], species_conquests['juggernaut']),
            new_fiend('Ashoor', zones['monte gagazet']),
            new_fiend('Mandragora', zones['monte gagazet']),
            new_fiend('Behemoth', zones['monte gagazet']),
            new_fiend('Splasher', zones['monte gagazet']),
            new_fiend('Aquelous', zones['monte gagazet']),
            new_fiend('Echeneis', zones['monte gagazet']),

            new_fiend('Exoray', zones['dentro sin'], species_conquests['sonnellino']),
            new_fiend('Alyadin', zones['dentro sin']),
            new_fiend('Ultra Might (spada normale)', zones['dentro sin'], species_conquests["clod d'acciaio"]),
            new_fiend('Ultra Might (spada stella)', zones['dentro sin'], species_conquests["clod d'acciaio"]),
            new_fiend('Demomonolix', zones['dentro sin']),
            new_fiend('Molboro il Grande', zones['dentro sin']),
            new_fiend('Barbatos', zones['dentro sin']),
            new_fiend('Adamanthart', zones['dentro sin']),
            new_fiend('King Behemoth', zones['dentro sin']),

            new_fiend('Zauras', zones['rovine di omega'], species_conquests['ornitorestes']),
            new_fiend('Byurobolos', zones['rovine di omega'], species_conquests['re piros']),
            new_fiend('Desflot', zones['rovine di omega'], species_conquests['unioculum']),
            new_fiend('Elemento nero', zones['rovine di omega'], species_conquests['elemento Nega']),
            new_fiend('Haruma', zones['rovine di omega'], species_conquests['tanket']),
            new_fiend('Esprit', zones['rovine di omega']),
            new_fiend('Mechy', zones['rovine di omega']),
            new_fiend('Master Iaguaro', zones['rovine di omega']),
            new_fiend('Mastro Tomberry', zones['rovine di omega']),
            new_fiend('Varna', zones['rovine di omega'])
        ]
        print('OK')

        print("Creazione delle CanBeFound...", end=' ')
        can_be_found_relations = [
            new_can_be_found('budino di tuono', 'via mihen'),

            new_can_be_found('raptor', 'via djose'),
            new_can_be_found('gandharva', 'via djose'),
            new_can_be_found('ramashut', 'via djose'),
            new_can_be_found('fungongo', 'via djose'),

            new_can_be_found('molboro', 'grotta del crepaccio'),
            new_can_be_found('iaguaro', 'grotta del crepaccio'),

            new_can_be_found('galkimasela', 'monte gagazet'),
            new_can_be_found('heg', 'monte gagazet'),

            new_can_be_found('alyman', 'dentro sin'),

            new_can_be_found('molboro il grande', 'rovine di omega'),
            new_can_be_found('demomonolix', 'rovine di omega'),
            new_can_be_found('adamanthart', 'rovine di omega'),
            new_can_be_found('alyadin', 'rovine di omega'),
            new_can_be_found('Ultra Might (spada normale)', 'rovine di omega'),
            new_can_be_found('Ultra Might (spada stella)', 'rovine di omega')
        ]
        print('OK')

        print("Creazione delle Conquest Rewards...", end=' ')
        creation_rewards = [
            new_area_conquest_reward('trusthevis', 'creation', 'filtro energetico', 99),
            new_area_conquest_reward('molboro beta', 'creation', 'zanna velenosa', 99),
            new_area_conquest_reward('kolossos', 'creation', 'fluido vitale', 99),
            new_area_conquest_reward('iaguaro regina', 'creation', 'candela della vita', 99),
            new_area_conquest_reward('yormungand', 'creation', 'granata fossile', 99),
            new_area_conquest_reward('kyactus', 'creation', 'piuma di chocobo', 99),
            new_area_conquest_reward('espada', 'creation', 'eliomagilite', 99),
            new_area_conquest_reward('abyss worm', 'creation', 'neromagilite', 99),
            new_area_conquest_reward('chimera x', 'creation', 'vento d\'oltremondo', 60),
            new_area_conquest_reward('don tomberry', 'creation', 'clessidra d\'argento', 40),
            new_area_conquest_reward('catoblepas', 'creation', 'corona di boccioli', 1),
            new_area_conquest_reward('abadon', 'creation', 'cortina lunare', 99),
            new_area_conquest_reward('vorban', 'creation', 'portafoglio gonfio', 60),

            new_species_conquest_reward('fenril', 'creation', 'coda di chocobo', 99),
            new_species_conquest_reward('ornitorestes', 'creation', 'fluido energetico', 99),
            new_species_conquest_reward('pterix', 'creation', 'megafenice', 99),
            new_species_conquest_reward('honet', 'creation', 'filtro magico', 60),
            new_species_conquest_reward('vizalsha', 'creation', 'fluido magico', 99),
            new_species_conquest_reward('unioculum', 'creation', 'nettare energetico', 60),
            new_species_conquest_reward('budino jumbo', 'creation', 'duostella', 60),
            new_species_conquest_reward('elemento nega', 'creation', 'cortina stellare', 99),
            new_species_conquest_reward('tanket', 'creation', 'clessidra d\'oro', 99),
            new_species_conquest_reward('fefnil', 'creation', 'sale purificatore', 60),
            new_species_conquest_reward('sonnellino', 'creation', 'fluido rigenerante', 99),
            new_species_conquest_reward('re piros', 'creation', 'turboetere', 60),
            new_species_conquest_reward('juggernaut', 'creation', 'cortina luminosa', 60),
            new_species_conquest_reward('clod d\'acciaio', 'creation', 'nettare magico', 90),

            new_original_creation_reward('mangiaterra', 'creation', 'triostella', 60),
            new_original_creation_reward('titanosfera', 'creation', 'examagilite', 60),
            new_original_creation_reward('catastrophe', 'creation', 'porta sul domani', 99),
            new_original_creation_reward('vlakorados', 'creation', 'anima del baro', 60),
            new_original_creation_reward('gasteropodos', 'creation', 'equazione cubica', 99),
            new_original_creation_reward('ultima x', 'creation', 'materioscura', 99),
            new_original_creation_reward('shinryu', 'creation', 'megaelisir', 30),
            new_original_creation_reward('il supremo', 'creation', 'mastersfera', 10)
        ]
        print('OK')

        print("Creazione delle Steal Rewards...", end=' ')
        steal_rewards = [
            new_area_conquest_reward('trusthevis', 'common_steal', 'lacrimogeno', 3),
            new_area_conquest_reward('trusthevis', 'rare_steal', 'filtro energetico', 2),

            new_area_conquest_reward('molboro beta', 'common_steal', 'panacea', 4),
            new_area_conquest_reward('molboro beta', 'rare_steal', 'fluido magico', 2),

            new_area_conquest_reward('kolossos', 'common_steal', 'fluido energetico', 4),
            new_area_conquest_reward('kolossos', 'rare_steal', 'fluido vitale', 2),

            new_area_conquest_reward('iaguaro regina', 'common_steal', 'vento d\'oltremondo', 2),
            new_area_conquest_reward('iaguaro regina', 'rare_steal', 'sacromagilite', 1),

            new_area_conquest_reward('yormungand', 'common_steal', 'granata fossile', 4),
            new_area_conquest_reward('yormungand', 'rare_steal', 'triostella', 1),

            new_area_conquest_reward('kyactus', 'common_steal', 'piuma di chocobo', 2),
            new_area_conquest_reward('kyactus', 'rare_steal', 'portafoglio gonfio', 1),

            new_area_conquest_reward('espada', 'common_steal', 'ombra d\'oltremondo', 4),
            new_area_conquest_reward('espada', 'rare_steal', 'vento d\'oltremondo', 1),

            new_area_conquest_reward('abyss worm', 'common_steal', 'neromagilite', 4),
            new_area_conquest_reward('abyss worm', 'rare_steal', 'nettare energetico', 1),

            new_area_conquest_reward('chimera x', 'common_steal', 'filtro magico', 2),
            new_area_conquest_reward('chimera x', 'rare_steal', 'fluido energetico', 2),

            new_area_conquest_reward('don tomberry', 'common_steal', 'candela della vita', 2),
            new_area_conquest_reward('don tomberry', 'rare_steal', 'portafoglio gonfio', 1),

            new_area_conquest_reward('catoblepas', 'common_steal', 'fluido rigenerante', 3),
            new_area_conquest_reward('catoblepas', 'rare_steal', 'filtro energetico', 1),

            new_area_conquest_reward('abadon', 'common_steal', 'sale purificatore', 3),
            new_area_conquest_reward('abadon', 'rare_steal', 'eliomagilite', 1),

            new_area_conquest_reward('vorban', 'common_steal', 'fluido rigenerante', 2),
            new_area_conquest_reward('vorban', 'rare_steal', 'nettare energetico', 1),

            new_species_conquest_reward('fenril', 'common_steal', 'coda di chocobo', 2),
            new_species_conquest_reward('fenril', 'rare_steal', 'piuma di chocobo', 1),

            new_species_conquest_reward('ornitorestes', 'common_steal', 'carta d\'identità', 1),
            new_species_conquest_reward('ornitorestes', 'rare_steal', 'piuma di chocobo', 1),

            new_species_conquest_reward('pterix', 'common_steal', 'lacrimogeno', 4),
            new_species_conquest_reward('pterix', 'rare_steal', 'candela della vita', 1),

            new_species_conquest_reward('honet', 'common_steal', 'zanna velenosa', 4),
            new_species_conquest_reward('honet', 'rare_steal', 'sale purificatore', 2),

            new_species_conquest_reward('vizalsha', 'common_steal', 'elettromagilite', 4),
            new_species_conquest_reward('vizalsha', 'rare_steal', 'filtro magico', 1),

            new_species_conquest_reward('unioculum', 'common_steal', 'cortina lunare', 3),
            new_species_conquest_reward('unioculum', 'rare_steal', 'sacromagilite', 1),

            new_species_conquest_reward('budino jumbo', 'common_steal', 'cortina lunare', 4),
            new_species_conquest_reward('budino jumbo', 'rare_steal', 'nettare magico', 1),

            new_species_conquest_reward('elemento nega', 'common_steal', 'cortina lunare', 4),
            new_species_conquest_reward('elemento nega', 'rare_steal', 'duostella', 1),

            new_species_conquest_reward('tanket', 'common_steal', 'cortina luminosa', 4),
            new_species_conquest_reward('tanket', 'rare_steal', 'cortina lunare', 4),

            new_species_conquest_reward('fefnil', 'common_steal', 'clessidra d\'oro', 2),
            new_species_conquest_reward('fefnil', 'rare_steal', 'fluido energetico', 2),

            new_species_conquest_reward('sonnellino', 'common_steal', 'zanna velenosa', 4),
            new_species_conquest_reward('sonnellino', 'rare_steal', 'vento d\'oltremondo', 1),

            new_species_conquest_reward('re piros', 'common_steal', 'magmagilite', 4),
            new_species_conquest_reward('re piros', 'rare_steal', 'eliomagilite', 1),

            new_species_conquest_reward('juggernaut', 'common_steal', 'cortina lunare', 4),
            new_species_conquest_reward('juggernaut', 'rare_steal', 'eliomagilite', 1),

            new_species_conquest_reward('clod d\'acciaio', 'common_steal', 'cortina luminosa', 4),
            new_species_conquest_reward('clod d\'acciaio', 'rare_steal', 'nettare energetico', 1),

            new_original_creation_reward('mangiaterra', 'rare_steal', 'passosfera lv 1', 1),
            new_original_creation_reward('titanosfera', 'rare_steal', 'gamberosfera', 1),
            new_original_creation_reward('catastrophe', 'rare_steal', 'passosfera lv 2', 1),
            new_original_creation_reward('vlakorados', 'rare_steal', 'telesfera', 1),
            new_original_creation_reward('gasteropodos', 'rare_steal', 'empatosfera', 1),
            new_original_creation_reward('ultima x', 'rare_steal', 'passosfera lv 3', 1),
            new_original_creation_reward('shinryu', 'rare_steal', 'triostella', 1),
            new_original_creation_reward('il supremo', 'common_steal', 'passosfera lv 4', 1),
            new_original_creation_reward('il supremo', 'rare_steal', 'onnisfera', 1)
        ]
        print('OK')

        print("Creazione delle Battle Rewards...", end=' ')
        battle_rewards = [
            # Area Conquests
            new_area_conquest_reward('trusthevis', 'battle', 'amuleto', 2),
            new_area_conquest_reward('molboro beta', 'battle', 'filtro magico', 2),
            new_area_conquest_reward('kolossos', 'battle', 'fluido rigenerante', 20),
            new_area_conquest_reward('iaguaro regina', 'battle', 'eliomagilite', 3),
            new_area_conquest_reward('yormungand', 'battle', 'examagilite', 2),
            new_area_conquest_reward('kyactus', 'battle', 'sacromagilite', 3),
            new_area_conquest_reward('espada', 'battle', 'carta d\'identità', 1),
            new_area_conquest_reward('abyss worm', 'battle', 'filtro energetico', 1),
            new_area_conquest_reward('chimera x', 'battle', 'gamberosfera', 1),
            new_area_conquest_reward('don tomberry', 'battle', 'vento d\'oltremondo', 3),
            new_area_conquest_reward('catoblepas', 'battle', 'triostella', 1),
            new_area_conquest_reward('abadon', 'battle', 'nettare magico', 1),
            new_area_conquest_reward('vorban', 'battle', 'empatosfera', 1),

            # Species Conquests
            new_species_conquest_reward('fenril', 'battle', 'rapidosfera', 1),
            new_species_conquest_reward('ornitorestes', 'battle', 'anima del baro', 2),
            new_species_conquest_reward('pterix', 'battle', 'destrosfera', 1),
            new_species_conquest_reward('honet', 'battle', 'mirasfera', 1),
            new_species_conquest_reward('vizalsha', 'battle', 'emmepisfera', 1),
            new_species_conquest_reward('unioculum', 'battle', 'difesfera mag', 1),
            new_species_conquest_reward('budino jumbo', 'battle', 'potesfera mag', 1),
            new_species_conquest_reward('elemento nega', 'battle', 'duostella', 2),
            new_species_conquest_reward('tanket', 'battle', 'difesfera fis', 1),
            new_species_conquest_reward('fefnil', 'battle', 'cortina luminosa', 20),
            new_species_conquest_reward('sonnellino', 'battle', 'telesfera', 1),
            new_species_conquest_reward('re piros', 'battle', 'porta sul domani', 1),
            new_species_conquest_reward('juggernaut', 'battle', 'potesfera fis', 1),
            new_species_conquest_reward('clod d\'acciaio', 'battle', 'accapisfera', 1),

            # Original Creations (Prototipi Zoolab)
            new_original_creation_reward('mangiaterra', 'battle', 'fatosfera', 1),
            new_original_creation_reward('titanosfera', 'battle', 'fortunosfera', 1),
            new_original_creation_reward('catastrophe', 'battle', 'portafoglio gonfio', 1),
            new_original_creation_reward('vlakorados', 'battle', 'controchiave', 1),
            new_original_creation_reward('gasteropodos', 'battle', 'pendulum', 1),
            new_original_creation_reward('ultima x', 'battle', 'equazione cubica', 1),
            new_original_creation_reward('shinryu', 'battle', 'ali x l\'ignoto', 1),
            new_original_creation_reward('il supremo', 'battle', 'onnisfera', 1)
        ]
        print('OK')

        print("Creazione delle Stats...", end=' ')
        stats = [
            new_stat("trusthevis", hp=320_000, mp=115, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),
            new_stat("molboro beta", hp=640_000, mp=200, guil=0, ap=8_000, ap_overkill=8_000, overkill=12_000),
            new_stat("kolossos", hp=440_000, mp=20, guil=0, ap=8_000, ap_overkill=8_000, overkill=15_000),
            new_stat("iaguaro regina", hp=380_000, mp=80, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),
            new_stat("yormungand", hp=520_000, mp=63, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),
            new_stat("kyactus", hp=100_000, mp=0, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),
            new_stat("espada", hp=280_000, mp=120, guil=0, ap=8_000, ap_overkill=8_000, overkill=15_000),
            new_stat("abyss worm", hp=480_000, mp=200, guil=0, ap=8_000, ap_overkill=8_000, overkill=12_000),
            new_stat("chimera x", hp=120_000, mp=30, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),
            new_stat("don tomberry", hp=480_000, mp=120, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),
            new_stat("catoblepas", hp=550_000, mp=160, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),
            new_stat("abadon", hp=380_000, mp=780, guil=0, ap=8_000, ap_overkill=16_000, overkill=10_000),
            new_stat("vorban", hp=630_000, mp=120, guil=0, ap=8_000, ap_overkill=8_000, overkill=10_000),

            new_stat("fenril", hp=850_000, mp=300, guil=0, ap=10_000, ap_overkill=10_000, overkill=99_999),
            new_stat("ornitorestes", hp=800_000, mp=300, guil=0, ap=10_000, ap_overkill=10_000, overkill=99_999),
            new_stat("pterix", hp=100_000, mp=0, guil=0, ap=10_000, ap_overkill=10_000, overkill=99_999),
            new_stat("honet", hp=620_000, mp=180, guil=0, ap=10_000, ap_overkill=10_000, overkill=50_000),
            new_stat("vizalsha", hp=95_000, mp=840, guil=0, ap=10_000, ap_overkill=10_000, overkill=10_000),
            new_stat("unioculum", hp=150_000, mp=270, guil=0, ap=10_000, ap_overkill=10_000, overkill=15_000),
            new_stat("budino jumbo", hp=1_300_000, mp=999, guil=0, ap=10_000, ap_overkill=10_000, overkill=99_999),
            new_stat("elemento nega", hp=1_300_000, mp=999, guil=0, ap=10_000, ap_overkill=10_000, overkill=15_000),
            new_stat("tanket", hp=900_000, mp=0, guil=0, ap=10_000, ap_overkill=10_000, overkill=10_000),
            new_stat("fefnil", hp=1_100_000, mp=30, guil=0, ap=10_000, ap_overkill=10_000, overkill=13_000),
            new_stat("sonnellino", hp=98_000, mp=820, guil=0, ap=10_000, ap_overkill=10_000, overkill=10_000),
            new_stat("re piros", hp=480_000, mp=780, guil=0, ap=10_000, ap_overkill=10_000, overkill=10_000),
            new_stat("juggernaut", hp=1_200_000, mp=20, guil=0, ap=8_000, ap_overkill=10_000, overkill=15_000),
            new_stat("clod d'acciaio", hp=2_000_000, mp=0, guil=0, ap=10_000, ap_overkill=10_000, overkill=99_999),

            new_stat("mangiaterra", hp=1_300_000, mp=30, guil=0, ap=50_000, ap_overkill=50_000, overkill=99_999),
            new_stat("titanosfera", hp=1_500_000, mp=999, guil=0, ap=50_000, ap_overkill=50_000, overkill=99_999),
            new_stat("catastrophe", hp=2_200_000, mp=380, guil=0, ap=50_000, ap_overkill=50_000, overkill=99_999),
            new_stat("vlakorados", hp=3_000_000, mp=85, guil=0, ap=50_000, ap_overkill=50_000, overkill=99_999),
            new_stat("gasteropodos", hp=4_000_000, mp=999, guil=0, ap=50_000, ap_overkill=50_000, overkill=12_000),
            new_stat("ultima x", hp=5_000_000, mp=140, guil=0, ap=50_000, ap_overkill=50_000, overkill=99_999),
            new_stat("shinryu", hp=2_000_000, mp=72, guil=0, ap=50_000, ap_overkill=50_000, overkill=99_999),
            new_stat("il supremo", hp=10_000_000, mp=9_999, guil=0, ap=55_000, ap_overkill=55_000, overkill=99_999)
        ]
        print('OK')

        print("Creazione delle associazioni delle stats...", end=' ')
        stats_associations = [
            new_area_conquest_stats('trusthevis'),
            new_area_conquest_stats('molboro beta'),
            new_area_conquest_stats('kolossos'),
            new_area_conquest_stats('iaguaro regina'),
            new_area_conquest_stats('yormungand'),
            new_area_conquest_stats('kyactus'),
            new_area_conquest_stats('espada'),
            new_area_conquest_stats('abyss worm'),
            new_area_conquest_stats('chimera x'),
            new_area_conquest_stats('don tomberry'),
            new_area_conquest_stats('catoblepas'),
            new_area_conquest_stats('abadon'),
            new_area_conquest_stats('vorban'),

            new_species_conquest_stats('fenril'),
            new_species_conquest_stats('ornitorestes'),
            new_species_conquest_stats('pterix'),
            new_species_conquest_stats('honet'),
            new_species_conquest_stats('vizalsha'),
            new_species_conquest_stats('unioculum'),
            new_species_conquest_stats('budino jumbo'),
            new_species_conquest_stats('elemento nega'),
            new_species_conquest_stats('tanket'),
            new_species_conquest_stats('fefnil'),
            new_species_conquest_stats('sonnellino'),
            new_species_conquest_stats('re piros'),
            new_species_conquest_stats('juggernaut'),
            new_species_conquest_stats('clod d\'acciaio'),

            new_original_creation_stats('mangiaterra'),
            new_original_creation_stats('titanosfera'),
            new_original_creation_stats('catastrophe'),
            new_original_creation_stats('vlakorados'),
            new_original_creation_stats('gasteropodos'),
            new_original_creation_stats('ultima x'),
            new_original_creation_stats('shinryu'),
            new_original_creation_stats('il supremo')
        ]
        print('OK')

        db.commit()
        print("\nDati inseriti con successo.\n")

    except SQLAlchemyError as e:
        # Effettua un rollback della sessione
        db.rollback()

        # Stampa il traceback completo
        print("Errore durante l'inserimento dei dati: ")
        print(traceback.format_exc())

        # Messaggio specifico sull'errore catturato
        print(f"Errore SQLAlchemy: {str(e)}")
    except Exception as e:
        db.rollback()
        print(f"Errore generico durante l'inserimento dei dati: {e}")
        print(traceback.format_exc())
    finally:
        db.close()


if __name__ == "__main__":
    populate_data()
