# backend/app/populate_data.py
from app.database import SessionLocal
from app.models import Zone, Fiend, AreaConquest, SpeciesConquest, OriginalCreation, CanBeFound


def lower_case(function):
    def wrapper(name: str, *args, **kwargs):
        return function(name.lower(), *args, **kwargs)

    return wrapper


@lower_case
def new_zone(zone_name: str) -> Zone:
    return Zone(name=zone_name, image_url=f"../images/zones/{zone_name}.png")


@lower_case
def new_fiend(fiend_name: str, zone: Zone, species_conquest: SpeciesConquest = None) -> Fiend:
    return Fiend(name=fiend_name, was_captured=0, zone=zone, species_conquest=species_conquest,
                 image_url=f"../images/fiends/{fiend_name}.png")


@lower_case
def new_area_conquest(fiend_name: str, zone: Zone) -> AreaConquest:
    return AreaConquest(name=fiend_name, zone=zone,
                        image_url=f"../images/area_conquests/{fiend_name}.png")


@lower_case
def new_species_conquest(fiend_name: str, required_fiends: int) -> SpeciesConquest:
    return SpeciesConquest(name=fiend_name, required_fiends=required_fiends,
                           image_url=f"../images/species_conquests/{fiend_name}.png")


@lower_case
def new_original_creation(fiend_name: str, creation_rule: str) -> OriginalCreation:
    return OriginalCreation(name=fiend_name, creation_rule=creation_rule,
                            image_url=f"../images/original_creations/{fiend_name}.png")


@lower_case
def new_can_be_found(fiend_name: str, zone_name: str, db: SessionLocal) -> CanBeFound:
    """
    Crea una relazione CanBeFound per un mostro che può essere trovato in una zona aggiuntiva.

    :param fiend_name: Nome del mostro che può essere trovato in una zona aggiuntiva.
    :param zone_name: Nome della zona aggiuntiva in cui può essere trovato il mostro.
    :param db: Sessione del database per cercare il mostro e la zona.
    :return: Un'istanza di CanBeFound.
    :raises ValueError: Se il mostro o la zona non vengono trovati nel database.
    """
    # Cerca il mostro nel database
    fiend = db.query(Fiend).filter(Fiend.name == fiend_name).first()
    if not fiend:
        raise ValueError(f"Il mostro '{fiend_name}' non è stato trovato nel database.")

    # Cerca la zona nel database
    zone = db.query(Zone).filter(Zone.name == zone_name).first()
    if not zone:
        raise ValueError(f"La zona '{zone_name}' non è stata trovata nel database.")

    return CanBeFound(fiend=fiend, zone=zone)


def populate_data():
    areas = [
        'besaid', 'kilika', 'via mihen', 'via micorocciosa', 'via djose',
        'piana dei lampi', 'macalania', 'bikanel', 'piana della bonaccia',
        'grotta del crepaccio', 'monte gagazet', 'dentro sin', 'rovine di omega'
    ]

    db = SessionLocal()
    try:
        zones = {area: new_zone(area) for area in areas}

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

        fiends = [
            new_fiend('dingo', zones['besaid'], species_conquests['fenril']),
            new_fiend('condor', zones['besaid'], species_conquests['pterix']),
            new_fiend('budino d\'acqua', zones['besaid'], species_conquests['budino Jumbo']),

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
            new_fiend('Kyactus', zones['piana dei lampi']),

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
            new_fiend('Kyactus?', zones['bikanel']),

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

        can_be_found_relations = [
            new_can_be_found('raptor', 'via djose', db),
            new_can_be_found('gandharva', 'via djose', db),
            new_can_be_found('ramashut', 'via djose', db),
            new_can_be_found('fungongo', 'via djose', db),

            new_can_be_found('molboro', 'grotta del crepaccio', db),
            new_can_be_found('iaguaro', 'grotta del crepaccio', db),

            new_can_be_found('galkimasela', 'monte gagazet', db),
            new_can_be_found('heg', 'monte gagazet', db),

            new_can_be_found('alyman', 'dentro sin', db),

            new_can_be_found('molboro il grande', 'rovine di omega', db),
            new_can_be_found('demomonolix', 'rovine di omega', db),
            new_can_be_found('adamanthart', 'rovine di omega', db),
            new_can_be_found('alyadin', 'rovine di omega', db)
        ]

        # Aggiungi al database
        db.add_all(area_conquests)
        db.add_all(species_conquests.all())
        db.add_all(zones.values())
        db.add_all(fiends)
        db.add_all(original_creations)
        db.add_all(can_be_found_relations)
        db.commit()
        print("Dati iniziali inseriti con successo.")
    except Exception as e:
        db.rollback()
        print(f"Errore durante l'inserimento dei dati: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    populate_data()
