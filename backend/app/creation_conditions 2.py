from typing import Optional, Iterator, Type, Any, Callable
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.sql.elements import BinaryExpression, and_


class CreationConditions:
    def __init__(self, db: Session, captured_fiends: list[models.Fiend], negative_check: bool):
        self.db = db
        self.captured_fiends = captured_fiends
        self.negative_check = negative_check

    def __check_originals(self):
        check = [
                self.check_mangiaterra(),
                self.check_titanosfera(),
                self.check_catastrophe(),
                self.check_vlakorados(),
                self.check_gasteropodos(),
                self.check_ultima_x(),
                self.check_shinryu()
            ]

        check = [el for el in check if el]

        if check:
            return check

    def check(self) -> dict:
        return {
            "area_conquests": self.check_area_conquest(),
            "species_conquests": self.check_species_conquest(),
            "original_creations": self.__check_originals()
        }

    def __originals_checker(
            self,
            *,
            original_creation_name: str,
            create_condition: bool
    ) -> schemas.OriginalCreationResponse:
        original_creation = self.db.query(models.OriginalCreation).filter(
            models.OriginalCreation.name == original_creation_name
        ).first()
        if not original_creation.created and create_condition:
            original_creation.created = True
            return schemas.OriginalCreationResponse(name=original_creation.name, created=True)
        elif self.negative_check and not create_condition:
            original_creation.created = False
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
        results = []

        for element in elements_to_check:
            # Controlla se la conquista è già stata creata
            conquest = self.db.query(conquest_model).filter(conquest_filter(element)).first()

            if not conquest:
                continue

            # Verifica se ci sono mostri che non soddisfano la condizione richiesta
            missing_count = self.db.query(missing_captures_target).filter(
                missing_captures_filter(element, conquest)).count()

            # Crea o annulla la creazione del campione in base alla condizione e al valore di negative_check
            if missing_count == 0:
                if not conquest.created:
                    conquest.created = True
                    results.append(schema_class(name=conquest.name, created=True))
            elif self.negative_check and conquest.created:
                conquest.created = False
                results.append(schema_class(name=conquest.name, created=False))

        if results:
            return results

    def check_area_conquest(self) -> Optional[list[schemas.AreaConquestResponse]]:
        return self.__conquests_checker(
            elements_to_check={fiend.zone_id for fiend in self.captured_fiends},
            conquest_model=models.AreaConquest,
            conquest_filter=lambda zone_id: models.AreaConquest.zone_id == zone_id,
            missing_captures_target=models.Fiend,
            missing_captures_filter=lambda zone_id, _: and_(models.Fiend.zone_id == zone_id,
                                                            models.Fiend.was_captured == 0),
            schema_class=schemas.AreaConquestResponse
        )

    def check_species_conquest(self):
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
