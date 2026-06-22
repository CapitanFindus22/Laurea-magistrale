import cv2
from pathlib import Path

# Path relativi
BASE_DIR = Path(__file__).resolve().parent
path_imm = BASE_DIR / "Originali"
path_rid = BASE_DIR / "Ridimensionate"

# Crea cartella se non esiste
path_rid.mkdir(exist_ok=True)

# Estensioni valide (Giusto per generalizzare)
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Dimensione target
TARGET_SIZE = (300, 300)

# Percentuale di compressione JPEG (0-100) (95 è praticamente lo standard)
JPEG_QUALITY = 95


# Funz. ridimensionamento
def resize(img):

    # Dimensioni target
    target_w, target_h = TARGET_SIZE

    # Dimensioni originali
    h, w = img.shape[:2]

    # Fattore di scala
    scale = min(target_w / w, target_h / h)

    # Nuove dimensioni mantenendo proporzioni
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Ridimensiona
    resized = cv2.resize(
        img,
        (new_w, new_h),
        interpolation=cv2.INTER_AREA,
    )

    # Calcola delta
    delta_w = target_w - new_w
    delta_h = target_h - new_h

    # Padding
    top = delta_h // 2
    bottom = delta_h - top
    left = delta_w // 2
    right = delta_w - left

    # Aggiungi padding
    return cv2.copyMakeBorder(
        resized, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT
    )


# Funz. principale
def analyze_folder(folder_path):

    total_images = 0
    skipped_small = 0
    skipped_ratio = 0
    saved_images = 0

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

        height, width = img.shape[:2]

        total_images += 1

        # Scarta immagini troppo piccole
        if width < 300 or height < 300:
            skipped_small += 1
            continue

        # Scarta immagini troppo sbilanciate
        ratio = width / height

        if ratio > 2 or ratio < 0.5:
            skipped_ratio += 1
            continue

        # Ridimensiona e salva
        processed = resize(img)

        output_file = path_rid / f"{f.stem}.jpg"

        cv2.imwrite(
            str(output_file),
            processed,
            [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY],
        )

        saved_images += 1

    # Statistiche varie
    print("\n===== RISULTATI =====\n")

    print(f"Totale immagini     : {total_images}")
    print(f"Salvate             : {saved_images}")
    print(f"Scartate            : {skipped_small + skipped_ratio}")


analyze_folder(path_imm)
