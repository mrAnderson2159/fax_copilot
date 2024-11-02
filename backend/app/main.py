# backend/app/main.py

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import zones, fiends, area_conquests, original_creations, species_conquests
from app.config import CORS_ORIGINS


# Definisce i colori per ciascuna parte del messaggio
RESET = "\x1b[0m"
GREY = "\x1b[38;21m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"
BOLD_RED = "\x1b[31;1m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"

# Definisce il formato del log, aggiungendo colori a ciascuna sezione
log_format = (
    f"{CYAN}%(asctime)s{RESET} - "
    f"{MAGENTA}%(name)s{RESET} - "
    f"{GREEN}%(levelname)s{RESET} - "
    f"{YELLOW}%(message)s{RESET}"
)

DEBUG_MODE = True

if DEBUG_MODE:
    # Configura il logging con il formatter colorato
    logging.basicConfig(
        level=logging.INFO,  # Livello di logging impostato a INFO
        format=log_format,  # Formato del log
    )

logger = logging.getLogger(__name__)
logger.info("Server starting...")

# Configurazione FastAPI
app = FastAPI()

# Routes e altre configurazioni...


# Costruisci il percorso assoluto per la directory delle immagini
images_dir = os.path.join(os.path.dirname(__file__), "..", "images")
if not os.path.exists(images_dir):
    raise RuntimeError(f"La directory '{images_dir}' non esiste.")

# Monta la directory delle immagini per il server
app.mount("/images", StaticFiles(directory=images_dir), name="images")

# Configura il middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(CORS_ORIGINS)

app.include_router(zones.router)
app.include_router(fiends.router)
app.include_router(area_conquests.router)
app.include_router(species_conquests.router)
app.include_router(original_creations.router)


@app.get("/")
def read_root():
    return {"message": "Benvenuti sull'app Zoolab!"}
