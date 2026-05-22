import cv2
import numpy as np
from pathlib import Path
import random

# Path relativi
path_in = Path(__file__).parent / "Originali"
path_out = Path(__file__).parent / "Da usare"
path_in_e = Path(__file__).parent / "Extra/Originali"
path_out_e = Path(__file__).parent / "Extra/Da usare"

# Lista dei kernel
kernel = {
    "Box 3": np.ones((3, 3)) / (3 * 3),  # Box blur 3x3
    "Box 5": np.ones((5, 5)) / (5 * 5),  # Box blur 5x5
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
            [3 / 76, 1 / 76, 4 / 76, 2 / 76, 5 / 76],
            [2 / 76, 6 / 76, 8 / 76, 3 / 76, 1 / 76],
            [5 / 76, 9 / 76, 12 / 76, 7 / 76, 2 / 76],
            [1 / 76, 4 / 76, 7 / 76, 6 / 76, 3 / 76],
            [2 / 76, 3 / 76, 5 / 76, 2 / 76, 1 / 76],
        ],
        dtype=np.float32,
    ),
}

# Per ogni immagine scegli un kernel a caso
for f in path_in.iterdir():
    img = cv2.imread(str(f))
    if img is not None:
        tp, ker = random.choice(list(kernel.items()))
        cv2.imwrite(
            str(path_out / f"{f.stem}_{tp}{f.suffix}"), cv2.filter2D(img, -1, ker)
        )

# Immagini B/N aggiuntive
for f in path_in_e.iterdir():
    img = cv2.imread(str(f))
    if img is not None:
        tp, ker = random.choice(list(kernel.items()))
        cv2.imwrite(
            str(path_out_e / f"{f.stem}_{tp}{f.suffix}"), cv2.filter2D(img, -1, ker)
        )
