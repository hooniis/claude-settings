# Calendar Brief

Google Calendar 일정을 Claude Code에서 바로 확인할 수 있는 스킬입니다.
개인/회사 계정의 일정을 통합하여 날짜별로 정리해 보여줍니다.

## 출력 예시

```
🔵 개인 | 🟠 회사

### 월 (2025-01-27)

| | 시간 | 일정 | 장소 | 참석 |
|--|------|------|------|------|
| 🔵 | All day | Friend's birthday | - | |
| 🟠 | 09:00 - 10:00 | Team standup | - | ✅ |
| 🟠 | 14:00 - 16:00 | Tech talk | Conference Room | ❓ |
```

## 사전 준비

### 1. gogcli 설치

[gogcli](https://gogcli.sh/)는 Google Workspace(Gmail, Calendar, Drive 등)를 CLI로 사용할 수 있는 도구입니다.

```bash
brew install steipete/tap/gogcli
```

설치 확인:

```bash
gog --version
```

> 소스 빌드 등 다른 설치 방법은 [GitHub 저장소](https://github.com/steipete/gogcli)를 참고하세요.

### 2. Google Cloud OAuth 인증 설정

gogcli가 Google Calendar에 접근하려면 OAuth 클라이언트 인증이 필요합니다.

#### 2-1. Google Cloud 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성 (또는 기존 프로젝트 사용)
3. **API 및 서비스 > 라이브러리**에서 **Google Calendar API** 활성화

#### 2-2. OAuth 동의 화면 설정

1. **API 및 서비스 > OAuth 동의 화면** 이동
2. 사용자 유형: **외부** 선택
3. 앱 이름, 사용자 지원 이메일 등 필수 항목 입력
4. 범위(Scopes) 추가: `https://www.googleapis.com/auth/calendar.readonly`
5. 테스트 사용자에 본인 이메일 추가

#### 2-3. OAuth 클라이언트 ID 생성

1. **API 및 서비스 > 사용자 인증 정보** 이동
2. **+ 사용자 인증 정보 만들기 > OAuth 클라이언트 ID**
3. 애플리케이션 유형: **데스크톱 앱**
4. JSON 파일 다운로드

#### 2-4. gogcli에 인증 정보 등록

```bash
# OAuth 클라이언트 등록
gog auth credentials ~/Downloads/client_secret_*.json

# 계정 인증 (브라우저가 열림)
gog auth add you@gmail.com
```

여러 계정을 사용하는 경우 각각 추가합니다:

```bash
gog auth add you@gmail.com
gog auth add you@company.com
```

#### 2-5. 인증 확인

```bash
gog auth list
```

등록된 계정 목록이 표시되면 설정 완료입니다.

### 3. 스킬 설치

스킬 파일을 Claude Code 스킬 디렉토리에 배치합니다:

```
~/.claude/skills/calendar-brief/
├── SKILL.md
├── README.md
└── scripts/
    └── calendar_brief.py
```

Python 3 이 설치되어 있어야 합니다 (추가 패키지 불필요, 표준 라이브러리만 사용).

## 사용 방법

### Claude Code에서 사용

스킬이 설치되면 자연어로 일정을 물어볼 수 있습니다:

```
/calendar-brief
/calendar-brief 이번주
/calendar-brief 내일
/calendar-brief next week
```

또는 대화형으로:

```
오늘 일정 알려줘
이번 주 스케줄 확인해줘
What's my schedule for tomorrow?
```

### 스크립트 직접 실행

```bash
# 오늘 일정 (기본값, 계정 자동 탐색)
python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py

# 이번 주
python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --this-week

# 다음 주
python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --next-week

# 내일
python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --tomorrow

# 계정 직접 지정
python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py \
  --personal=you@gmail.com \
  --work=you@company.com \
  --this-week
```

## 스크립트 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `--personal` | No | 개인 계정 이메일 |
| `--work` | No | 회사 계정 이메일 |
| `--today` | No | 오늘 일정 (기본값) |
| `--tomorrow` | No | 내일 일정 |
| `--this-week` | No | 이번 주 (월~일) |
| `--next-week` | No | 다음 주 (월~일) |

- `--personal` / `--work`를 생략하면 `gog auth list`에서 자동 탐색
- 도메인 기반 자동 분류: gmail.com, naver.com 등 -> 개인 / 그 외 -> 회사

## 출력 형식

### 계정 구분

| 표시 | 의미 |
|------|------|
| 🔵 | 개인 계정 |
| 🟠 | 회사 계정 |

### 참석 상태

| 표시 | 의미 |
|------|------|
| ✅ | 수락 |
| ❌ | 거절 |
| ❓ | 미응답 |
| 🤔 | 미정 |
| (빈칸) | 참석자 없음 / 본인이 만든 일정 |

### 정렬 규칙

- 날짜별 그룹핑
- 종일 이벤트가 먼저, 이후 시간순 정렬
- 이벤트가 없는 날은 생략

## 트러블슈팅

### `gog` 명령어를 찾을 수 없음

```bash
brew install steipete/tap/gogcli
```

### 인증 오류 (`missing --account`)

계정이 등록되어 있는지 확인:

```bash
gog auth list
```

계정이 없으면 추가:

```bash
gog auth add you@gmail.com
```

### Calendar API 권한 오류

Google Cloud Console에서 **Google Calendar API**가 활성화되어 있는지 확인하세요.
OAuth 동의 화면의 테스트 사용자에 본인 이메일이 포함되어 있는지도 확인하세요.

### 토큰 만료

OAuth 토큰이 만료되면 재인증합니다:

```bash
gog auth add you@gmail.com
```

## 참고 링크

- [gogcli 공식 사이트](https://gogcli.sh/)
- [gogcli GitHub](https://github.com/steipete/gogcli)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Claude Code Skills 문서](https://docs.anthropic.com/en/docs/claude-code/skills)
