# 📸 PhotoRenamer (파일명 표준화 유틸리티)

다양한 카메라(Canon, Pentax 등) 및 원본 소스에서 생성된 사진/영상 파일명을 표준 형식(`IMG_XXXX`)으로 일괄 변환하고, HEIC 이미지를 JPG로 자동 변환해주는 윈도우용 GUI 도구입니다.

## ✨ 주요 기능

* **파일명 표준화**: 복잡한 원본 파일명을 `IMG_XXXX.jpg` 형식으로 통일
    * `0R2A0813.JPG` → `IMG_0813.jpg`
    * `IMGP1234.JPG` → `IMG_1234.jpg`
    * `Law_231009_5019.JPG` → `IMG_5019.jpg`
    * `Mey_123456_7890.JPG` → `IMG_7890.jpg`
* **보정 파일 자동 처리**: `_보정` 태그가 붙은 파일은 숫자를 덧붙여 충돌 방지
    * `0R2A0813_보정.png` → `IMG_08131.png`
    * `_보정1`, `_보정2` 등의 순차적 태그 지원
* **포맷 변환**: 아이폰 등의 **HEIC/HIF** 이미지를 **JPG**로 자동 변환
* **재귀적 처리**: 하위 폴더의 파일까지 모두 탐색하여 구조 유지
* **GUI 인터페이스**: 직관적인 진행바(Progress Bar)와 로그 확인 창 제공

## 🛠 기술 스택

* **Language**: Python 3.x
* **GUI**: tkinter
* **Image Processing**: Pillow, pillow-heif
* **Packaging**: PyInstaller

## 🚀 설치 및 실행 방법

### 방법 1: 실행 파일(EXE)로 실행 (Python 불필요)
[Releases] 탭에서 최신 `filename-standardizer.exe` 파일을 다운로드하여 실행합니다. (준비 중)

### 방법 2: 소스 코드로 실행
Python이 설치된 환경에서 다음 명령어로 실행할 수 있습니다.

**1. 저장소 클론 (Clone)**

    git clone https://github.com/licentia-law/filename-standardizer.git
    cd PhotoRenamer

**2. 가상환경 설정 및 패키지 설치**

    # 가상환경 생성
    python -m venv .venv
    
    # 가상환경 활성화 (Windows)
    .venv\Scripts\activate

    # 의존성 패키지 설치
    pip install -r requirements.txt

**3. 프로그램 실행**

    python main.py

## 📂 프로젝트 구조

    PhotoRenamer/
    ├── docs/                # 기획 문서 (PRD 등)
    ├── file_processor.py    # 파일명 변환 및 이미지 처리 핵심 로직
    ├── gui.py               # Tkinter 기반 GUI 구성
    ├── main.py              # 프로그램 진입점 (Entry Point)
    ├── requirements.txt     # 의존성 패키지 목록
    └── test_file_processor.py # 단위 테스트 (Unit Test)

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.