# Documentation Architecture

기술 문서의 정보 구조를 설계하는 원칙과 방법을 다룹니다. 핵심 철학은 독자의 관점에서 설계하는 것입니다.

---

## Key Principles Overview

| 원칙 | 설명 |
|------|------|
| One Topic Per Page | 한 페이지에 하나의 주제만 다룸 |
| Value First, Cost Later | 가치를 먼저, 부가 정보는 나중에 |
| Effective Headings | 핵심 키워드 포함, 일관성 유지, 30자 이내 |
| Include Overviews | 개요로 핵심 내용 요약 |
| Predictability | 일관된 제목, 형식, 구조 유지 |
| Detailed Explanations | 새로운 개념을 충분히 설명 |

---

## One Topic Per Page

한 페이지에 하나의 핵심 목표만 집중합니다. 문서가 너무 많은 내용을 다루면 독자가 핵심 정보를 빠르게 찾기 어렵습니다.

### Three Key Benefits

**1. Improved Readability and Navigation (가독성과 탐색 개선)**

> 문서가 너무 길어지거나 한 페이지에 여러 개념이 뒤섞이면 독자가 원하는 정보를 찾기가 어려워요.

**2. Easier Maintenance (유지보수 용이)**

한 문서에 과도한 내용을 담으면 향후 업데이트가 복잡해집니다. 변경 시 관련 섹션을 찾고 수정하기 어렵고, 중복 정보가 문서 간에 나타날 수 있습니다.

**3. Prevents Complex Structure (복잡한 구조 방지)**

> 제목의 위계가 4단계(####, H4) 이상으로 깊어진다면, 그 문서는 여러 개의 문서로 나누어야 할 신호예요.

### Practical Recommendations

- H4 이상의 깊이에 도달하면 문서 분할
- 개별 주제 페이지로 연결되는 개요 페이지 생성
- 주제를 가능한 구체적으로 유지
- 단일 페이지에서 여러 핵심 주제 다루기 지양

---

## Value First, Cost Later

독자 가치를 기능 설명보다 우선합니다.

> 독자는 '이 기능이 왜 필요한가?', '내게 어떤 도움이 되는가?'를 먼저 알고 싶어 해요.

### Two Main Benefits

**1. Avoid Feature-Focused Mistakes**

작성자는 종종 독자가 해결할 수 있는 문제를 설명하기보다 자신의 관점에서 세부사항과 설정을 설명합니다.

**2. Capture Reader Attention Quickly**

독자가 달성할 수 있는 것이나 기대할 수 있는 긍정적 변화를 명확히 전달하면 전체 문서를 읽을 가능성이 높아집니다.

### Practical Guidelines

**Put supplementary details later (부가 정보는 나중에)**

배경 정보에 들어가기 전에 핵심 문제 해결 가치나 긍정적 결과를 먼저 설명합니다.

**Emphasize benefits over functions (기능보다 이점 강조)**

도구가 무엇을 하는지 나열하는 대신, 사용자가 무엇을 달성할 수 있는지 설명합니다.

### Examples

| Bad | Good |
|-----|------|
| 리버스 프록시 설정은 2019년에 도입되었고... | 리버스 프록시 설정을 적용하면 네트워크 지연 문제를 최소화할 수 있어요 |

---

## Effective Headings

### Key Benefits

1. **Improved Readability** - 명확하고 간결한 제목으로 독자가 빠르게 문서를 스캔하고 주요 주제를 한눈에 파악
2. **Enhanced Searchability** - 핵심 키워드를 제목에 포함하면 검색 엔진과 내부 탐색을 통해 문서 찾기 용이
3. **Document Consistency** - 일관된 제목 스타일로 더 정돈된 외관 생성, 문서 간 관계 이해 도움

### Four Essential Guidelines

**1. Include Core Keywords (핵심 키워드 포함)**

독자가 검색할 가능성이 있는 키워드를 제목에 포함하여 문서 목적을 즉시 명확히 합니다.

| Bad | Good |
|-----|------|
| 오류 해결 방법 | `NOT_FOUND_USER` 오류 해결 |

**2. Maintain Consistency (일관성 유지)**

같은 수준의 제목은 동일한 스타일과 어구 규칙을 따릅니다. 동사형 또는 명사형을 일관되게 사용합니다.

**3. Keep It Concise (간결하게 유지)**

> 제목은 30자 이내로 간결하게 쓰세요.

불필요한 단어를 제거하면서 필수 정보는 보존합니다.

**4. Use Declarative Statements (평서문 사용)**

기술 문서에서는 감정적 강조보다 명확성을 우선하여 느낌표나 물음표를 피하고 직설적인 문장을 사용합니다.

---

## Overview: Don't Skip the Summary

개요의 중요성을 강조합니다.

### Three Key Benefits

**1. Reader Comprehension (독자 이해)**

> 개요는 문서의 핵심 내용을 요약하고, 독자가 문서를 읽기 전에 내용을 빠르게 이해할 수 있도록 돕습니다.

**2. Search Visibility (검색 가시성)**

잘 작성된 개요는 문서 가치를 효과적으로 전달하여 검색 결과를 개선합니다.

**3. Writing Focus (작성 집중)**

개요를 먼저 작성하면 문서 일관성을 유지하고 불필요한 내용을 줄이는 데 도움이 됩니다.

### Checklist Guidelines

- **Summarize core content** - 개요만으로 주제를 이해할 수 있어야 하며, 추가 읽기가 필요하지 않아야 함
- **Clarify document goals** - 독자가 이 자료를 읽으면 무엇을 달성할 수 있는지 명시적으로 답변
- **Prioritize value over background** - 기술적 배경보다 실용적 이점을 앞세움

### Example

| Bad | Good |
|-----|------|
| React 상태 관리에 대한 추상적 설명 | `useState`, `useReducer`, Redux 등 구체적 도구를 언급하는 명확한 개요 |

---

## Predictability

예측 가능한 문서는 일관된 용어, 논리적 흐름, 체계적인 정보 계층을 사용합니다.

### Key Benefits

1. **Fast Navigation** - 일관된 구조로 독자가 필요한 정보를 쉽게 찾음
2. **Reduced Learning Curve** - 여러 문서에 걸친 일관된 형식으로 이전 지식을 확장하여 새 콘텐츠 이해
3. **Easier Maintenance** - 명확한 패턴으로 팀이 정보를 어디에 배치할지 쉽게 결정

### Four Main Guidelines

**1. Maintain Consistent Headings, Format, and Structure**

섹션 계층을 규칙적으로 유지하고 명확히 연결합니다. 일관된 구성 패턴으로 번호 매긴 섹션을 사용합니다.

**2. Follow Uniform Section Title Patterns**

독자 혼란을 피하기 위해 문서 전체에서 동일한 섹션 이름을 사용합니다.

| Bad | Good |
|-----|------|
| "설치"와 "환경 설정"을 번갈아 사용 | 일관되게 "설치" 사용 |

**3. Arrange Information in Logical Order**

기초 개념을 먼저 시작한 후 복잡한 세부사항으로 진행합니다.

```
핵심 개념 → 구체적 사용법 → 코드 예제 → 고급 주제
```

**4. Use Terminology Consistently**

같은 개념에 대해 용어를 혼용하지 않습니다.

| Bad | Good |
|-----|------|
| 같은 개념에 "상태", "데이터", "값" 혼용 | 용어 가이드를 만들고 문서 전체에 적용 |

---

## Detailed Explanations

문서는 독자의 이해 수준에 맞춰야 합니다. 독자는 콘텐츠를 처음 접하므로 배경 지식이 부족할 수 있습니다. 필요한 정보를 생략하면 독자가 의미를 추론해야 하여 오해와 인지 부담을 만듭니다.

### Two Key Benefits

**1. Reduced Learning Curve (학습 곡선 감소)**

기술 문서는 자주 선행 개념을 도입합니다. 간단한 사전 설명이 독자의 학습 부담을 줄입니다.

**2. Accurate Understanding (정확한 이해)**

기능 조건을 설명하지 않으면 독자가 기능을 잘못 해석하거나 잘못 적용할 수 있습니다. 조건, 입력, 상태, 시간에 따른 결과에 대한 구체적인 세부사항이 오해를 방지합니다.

### Checklist Guidelines

**Explain New Concepts Thoroughly (새로운 개념을 충분히 설명)**

개념을 한두 문장으로 정의하고, 독자가 이 지식이 왜 필요한지와 어디에 적용되는지 포함합니다.

| Bad | Good |
|-----|------|
| 서비스가 "이벤트 소싱"을 사용한다고만 명시 | "이벤트 소싱은 최종 상태만 저장하는 대신 모든 상태 변경 이벤트를 기록합니다" |

**Provide Sufficient Information About Function Operation (기능 작동에 대한 충분한 정보 제공)**

기능에 영향을 미치는 조건, 입력이나 상태가 어떻게 차이를 만드는지, 시간에 따른 변화를 구체적으로 설명합니다.

| Bad | Good |
|-----|------|
| duration 필드만 표시 | 기간을 결정하는 요소, 수동 로그아웃 vs 타임아웃 시나리오, 단위(밀리초) 명시 |

---

## Checklist Summary

### One Topic Per Page
- [ ] H4 이상의 깊이가 있으면 문서를 분할했는가?
- [ ] 각 페이지가 하나의 핵심 주제에 집중하는가?

### Value First
- [ ] 독자 가치가 문서 앞부분에 있는가?
- [ ] 기능보다 이점을 강조하는가?

### Headings
- [ ] 핵심 키워드가 제목에 포함되어 있는가?
- [ ] 같은 수준의 제목이 일관된 스타일을 따르는가?
- [ ] 제목이 30자 이내인가?

### Overview
- [ ] 개요만으로 주제를 이해할 수 있는가?
- [ ] 문서 목표가 명확히 명시되어 있는가?

### Predictability
- [ ] 일관된 제목, 형식, 구조를 유지하는가?
- [ ] 용어를 일관되게 사용하는가?
- [ ] 정보가 논리적 순서로 배열되어 있는가?

### Detailed Explanations
- [ ] 새로운 개념을 충분히 설명했는가?
- [ ] 기능 작동에 대한 충분한 정보를 제공했는가?

---

*Source: [technical-writing.dev](https://technical-writing.dev/architecture/index.html)*
