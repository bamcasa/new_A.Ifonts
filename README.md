> 작성 진행 중, 부족하거나 어색한 부분 있으면 아무나 추가, 수정 해주세요

# new_A.Ifonts

영어는 대소문자를 모두 합쳐도 글자가 52자 밖에 되지 않아 폰트 제작에 시간이 많이 걸리지 않는 데에 반해 한글은 초성, 중성, 종성의 다양한 조합으로 인해 11,172자의 글자를 모두 디자인해야 합니다. 따라서 폰트 제작에 수많은 시간과 비용이 들게 되고 결국 한글 폰트의 부족이라는 결과로 이어지게 됩니다.
 
그래서 한글 폰트 제작에 도움이 되는 프로그램을 만들고자 해당 프로젝트를 시작하게 되었습니다.

# Used Tools

- Teachable Machine
- Python (3.7.X)
- Node.js (v12.XX.X)

# Usage

### Install

- [Python (3.7)](https://www.python.org/downloads/release/python-379)과 [Node.js (v12)](https://nodejs.org/download/release/v12.19.0/)를 설치합니다.

- 해당 프로젝트를 `git clone https://github.com/bamcasa/new_A.Ifonts.git` 또는 압축 파일 다운로드를 통해서 다운받습니다.

- 프로젝트의 루트 폴더에서 다음을 실행하여 파이썬 라이브러리를 설치합니다.
```sh
pip install -r requirements.txt
```

- `result` 폴더로 이동 후 다음을 실행하여 Node.js 라이브러리를 설치합니다.
```sh
npm install
```

### Prepare Handwriting

- `INPUT_IMAGE` 폴더에 손글씨체 이미지를 준비합니다.

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


### Formulate

```sh
python Formalization.py
```

- 분류된 이미지를 가운데에 위치시킵니다.

### Confirm

```sh
python show.py
```

- 자음, 모음의 분류가 잘 이루어졌는지 확인합니다.

### Set Name

```sh
python covent_name.py
```

- 이미지들을 `glyph` 폴더에 초성, 중성, 종성으로 분류하여 저장합니다.

### Combine

```sh
python combine.py
```

- 초성, 중성, 종성들을 결합하여 글자들을 만듭니다.

### Make Font

```sh
node ttf.js
```

- `.png` 파일들을 `.ttf` 파일로 만들고 `fonts` 폴더에서 만들어진 폰트를 확인합니다.

# 메모장..

[손글씨 데이터셋](https://drive.google.com/file/d/1dIlFuKEJLK09IqLET5nfai3q7h_XAOmT/view?usp=sharing)
