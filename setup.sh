#!/bin/bash

set -e  # Interrompi lo script se un comando fallisce

echo "Configurazione dell'ambiente virtuale per il backend..."
python3 -m venv backend/venv
source backend/venv/bin/activate

echo "Aggiornamento di pip..."
pip install --upgrade pip

echo "Installazione delle dipendenze per il backend..."
pip install -r backend/requirements.txt

echo "Configurazione del database PostgreSQL..."
DB_NAME="zoolab"
DB_USER="mr.anderson2159"  # Sostituisci con il tuo nome utente
# DB_PASSWORD="password"  # Imposta una password corretta o richiedi input

# Controlla se il database esiste già
if psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Il database $DB_NAME esiste già, salto la creazione."
else
    echo "Creazione del database $DB_NAME..."
    createdb -U "$DB_USER" "$DB_NAME"
fi

echo "Eseguo le migrazioni (se presenti)..."
# Qui potresti aggiungere comandi per le migrazioni del database, se usi Alembic o Django Migrations
# esempio: alembic upgrade head

echo "Popolamento dei dati iniziali nel database..."
python3 -m app.populate_data

echo "Applicazione delle correzioni al database..."
psql -U postgres -d zoolab -f backend/sql_scripts/correzione_ordinamento_zone.sql

# Configura il PYTHONPATH
export PYTHONPATH="$PYTHONPATH:/path/to/zoolab"

echo "Installazione delle dipendenze per il frontend..."
cd zoolab-frontend
npm install

echo "Configurazione completata! Per avviare il backend, esegui:"
echo "source backend/venv/bin/activate && uvicorn app.main:app --reload"

echo "Per avviare il frontend, esegui:"
echo "cd zoolab-frontend && npm start"
