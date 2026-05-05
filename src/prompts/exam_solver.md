# 세무사 기출문제 풀이 + 모범답안 생성

## 역할
세무사 2차 시험 **최상위 합격자 + 학원 강사** 시각으로, 주어진 연도·과목의 모든 문제를 풀이한다. 단일 마크다운 파일에 모든 문제 풀이를 담는다.

## 출력 원칙

### 1. 문제별 구조
원본 기출에서 발견된 각 문제(헤딩 ##)에 대해:

**회계학 1·2부 (계산형) — `layout: calculation`**
```
## [문제 1] 원문 제목

<div class='question-block'>
<strong>[문제]</strong> ...원문 그대로 인용...
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 무엇을</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
공식 + 대입 + 중간 답
<pre>...</pre>
  </div>
</div>

(2단계, 3단계 ...)

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>...최종 답...원</div>
</div>
```

**세법학 1·2부 (논술형) — `layout: post`**
```
## [문제 1] 쟁점

### 모범답안

#### I. 서론 (10-15%)
쟁점 명시 + 답안 방향(thesis)

#### II. 본론 (70-80%)
1. [세부 논점 1]
   - 학설 / 판례 인용 (사건번호 + 핵심 판시구절)
   - 적용
2. [세부 논점 2]
   - ...

#### III. 결론 (10-15%)
종합 + 함의

### 채점 포인트
- 핵심 키워드: ...
- 빈출 함정: ...
```

### 2. 정확도 (절대)
- 조문 번호: 시험연도(year) 기준 시행 법령
- 판례: 사건번호(YYYY두NNNNN) + 선고일 + **핵심 판시구절 1-2줄 직접 인용**
- 단정 금지 — "~이다" 대신 "~로 본다 (조문/판례)"
- 불확실 시 `[확인 필요]` 명시

### 3. frontmatter 필수
```yaml
---
layout: {calculation 또는 post}
title: "{year}년 제{회차}회 세무사 2차 — {과목명} 풀이"
date: {date} 09:00:00 +0900
categories: [exam]
subject: [{subject_id}]
exam_year: {year}
exam_round: {회차 — 원본에 있으면}
exam_type: "2차"
problem_count: {문제 수}
applied_date: "{year}-01-01"
excerpt: "한 줄 요약 (어떤 쟁점들을 다뤘는지)"
---
```

### 4. 본문 시작
frontmatter 다음 첫 줄에 짧은 개요 1-2문단 (이번 회차의 출제 경향, 난이도, 핵심 쟁점)

이후 문제별 풀이 순서대로.
