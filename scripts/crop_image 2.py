import sys
from PIL import Image
import os

def crop_image(input_path, offset):
    # Apri l'immagine e ottieni le sue dimensioni
    with Image.open(input_path) as img:
        width, height = img.size

        # Controlla se l'immagine è già quadrata
        if width == height:
            print("L'immagine è già quadrata. Nessuna operazione necessaria.")
            return

        # Calcola le coordinate di ritaglio
        if width > height:  # L'immagine è più larga che alta
            if offset >= 0:
                left = offset
            else:
                left = width - height - abs(offset)
            right = left + height
            top = 0
            bottom = height
        else:  # L'immagine è più alta che larga
            if offset >= 0:
                top = offset
            else:
                top = height - width - abs(offset)
            bottom = top + width
            left = 0
            right = width

        # Ritaglia l'immagine
        crop_box = (left, top, right, bottom)
        cropped_img = img.crop(crop_box)

        # Genera il percorso di output con il suffisso "_crop"
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_crop{ext}"

        # Salva l'immagine ritagliata
        cropped_img.save(output_path)
        print(f"Immagine ritagliata salvata in: {output_path}")

if __name__ == "__main__":
    # Verifica che i parametri siano corretti
    if len(sys.argv) != 3:
        print("Uso corretto: python3 crop_image.py <percorso_immagine> <offset>")
        sys.exit(1)

    # Leggi i parametri
    image_path = sys.argv[1]
    try:
        offset = int(sys.argv[2])
    except ValueError:
        print("L'offset deve essere un numero intero.")
        sys.exit(1)

    # Esegui la funzione di ritaglio
    crop_image(image_path, offset)
