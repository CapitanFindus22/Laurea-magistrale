import csv
import sys
import cv2
import random
import numpy as np
from pathlib import Path

# Per riproducibilità
random.seed(42)

MAX_IMAGES = 60000

# Path da usare
BASE_DIR = Path(__file__).resolve().parent
path_in = BASE_DIR / "Originali"
path_out = BASE_DIR / "Da usare"

# Per altro dataset
# path_in = BASE_DIR / "Originali1"
# path_out = BASE_DIR / "Da usare1"

# Controlla esistenza cartella di input
if not path_in.exists():
    print(f"Cartella non trovata: {path_in}")
    sys.exit(1)

# Crea cartella di output se non esiste
path_out.mkdir(exist_ok=True)

# Estensioni valide
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Dimensione immagine output (224x224)
TARGET_SIZE = 224

# Percentuale di compressione JPEG (0-100)
JPEG_QUALITY = 95

# Soglia di blur
BLUR_THRESHOLD = 500

# Lista dei "kernel"
kernel = {
    "Box_3": np.ones((3, 3)) / 9,  # Box blur 3x3
    "Box_5": np.ones((5, 5)) / 25,  # Box blur 5x5
    "Gauss_3": np.array(
        [  # Gauss blur 3x3
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1],
        ],
        dtype=np.float32,
    )
    / 16,
    "Gauss_5": np.array(
        [  # Gauss blur 5x5
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1],
        ],
        dtype=np.float32,
    )
    / 256,
    "Circ_5": np.array(
        [  # Circular blur 5x5
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
        ],
        dtype=np.float32,
    )
    / 13,
    "Cross_5": np.array(
        [  # Cross blur 5x5
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ],
        dtype=np.float32,
    )
    / 9,
    "Mot_d": np.array(
        [  # Motion blur diagonale \
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ],
        dtype=np.float32,
    )
    / 5,
    "Mot_h": np.array(
        [  # Motion blur orizzontale -
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        dtype=np.float32,
    )
    / 5,
    "Mot_v": np.array(
        [  # Motion blur verticale |
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ],
        dtype=np.float32,
    )
    / 5,
    "Median_5": None,  # Blur tramite mediana (bonus)
    "Originale": None, # Nessun cambiamento
}

# Controllo kernel
# for name, ker in kernel.items():
#    if ker is not None:
#        print(f"{name:10} -> {ker.sum():.6f}")

# Crea sottocartelle per ogni kernel
for tp in kernel:
    (path_out / tp).mkdir(exist_ok=True)

# Serve per sceglierli casualmente
kernel_items = list(kernel.items())

# Lista dei file immagine ordinati casualmente (sempre per riproducibilità)
files = [f for f in path_in.iterdir() if f.suffix.lower() in VALID_EXTENSIONS]
random.shuffle(files)


# Funzione per calcolare il valore di sfocatura di un'immagine
def blur_score(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()


# Funzione per ritagliare l'immagine (centrandola)
def center_cut(img):
    h, w = img.shape[:2]

    start_x = (w - TARGET_SIZE) // 2
    start_y = (h - TARGET_SIZE) // 2

    return img[
        start_y : start_y + TARGET_SIZE,
        start_x : start_x + TARGET_SIZE,
    ]


# Righe file csv
rows = []

# Contatore immagini
i = 0

# Per ogni immagine scegli un kernel a caso
for f in files:

    # Limite immagini
    if i >= MAX_IMAGES:
        break

    # Leggi immagine in scala di grigi
    img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)

    # Controlla problemi di lettura
    if img is None:
        print(f"Errore lettura: {f.name}")
        continue

    h, w = img.shape[:2]

    # Scarta immagini troppo piccole
    # Il + 10 serve per non predere un eventuale bordo generato dalla convoluzione
    if h < (TARGET_SIZE + 10) or w < (TARGET_SIZE + 10):
        continue

    blur = blur_score(img)

    # Scarta immagini già sfocate in partenza
    if blur < BLUR_THRESHOLD:
        continue

    # Scegli kernel
    tp, ker = random.choice(kernel_items)

    # Applica sfocatura
    if tp == "Originale":
        out = center_cut(img)
    elif tp == "Median_5":
        out = center_cut(cv2.medianBlur(img, 5))
    else:
        out = center_cut(cv2.filter2D(img, -1, ker))

    # Salva specificando il kernel usato
    cv2.imwrite(
        str(path_out / tp / f"{i:06d}_{f.stem}_{tp}.jpg"),
        out,
        [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY],
    )

    i += 1

    # Aggiungi riga al file csv
    rows.append([f.name, tp, blur, blur_score(out)])

# Salva file csv
with open(path_out / "blur_scores.csv", "w", newline="") as fcsv:

    writer = csv.writer(fcsv)

    writer.writerow(["file", "kernel", "blur_score_prima", "blur_score_dopo"])

    writer.writerows(rows)
