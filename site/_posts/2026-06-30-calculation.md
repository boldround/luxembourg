---
layout: calculation
title: "[회계학2부] 소득세 — 종합소득금액부터 산출세액까지 (거주자 종합과세)"
date: 2026-06-30 09:00:00 +0900
categories: [calculation]
subject: [accounting2]
topics: [소득세, 종합소득금액, 과세표준, 산출세액, 종합소득공제]
difficulty: 중상
applied_date: "2026-06-30"
---

종합과세 대상 소득을 가려내고, 종합소득금액 → 종합소득공제 → 과세표준 → 산출세액으로 이어지는 한 줄기를 끝까지 계산하는 문제입니다. 실무에서 가장 자주 틀리는 지점은 **금융소득 종합과세 여부 판단**과 **근로소득공제·기타소득 필요경비 의제율 적용**입니다.

<div class='question-block'>
<strong>[문제]</strong>

거주자 갑(남, 50세)의 2026년 귀속 종합소득 관련 자료는 다음과 같다. 자료에 제시된 금액은 모두 당해 과세기간(2026.1.1.~2026.12.31.) 중 발생·수령한 것이며, 원천징수는 적법하게 이루어졌다. 갑의 <strong>종합소득 산출세액</strong>을 계산하시오.

<strong>(1) 근로소득</strong>
- (주)대한에서 받은 총급여액: 80,000,000원 (비과세소득 제외 후 금액)

<strong>(2) 사업소득</strong>
- 부동산임대업 외 사업소득금액(필요경비 차감 후): 50,000,000원

<strong>(3) 금융소득</strong>
- 내국법인으로부터 받은 이자소득: 12,000,000원
- 내국법인으로부터 받은 현금배당(Gross-up 대상): 6,000,000원
- 위 금융소득은 모두 적법하게 14% 원천징수되었다.

<strong>(4) 기타소득</strong>
- 일시적 강연료 수입금액: 10,000,000원 (실제 필요경비는 없으며, 의제필요경비를 적용한다)
- 갑은 기타소득에 대해 종합과세를 선택할 수 있는 경우 종합과세한다.

<strong>(5) 종합소득공제 관련 부양가족 (모두 생계를 같이 하며 소득 없음)</strong>
- 배우자(48세)
- 자녀 A(20세, 장애인)
- 자녀 B(15세)
- 본인이 납부한 국민연금보험료(본인부담분): 4,000,000원

<em>※ 근로소득공제율: 4,500만원 초과 1억원 이하 → 1,200만원 + (총급여 − 4,500만원) × 5%</em>
<em>※ 강연료 의제필요경비율: 60%</em>
<em>※ 2026년 종합소득세 기본세율(과세표준 8,800만원 초과 1.5억원 이하): 35%, 누진공제 1,544만원</em>
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 종합과세 대상 소득의 선별 (금융소득 분리과세 판단)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
금융소득(이자 + 배당)의 합계가 2,000만원을 초과하는 경우에만 종합과세하고, 2,000만원 이하이면 14% 원천징수로 납세의무가 종결(분리과세)된다.

<pre>
금융소득 합계 = 이자 12,000,000 + 배당 6,000,000
            = 18,000,000원  ≤  20,000,000원
→ 분리과세 (종합소득금액에 합산하지 않음)
</pre>

또한 배당가산액(Gross-up)도 종합과세되는 경우에만 적용되므로, 여기서는 적용하지 않는다.

**중간 결론 = 금융소득 18,000,000원은 종합소득금액에서 제외**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>2</span>
      <span class='calc-step-title'>2단계 — 각 소득금액 산출 (근로소득금액 · 기타소득금액)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
<strong>① 근로소득금액 = 총급여 − 근로소득공제</strong>
<pre>
근로소득공제 = 12,000,000 + (80,000,000 − 45,000,000) × 5%
           = 12,000,000 + 35,000,000 × 5%
           = 12,000,000 + 1,750,000
           = 13,750,000원

근로소득금액 = 80,000,000 − 13,750,000 = 66,250,000원
</pre>

<strong>② 기타소득금액 = 수입금액 − 의제필요경비(60%)</strong>
<pre>
기타소득금액 = 10,000,000 × (1 − 60%)
           = 10,000,000 × 40%
           = 4,000,000원

판단: 기타소득금액 4,000,000원 > 3,000,000원
→ 종합과세 대상 (300만원 초과 시 종합과세)
</pre>

**근로소득금액 = 66,250,000원, 기타소득금액 = 4,000,000원**
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
1·2단계에서 가려낸 종합과세 대상 소득금액을 합산한다.

<pre>
종합소득금액 = 근로소득금액 + 사업소득금액 + 기타소득금액
          = 66,250,000 + 50,000,000 + 4,000,000
          = 120,250,000원
(금융소득 18,000,000원은 분리과세 → 합산 제외)
</pre>

**종합소득금액 = 120,250,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>4</span>
      <span class='calc-step-title'>4단계 — 종합소득공제 계산 (인적공제 + 연금보험료공제)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
<strong>① 기본공제 (1인당 1,500,000원)</strong>
<pre>
대상: 본인 + 배우자 + 자녀A + 자녀B = 4명
   (배우자·자녀 모두 소득 없음 → 요건 충족)
기본공제 = 4명 × 1,500,000 = 6,000,000원
</pre>

<strong>② 추가공제 — 장애인공제 (1인당 2,000,000원)</strong>
<pre>
대상: 자녀A(장애인) 1명
장애인공제 = 1 × 2,000,000 = 2,000,000원
</pre>

<strong>③ 연금보험료공제 (국민연금 본인부담분 전액)</strong>
<pre>
연금보험료공제 = 4,000,000원
</pre>

<pre>
종합소득공제 합계 = 6,000,000 + 2,000,000 + 4,000,000
              = 12,000,000원
</pre>

**종합소득공제 = 12,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>5</span>
      <span class='calc-step-title'>5단계 — 과세표준 → 산출세액</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
<strong>① 과세표준 = 종합소득금액 − 종합소득공제</strong>
<pre>
과세표준 = 120,250,000 − 12,000,000 = 108,250,000원
</pre>

<strong>② 산출세액 = 과세표준 × 세율 − 누진공제</strong>
과세표준 108,250,000원은 「8,800만원 초과 1.5억원 이하」 구간 → 세율 35%, 누진공제 15,440,000원
<pre>
산출세액 = 108,250,000 × 35% − 15,440,000
       = 37,887,500 − 15,440,000
       = 22,447,500원
</pre>

**과세표준 = 108,250,000원, 산출세액 = 22,447,500원**
  </div>
</div>

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>종합소득 산출세액 = 22,447,500원</div>
</div>

> **채점 포인트**
> - 금융소득 18,000,000원을 2,000만원 이하로 보고 **분리과세 처리(합산 제외)** 했는가 — 이것을 합산하면 과세표준·세율 구간이 통째로 달라진다.
> - 기타소득금액 4,000,000원이 **300만원 초과**임을 근거로 종합과세 대상으로 판단했는가.
> - 근로소득공제 구간(4,500만~1억) 산식을 정확히 적용했는가.
> - 장애인공제(추가공제)와 국민연금 본인부담분 전액공제를 빠뜨리지 않았는가.
