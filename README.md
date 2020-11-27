# new_A.Ifonts

영어는 대소문자를 모두 합쳐도 글자가 52자 밖에 되지 않아 폰트 제작에 시간이 많이 걸리지 않는 데에 반해 한글은 초성, 중성, 종성의 다양한 조합으로 인해 11,172자의 글자를 모두 디자인해야 합니다. 따라서 폰트 제작에 수많은 시간과 비용이 들게 되고 결국 한글 폰트의 부족이라는 결과로 이어지게 됩니다.

그래서 한글 폰트 제작에 도움이 되는 프로그램을 만들고자 해당 프로젝트를 시작하게 되었습니다.

# Used Tools

- Teachable Machine
- Python (3.7.X)
- Node.js (v12.XX.X)

# Easy Usage

### Install

- [이곳](https://drive.google.com/file/d/1p61EpwAZgZmGEQl3JfYlIro0_HqfaZX7/view?usp=sharing)에서 `A.Ifonts_executable.zip`을 다운받습니다.

- 압축을 풀고 해당 폴더 안에 있는 `start.bat`을 실행시킵니다.

### Prepare Handwriting

- `INPUT_IMAGE` 폴더에 손글씨체 이미지를 준비합니다.

### Execute

- `start.bat`을 실행하여 폰트를 생성합니다.

# Hard Usage

### Install

- [Python (3.7)](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe)과 [Node.js (v12)](https://nodejs.org/dist/v12.19.1/node-v12.19.1-x64.msi)를 설치합니다.

- 해당 프로젝트를 `git clone https://github.com/bamcasa/new_A.Ifonts.git` 또는 압축 파일 다운로드를 통해서 다운받습니다.

- 다음을 실행하여 파이썬 라이브러리를 설치합니다.

```sh
pip install -r requirements.txt
```

- 다음을 실행하여 Node.js 라이브러리를 설치합니다.

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

### Make Transparent

```sh
python invisible.py
```

- 합성에 용이하도록 이미지들을 투명하게 만듭니다.

### Add Some Mo

```sh
python dual.py
```

- 모음을 결합하여 이중모음을 만듭니다.

(여기서 이중모음은 모델에 학습되지 않은, 단순히 모음 두개가 합쳐진 모양의 이중모음을 뜻합니다.)

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

# Dev Memo

### Prepare

```sh
pip install pyinstaller
```

```sh
npm installl -g pkg
```

### Build

- Python Build

```sh
python -m PyInstaller -F crop.py
python -m PyInstaller -F convert_grayscale.py
python -m PyInstaller -F division.py
python -m PyInstaller -F Formalization.py
python -m PyInstaller -F covent_name.py
python -m PyInstaller -F invisible.py
python -m PyInstaller -F dual.py
python -m PyInstaller -F combine.py
```

> python -m PyInstaller -F crop.py & python -m PyInstaller -F convert_grayscale.py & python -m PyInstaller -F division.py & python -m PyInstaller -F Formalization.py & python -m PyInstaller -F covent_name.py & python -m PyInstaller -F invisible.py & python -m PyInstaller -F dual.py & python -m PyInstaller -F combine.py

- Node.js Build

```sh
pkg ttf.js -t node12-win-x64
```
