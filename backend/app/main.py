# backend/app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import zones, fiends, area_conquests, original_creations, species_conquests
from app.config import CORS_ORIGINS

app = FastAPI()

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
