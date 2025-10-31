# AI 사주 운세 분석 웹 애플리케이션

이 프로젝트는 사용자의 생년월일시 정보를 기반으로 AI가 사주 팔자를 분석하고, 상세한 운세 정보를 제공하는 간단한 웹 애플리케이션입니다.

## 주요 기능

- **사주 정보 입력:** 사용자는 생년, 월, 일, 시, 태어난 지역 및 특정 질문을 입력할 수 있습니다.
- **AI 기반 사주 분석:** Google Gemini AI 모델을 활용하여 다음 항목에 대한 깊이 있는 분석을 제공합니다.
    - 사주 전체에 대한 종합 요약
    - 연주, 월주, 일주, 시주 각 사주팔자 기둥에 대한 상세 분석
    - 사주에 분포된 오행(목, 화, 토, 금, 수)의 균형 분석
    - 초년, 중년, 말년으로 이어지는 인생 총운
    - 오늘의 사랑, 직업, 건강, 재물 운세
- **사용자 질문 답변:** 사주 분석과 더불어 사용자가 궁금한 점에 대해 AI가 맞춤형 답변을 제공합니다.
- **탭 기반 UI:** 분석 결과를 여러 탭으로 나누어 보여줌으로써 사용자가 원하는 정보를 쉽게 찾아볼 수 있습니다.
- **로딩 상태 표시:** API로부터 결과를 기다리는 동안 로딩 메시지를 표시하여 사용자 경험을 개선했습니다.

## 프로젝트 구조

```
google_AI_project/
├── app.py                  # Flask 웹 애플리케이션 실행 파일
├── saju_core.py            # Gemini AI 호출 및 사주 분석 로직
├── saju_fortuneteller.py   # 초기 버전의 사주 분석 스크립트 (현재는 사용되지 않음)
├── templates/
│   ├── index.html          # 사용자 입력 페이지
│   └── result.html         # 분석 결과 표시 페이지
└── .venv/                    # 파이썬 가상 환경
```

## 설치 및 실행 방법

**1. 가상환경 설정**

프로젝트가 `.venv`를 포함하고 있으나, 다른 환경에서 새로 시작하는 경우 아래 명령어로 가상환경을 생성하고 활성화합니다.

```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source .venv/bin/activate
```

**2. 의존성 패키지 설치**

필요한 라이브러리를 설치합니다.

```bash
pip install Flask google-generativeai
```

**3. Google API 키 설정**

Gemini API를 사용하기 위해 Google API 키를 환경 변수로 설정해야 합니다.

- **Windows (CMD):**
  ```
  set GEMINI_API_KEY="YOUR_API_KEY"
  ```
- **Windows (PowerShell):**
  ```
  $env:GEMINI_API_KEY="YOUR_API_KEY"
  ```
- **macOS/Linux:**
  ```
  export GEMINI_API_KEY="YOUR_API_KEY"
  ```

**4. 애플리케이션 실행**

아래 명령어를 사용하여 Flask 개발 서버를 시작합니다.

```bash
python app.py
```

**5. 서비스 접속**

웹 브라우저를 열고 `http://127.0.0.1:5000` 주소로 접속하면 사주 분석 서비스를 이용할 수 있습니다.
