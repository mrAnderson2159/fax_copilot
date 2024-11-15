# backend/app/config.py
import os


def get_cors_origins():
    mode = os.getenv("ZOO_MODE", "local")
    if mode == "ngrok":
        frontend_url = os.getenv("NGROK_FRONTEND_URL", "")
        if frontend_url:
            return [frontend_url]  # Usa l'URL specifico del frontend su Ngrok
        else:
            raise RuntimeError("NGROK_FRONTEND_URL non è stato impostato correttamente.")
    return ["http://localhost:3000"]  # Modalità locale con React


def get_debug_mode():
    mode = os.getenv("DEBUG_MODE", "false")
    return mode == "true"


def get_db_name():
    return os.getenv("DATABASE", "zoolab")


CORS_ORIGINS = get_cors_origins()
DEBUG_MODE = get_debug_mode()
DATABASE_NAME = get_db_name()
