import cv2
from pathlib import Path

# Path relativi
BASE_DIR = Path(__file__).resolve().parent
path_imm = BASE_DIR / "Ridimensionate"

# Soglia di cancellazione
BLUR_THRESHOLD = 300

# Cancella SI/NO
DELETE_BLURRY = True

# Estensioni valide (Giusto per generalizzare)
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}


# Varianza del Laplaciano
def blur_score(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


# Funz. principale
def analyze_folder(folder_path):

    total_images = blurry_images = deleted_images = 0

    min_resolution = None
    max_resolution = None

    # Controlla se cartella esiste
    if not folder_path.exists():
        print(f"Cartella non trovata: {folder_path}")
        return

    # Analizza ogni file
    for f in folder_path.iterdir():

        # Immagine non supportata?
        if f.suffix.lower() not in VALID_EXTENSIONS:
            continue

        # Apri immagine
        img = cv2.imread(str(f))

        # Errore lettura?
        if img is None:
            print(f"Errore lettura: {f.name}")
            continue

        # Calcola risoluzione
        height, width = img.shape[:2]
        resolution = (width, height)
        pixels = width * height

        # Aggiorna min/max risoluzione
        if min_resolution is None or pixels < min_resolution[0] * min_resolution[1]:
            min_resolution = resolution

        if max_resolution is None or pixels > max_resolution[0] * max_resolution[1]:
            max_resolution = resolution

        # Calcola blur score
        score = blur_score(img)

        total_images += 1

        # Sfocata?
        if score < BLUR_THRESHOLD:
            blurry_images += 1

            # Cancella se richiesto
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

    # Num. cancellate
    if DELETE_BLURRY:
        print(f"Cancellate      : {deleted_images}")

    # Risoluzioni min/max
    if total_images > 0:
        print(f"Risoluzione min : {min_resolution[0]}x{min_resolution[1]}")
        print(f"Risoluzione max : {max_resolution[0]}x{max_resolution[1]}")


analyze_folder(path_imm)
