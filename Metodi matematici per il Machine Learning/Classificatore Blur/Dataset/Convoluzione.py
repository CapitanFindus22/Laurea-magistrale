import cv2
import numpy as np
from pathlib import Path
import random

# Riproducibilità
random.seed(42)

# Path relativi
BASE_DIR = Path(__file__).resolve().parent
path_in = BASE_DIR / "Ridimensionate"
path_out = BASE_DIR / "Da usare"

# Crea cartella se non esiste
path_out.mkdir(exist_ok=True)

# Lista dei kernel
kernel = {
    "Box 3": np.ones((3, 3)) / 9,  # Box blur 3x3
    "Box 5": np.ones((5, 5)) / 25,  # Box blur 5x5
    "Gauss 3": np.array(
        [  # Gauss blur 3x3
            [1 / 16, 2 / 16, 1 / 16],
            [2 / 16, 4 / 16, 2 / 16],
            [1 / 16, 2 / 16, 1 / 16],
        ],
        dtype=np.float32,
    ),
    "Gauss 5": np.array(
        [  # Gauss blur 5x5
            [1 / 256, 4 / 256, 6 / 256, 4 / 256, 1 / 256],
            [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
            [6 / 256, 24 / 256, 36 / 256, 24 / 256, 6 / 256],
            [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
            [1 / 256, 4 / 256, 6 / 256, 4 / 256, 1 / 256],
        ],
        dtype=np.float32,
    ),
    "Circ 5": np.array(
        [  # Circular blur 5x5
            [0, 0, 1 / 13, 0, 0],
            [0, 1 / 13, 1 / 13, 1 / 13, 0],
            [1 / 13, 1 / 13, 1 / 13, 1 / 13, 1 / 13],
            [0, 1 / 13, 1 / 13, 1 / 13, 0],
            [0, 0, 1 / 13, 0, 0],
        ],
        dtype=np.float32,
    ),
    "Kaw 5": np.array(
        [  # Kawase blur 5x5
            [0, 0, 1 / 8, 0, 0],
            [0, 1 / 8, 0, 1 / 8, 0],
            [1 / 8, 0, 0, 0, 1 / 8],
            [0, 1 / 8, 0, 1 / 8, 0],
            [0, 0, 1 / 8, 0, 0],
        ],
        dtype=np.float32,
    ),
    "Mot_d": np.array(
        [  # Motion blur diagonale
            [1 / 5, 0, 0, 0, 0],
            [0, 1 / 5, 0, 0, 0],
            [0, 0, 1 / 5, 0, 0],
            [0, 0, 0, 1 / 5, 0],
            [0, 0, 0, 0, 1 / 5],
        ],
        dtype=np.float32,
    ),
    "Mot_h": np.array(
        [  # Motion blur orizzontale
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        dtype=np.float32,
    ),
    "Mot_v": np.array(
        [  # Motion blur verticale
            [0, 0, 1 / 5, 0, 0],
            [0, 0, 1 / 5, 0, 0],
            [0, 0, 1 / 5, 0, 0],
            [0, 0, 1 / 5, 0, 0],
            [0, 0, 1 / 5, 0, 0],
        ],
        dtype=np.float32,
    ),
    "GPT": np.array(
        [  # Creato da ChatGPT (così sono 10)
            [3 / 104, 1 / 104, 4 / 104, 2 / 104, 5 / 104],
            [2 / 104, 6 / 104, 8 / 104, 3 / 104, 1 / 104],
            [5 / 104, 9 / 104, 12 / 104, 7 / 104, 2 / 104],
            [1 / 104, 4 / 104, 7 / 104, 6 / 104, 3 / 104],
            [2 / 104, 3 / 104, 5 / 104, 2 / 104, 1 / 104],
        ],
        dtype=np.float32,
    ),
}

# Estensioni valide (Giusto per generalizzare)
VALID_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# Crea sottocartelle
for tp in kernel:
    (path_out / tp).mkdir(exist_ok=True)


kernel_items = list(kernel.items())

# Per ogni immagine scegli un kernel a caso
for f in sorted(path_in.iterdir()):

    # Immagine non supportata?
    if f.suffix.lower() not in VALID_EXTENSIONS:
        continue

    # Apri immagine
    img = cv2.imread(str(f))

    # Lettura ok?
    if img is not None:

        # Scegli kernel
        tp, ker = random.choice(kernel_items)

        # Applica convoluzione
        out = cv2.filter2D(img, -1, ker)

        # Salva specificando il kernel usato
        cv2.imwrite(
            str(path_out / tp / f"{f.stem}_{tp}{f.suffix}"),
            out,
        )
