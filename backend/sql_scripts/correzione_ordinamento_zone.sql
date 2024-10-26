-- -- Rimozione dei vincoli esistenti
-- ALTER TABLE area_conquests DROP CONSTRAINT IF EXISTS area_conquests_zone_id_fkey;
-- ALTER TABLE fiends DROP CONSTRAINT IF EXISTS fiends_zone_id_fkey;
-- ALTER TABLE fiends DROP CONSTRAINT IF EXISTS fiends_species_conquest_id_fkey;

-- -- Aggiunta dei nuovi vincoli con CASCADE
-- ALTER TABLE area_conquests
-- ADD CONSTRAINT area_conquests_zone_id_fkey
-- FOREIGN KEY (zone_id) REFERENCES zones (id)
-- ON UPDATE CASCADE ON DELETE CASCADE;

-- ALTER TABLE fiends
-- ADD CONSTRAINT fiends_zone_id_fkey
-- FOREIGN KEY (zone_id) REFERENCES zones (id)
-- ON UPDATE CASCADE ON DELETE CASCADE;

-- ALTER TABLE fiends
-- ADD CONSTRAINT fiends_species_conquest_id_fkey
-- FOREIGN KEY (species_conquest_id) REFERENCES species_conquests (id)
-- ON UPDATE CASCADE ON DELETE CASCADE;


-- Cambia temporaneamente gli ID per evitare conflitti
UPDATE zones SET id = id + 100 WHERE id <= 13;

-- Imposta i nuovi ID secondo l'ordine corretto
UPDATE zones SET id = 1 WHERE name = 'besaid';
UPDATE zones SET id = 2 WHERE name = 'kilika';
UPDATE zones SET id = 3 WHERE name = 'via mihen';
UPDATE zones SET id = 4 WHERE name = 'via micorocciosa';
UPDATE zones SET id = 5 WHERE name = 'via djose';
UPDATE zones SET id = 6 WHERE name = 'piana dei lampi';
UPDATE zones SET id = 7 WHERE name = 'macalania';
UPDATE zones SET id = 8 WHERE name = 'bikanel';
UPDATE zones SET id = 9 WHERE name = 'piana della bonaccia';
UPDATE zones SET id = 10 WHERE name = 'grotta del crepaccio';
UPDATE zones SET id = 11 WHERE name = 'monte gagazet';
UPDATE zones SET id = 12 WHERE name = 'dentro sin';
UPDATE zones SET id = 13 WHERE name = 'rovine di omega';
