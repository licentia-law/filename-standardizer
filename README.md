# PhotoRenamer (Filename Standardizer)

다양한 카메라 및 소스에서 생성된 파일명을 표준 형식(`IMG_<번호>`)으로 일괄 변환하고, HEIC/HIF 이미지를 JPG로 자동 변환하는 **로컬 GUI 기반 유틸리티**입니다.

## 📋 주요 기능 (Features)

*   **파일명 표준화**: 다양한 형식의 파일명을 `IMG_<번호>` 규칙으로 통일
    *   **Canon**: `0R2A0813.JPG` → `IMG_0813.jpg`
    *   **Pentax**: `IMGP1234.JPG` → `IMG_1234.jpg`
    *   **Law/Mey**: 
        *   `Law_231009_5019.JPG` → `IMG_5019.jpg`
        *   `Mey_123456_7890.JPG` → `IMG_7890.jpg`
    *   **보정 파일 처리**: `_보정` 태그 감지 시 접미사 숫자 증가
        *   `..._보정.png` → `...1.png`
        *   `..._보정1.png` → `...2.png`
    *   **중복 방지**: 변환된 파일명이 이미 존재할 경우 자동으로 숫자 카운터를 추가하여 충돌 방지
*   **포맷 변환**: `.heic`, `.hif` 파일을 호환성 높은 `.jpg`로 자동 변환
*   **폴더 구조 유지**: 하위 폴더를 포함하여 재귀적으로 처리하며, 원본 폴더 구조를 유지한 채 `result` 폴더에 저장
*   **GUI 인터페이스**: 직관적인 폴더 선택 및 진행 상황(Progress Bar, 로그) 실시간 확인
*   **지원 확장자**:
    *   이미지: `.cr3`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.heic`, `.hif`, `.dng`
    *   영상: `.mp4`, `.wma`, `.mov`

## 🛠 기술 스택 (Tech Stack)

*   **Language**: Python 3.x
*   **GUI**: tkinter (Python 표준 라이브러리)
*   **Image Processing**: Pillow, pillow-heif
*   **Packaging**: PyInstaller

## 🚀 설치 및 실행 (Installation & Run)

### 사전 요구사항 (Prerequisites)
*   Python 3.8 이상이 설치되어 있어야 합니다.

### 설치 (Installation)
프로젝트루트 디렉토리에서 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

### 실행 (Run)
아래 명령어로 프로그램을 실행합니다.

```bash
python main.py
```

## � 사용 방법 (How to Use)

1.  프로그램 실행 후, 상단의 **"선택"** 버튼을 클릭하여 변환할 파일이 포함된 최상위 폴더를 지정합니다.
2.  폴더 경로가 입력되면 **"변환 시작"** 버튼을 클릭하여 작업을 수행합니다.
    *   선택된 폴더와 그 하위 폴더 내의 모든 대상 파일을 탐색합니다.
3.  중앙의 로그 창과 하단의 진행률 바(Progress Bar)를 통해 실시간 처리 현황을 확인합니다.
4.  작업이 완료되면 "파일 처리 작업이 완료되었습니다"라는 알림 메시지가 표시됩니다.
5.  **"결과 폴더 열기"** 버튼을 클릭하여, 생성된 `result` 폴더와 변환된 파일들을 확인합니다.
    *   **참고**: 원본 파일은 보존되며, 변환된 파일은 소스 폴더 내 `result` 하위 폴더에 원본 구조를 따라 저장됩니다.

## �📦 실행 파일 빌드 (Build Executable)

PyInstaller를 사용하여 단일 실행 파일(`.exe`)로 빌드할 수 있습니다. 이미 포함된 `.spec` 파일을 사용하면 간편하게 빌드할 수 있습니다.

```bash
pyinstaller filename-standardizer.spec
```

빌드가 완료되면 `dist/` 폴더 내에 실행 파일이 생성됩니다.

## 📄 라이선스 (License)

이 프로젝트는 **MIT License**를 따릅니다. 자세한 내용은 `LICENSE.txt` 파일을 참조하세요.
