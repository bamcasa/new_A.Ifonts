import cv2
import numpy as np
import os


def invisible(directory):
    path, dirs, files = next(os.walk(directory))

    for file in files:
        image_bgr = cv2.imread(f"{directory}/{file}")
        h, w, c = image_bgr.shape
        image_bgra = np.concatenate(
            [image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        white = np.all(image_bgr == [255, 255, 255], axis=-1)
        image_bgra[white, -1] = 0
        cv2.imwrite(f"{directory}/{file}", image_bgra)


invisible("glyph/cho")
invisible("glyph/mo")
invisible("glyph/jong")
