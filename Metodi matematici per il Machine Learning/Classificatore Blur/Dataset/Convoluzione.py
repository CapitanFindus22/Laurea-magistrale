import cv2
import numpy as np
from pathlib import Path
import random

# Riproducibilità
random.seed(42)

MAX_IMAGES = 50000

# Path relativi
BASE_DIR = Path(__file__).resolve().parent
path_in = BASE_DIR / "Ridimensionate"
path_out = BASE_DIR / "Da usare"

path_out.mkdir(exist_ok=True)

# Lista dei kernel
kernel = {
    "Box_3": np.ones((3, 3)) / 9,  # Box blur 3x3
    "Box_5": np.ones((5, 5)) / 25,  # Box blur 5x5
    "Gauss_3": np.array(
        [  # Gauss blur 3x3
            [1 / 16, 2 / 16, 1 / 16],
            [2 / 16, 4 / 16, 2 / 16],
            [1 / 16, 2 / 16, 1 / 16],
        ],
        dtype=np.float32,
    ),
    "Gauss_5": np.array(
        [  # Gauss blur 5x5
            [1 / 256, 4 / 256, 6 / 256, 4 / 256, 1 / 256],
            [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
            [6 / 256, 24 / 256, 36 / 256, 24 / 256, 6 / 256],
            [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
            [1 / 256, 4 / 256, 6 / 256, 4 / 256, 1 / 256],
        ],
        dtype=np.float32,
    ),
    "Circ_5": np.array(
        [  # Circular blur 5x5
            [0, 0, 1 / 13, 0, 0],
            [0, 1 / 13, 1 / 13, 1 / 13, 0],
            [1 / 13, 1 / 13, 1 / 13, 1 / 13, 1 / 13],
            [0, 1 / 13, 1 / 13, 1 / 13, 0],
            [0, 0, 1 / 13, 0, 0],
        ],
        dtype=np.float32,
    ),
    "Kaw_5": np.array(
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
    "Originale": np.array(
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ],
        dtype=np.float32,
    ),
}

VALID_EXTENSIONS = [".jpg", ".jpeg", ".png"]

for tp in kernel:
    (path_out / tp).mkdir(exist_ok=True)

# Per riproducibilità al 100%
kernel_items = list(kernel.items())

files = [f for f in path_in.iterdir() if f.suffix.lower() in VALID_EXTENSIONS]

random.shuffle(files)

files = files[:MAX_IMAGES]

# Per ogni immagine scegli un kernel a caso
for f in files:

    if f.suffix.lower() not in VALID_EXTENSIONS:
        continue

    img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)

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
