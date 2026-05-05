---
layout: calculation
title: "종합소득세 산출세액 계산 — 종합소득금액에서 과세표준·산출세액까지"
date: 2026-05-05 09:00:00 +0900
categories: [calculation]
subject: [accounting2]
topics: [소득세, 종합소득금액, 과세표준, 산출세액, 종합소득공제]
difficulty: 상
applied_date: "2026-01-01"
excerpt: "사업·근로·기타소득 종합 + 차량유지비 부인 등 실전 세무조정 후 산출세액 도출."
---

<div class='question-block'>
<strong>[문제]</strong> 거주자 갑(만 48세, 남성)의 2026년 귀속 종합소득 관련 자료는 다음과 같다. 갑의 2026년 종합소득 산출세액을 계산하시오. (단, 모든 금액은 원 단위이며, 별도 언급이 없는 항목은 고려하지 않는다.)

<br><br>

<strong>(1) 사업소득 관련 자료</strong>
<ul>
<li>도매업 총수입금액: 850,000,000원</li>
<li>필요경비: 612,000,000원 (아래 (2) 항목은 반영 전)</li>
<li>필요경비 중 갑 본인의 급여로 계상된 금액: 36,000,000원이 포함되어 있다.</li>
<li>사업용 차량(업무전용보험 미가입)의 차량유지비 8,000,000원이 필요경비에 산입되어 있다. (전액 부인 가정)</li>
</ul>

<strong>(2) 근로소득 (겸직 임원)</strong>
<ul>
<li>총급여액: 78,000,000원</li>
<li>근로소득공제: 총급여액 구간 7,500만원 초과 1억원 이하 → 12,475,000원 + (총급여액 - 75,000,000원) × 5%</li>
</ul>

<strong>(3) 기타소득 (강연료, 일시적 인적용역)</strong>
<ul>
<li>총수입금액: 20,000,000원</li>
<li>실제 필요경비: 3,000,000원 (의제필요경비율 60%와 비교하여 큰 금액 적용)</li>
</ul>

<strong>(4) 종합소득공제</strong>
<ul>
<li>본인 기본공제: 1,500,000원</li>
<li>배우자 기본공제: 1,500,000원 (소득 없음)</li>
<li>자녀 2명 기본공제 (8세, 12세): 각 1,500,000원</li>
<li>국민연금보험료: 4,800,000원</li>
<li>건강보험료: 3,200,000원 (특별소득공제)</li>
</ul>

<strong>(5) 종합소득세율 (2026년 적용)</strong>
<ul>
<li>1,400만원 이하: 6%</li>
<li>1,400만원 초과 5,000만원 이하: 84만원 + 1,400만원 초과액 × 15%</li>
<li>5,000만원 초과 8,800만원 이하: 624만원 + 5,000만원 초과액 × 24%</li>
<li>8,800만원 초과 1억 5천만원 이하: 1,536만원 + 8,800만원 초과액 × 35%</li>
<li>1억 5천만원 초과 3억원 이하: 3,706만원 + 1억 5천만원 초과액 × 38%</li>
</ul>
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 사업소득금액 계산 (대표자 급여·차량유지비 부인)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
사업주 본인의 급여는 필요경비 불산입(소득세법 §33), 업무전용보험 미가입 차량의 차량유지비는 전액 손금부인.

<pre>
사업소득금액 = 총수입금액 - (필요경비 - 부인액)
            = 850,000,000 - (612,000,000 - 36,000,000 - 8,000,000)
            = 850,000,000 - 568,000,000
            = 282,000,000원
</pre>

**중간 답 = 282,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>2</span>
      <span class='calc-step-title'>2단계 — 근로소득금액 및 기타소득금액 계산</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
**근로소득공제**
<pre>
공제액 = 12,475,000 + (78,000,000 - 75,000,000) × 5%
      = 12,475,000 + 150,000
      = 12,625,000원

근로소득금액 = 78,000,000 - 12,625,000 = 65,375,000원
</pre>

**기타소득금액 (의제필요경비 60% vs 실제 비교)**
<pre>
의제필요경비 = 20,000,000 × 60% = 12,000,000원
실제 필요경비 = 3,000,000원
→ 큰 금액인 12,000,000원 적용

기타소득금액 = 20,000,000 - 12,000,000 = 8,000,000원
</pre>

**중간 답: 근로 65,375,000원 / 기타 8,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>3</span>
      <span class='calc-step-title'>3단계 — 종합소득금액 합산</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
기타소득금액 8,000,000원 > 3,000,000원이므로 **종합과세 대상**(분리과세 선택 불가).

<pre>
종합소득금액 = 사업소득금액 + 근로소득금액 + 기타소득금액
           = 282,000,000 + 65,375,000 + 8,000,000
           = 355,375,000원
</pre>

**중간 답 = 355,375,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>4</span>
      <span class='calc-step-title'>4단계 — 종합소득공제 및 과세표준</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
<pre>
인적공제 = 본인 1,500,000 + 배우자 1,500,000 + 자녀 2명 × 1,500,000
       = 6,000,000원

연금보험료공제 = 4,800,000원
특별소득공제(건강보험료) = 3,200,000원

종합소득공제 합계 = 6,000,000 + 4,800,000 + 3,200,000 = 14,000,000원

과세표준 = 종합소득금액 - 종합소득공제
       = 355,375,000 - 14,000,000
       = 341,375,000원
</pre>

**중간 답 = 341,375,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>5</span>
      <span class='calc-step-title'>5단계 — 산출세액 계산 (1.5억 초과 3억 이하 구간)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
과세표준 341,375,000원 → 3억원 초과 5억원 이하 구간 적용 (3억 초과 5억 이하: 9,406만원 + 3억 초과액 × 40%).

<pre>
산출세액 = 94,060,000 + (341,375,000 - 300,000,000) × 40%
       = 94,060,000 + 41,375,000 × 40%
       = 94,060,000 + 16,550,000
       = 110,610,000원
</pre>

**중간 답 = 110,610,000원**
  </div>
</div>

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>종합소득 산출세액 = 110,610,000원</div>
</div>
