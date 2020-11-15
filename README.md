> 작성 진행 중, 부족하거나 어색한 부분 있으면 아무나 추가, 수정 해주세요

# new_A.Ifonts

영어는 대소문자를 모두 합쳐도 글자가 52자 밖에 되지 않아 폰트 제작에 시간이 많이 걸리지 않는 데에 반해 한글은 초성, 중성, 종성의 다양한 조합으로 인해 11,172자의 글자를 모두 디자인해야 합니다. 따라서 폰트 제작에 수많은 시간과 비용이 들게 되고 결국 한글 폰트의 부족이라는 결과로 이어지게 됩니다.
 
그래서 한글 폰트 제작에 도움이 되는 프로그램을 만들고자 해당 프로젝트를 시작하게 되었습니다.

# Used Tools

### Technology Stack

> 프로젝트에 사용된 기술

- Python
- Teachable Machine
- Node.js

### Python 3.7 Requirements

// requirements.txt 를 사용하는 쪽으로 바꿀 생각 중

> 코드 실행에 필요한 파이썬 라이브러리 및 버전

- opencv-python==4.4.0.44
- pillow==8.0.1
- tensorflow==2.3.0

# Usage

### Prepare Handwriting Image

- `INPUT_IMAGE` 폴더에 손글씨체 이미지를 넣습니다.

### Crop

```sh
python crop.py
```

- 윤곽선을 이용해 이미지에서 음운을 추출해냅니다.

### Convert Grayscale

```sh
python convert_grayscale.py
```

- 이미지를 검정과 흰색 두가지 색만으로 바꿉니다.

### Classify

```sh
python division.py
```

- 티처블 머신으로 자음과 모음을 학습시킨 모델을 이용하여 추출된 음운을 분류합니다.


### Formalization.py

```sh
python Formalization.py
```

- 분류된 이미지를 가운데에 위치시킵니다.

### Check 

```sh
python show.py
```

- 자음, 모음의 분류가 잘 이루어졌는지 확인합니다.

# 메모장..

[손글씨 데이터셋](https://drive.google.com/file/d/1dIlFuKEJLK09IqLET5nfai3q7h_XAOmT/view?usp=sharing)
