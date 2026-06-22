---
layout: calculation
title: "법인세 산출세액 계산 — 각사업연도소득금액에서 산출세액까지"
date: 2026-06-23 09:00:00 +0900
categories: [calculation]
subject: [accounting2]
topics: [법인세, 각사업연도소득금액, 과세표준, 산출세액, 세무조정]
difficulty: 중상
applied_date: "2026-06-23"
---

영리내국법인 ㈜한라의 제24기 사업연도(2025.1.1.~2025.12.31.) 법인세 신고 자료를 토대로, **각사업연도소득금액 → 과세표준 → 산출세액**의 3단계 구조를 단계별로 산출한다. 세무조정 항목의 가산·차감 방향과 누진세율 적용이 핵심이다.

<div class='question-block'>
<strong>[문제]</strong> 영리내국법인 ㈜한라(중소기업 아님)의 제24기 사업연도(2025.1.1.~2025.12.31.) 자료는 다음과 같다. 각사업연도소득금액, 과세표준, 산출세액을 계산하시오. (1,000원 미만 단수는 무시한다.)

<strong>1. 손익계산서상 당기순이익</strong>
- 당기순이익: 1,500,000,000원

<strong>2. 세무조정 사항</strong>
- (가) 손익계산서에 비용으로 계상된 법인세비용: 200,000,000원
- (나) 기업업무추진비(접대비) 한도초과액: 50,000,000원
- (다) 감가상각비 한도초과액: 30,000,000원
- (라) 국세 과오납금에 대한 환급가산금: 10,000,000원 (영업외수익으로 계상됨)
- (마) 자기주식처분이익 중 익금 계상 누락분: 20,000,000원 (장부 미계상)

<strong>3. 과세표준 차감 항목</strong>
- 세무상 이월결손금(제20기분, 2020 사업연도 발생): 200,000,000원
- 비과세소득·소득공제: 없음

<strong>4. 적용 세율 (2026년 시행 법인세법 제55조)</strong>
- 과세표준 2억원 이하: 9%
- 2억원 초과 200억원 이하: 19%
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 세무조정의 가산·차감 방향 분류</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
각 항목의 세무조정 방향을 판정한다.

<pre>
(가) 법인세비용         → 손금불산입(가산)   +200,000,000
(나) 접대비 한도초과     → 손금불산입(가산)   + 50,000,000
(다) 감가상각비 한도초과 → 손금불산입(가산)   + 30,000,000
(마) 자기주식처분이익    → 익금산입(가산)     + 20,000,000
(라) 환급가산금         → 익금불산입(차감)   - 10,000,000
</pre>

(라) 국세 환급가산금은 법인세법 제18조에 따라 익금에 산입하지 않으므로 **차감**한다. (마) 자기주식처분이익은 익금이나 장부에 누락되었으므로 **가산**한다.

**가산조정 합계 = 200,000,000 + 50,000,000 + 30,000,000 + 20,000,000 = 300,000,000원**
**차감조정 합계 = 10,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>2</span>
      <span class='calc-step-title'>2단계 — 각사업연도소득금액 산출</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
당기순이익에 가산조정을 더하고 차감조정을 뺀다.

<pre>
각사업연도소득금액
= 당기순이익 + 가산조정 - 차감조정
= 1,500,000,000 + 300,000,000 - 10,000,000
= 1,790,000,000
</pre>

**각사업연도소득금액 = 1,790,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>3</span>
      <span class='calc-step-title'>3단계 — 과세표준 산출 (이월결손금 공제)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
각사업연도소득금액에서 이월결손금·비과세소득·소득공제를 차감한다. 일반법인의 이월결손금 공제한도는 각사업연도소득금액의 80%이다.

<pre>
공제한도 = 1,790,000,000 × 80% = 1,432,000,000
이월결손금(200,000,000) < 한도 → 전액 공제

과세표준
= 각사업연도소득금액 - 이월결손금 - 비과세 - 소득공제
= 1,790,000,000 - 200,000,000 - 0 - 0
= 1,590,000,000
</pre>

**과세표준 = 1,590,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>4</span>
      <span class='calc-step-title'>4단계 — 누진세율 적용 산출세액</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
과세표준 15.9억원은 「2억원 초과 200억원 이하」 구간이므로 2단계 누진구조로 계산한다.

<pre>
산출세액
= 2억원 × 9% + (과세표준 - 2억원) × 19%
= 200,000,000 × 9% + (1,590,000,000 - 200,000,000) × 19%
= 18,000,000 + 1,390,000,000 × 19%
= 18,000,000 + 264,100,000
= 282,100,000
</pre>

> 누진공제 방식으로 검산: 1,590,000,000 × 19% - 20,000,000 = 302,100,000 - 20,000,000 = 282,100,000원 (일치)

**산출세액 = 282,100,000원**
  </div>
</div>

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>각사업연도소득금액 1,790,000,000원 → 과세표준 1,590,000,000원 → 산출세액 282,100,000원</div>
</div>
