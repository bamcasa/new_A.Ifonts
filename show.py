import cv2
import os
import numpy as np


base = np.zeros((300, 2000, 3), dtype= np.uint8)
base[:] = 255  #배열 생성부터 값 넣는 방법을 몰라서....

ja = ["ㄱ","ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", 'ㅇ', "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ", "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]
mo = ["ㅏ", 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']

x = 0
y = 0

for ja_dir in ja:
    if os.path.isdir(f"Classified_image/{ja_dir}"):
        path, dirs, files = next(os.walk(f"Classified_image/{ja_dir}"))
        #print(f'Classified_image/{ja_dir}/{files[1]}')
        ff = np.fromfile(f'Classified_image/{ja_dir}/{files[1]}', np.uint8)
        img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
        height, width, channel = img.shape
        base[y:y+height,x:x+width] = img
        x = x + width + 10
    else:
        print(ja_dir,"이 없음")
        x = x + width + 10
y = y + height + 10
x = 0
for mo_dir in mo:
    if os.path.isdir(f"Classified_image/{mo_dir}"):
        path, dirs, files = next(os.walk(f"Classified_image/{mo_dir}"))
        #print(f'Classified_image/{mo_dir}/{files[1]}')
        ff = np.fromfile(f'Classified_image/{mo_dir}/{files[1]}', np.uint8)
        img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
        height, width, channel = img.shape
        base[y:y + height, x:x + width] = img
        x = x + width + 10
    else:
        print(mo_dir, "이 없음")
        x = x + width + 10

cv2.imshow("img",base)
cv2.waitKey(0)
cv2.destroyAllWindows()
