---
layout: calculation
title: "리스이용자 회계처리 — 사용권자산·리스부채 인식 및 측정"
date: 2026-05-12 09:00:00 +0900
categories: [calculation]
subject: [accounting1]
topics: [재무회계, 리스, K-IFRS 1116호, 사용권자산, 리스부채]
difficulty: 상
applied_date: "2026-05-12"
---

<div class='question-block'>
<strong>[문제]</strong>

㈜대한은 20×6년 1월 1일 ㈜민국과 다음 조건의 영업용 건물 리스계약을 체결하였다. ㈜대한의 회계기간은 1월 1일부터 12월 31일까지이며, K-IFRS 제1116호 '리스'를 적용한다.

<strong>1. 리스계약 조건</strong>
<ul>
<li>리스기간 : 20×6년 1월 1일부터 20×10년 12월 31일까지 (5년)</li>
<li>고정리스료 : 매년 12월 31일에 30,000,000원 후급 (총 5회)</li>
<li>리스개시일 이전 선급한 리스료 : 5,000,000원 (20×5년 12월 20일 지급)</li>
<li>리스인센티브로 ㈜민국으로부터 수령한 금액 : 3,000,000원 (개시일에 수령)</li>
<li>리스개설직접원가 : ㈜대한이 지출한 법률검토수수료 4,000,000원</li>
<li>리스기간 종료 시 ㈜대한은 건물을 원상복구해야 하며, 원상복구원가의 현재가치는 8,000,000원으로 추정된다.</li>
</ul>

<strong>2. 매수선택권 및 연장선택권</strong>
<ul>
<li>리스기간 종료 시 매수선택권 행사가격 20,000,000원이 부여되었으나, 행사가능성이 매우 낮은 것으로 평가된다.</li>
<li>연장선택권은 부여되지 않았다.</li>
</ul>

<strong>3. 할인율 및 기타 정보</strong>
<ul>
<li>리스의 내재이자율은 쉽게 산정할 수 없으며, ㈜대한의 증분차입이자율은 연 8%이다.</li>
<li>5년, 8% 정상연금현가계수 : 3.99271</li>
<li>5년, 8% 단일금액현가계수 : 0.68058</li>
<li>건물의 내용연수는 8년이며, 정액법으로 감가상각한다 (잔존가치 0원).</li>
<li>매수선택권은 행사가능성이 낮으므로 리스부채 산정에서 제외한다.</li>
</ul>

<strong>[물음]</strong> ㈜대한이 20×6년 12월 31일 인식할 ① 리스부채 장부금액, ② 사용권자산의 감가상각비, ③ 당기 포괄손익계산서에 인식할 총 비용을 계산하시오.
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 리스개시일(20×6.1.1) 리스부채 측정</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>

리스부채는 리스개시일 현재 지급되지 않은 리스료를 내재이자율(또는 증분차입이자율)로 할인한 현재가치로 측정한다. 매수선택권은 행사가능성이 낮아 리스료에서 제외한다.

<pre>
리스부채 = 고정리스료 × 정상연금현가계수(5년, 8%)
        = 30,000,000원 × 3.99271
        = 119,781,300원
</pre>

**리스부채(20×6.1.1) = 119,781,300원**

  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>2</span>
      <span class='calc-step-title'>2단계 — 사용권자산 최초원가 산정</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>

K-IFRS 1116호 문단 24에 따라 사용권자산은 다음 항목의 합으로 측정한다.
(① 리스부채 최초측정금액 + ② 리스개시일 또는 그 전에 지급한 리스료 − 수령한 리스인센티브 + ③ 리스개설직접원가 + ④ 복구원가 추정치)

<pre>
사용권자산 = 리스부채       119,781,300
          + 선급리스료         5,000,000
          - 리스인센티브       (3,000,000)
          + 리스개설직접원가    4,000,000
          + 복구충당부채        8,000,000
          ─────────────────────────────
          = 133,781,300원
</pre>

**사용권자산 최초원가 = 133,781,300원**

  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>3</span>
      <span class='calc-step-title'>3단계 — 20×6년 말 리스부채 장부금액</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>

리스부채는 유효이자율법으로 이자를 가산하고 지급액을 차감한다.

<pre>
이자비용     = 119,781,300 × 8%       = 9,582,504원
리스료지급    = (30,000,000)
─────────────────────────────────────────
20×6년 말 리스부채
            = 119,781,300 + 9,582,504 − 30,000,000
            = 99,363,804원
</pre>

**① 리스부채 장부금액(20×6.12.31) = 99,363,804원**

  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>4</span>
      <span class='calc-step-title'>4단계 — 사용권자산 감가상각비 계산</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>

매수선택권 행사가능성이 낮아 소유권 이전이 확실하지 않으므로, 상각기간은 **리스기간(5년)과 내용연수(8년) 중 짧은 기간**인 5년을 적용한다 (K-IFRS 1116호 문단 32).

<pre>
감가상각비 = (사용권자산 최초원가 − 잔존가치) ÷ 상각기간
         = (133,781,300 − 0) ÷ 5
         = 26,756,260원
</pre>

**② 사용권자산 감가상각비 = 26,756,260원**

  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>5</span>
      <span class='calc-step-title'>5단계 — 20×6년 포괄손익계산서 총 비용</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>

리스이용자 회계처리에서 당기 비용은 ① 사용권자산 감가상각비, ② 리스부채 이자비용으로 구성된다. 복구충당부채에 대한 이자(전입액)도 별도로 인식해야 한다.

<pre>
감가상각비          26,756,260
리스부채 이자비용     9,582,504
복구충당부채 전입액   640,000  (= 8,000,000 × 8%)
─────────────────────────────
총 비용           36,978,764원
</pre>

**③ 20×6년 인식할 총 비용 = 36,978,764원**

  </div>
</div>

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>
① 리스부채 장부금액(20×6.12.31) = <strong>99,363,804원</strong><br>
② 사용권자산 감가상각비 = <strong>26,756,260원</strong><br>
③ 20×6년 총 비용 = <strong>36,978,764원</strong>
  </div>
</div>
