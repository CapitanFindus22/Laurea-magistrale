import cv2
from pathlib import Path
from collections import Counter

# Path immagini
BASE_DIR = Path(__file__).resolve().parent
path_out = BASE_DIR / "Originali"

# Valore standard
BLUR_THRESHOLD = 100
DELETE_BLURRY = True

VALID_EXTENSIONS = [".jpg", ".jpeg", ".png"]


# Laplaciano
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


# Funz. principale
def analyze_folder(folder_path, folder_name):

    total_images = 0
    blurry_images = 0
    sharp_images = 0
    deleted_images = 0

    min_resolution = None
    max_resolution = None

    resolution_counter = Counter()

    if not folder_path.exists():
        print(f"Cartella non trovata: {folder_path}")
        return

    files = list(folder_path.iterdir())

    for f in files:

        if f.suffix.lower() not in VALID_EXTENSIONS:
            continue

        img = cv2.imread(str(f))

        if img is None:
            print(f"Errore lettura: {f.name}")
            continue

        # La risoluzione mi serve poi per la cnn
        height, width = img.shape[:2]
        resolution = (width, height)
        resolution_counter[f"{width}x{height}"] += 1

        if min_resolution is None or (width * height) < (
            min_resolution[0] * min_resolution[1]
        ):
            min_resolution = resolution
        if max_resolution is None or (width * height) > (
            max_resolution[0] * max_resolution[1]
        ):
            max_resolution = resolution

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        score = variance_of_laplacian(gray)

        total_images += 1

        if score < BLUR_THRESHOLD:
            blurry_images += 1
            status = "SFOCATA"

            # Cancella se sfocata
            if DELETE_BLURRY:
                try:
                    f.unlink()
                    deleted_images += 1
                    status += " -> CANCELLATA"
                except Exception as e:
                    status += f" -> ERRORE CANCELLAZIONE: {e}"
        else:
            sharp_images += 1
            status = "NITIDA"

        print(f"{f.name:40} | {width}x{height:5} | {score:10.2f} | {status}")

        del img

    # Statistiche varie
    print("\n===== RISULTATI =====\n")
    print(f"Totale immagini : {total_images}")
    print(f"Nitide          : {sharp_images}")
    print(f"Sfocate         : {blurry_images}")

    if DELETE_BLURRY:
        print(f"Cancellate      : {deleted_images}")

    if total_images > 0:
        print(f"Risoluzione min : {min_resolution[0]}x{min_resolution[1]}")
        print(f"Risoluzione max : {max_resolution[0]}x{max_resolution[1]}")

    if resolution_counter:
        print("\nDistribuzione risoluzioni:")
        for res, count in sorted(
            resolution_counter.items(),
            key=lambda x: (int(x[0].split("x")[0]), int(x[0].split("x")[1])),
        ):
            print(f"{res:10} -> {count} immagini")


analyze_folder(path_out, "Originali")
