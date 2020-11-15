import cv2
import numpy as np
import os

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


if not(os.path.isdir("glyph")):
    os.makedirs("glyph")
if not (os.path.isdir(f"glyph/cho")):
    os.makedirs(f"glyph/cho")
if not (os.path.isdir(f"glyph/mo")):
    os.makedirs(f"glyph/mo")
if not (os.path.isdir(f"glyph/jong")):
    os.makedirs(f"glyph/jong")

ja = ["ㄱ","ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", 'ㅇ', "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ", "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]
mo = ["ㅏ", 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']

path, dirs, files = next(os.walk("Formalization_image"))
for dir in dirs:
    path, dirs2, files = next(os.walk(f"Formalization_image/{dir}"))
    number = 0
    for file in files:
        ff = np.fromfile(f'Formalization_image/{dir}/{file}', np.uint8)
        img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)

        img_roi = img[10:204, 10:204]  # 공백 지우기
        img = cv2.resize(img, dsize=(85, 85), interpolation=cv2.INTER_AREA)  # 이미지 85*85로 줄이기
        if dir in ja: #이미지가 자음일경우
            imwrite(f"glyph/cho/{number}_{dir}.png",img) #cho 디렉토리 넣기
            imwrite(f"glyph/jong/{number}_{dir}.png",img) #jong 디렉토리 넣기
            number += 1
        if dir in mo:  # 이미지가 모음일경우
            imwrite(f"glyph/mo/{number}_{dir}.png",img) #mo 디렉토리 넣기
            number += 1


