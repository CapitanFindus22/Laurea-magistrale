import cv2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path_imm = BASE_DIR / "Ridimensionate"

BLUR_THRESHOLD = 300
DELETE_BLURRY = True

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def blur_score(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def analyze_folder(folder_path):

    total_images = blurry_images = deleted_images = 0

    min_resolution = None
    max_resolution = None

    if not folder_path.exists():
        print(f"Cartella non trovata: {folder_path}")
        return

    for f in folder_path.iterdir():

        if f.suffix.lower() not in VALID_EXTENSIONS:
            continue

        img = cv2.imread(str(f))

        if img is None:
            print(f"Errore lettura: {f.name}")
            continue

        height, width = img.shape[:2]
        resolution = (width, height)
        pixels = width * height

        if min_resolution is None or pixels < min_resolution[0] * min_resolution[1]:
            min_resolution = resolution

        if max_resolution is None or pixels > max_resolution[0] * max_resolution[1]:
            max_resolution = resolution

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

    print("\n===== RISULTATI =====\n")
    print(f"Totale immagini : {total_images}")
    print(f"Nitide          : {total_images - blurry_images}")
    print(f"Sfocate         : {blurry_images}")

    if DELETE_BLURRY:
        print(f"Cancellate      : {deleted_images}")

    if total_images > 0:
        print(f"Risoluzione min : {min_resolution[0]}x{min_resolution[1]}")
        print(f"Risoluzione max : {max_resolution[0]}x{max_resolution[1]}")


analyze_folder(path_imm)
