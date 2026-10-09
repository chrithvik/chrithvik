"""
Prepare a portrait photo for clean ASCII conversion:
  1. Remove background (rembg)
  2. Boost local contrast with CLAHE
  3. Composite onto pure white

Output: source-prepped.png (grayscale)

    python scripts/prep_photo.py <input.png> [output.png]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

cut = remove(Image.open(INP).convert("RGBA"))
rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8, 8))
subject = alpha > 128
enhanced = clahe.apply(gray)
enhanced = np.where(subject, enhanced, gray)

lo, hi = np.percentile(enhanced[subject], [1, 99])
tone = np.clip((enhanced.astype(np.float32) - lo) / max(hi - lo, 1), 0, 1) * 255

mask = cv2.GaussianBlur(alpha.astype(np.float32) / 255.0, (0, 0), 1.5)
out = tone * mask + 255.0 * (1.0 - mask)

ys, xs = np.where(alpha > 20)
side = max(xs.max() - xs.min(), ys.max() - ys.min()) + 80
cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
canvas = np.full((side, side), 255, np.uint8)
x0, y0 = cx - side // 2, cy - side // 2
sx0, sy0 = max(x0, 0), max(y0, 0)
sx1, sy1 = min(x0 + side, out.shape[1]), min(y0 + side, out.shape[0])
canvas[sy0 - y0 : sy1 - y0, sx0 - x0 : sx1 - x0] = out[sy0:sy1, sx0:sx1].astype(np.uint8)

Image.fromarray(canvas, mode="L").save(OUT)
print("wrote", OUT, canvas.shape)
