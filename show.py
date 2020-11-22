import cv2
import os
import numpy as np

base = cv2.imread("base.png")
height, width, channel = base.shape
print(channel)
ja = ["ㄱ","ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", 'ㅇ', "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ", "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]
mo = ["ㅏ", 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']

x = 3
y = 55

for ja_dir in ja:
    if os.path.isdir(f"Formalization_image/{ja_dir}"):
        path, dirs, files = next(os.walk(f"Formalization_image/{ja_dir}"))
        max = [0,0]
        for file in files:
            if int(file.split(".")[0]) >= max[0]:
                max[0] = int(file.split(".")[0])
                max[1] = file
        #print(f'Formalization_image/{ja_dir}/{files[0]}')
        ff = np.fromfile(f'Formalization_image/{ja_dir}/{max[1]}', np.uint8)
        img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, dsize=(85, 85), interpolation=cv2.INTER_AREA)
        height, width, channel = img.shape
        base[y:y+height,x:x+width] = img
        x = x + width + 6
    else:
        print(ja_dir,"이 없음")
        x = x + width + 6
y = y + height + 60 + 6
x = 3
for mo_dir in mo:
    if os.path.isdir(f"Formalization_image/{mo_dir}"):
        path, dirs, files = next(os.walk(f"Formalization_image/{mo_dir}"))
        max = [0,0]
        for file in files:
            if int(file.split(".")[0]) >= max[0]:
                max[0] = int(file.split(".")[0])
                max[1] = file
        #print(f'Classified_image/{mo_dir}/{files[1]}')
        ff = np.fromfile(f'Formalization_image/{mo_dir}/{max[1]}', np.uint8)
        img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, dsize=(85, 85), interpolation=cv2.INTER_AREA)
        height, width, channel = img.shape
        base[y:y + height, x:x + width] = img
        x = x + width + 6
    else:
        print(mo_dir, "이 없음")
        x = x + width + 6

cv2.imshow("img",base)
cv2.waitKey(0)
cv2.destroyAllWindows()
