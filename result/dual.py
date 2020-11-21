import os
import cv2
import numpy as np

"""
모음을 결합하여 이중모음 만듦
"""

dual_base = cv2.imread("dual_base.png")  # 224 * 244


def combine(roi, mo):
    mo_gray = cv2.cvtColor(mo, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mo_gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    bg = cv2.bitwise_and(roi, roi, mask=mask)
    fg = cv2.bitwise_and(mo, mo, mask=mask_inv)

    dist = cv2.add(bg, fg)

    return dist


def make_dual_mo(mo_unicode_str, mo1_start, mo2_start):
    '''이중모음 생성'''

    # 이중모음 한글
    mo_name = bytes(
        "\\u" + mo_unicode_str.lower(), "utf8").decode("unicode_escape")

    # 이중모음에 따른 합성 대상 모음 지정
    if mo_name == "ㅒ":
        mo1_name = "ㅑ"
        mo2_name = "ㅣ"
    elif mo_name == "ㅐ":
        mo1_name = "ㅏ"
        mo2_name = "ㅣ"
    elif mo_name == "ㅞ":
        mo1_name = "ㅜ"
        mo2_name = "ㅔ"
    elif mo_name == "ㅘ":
        mo1_name = "ㅗ"
        mo2_name = "ㅏ"
    elif mo_name == "ㅙ":
        mo1_name = "ㅗ"
        mo2_name = "ㅐ"
    elif mo_name == "ㅝ":
        mo1_name = "ㅜ"
        mo2_name = "ㅓ"
    elif mo_name == "ㅚ":
        mo1_name = "ㅗ"
        mo2_name = "ㅣ"
    elif mo_name == "ㅖ":
        mo1_name = "ㅕ"
        mo2_name = "ㅣ"
    elif mo_name == "ㅢ":
        mo1_name = "ㅡ"
        mo2_name = "ㅣ"
    elif mo_name == "ㅔ":
        mo1_name = "ㅓ"
        mo2_name = "ㅣ"
    elif mo_name == "ㅟ":
        mo1_name = "ㅜ"
        mo2_name = "ㅣ"

    mo1_unicode_str = str(mo1_name.encode("unicode_escape")).replace(
        "b'\\\\u", "").replace("'", "").upper()
    mo2_unicode_str = str(mo2_name.encode("unicode_escape")).replace(
        "b'\\\\u", "").replace("'", "").upper()

    mo1_path = f"glyph/mo/{mo1_unicode_str}.png"
    mo2_path = f"glyph/mo/{mo2_unicode_str}.png"

    mo1 = cv2.imread(mo1_path)  # 모음 1 불러오기
    mo1_height, mo1_width, _ = mo1.shape  # 모음 1 픽셀 정보 저장
    mo2 = cv2.imread(mo2_path)  # 모음 2 불러오기
    mo2_height, mo2_width, _ = mo2.shape  # 모음 2 픽셀 정보 저장

    # 모음 합성 시작점 설정
    mo1_height_start = mo1_start[0]
    mo1_width_start = mo1_start[1]
    mo2_height_start = mo2_start[0]
    mo2_width_start = mo2_start[1]

    mo1_roi = dual_base[mo1_height_start:mo1_height_start+mo1_height,
                        mo1_width_start:mo1_width_start+mo1_width]  # 모음 1 합성 영역 지정
    mo1 = combine(mo1_roi, mo1)

    dual_base[mo1_height_start:mo1_height_start+mo1_height,
              mo1_width_start:mo1_width_start+mo1_width] = mo1  # 모음 1 합성

    mo2_roi = dual_base[mo2_height_start:mo2_height_start+mo2_height,
                        mo2_width_start:mo2_width_start+mo2_width]  # 모음 2 합성 영역 지정
    mo2 = combine(mo2_roi, mo2)

    dual_base[mo2_height_start:mo2_height_start+mo2_height,
              mo2_width_start:mo2_width_start+mo2_width] = mo2  # 모음 2 합성

    mo_unicode_str = str(mo_name.encode("unicode_escape")).replace(
        "b'\\\\u", "").replace("'", "").upper()  # 완성된 이중모음의 유니코드 값 (4자리)

    cv2.imwrite(f"glyph/mo/{mo_unicode_str}.png", dual_base)

    dual_base[:, :] = 255  # 베이스 초기화

    print(mo1_name, mo2_name)


make_dual_mo(mo_unicode_str="3152",
             mo1_start=(70, 105), mo2_start=(70, 120))  # ㅒ

make_dual_mo(mo_unicode_str="315F",
             mo1_start=(100, 70), mo2_start=(90, 110))  # ㅟ

make_dual_mo(mo_unicode_str="3150",
             mo1_start=(70, 95), mo2_start=(70, 120))  # ㅐ

make_dual_mo(mo_unicode_str="3158",
             mo1_start=(110, 60), mo2_start=(90, 120))  # ㅘ

make_dual_mo(mo_unicode_str="3154",
             mo1_start=(75, 90), mo2_start=(70, 130))  # ㅔ

make_dual_mo(mo_unicode_str="315D",
             mo1_start=(100, 60), mo2_start=(100, 100))  # ㅝ

make_dual_mo(mo_unicode_str="3156",
             mo1_start=(75, 80), mo2_start=(70, 120))  # ㅖ

make_dual_mo(mo_unicode_str="315A",
             mo1_start=(95, 60), mo2_start=(100, 115))  # ㅚ

make_dual_mo(mo_unicode_str="3162",
             mo1_start=(95, 60), mo2_start=(90, 115))  # ㅢ

make_dual_mo(mo_unicode_str="3159",
             mo1_start=(75, 55), mo2_start=(0, 0))  # ㅙ

make_dual_mo(mo_unicode_str="315E",
             mo1_start=(75, 50), mo2_start=(0, 0))  # ㅞ
