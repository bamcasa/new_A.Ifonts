import os
import cv2
import numpy as np

"""
추출된 음운들을 결합하여 글자 만듦

>>> doble, triple 함수 사용시 주의 사항
XX_start 인자의 경우 (y좌표, x좌표) 의 형태로 넣어야하며
아래와 같은 좌표평면을 사용합니다.

(0,0)ㅡㅡㅡㅡㅡ (+) x축
|
|
|
|
|
(+)
y축
"""

base = cv2.imread("combine_base.png")  # 224 * 244
dual_base = cv2.imread("dual_base.png")  # 224 * 244


def double(mo_path, mo_start, ja_start):
    '''초성, 중성으로 구성된 음운 생성'''
    ja_dir = "glyph/cho"

    mo_filename = mo_path[-8:]  # 모음 이미지 파일 이름
    mo_unicode_str = mo_filename[:4]  # 모음 유니코드 값 (4자리)
    mo_name = bytes(
        "\\u" + mo_unicode_str.lower(), "utf8").decode("unicode_escape")  # 모음 한글

    ja_list = os.listdir(ja_dir)  # 자음 이미지 목록

    mo = cv2.imread(mo_path)  # 모음 불러오기
    mo_height, mo_width, _ = mo.shape  # 모음 픽셀 정보 저장

    # 모음 합성 시작점 설정
    mo_height_start = mo_start[0]
    mo_width_start = mo_start[1]

    for ja_filename in ja_list:
        ja_unicode_str = ja_filename[:4]  # 자음 유니코드 값 (4자리)
        ja_name = bytes(
            "\\u" + ja_unicode_str.lower(), "utf8").decode("unicode_escape")  # 자음 한글

        base[mo_height_start:mo_height_start+mo_height,
             mo_width_start:mo_width_start+mo_width] = mo  # 모음 합성

        ja = cv2.imread(f"{ja_dir}/{ja_filename}")  # 자음 불러오기
        ja_height, ja_width, _ = ja.shape  # 자음 픽셀 정보 저장

        # 자음 합성 시작점 설정
        ja_height_start = ja_start[0]
        ja_width_start = ja_start[1]

        base[ja_height_start:ja_height_start+ja_height,
             ja_width_start:ja_width_start+ja_width] = ja  # 자음 합성

        glyph_name = chr(get_unicode_int(ja_name, mo_name))
        glyph_unicode_str = str(glyph_name.encode("unicode_escape")).replace(
            "b'\\\\u", "").replace("'", "").upper()  # 완성된 글자의 유니코드 값 (4자리)

        cv2.imwrite(f"save_dir/{glyph_unicode_str}.png", base)

        base[:, :] = 255  # 베이스 초기화


def triple(mo_path, mo_start, ja1_start, ja2_start):
    '''초성, 중성, 종성으로 구성된 음운 생성'''
    ja1_dir = "glyph/cho"
    ja2_dir = "glyph/jong"

    mo_filename = mo_path[-8:]  # 모음 이미지 파일 이름
    mo_unicode_str = mo_filename[:4]  # 모음 유니코드 값 (4자리)
    mo_name = bytes(
        "\\u" + mo_unicode_str.lower(), "utf8").decode("unicode_escape")  # 모음 한글

    ja1_list = os.listdir(ja1_dir)  # 초성 이미지 목록
    ja2_list = os.listdir(ja2_dir)  # 종성 이미지 목록

    mo = cv2.imread(mo_path)  # 모음 불러오기
    mo_height, mo_width, _ = mo.shape  # 모음 픽셀 정보 저장

    # 모음 합성 시작점 설정
    mo_height_start = mo_start[0]
    mo_width_start = mo_start[1]

    for ja1_filename in ja1_list:
        ja1_unicode_str = ja1_filename[:4]  # 초성 유니코드 값 (4자리)
        ja1_name = bytes(
            "\\u" + ja1_unicode_str.lower(), "utf8").decode("unicode_escape")  # 초성 한글

        for ja2_filename in ja2_list:
            ja2_unicode_str = ja2_filename[:4]  # 종성 유니코드 값 (4자리)
            ja2_name = bytes(
                "\\u" + ja2_unicode_str.lower(), "utf8").decode("unicode_escape")  # 종성 한글

            base[mo_height_start:mo_height_start+mo_height,
                 mo_width_start:mo_width_start+mo_width] = mo  # 모음 합성

            ja1 = cv2.imread(f"{ja1_dir}/{ja1_filename}")  # 초성 불러오기
            ja1_height, ja1_width, _ = ja1.shape  # 초성 픽셀 정보 저장

            # 초성 합성 시작점 설정
            ja1_height_start = ja1_start[0]
            ja1_width_start = ja1_start[1]

            base[ja1_height_start:ja1_height_start+ja1_height,
                 ja1_width_start:ja1_width_start+ja1_width] = ja1  # 초성 합성

            '''초성/종성 구분선'''

            ja2 = cv2.imread(f"{ja2_dir}/{ja2_filename}")  # 종성 불러오기
            ja2_height, ja2_width, _ = ja2.shape  # 종성 픽셀 정보 저장

            # 종성 합성 시작점 설정
            ja2_height_start = ja2_start[0]
            ja2_width_start = ja2_start[1]

            base[ja2_height_start:ja2_height_start+ja2_height,
                 ja2_width_start:ja2_width_start+ja2_width] = ja2  # 종성 합성

            glyph_name = chr(get_unicode_int(ja1_name, mo_name, ja2_name))
            glyph_unicode_str = str(glyph_name.encode("unicode_escape")).replace(
                "b'\\\\u", "").replace("'", "").upper()  # 완성된 글자의 유니코드 값 (4자리)

            cv2.imwrite(f"save_dir/{glyph_unicode_str}.png", base)

            base[:, :] = 255  # 베이스 초기화


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

    dual_base[mo1_height_start:mo1_height_start+mo1_height,
              mo1_width_start:mo1_width_start+mo1_width] = mo1  # 모음 1 합성

    dual_base[mo2_height_start:mo2_height_start+mo2_height,
              mo2_width_start:mo2_width_start+mo2_width] = mo2  # 모음 2 합성

    mo_unicode_str = str(mo_name.encode("unicode_escape")).replace(
        "b'\\\\u", "").replace("'", "").upper()  # 완성된 이중모음의 유니코드 값 (4자리)

    cv2.imwrite(f"glyph/mo/{mo_unicode_str}.png", dual_base)

    dual_base[:, :] = 255  # 베이스 초기화


def get_unicode_int(ja1_name, mo_name, ja2_name=""):
    '''글자의 유니코드 정수값 생성'''
    ja1_table = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ",
                 "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

    mo_table = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
                "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]

    ja2_table = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ",
                 "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

    ja1_index = ja1_table.index(ja1_name)
    mo_index = mo_table.index(mo_name)
    ja2_index = ja2_table.index(ja2_name)

    unicode_int = (ja1_index*588 + mo_index*28 + ja2_index) + 44032
    return unicode_int


# make_dual_mo(mo_unicode_str="3152",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅒ

# make_dual_mo(mo_unicode_str="315F",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅟ

# make_dual_mo(mo_unicode_str="3150",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅐ

# make_dual_mo(mo_unicode_str="3158",
#              mo1_start=(110, 60), mo2_start=(90, 120))  # ㅘ

# make_dual_mo(mo_unicode_str="3154",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅔ

# make_dual_mo(mo_unicode_str="315D",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅝ

# make_dual_mo(mo_unicode_str="3156",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅖ

# make_dual_mo(mo_unicode_str="315A",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅚ

# make_dual_mo(mo_unicode_str="3162",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅢ

# make_dual_mo(mo_unicode_str="3159",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅙ

# make_dual_mo(mo_unicode_str="315E",
#              mo1_start=(75, 120), mo2_start=(80, 55))  # ㅞ


''''''

if not os.path.exists("save_dir"):
    os.mkdir("save_dir")

# double(mo_path="glyph/mo/314F.png",
#        mo_start=(75, 120), ja_start=(80, 55))  # ㅏ

# double(mo_path="glyph/mo/3157.png",
#        mo_start=(120, 70), ja_start=(55, 70))  # ㅗ

# double(mo_path="glyph/mo/315C.png",
#        mo_start=(110, 40), ja_start=(40, 70))  # ㅜ

# double(mo_path="glyph/mo/3154.png",
#        mo_start=(63, 110), ja_start=(80, 40))  # ㅓ

# double(mo_path="glyph/mo/315B.png",
#        mo_start=(120, 65), ja_start=(50, 85))  # ㅛ

# double(mo_path="glyph/mo/3160.png",
#        mo_start=(125, 65), ja_start=(35, 85))  # ㅠ

# double(mo_path="glyph/mo/3151.png",
#        mo_start=(50, 120), ja_start=(55, 50))  # ㅑ

# double(mo_path="glyph/mo/3155.png",
#        mo_start=(50, 120), ja_start=(75, 50))  # ㅕ

# double(mo_path="glyph/mo/3163.png",
#        mo_start=(50, 145), ja_start=(75, 50))  # ㅣ

# double(mo_path="glyph/mo/3161.png",
#        mo_start=(160, 60), ja_start=(75, 75))  # ㅡ

# double(mo_path="glyph/mo/3152.png",
#        mo_start=(40, 130), ja_start=(65, 60))  # ㅒ

# double(mo_path="glyph/mo/3150.png",
#        mo_start=(40, 130), ja_start=(65, 55))  # ㅐ

# double(mo_path="glyph/mo/315E.png",
#        mo_start=(80, 40), ja_start=(35, 55))  # ㅞ

# double(mo_path="glyph/mo/3158.png",
#        mo_start=(80, 50), ja_start=(35, 65))  # ㅘ

# double(mo_path="glyph/mo/3159.png",
#        mo_start=(80, 40), ja_start=(45, 55))  # ㅙ

# double(mo_path="glyph/mo/315D.png",
#        mo_start=(80, 60), ja_start=(45, 75))  # ㅝ

# double(mo_path="glyph/mo/315A.png",
#        mo_start=(80, 50), ja_start=(45, 75))  # ㅚ

# double(mo_path="glyph/mo/3156.png",
#        mo_start=(60, 100), ja_start=(80, 45))  # ㅖ

# double(mo_path="glyph/mo/3162.png",
#        mo_start=(60, 50), ja_start=(40, 60))  # ㅢ

# double(mo_path="glyph/mo/3154.png",
#        mo_start=(53, 110), ja_start=(80, 60)) # ㅔ

# double(mo_path="glyph/mo/315F.png",
#        mo_start=(60, 50), ja_start=(40, 50))  # ㅟ

''''''

# triple(mo_path="glyph/mo/314F.png",
#        mo_start=(40, 115), ja1_start=(30, 50), ja2_start=(119, 80))  # ㅏ

# triple(mo_path="glyph/mo/3157.png",
#        mo_start=(40, 70), ja1_start=(15, 70), ja2_start=(130, 70))  # ㅗ

# triple(mo_path="glyph/mo/315C.png",
#         mo_start=(60, 50), ja1_start=(20, 80), ja2_start=(145, 70))  # ㅜ

# triple(mo_path="glyph/mo/3153.png",
#         mo_start=(45, 110), ja1_start=(40, 60), ja2_start=(129, 80))  # ㅓ

# triple(mo_path="glyph/mo/315B.png",
#         mo_start=(60, 55), ja1_start=(30, 80), ja2_start=(140, 80))  # ㅛ

# triple(mo_path="glyph/mo/3160.png",
#         mo_start=(90, 55), ja1_start=(30, 80), ja2_start=(145, 80))  # ㅠ

# triple(mo_path="glyph/mo/3151.png",
#         mo_start=(30, 130), ja1_start=(50, 60), ja2_start=(125, 70))  # ㅑ

# triple(mo_path="glyph/mo/3155.png",
#         mo_start=(20, 120), ja1_start=(50, 60), ja2_start=(135, 90))  # ㅕ

# triple(mo_path="glyph/mo/3163.png",
#         mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(135, 90))  # ㅣ

# triple(mo_path="glyph/mo/3161.png",
#         mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(135, 90))  # ㅡ

# triple(mo_path="glyph/mo/3152.png",
#         mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(135, 80))  # ㅒ

# triple(mo_path="glyph/mo/3150.png",
#         mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(140, 90))  # ㅐ

# triple(mo_path="glyph/mo/315E.png",
#         mo_start=(50, 50), ja1_start=(25, 70), ja2_start=(145, 90))  # ㅞ

# triple(mo_path="glyph/mo/3158.png",
#         mo_start=(50, 45), ja1_start=(25, 80), ja2_start=(145, 90))  # ㅘ

# triple(mo_path="glyph/mo/3159.png",
#         mo_start=(50, 45), ja1_start=(25, 70), ja2_start=(145, 90))  # ㅙ

# triple(mo_path="glyph/mo/315D.png",
#         mo_start=(50, 45), ja1_start=(25, 70), ja2_start=(145, 90))  # ㅝ

# triple(mo_path="glyph/mo/315A.png",
#         mo_start=(50, 50), ja1_start=(25, 80), ja2_start=(145, 90))  # ㅚ

# triple(mo_path="glyph/mo/3156.png",
#         mo_start=(50, 110), ja1_start=(50, 60), ja2_start=(135, 80))  # ㅖ

# triple(mo_path="glyph/mo/3162.png",
#         mo_start=(40, 50), ja1_start=(30, 70), ja2_start=(145, 70))  # ㅢ

# triple(mo_path="glyph/mo/3154.png",
#        mo_start=(55, 110), ja1_start=(60, 40), ja2_start=(129, 80))  # ㅔ

# triple(mo_path="glyph/mo/315F.png",
#         mo_start=(35, 50), ja1_start=(30, 70), ja2_start=(139, 80))  # ㅟ
