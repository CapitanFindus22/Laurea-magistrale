import cv2
from pathlib import Path

# PATH
BASE_DIR = Path(__file__).resolve().parent

path_imm = BASE_DIR / "Originali"
path_rid = BASE_DIR / "Ridimensionate"

path_rid.mkdir(exist_ok=True)

# CONFIG
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}

TARGET_SIZE = (300, 300)

JPEG_QUALITY = 100


def resize(img):

    target_w, target_h = TARGET_SIZE

    h, w = img.shape[:2]

    scale = min(target_w / w, target_h / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(
        img,
        (new_w, new_h),
        interpolation=cv2.INTER_AREA,
    )

    delta_w = target_w - new_w
    delta_h = target_h - new_h

    top = delta_h // 2
    bottom = delta_h - top

    left = delta_w // 2
    right = delta_w - left

    return cv2.copyMakeBorder(
        resized, top, bottom, left, right, borderType=cv2.BORDER_REPLICATE
    )


def analyze_folder(folder_path):

    total_images = 0
    skipped_small = 0
    saved_images = 0

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

        total_images += 1

        # Scarta immagini troppo piccole
        if width < 300 or height < 300:
            skipped_small += 1
            continue

        processed = resize(img)

        output_file = path_rid / f"{f.stem}.jpg"

        cv2.imwrite(
            str(output_file),
            processed,
            [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY],
        )

        saved_images += 1

    # STATISTICHE
    print("\n===== RISULTATI =====\n")

    print(f"Totale immagini     : {total_images}")
    print(f"Salvate             : {saved_images}")
    print(f"Scartate piccole    : {skipped_small}")


analyze_folder(path_imm)
