---
layout: calculation
title: "[샘플] 법인세 산출세액 계산"
date: 2026-05-02 11:00:00 +0900
categories: [calculation]
subject: [accounting2]
topics: ["법인세", "산출세액", "세무조정"]
difficulty: 기본
applied_date: "2026-01-01"
excerpt: "법인세 산출세액 기본 흐름 — 결산서상 당기순이익 → 각사업연도소득금액 → 과세표준 → 산출세액."
---

<div class="question-block">
<strong>[문제]</strong> ㈜룩셈부르크의 제22기(2026.1.1.~12.31.) 결산서상 당기순이익은 1,000,000,000원이다. 다음 자료를 이용하여 법인세 산출세액을 계산하시오. (모든 금액은 원 단위)

<ul style="margin-top:0.7rem;">
<li>익금산입·손금불산입 합계: 80,000,000원</li>
<li>손금산입·익금불산입 합계: 30,000,000원</li>
<li>이월결손금 (15년 이내): 50,000,000원</li>
<li>비과세소득: 10,000,000원</li>
<li>법인세율 (2026 적용): 2억 이하 9%, 2억 초과 ~ 200억 이하 19%, 200억 초과 ~ 3,000억 이하 21%, 3,000억 초과 24%</li>
</ul>
</div>

<span class="calc-show-all">단계별 풀이 보기</span>

<div class="calc-step">
  <div class="calc-step-header">
    <span style="display:flex;align-items:center;flex:1;">
      <span class="calc-step-num">1</span>
      <span class="calc-step-title">각 사업연도 소득금액 계산</span>
    </span>
    <span class="calc-step-toggle">▼</span>
  </div>
  <div class="calc-step-body">
    각 사업연도 소득금액 = 결산서상 당기순이익 + 익금산입·손금불산입 − 손금산입·익금불산입

    <pre>= 1,000,000,000 + 80,000,000 − 30,000,000
= 1,050,000,000원</pre>

    <strong>각 사업연도 소득금액 = 1,050,000,000원</strong>
  </div>
</div>

<div class="calc-step">
  <div class="calc-step-header">
    <span style="display:flex;align-items:center;flex:1;">
      <span class="calc-step-num">2</span>
      <span class="calc-step-title">과세표준 계산 (이월결손금·비과세 차감)</span>
    </span>
    <span class="calc-step-toggle">▼</span>
  </div>
  <div class="calc-step-body">
    과세표준 = 각 사업연도 소득금액 − 이월결손금 − 비과세소득 − 소득공제

    <pre>= 1,050,000,000 − 50,000,000 − 10,000,000 − 0
= 990,000,000원</pre>

    <strong>과세표준 = 990,000,000원</strong>
  </div>
</div>

<div class="calc-step">
  <div class="calc-step-header">
    <span style="display:flex;align-items:center;flex:1;">
      <span class="calc-step-num">3</span>
      <span class="calc-step-title">산출세액 계산 (누진공제 방식)</span>
    </span>
    <span class="calc-step-toggle">▼</span>
  </div>
  <div class="calc-step-body">
    과세표준 990,000,000원은 2억 초과 ~ 200억 이하 구간에 해당.

    <pre>2억 이하: 200,000,000 × 9% = 18,000,000
2억 초과분: (990,000,000 − 200,000,000) × 19%
         = 790,000,000 × 19%
         = 150,100,000

산출세액 = 18,000,000 + 150,100,000 = 168,100,000원</pre>
  </div>
</div>

<div class="calc-answer">
  <div class="calc-answer-label">정답</div>
  <div class="calc-answer-value">법인세 산출세액 = 168,100,000원</div>
  <p style="margin-top:0.6rem;font-size:0.85rem;color:var(--text-secondary);">
  ※ 본 문제는 사이트 빌드 검증용 샘플입니다. 실제 콘텐츠는 calc_gen 파이프라인이 생성합니다.
  </p>
</div>
