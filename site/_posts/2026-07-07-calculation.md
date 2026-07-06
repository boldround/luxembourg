---
layout: calculation
title: "전환사채 발행·이자비용·전환 — 복합금융상품 회계처리 종합"
date: 2026-07-07 06:00:00 +0900
categories: [calculation]
subject: [accounting1]
topics: [전환사채, 복합금융상품, 유효이자율법, 자본거래]
difficulty: 상
applied_date: "2026-07-07"
---

<div class='question-block'>
<strong>[문제]</strong> ㈜한국은 2026년 1월 1일 다음 조건의 전환사채를 액면발행하였다. (회계기간: 매년 1월 1일 ~ 12월 31일, K-IFRS 제1032호 '금융상품: 표시' 및 제1109호 '금융상품' 적용)

<ul>
<li>액면금액: 1,000,000,000원 (만기 3년, 2028년 12월 31일 액면상환, 상환할증금 없음)</li>
<li>표시이자율: 연 4% (매년 12월 31일 후급)</li>
<li>발행 당시 전환권이 없는 유사한 일반사채의 시장이자율: 연 8%</li>
<li>전환조건: 사채 액면 20,000원당 보통주(액면 5,000원) 1주로 전환 가능</li>
<li>2027년 1월 1일 전환사채 액면금액의 60%가 보통주로 전환됨 (전환 시 전환권대가는 주식발행초과금으로 대체하는 정책 채택)</li>
</ul>

<strong>현가계수 자료 (이자율 8%, 3기간)</strong>
<ul>
<li>단일금액 1원의 현가계수: 0.7938</li>
<li>정상연금 1원의 현가계수: 2.5771</li>
</ul>

<strong>(물음)</strong> ① 발행시점의 부채요소와 자본요소(전환권대가)를 각각 구하고, ② 2026년도 포괄손익계산서에 인식할 이자비용을 계산한 후, ③ 2027년 1월 1일 전환으로 인해 증가하는 <u>주식발행초과금</u>을 구하시오. (단, 원 단위 미만은 절사하지 않고 제시된 현가계수로 계산한 금액을 그대로 사용한다)
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 부채요소의 공정가치(현재가치) 산정</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
복합금융상품은 <strong>부채요소를 먼저 측정</strong>하고, 잔액을 자본요소로 배분한다(잔여지분법, K-IFRS 1032 문단 31~32). 부채요소는 전환권이 없는 유사 일반사채의 시장이자율 8%로 미래 현금흐름을 할인한다.

<pre>
연간 표시이자      = 1,000,000,000 × 4%          = 40,000,000원

원금의 현재가치    = 1,000,000,000 × 0.7938       = 793,800,000원
이자의 현재가치    =    40,000,000 × 2.5771       = 103,084,000원
─────────────────────────────────────────────────
부채요소 공정가치  = 793,800,000 + 103,084,000    = 896,884,000원
</pre>
**중간 답: 부채요소 = 896,884,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>2</span>
      <span class='calc-step-title'>2단계 — 자본요소(전환권대가) 산정</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
자본요소는 발행금액 총액에서 부채요소를 차감한 잔액이다. 전환권대가는 자본항목으로 분류하며 이후 재측정하지 않는다.

<pre>
전환권대가 = 발행금액 − 부채요소
          = 1,000,000,000 − 896,884,000
          = 103,116,000원
</pre>
**중간 답: 전환권대가(자본요소) = 103,116,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>3</span>
      <span class='calc-step-title'>3단계 — 2026년 이자비용과 기말 부채 장부금액 (유효이자율법)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
부채요소는 상각후원가로 후속측정하며, 유효이자율은 발행시점 시장이자율 8%이다.

<pre>
2026년 이자비용   = 896,884,000 × 8%              = 71,750,720원
현금 지급이자     = 1,000,000,000 × 4%             = 40,000,000원
사채할인 상각액   = 71,750,720 − 40,000,000        = 31,750,720원

2026.12.31 부채 장부금액
  = 896,884,000 + 31,750,720                      = 928,634,720원
</pre>
**중간 답: 2026년 이자비용 = 71,750,720원, 기말 부채 장부금액 = 928,634,720원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>4</span>
      <span class='calc-step-title'>4단계 — 전환분에 대한 자본 대체금액과 자본금 산정</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
2027년 1월 1일은 이자지급 직후이므로 전환 직전 부채 장부금액은 928,634,720원이다. 전환 시 손익을 인식하지 않고, <strong>전환된 부분의 부채 장부금액과 전환권대가를 자본으로 대체</strong>한다(장부금액법).

<pre>
전환분 부채 장부금액 대체 = 928,634,720 × 60%     = 557,180,832원
전환분 전환권대가 대체    = 103,116,000 × 60%     = 61,869,600원

발행 주식수 = (1,000,000,000 × 60%) ÷ 20,000원   = 30,000주
자본금 증가 = 30,000주 × 5,000원                  = 150,000,000원
</pre>
**중간 답: 자본 대체 총액 = 619,050,432원, 자본금 = 150,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>5</span>
      <span class='calc-step-title'>5단계 — 주식발행초과금 증가액 산정</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
자본으로 대체된 총액에서 자본금(액면총액)을 차감한 잔액이 주식발행초과금이다.

<pre>
주식발행초과금 = 부채 대체액 + 전환권대가 대체액 − 자본금
             = 557,180,832 + 61,869,600 − 150,000,000
             = 469,050,432원
</pre>

참고 분개 (2027.1.1):
<pre>
(차) 전환사채(장부금액)  557,180,832   (대) 자본금            150,000,000
     전환권대가           61,869,600        주식발행초과금     469,050,432
</pre>
**중간 답: 주식발행초과금 증가액 = 469,050,432원**
  </div>
</div>

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>① 부채요소 896,884,000원 / 전환권대가 103,116,000원 ② 2026년 이자비용 71,750,720원 ③ 주식발행초과금 증가액 = 469,050,432원</div>
</div>

**출제 포인트**

- 복합금융상품의 최초 인식은 **부채 우선 측정 후 잔여액을 자본에 배분**하는 잔여지분법이며, 자본요소부터 측정하면 안 된다는 점이 핵심이다.
- 전환 시점이 이자지급 직후(1월 1일)이므로 경과이자 안분 없이 직전 기말 장부금액을 그대로 사용한다. 전환일이 기중이면 전환일까지의 이자비용을 먼저 인식한 후 장부금액을 대체해야 한다.
- 전환으로 인한 자본 총증가액(619,050,432원)과 주식발행초과금(469,050,432원)을 구분해서 묻는 것이 채점 포인트이며, 자본금 150,000,000원을 차감하지 않으면 감점된다.
