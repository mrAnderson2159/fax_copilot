from typing import Optional, Iterator, Type, Any, Callable
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.sql.elements import BinaryExpression, and_
import logging

# Configura il logger
logger = logging.getLogger(__name__)

class CreationConditions:
    """
    Classe CreationConditions per verificare le condizioni di creazione dei vari campioni di zona,
    campioni di specie e prototipi zoolab, basandosi sulle catture dei mostri nella zona specifica.

    Attributes:
        db (Session): Sessione del database per eseguire query.
        captured_fiends (list[models.Fiend]): Lista di mostri catturati.
        negative_check (bool): Flag per determinare se eseguire la logica di annullamento.
    """

    def __init__(self, db: Session, captured_fiends: list[models.Fiend], negative_check: bool):
        """
        Inizializza un'istanza della classe CreationConditions.

        Args:
            db (Session): Sessione del database per eseguire query.
            captured_fiends (list[models.Fiend]): Lista di mostri catturati.
            negative_check (bool): Flag per determinare se eseguire la logica di annullamento.
        """
        self.db = db
        self.captured_fiends = captured_fiends
        self.negative_check = negative_check
        logger.info(f"Inizializzazione CreationConditions: negative_check={negative_check}, captured_fiends={[fiend.name for fiend in captured_fiends]}")

    def __check_originals(self) -> Optional[list[schemas.OriginalCreationResponse]]:
        """
        Verifica le condizioni di creazione per i prototipi zoolab specifici.

        Returns:
            Una lista di OriginalCreationResponse contenente le informazioni sulle creazioni effettuate.
        """
        logger.info("Inizio verifica dei prototipi zoolab originali")
        check = [
            self.check_mangiaterra(),
            self.check_titanosfera(),
            self.check_catastrophe(),
            self.check_vlakorados(),
            self.check_gasteropodos(),
            self.check_ultima_x(),
            self.check_shinryu()
        ]

        # Restituisce solo i prototipi creati con successo
        check = [el for el in check if el]

        if check:
            logger.info(f"Prototipi zoolab creati: {[creation.name for creation in check]}")
            return check

    def check(self) -> dict:
        """
        Controlla e verifica le condizioni per campioni di area, specie e prototipi zoolab.

        Returns:
            Un dizionario contenente i risultati di ciascun tipo di conquista o creazione.
        """
        logger.info("Inizio verifica delle condizioni di creazione")
        result = {
            "area_conquests": self.check_area_conquest(),
            "species_conquests": self.check_species_conquest(),
            "original_creations": self.__check_originals()
        }
        logger.info(f"Risultato della verifica delle condizioni di creazione: {result}")
        return result

    def __originals_checker(
            self,
            *,
            original_creation_name: str,
            create_condition: bool
    ) -> schemas.OriginalCreationResponse:
        """
        Metodo privato per verificare e gestire la creazione di un prototipo zoolab.

        Args:
            original_creation_name (str): Nome del prototipo da verificare.
            create_condition (bool): Condizione per la creazione.

        Returns:
            Un oggetto OriginalCreationResponse con lo stato di creazione aggiornato.
        """
        logger.info(f"Verifica creazione prototipo: {original_creation_name}, condizione: {create_condition}")
        original_creation = self.db.query(models.OriginalCreation).filter(
            models.OriginalCreation.name == original_creation_name
        ).first()
        if not original_creation.created and create_condition:
            original_creation.created = True
            logger.info(f"Prototipo creato: {original_creation_name}")
            return schemas.OriginalCreationResponse(name=original_creation.name, created=True)
        elif self.negative_check and not create_condition:
            original_creation.created = False
            logger.info(f"Prototipo annullato: {original_creation_name}")
            return schemas.OriginalCreationResponse(name=original_creation.name, created=False)

    def __conquests_checker(
            self,
            *,
            elements_to_check: Any,
            conquest_model: Optional[Type[models.Base]],
            conquest_filter: Callable[[Any], BinaryExpression],
            missing_captures_target: Type[models.Base],
            missing_captures_filter: Callable[[Any, Type[models.Base]], BinaryExpression],
            schema_class: Type[schemas.BaseModel],
    ) -> Optional[list[schemas.BaseModel]]:
        """
        Metodo generico per verificare e gestire la creazione o l'annullamento dei campioni di area e specie.

        Args:
            elements_to_check (Any): Elementi da verificare per la creazione.
            conquest_model (Optional[Type[models.Base]]): Modello di conquista da verificare.
            conquest_filter (Callable[[Any], BinaryExpression]): Filtro per verificare la conquista.
            missing_captures_target (Type[models.Base]): Modello di mostri da verificare per mancanza di catture.
            missing_captures_filter (Callable[[Any, Type[models.Base]], BinaryExpression]): Filtro per le catture mancanti.
            schema_class (Type[schemas.BaseModel]): Classe dello schema di risposta.

        Returns:
            Una lista di conquiste con il loro stato aggiornato.
        """
        results = []

        for element in elements_to_check:
            logger.info(f"Verifica conquista per elemento: {element}")
            # Controlla se la conquista è già stata creata
            conquest = self.db.query(conquest_model).filter(conquest_filter(element)).first()

            if not conquest:
                logger.info(f"Conquista non trovata per elemento: {element}")
                continue

            # Verifica se ci sono mostri che non soddisfano la condizione richiesta
            missing_count = self.db.query(missing_captures_target).filter(
                missing_captures_filter(element, conquest)).count()
            logger.info(f"Numero di mostri mancanti per la conquista {conquest.name}: {missing_count}")

            # Crea o annulla la creazione del campione in base alla condizione e al valore di negative_check
            if missing_count == 0:
                if not conquest.created:
                    conquest.created = True
                    logger.info(f"Conquista creata: {conquest.name}")
                    results.append(schema_class(name=conquest.name, created=True))
            elif self.negative_check and conquest.created:
                conquest.created = False
                logger.info(f"Conquista annullata: {conquest.name}")
                results.append(schema_class(name=conquest.name, created=False))

        if results:
            return results

    def check_area_conquest(self) -> Optional[list[schemas.AreaConquestResponse]]:
        """
        Verifica le condizioni di creazione per i campioni di area.

        Returns:
            Una lista di AreaConquestResponse contenente i campioni di area creati o annullati.
        """
        return self.__conquests_checker(
            elements_to_check={fiend.zone_id for fiend in self.captured_fiends},
            conquest_model=models.AreaConquest,
            conquest_filter=lambda zone_id: models.AreaConquest.zone_id == zone_id,
            missing_captures_target=models.Fiend,
            missing_captures_filter=lambda zone_id, _: and_(models.Fiend.zone_id == zone_id,
                                                            models.Fiend.was_captured == 0),
            schema_class=schemas.AreaConquestResponse
        )

    def check_species_conquest(self) -> Optional[list[schemas.SpeciesConquestResponse]]:
        """
        Verifica le condizioni di creazione per i campioni di specie.

        Returns:
            Una lista di SpeciesConquestResponse contenente i campioni di specie creati o annullati.
        """
        return self.__conquests_checker(
            elements_to_check=self.captured_fiends,
            conquest_model=models.SpeciesConquest,
            conquest_filter=lambda fiend: models.SpeciesConquest.id == fiend.species_conquest_id,
            missing_captures_target=models.Fiend,
            missing_captures_filter=lambda fiend, conquest: and_(
                models.Fiend.species_conquest_id == conquest.id,
                models.Fiend.was_captured < conquest.required_fiends
            ),
            schema_class=schemas.SpeciesConquestResponse
        )

    # Metodi per verificare la creazione di specifici prototipi zoolab
    def check_mangiaterra(self):
        return self.__originals_checker(
            original_creation_name="mangiaterra",
            create_condition=self.db.query(models.AreaConquest).filter(
                models.AreaConquest.created == True
            ).count() >= 2
        )

    def check_titanosfera(self):
        return self.__originals_checker(
            original_creation_name="titanosfera",
            create_condition=self.db.query(models.SpeciesConquest).filter(
                models.SpeciesConquest.created == True
            ).count() >= 2
        )

    def check_catastrophe(self):
        return self.__originals_checker(
            original_creation_name="catastrophe",
            create_condition=self.db.query(models.AreaConquest).filter(
                models.AreaConquest.created == True
            ).count() >= 6
        )

    def check_vlakorados(self):
        return self.__originals_checker(
            original_creation_name="vlakorados",
            create_condition=self.db.query(models.SpeciesConquest).filter(
                models.SpeciesConquest.created == True
            ).count() >= 6
        )

    def check_gasteropodos(self):
        return self.__originals_checker(
            original_creation_name="gasteropodos",
            create_condition=self.db.query(models.AreaConquest).filter(
                models.AreaConquest.created == False
            ).count() == 0
        )

    def check_ultima_x(self):
        return self.__originals_checker(
            original_creation_name="ultima x",
            create_condition=self.db.query(models.Fiend).filter(
                models.Fiend.was_captured < 5
            ).count() == 0
        )

    def check_shinryu(self):
        gagazet_id = self.db.query(models.Zone.id).filter(models.Zone.name == "monte gagazet").scalar()

        return self.__originals_checker(
            original_creation_name="shinryu",
            create_condition=self.db.query(models.Fiend).filter(
                models.Fiend.zone_id == gagazet_id,
                models.Fiend.name.in_(["splasher", "aquelous", "echeneis"]),
                models.Fiend.was_captured < 2
            ).count() == 0
        )

    def check_il_supremo(self):
        """
        Verifica se la creazione "il supremo" può essere sbloccata.
        La condizione è che tutti i mostri siano stati catturati 10 volte,
        e che tutti i campioni di zona, campioni di specie, e prototipi zoolab siano stati sconfitti almeno una volta.

        :return: Un oggetto OriginalCreationResponse se la condizione è soddisfatta.
        """
        il_supremo_id = self.db.query(models.OriginalCreation.id).filter(models.OriginalCreation.name == "il supremo").scalar()

        # Verifica che tutti i mostri siano stati catturati almeno 10 volte
        all_fiends_captured = self.db.query(models.Fiend).filter(
            models.Fiend.was_captured < 10
        ).count() == 0

        # Verifica che tutti i campioni di zona siano stati sconfitti
        all_area_conquests_defeated = self.db.query(models.AreaConquest).filter(
            models.AreaConquest.defeated == False
        ).count() == 0

        # Verifica che tutti i campioni di specie siano stati sconfitti
        all_species_conquests_defeated = self.db.query(models.SpeciesConquest).filter(
            models.SpeciesConquest.defeated == False
        ).count() == 0

        # Verifica che tutti i prototipi zoolab siano stati sconfitti
        all_original_creations_defeated = self.db.query(models.OriginalCreation).filter(
            models.OriginalCreation.defeated == False,
            models.OriginalCreation.id != il_supremo_id
        ).count() == 0

        # La creazione "il supremo" può essere sbloccata solo se tutte le condizioni sono soddisfatte
        create_condition = (
                all_fiends_captured and
                all_area_conquests_defeated and
                all_species_conquests_defeated and
                all_original_creations_defeated
        )

        return self.__originals_checker(
            original_creation_name="il supremo",
            create_condition=create_condition
        )