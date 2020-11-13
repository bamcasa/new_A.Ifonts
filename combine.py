import os
import cv2
import numpy as np

""" * 음운간 거리 지정은 double, triple 함수 실행할 때 ja_start등의 인자에 활용하면 됨
    * base 이미지 크기 바꾸면 png2ttf에서도 변경 필요
    * 파이썬으로 png2ttf를 구현해보려 했으나 이미지 벡터화 라이브러리가 마땅치 않음
    * 현재 코드는 음운의 파일 이름이 3131.png('ㄱ' 유니코드)처럼 음운의 유니코드 값 네 글자로 함
      -> 파일 이름 저장 방식 바뀌더라도 수정 가능 (한글로 저장해도 괜찮지 않을까..)"""

base = cv2.imread("base.png")  # 224 * 244


def double(mo_path, ja_dir, mo_start, ja_start):
    """초성, 중성으로 구성된 음운 생성"""
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

        if not os.path.exists("save_dir"):
            os.mkdir("save_dir")

        glyph_name = chr(get_unicode_int(ja_name, mo_name))
        glyph_unicode_str = str(glyph_name.encode("unicode_escape")).replace(
            "b'\\\\u", "").replace("'", "").upper()  # 완성된 글자의 유니코드 값 (4자리)

        cv2.imwrite(f"save_dir/{glyph_unicode_str}.png", base)

        base[:, :] = 255  # 베이스 초기화


def triple(mo_path, ja1_dir, ja2_dir, mo_start, ja1_start, ja2_start):
    """초성, 중성, 종성으로 구성된 음운 생성"""
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

            if not os.path.exists("save_dir"):
                os.mkdir("save_dir")

            glyph_name = chr(get_unicode_int(ja1_name, mo_name, ja2_name))
            glyph_unicode_str = str(glyph_name.encode("unicode_escape")).replace(
                "b'\\\\u", "").replace("'", "").upper()  # 완성된 글자의 유니코드 값 (4자리)

            cv2.imwrite(f"save_dir/{glyph_unicode_str}.png", base)

            base[:, :] = 255  # 베이스 초기화


def get_unicode_int(ja1_name, mo_name, ja2_name=""):
    """글자의 유니코드 정수값 생성"""
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


# double(mo_path="glyph/mo/314F.png",
#        ja_dir="glyph/cho", mo_start=(75, 110), ja_start=(80, 60)) # ㅏ

# double(mo_path="glyph/mo/3154.png",
#        ja_dir="glyph/cho", mo_start=(53, 110), ja_start=(80, 60)) # ㅔ

# double(mo_path="glyph/mo/3157.png",
#        ja_dir="glyph/cho", mo_start=(110, 70), ja_start=(60, 90))  # ㅗ

# double(mo_path="glyph/mo/315F.png",
#        ja_dir="glyph/cho", mo_start=(60, 50), ja_start=(40, 50))  # ㅟ

# double(mo_path="glyph/mo/3154.png",
#        ja_dir="glyph/cho", mo_start=(63, 110), ja_start=(80, 40))  # ㅓ

# double(mo_path="glyph/mo/315B.png",
#        ja_dir="glyph/cho", mo_start=(120, 65), ja_start=(50, 85))  # ㅛ

# double(mo_path="glyph/mo/3160.png",
#        ja_dir="glyph/cho", mo_start=(125, 65), ja_start=(35, 85))  # ㅠ

# double(mo_path="glyph/mo/3151.png",
#        ja_dir="glyph/cho", mo_start=(50, 120), ja_start=(55, 50))  # ㅑ

# double(mo_path="glyph/mo/3155.png",
#        ja_dir="glyph/cho", mo_start=(50, 120), ja_start=(75, 50))  # ㅕ

# double(mo_path="glyph/mo/3163.png",
#        ja_dir="glyph/cho", mo_start=(50, 145), ja_start=(75, 50))  # ㅣ

# double(mo_path="glyph/mo/3161.png",
#        ja_dir="glyph/cho", mo_start=(160, 60), ja_start=(75, 75))  # ㅡ

# double(mo_path="glyph/mo/3152.png",
#        ja_dir="glyph/cho", mo_start=(40, 130), ja_start=(65, 60))  # ㅒ

# double(mo_path="glyph/mo/3150.png",
#        ja_dir="glyph/cho", mo_start=(40, 130), ja_start=(65, 55))  # ㅐ

# double(mo_path="glyph/mo/315E.png",
#        ja_dir="glyph/cho", mo_start=(80, 40), ja_start=(35, 55))  # ㅞ

# double(mo_path="glyph/mo/3158.png",
#        ja_dir="glyph/cho", mo_start=(80, 50), ja_start=(35, 65))  # ㅘ

# double(mo_path="glyph/mo/3159.png",
#        ja_dir="glyph/cho", mo_start=(80, 40), ja_start=(45, 55))  # ㅙ

# double(mo_path="glyph/mo/315D.png",
#        ja_dir="glyph/cho", mo_start=(80, 60), ja_start=(45, 75))  # ㅝ

# double(mo_path="glyph/mo/315A.png",
#        ja_dir="glyph/cho", mo_start=(80, 50), ja_start=(45, 75))  # ㅚ

# double(mo_path="glyph/mo/3156.png",
#        ja_dir="glyph/cho", mo_start=(60, 100), ja_start=(80, 45))  # ㅖ

# double(mo_path="glyph/mo/315C.png",
#        ja_dir="glyph/cho", mo_start=(110, 40), ja_start=(40, 70))  # ㅜ

# double(mo_path="glyph/mo/3162.png",
#        ja_dir="glyph/cho", mo_start=(60, 50), ja_start=(40, 60))  # ㅢ

''''''

# triple(mo_path="glyph/mo/314F.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(55, 110), ja1_start=(60, 60), ja2_start=(129, 80)) # ㅏ

# triple(mo_path="glyph/mo/3154.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(55, 110), ja1_start=(60, 40), ja2_start=(129, 80))  # ㅔ

# triple(mo_path="glyph/mo/315F.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(35, 50), ja1_start=(30, 70), ja2_start=(139, 80))  # ㅟ

# triple(mo_path="glyph/mo/3157.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(40, 70), ja1_start=(30, 90), ja2_start=(120, 80))  # ㅗ

# triple(mo_path="glyph/mo/3153.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(45, 110), ja1_start=(40, 60), ja2_start=(129, 80))  # ㅓ

# triple(mo_path="glyph/mo/315B.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(60, 55), ja1_start=(30, 80), ja2_start=(140, 80))  # ㅛ

# triple(mo_path="glyph/mo/3160.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(90, 55), ja1_start=(30, 80), ja2_start=(145, 80))  # ㅠ

# triple(mo_path="glyph/mo/3151.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(30, 130), ja1_start=(50, 60), ja2_start=(125, 70))  # ㅑ

# triple(mo_path="glyph/mo/3155.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(20, 120), ja1_start=(50, 60), ja2_start=(135, 90))  # ㅕ

# triple(mo_path="glyph/mo/3163.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(135, 90))  # ㅣ

# triple(mo_path="glyph/mo/3161.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(135, 90))  # ㅡ

# triple(mo_path="glyph/mo/3152.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(135, 80))  # ㅒ

# triple(mo_path="glyph/mo/3150.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(20, 140), ja1_start=(50, 60), ja2_start=(140, 90))  # ㅐ

# triple(mo_path="glyph/mo/315E.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(50, 50), ja1_start=(25, 70), ja2_start=(145, 90))  # ㅞ

# triple(mo_path="glyph/mo/3158.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(50, 45), ja1_start=(25, 80), ja2_start=(145, 90))  # ㅘ

# triple(mo_path="glyph/mo/3159.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(50, 45), ja1_start=(25, 70), ja2_start=(145, 90))  # ㅙ

# triple(mo_path="glyph/mo/315D.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(50, 45), ja1_start=(25, 70), ja2_start=(145, 90))  # ㅝ

# triple(mo_path="glyph/mo/315A.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(50, 50), ja1_start=(25, 80), ja2_start=(145, 90))  # ㅚ

# triple(mo_path="glyph/mo/3156.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(50, 110), ja1_start=(50, 60), ja2_start=(135, 80))  # ㅖ

# triple(mo_path="glyph/mo/315C.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(60, 50), ja1_start=(20, 80), ja2_start=(145, 70))  # ㅜ

# triple(mo_path="glyph/mo/3162.png", ja1_dir="glyph/cho",
#        ja2_dir="glyph/jong", mo_start=(40, 50), ja1_start=(30, 70), ja2_start=(145, 70))  # ㅢ
