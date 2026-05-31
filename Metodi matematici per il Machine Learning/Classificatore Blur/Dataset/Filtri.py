import cv2
import numpy as np

# Da modificare

# ======================================
# Carica immagine
# ======================================
img = cv2.imread("foto.jpg")

if img is None:
    raise FileNotFoundError("Impossibile aprire foto.jpg")

# ======================================
# Scala di grigi
# ======================================
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("output_scala_grigi.jpg", gray)

# ======================================
# Bianco e Nero puro
# ======================================
_, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite("output_bn.jpg", bw)

# ======================================
# Negativo
# ======================================
negative = 255 - img
cv2.imwrite("output_negativo.jpg", negative)

# ======================================
# Seppia
# ======================================
sepia_matrix = np.array([
    [0.272, 0.534, 0.131],
    [0.349, 0.686, 0.168],
    [0.393, 0.769, 0.189]
])

sepia = cv2.transform(img, sepia_matrix)
sepia = np.clip(sepia, 0, 255).astype(np.uint8)

cv2.imwrite("output_seppia.jpg", sepia)

# ======================================
# Monocromatico Blu
# ======================================
mono_blue = np.zeros_like(img)
mono_blue[:, :, 0] = gray
cv2.imwrite("output_monocromo_blu.jpg", mono_blue)

# ======================================
# Monocromatico Rosso
# ======================================
mono_red = np.zeros_like(img)
mono_red[:, :, 2] = gray
cv2.imwrite("output_monocromo_rosso.jpg", mono_red)

# ======================================
# Monocromatico Verde
# ======================================
mono_green = np.zeros_like(img)
mono_green[:, :, 1] = gray
cv2.imwrite("output_monocromo_verde.jpg", mono_green)

# ======================================
# Cianotipo
# ======================================
cyan = np.zeros_like(img)

cyan[:, :, 0] = np.clip(gray * 1.2, 0, 255)
cyan[:, :, 1] = np.clip(gray * 0.8, 0, 255)
cyan[:, :, 2] = np.clip(gray * 0.3, 0, 255)

cv2.imwrite("output_cianotipo.jpg", cyan.astype(np.uint8))

# ======================================
# Duotone Blu-Giallo
# ======================================
gray_norm = gray.astype(np.float32) / 255.0

dark_color = np.array([120, 40, 0], dtype=np.float32)
light_color = np.array([0, 220, 255], dtype=np.float32)

duotone = np.zeros_like(img, dtype=np.float32)

for c in range(3):
    duotone[:, :, c] = (
        dark_color[c] * (1 - gray_norm)
        + light_color[c] * gray_norm
    )

duotone = np.clip(duotone, 0, 255).astype(np.uint8)

cv2.imwrite("output_duotone.jpg", duotone)

# ======================================
# Solarizzazione
# ======================================
solarized = img.copy()

mask = solarized > 128
solarized[mask] = 255 - solarized[mask]

cv2.imwrite("output_solarizzata.jpg", solarized)

# ======================================
# Pastello
# ======================================
pastel = cv2.convertScaleAbs(
    img,
    alpha=0.6,
    beta=40
)

cv2.imwrite("output_pastello.jpg", pastel)

# ======================================
# Vintage anni '70
# ======================================
vintage_matrix = np.array([
    [0.9, 0.5, 0.2],
    [0.3, 0.7, 0.2],
    [0.1, 0.3, 0.5]
])

vintage = cv2.transform(img, vintage_matrix)
vintage = np.clip(vintage, 0, 255).astype(np.uint8)

cv2.imwrite("output_vintage70.jpg", vintage)

# ======================================
# HDR simulato
# ======================================
hdr = cv2.detailEnhance(
    img,
    sigma_s=12,
    sigma_r=0.15
)

cv2.imwrite("output_hdr.jpg", hdr)

# ======================================
# High Key
# ======================================
high_key = cv2.convertScaleAbs(
    img,
    alpha=1.1,
    beta=50
)

cv2.imwrite("output_highkey.jpg", high_key)

# ======================================
# Low Key
# ======================================
low_key = cv2.convertScaleAbs(
    img,
    alpha=0.7,
    beta=-30
)

cv2.imwrite("output_lowkey.jpg", low_key)

# ======================================
# Cinematic Teal & Orange
# ======================================
cinematic = img.astype(np.float32)

cinematic[:, :, 0] *= 1.2
cinematic[:, :, 2] = cinematic[:, :, 2] * 1.1 + 20

cinematic = np.clip(cinematic, 0, 255).astype(np.uint8)

cv2.imwrite("output_cinematic.jpg", cinematic)

print("Tutti i filtri generati con successo.")