import os
import sys
from PIL import Image

def resize_and_convert_to_webp(input_folder, output_folder, size=(200, 200)):
    # Assicurati che la cartella di output esista
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):  # Gestisci più formati di immagini
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # Controlla se l'immagine è già di 200x200 pixel
                if img.size != size:
                    # Ridimensiona l'immagine
                    img_resized = img.resize(size, Image.Resampling.LANCZOS)
                    # Modifica l'estensione del nome file in .webp
                    output_filename = os.path.splitext(filename)[0] + ".webp"
                    output_path = os.path.join(output_folder, output_filename)
                    # Salva l'immagine ridimensionata come WebP
                    img_resized.save(output_path, format='WEBP')
                    print(f"Immagine {filename} ridimensionata e convertita a WebP e salvata in {output_path}")
                else:
                    # Se l'immagine è già 200x200, salvala solo come WebP
                    output_filename = os.path.splitext(filename)[0] + ".webp"
                    output_path = os.path.join(output_folder, output_filename)
                    img.save(output_path, format='WEBP')
                    print(f"Immagine {filename} convertita a WebP e salvata in {output_path}")

def main():
    if len(sys.argv) != 2:
        print("Utilizzo: python script.py <path_to_directory>")
        sys.exit(1)

    input_folder = sys.argv[1]
    if not os.path.exists(input_folder):
        print(f"Errore: La cartella {input_folder} non esiste.")
        sys.exit(1)

    # Creazione del nome della cartella di output
    output_folder = input_folder.rstrip(os.sep) + "_webp"

    # Esegui la funzione di conversione
    resize_and_convert_to_webp(input_folder, output_folder)

if __name__ == "__main__":
    main()
