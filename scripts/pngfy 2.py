import sys
from PIL import Image
import os

def convert_images(image_paths, output_format):
    for image_path in image_paths:
        # Verifica se il file esiste
        if not os.path.isfile(image_path):
            print(f"Il file {image_path} non esiste. Saltato.")
            continue

        # Apri l'immagine
        with Image.open(image_path) as img:
            # Genera il percorso di output con il nuovo formato
            base, _ = os.path.splitext(image_path)
            output_path = f"{base}.{output_format.lower()}"

            # Converte e salva l'immagine nel formato specificato
            img.convert("RGB").save(output_path, format=output_format.upper())
            print(f"Immagine {image_path} convertita in {output_path}")


if __name__ == "__main__":
    # Verifica che ci siano abbastanza argomenti
    if len(sys.argv) < 3:
        print("Uso corretto: python3 convert_images.py <immagine1> <immagine2> ...")
        sys.exit(1)

    # Leggi il formato di output e le immagini
    output_format = 'png'
    image_paths = sys.argv[1:]

    # Esegui la conversione
    convert_images(image_paths, output_format)
