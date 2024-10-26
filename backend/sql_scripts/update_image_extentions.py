# backend/scripts/update_image_extensions.py
from app.database import SessionLocal
from app.models import Fiend


def update_fiend_image_extensions():
    db = SessionLocal()
    try:
        # Recupera tutti i mostri (fiends) dal database
        fiends = db.query(Fiend).all()

        for fiend in fiends:
            if fiend.image_url.endswith(".png"):
                # Sostituisci l'estensione .png con .webp
                fiend.image_url = fiend.image_url.replace(".png", ".webp")
                print(f"Aggiornato {fiend.name}: {fiend.image_url}")

        # Commit delle modifiche nel database
        db.commit()
        print("Aggiornamento delle estensioni delle immagini completato.")
    except Exception as e:
        db.rollback()
        print(f"Errore durante l'aggiornamento: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    update_fiend_image_extensions()
