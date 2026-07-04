import cv2
from pathlib import Path

# Path relativi
BASE_DIR = Path(__file__).resolve().parent
path_imm = BASE_DIR / "Ridimensionate"

# Soglia di cancellazione
BLUR_THRESHOLD = 350

# Cancella SI/NO
DELETE_BLURRY = True

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}


# Varianza del Laplaciano
def blur_score(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()


# Funz. principale
def analyze_folder(folder_path):

    total_images = blurry_images = deleted_images = 0

    if not folder_path.exists():
        print(f"Cartella non trovata: {folder_path}")
        return

    # Analizza ogni file
    for f in folder_path.iterdir():

        if f.suffix.lower() not in VALID_EXTENSIONS:
            continue

        img = cv2.imread(str(f))

        if img is None:
            print(f"Errore lettura: {f.name}")
            continue

        # Calcola valore di blur
        score = blur_score(img)

        total_images += 1

        if score < BLUR_THRESHOLD:
            blurry_images += 1

            if DELETE_BLURRY:
                try:
                    f.unlink()
                    deleted_images += 1
                except Exception as e:
                    print(f"Errore cancellazione {f.name}: {e}")

    # Statistiche varie
    print("\n===== RISULTATI =====\n")
    print(f"Totale immagini : {total_images}")
    print(f"Nitide          : {total_images - blurry_images}")
    print(f"Sfocate         : {blurry_images}")

    if DELETE_BLURRY:
        print(f"Cancellate      : {deleted_images}")


analyze_folder(path_imm)
