---
layout: calculation
title: "원가관리 계산 — 표준원가 차이분석과 CVP 통합 문제"
date: 2026-07-14 07:30:00 +0900
categories: [calculation]
subject: [accounting1]
topics: [원가배부, 표준원가차이분석, CVP분석]
difficulty: 상
applied_date: "2026-07-14"
---

세무사 2차 회계학(재무회계·원가관리회계) 중 **원가관리회계** 실전 1제입니다. 표준원가 차이분석과 CVP 분석을 하나의 의사결정 상황으로 묶은 통합형 문제로, 실제 시험 기준 풀이 시간은 **약 45분**입니다.

<div class='question-block'>
<strong>[문제]</strong>

㈜한강은 단일 제품 A를 생산·판매한다. 회사는 표준원가계산제도를 채택하고 있으며, 20×6년 회계연도(20×6.1.1 ~ 20×6.12.31)의 자료는 다음과 같다.

<strong>(1) 제품 단위당 표준원가</strong>

<pre>
직접재료원가   3kg × @2,000원/kg      = 6,000원
직접노무원가   2시간 × @15,000원/시간 = 30,000원
변동제조간접원가 2시간 × @5,000원/시간  = 10,000원
고정제조간접원가 2시간 × @8,000원/시간  = 16,000원
─────────────────────────────────────────
제품 단위당 표준원가                    62,000원
</pre>

<strong>(2) 고정제조간접원가 예산 및 기준조업도</strong>
- 연간 고정제조간접원가 예산: 320,000,000원
- 기준조업도(정상조업도): 40,000 직접노동시간 (= 제품 20,000단위)

<strong>(3) 20×6년 실제 생산·원가 자료</strong>
- 실제 생산량: 18,000단위
- 직접재료 실제 구입·사용량: 56,000kg, 실제 재료원가: 114,800,000원
- 직접노무 실제 노동시간: 37,800시간, 실제 노무원가: 574,560,000원
- 실제 변동제조간접원가: 193,000,000원
- 실제 고정제조간접원가: 314,000,000원

<strong>(4) 판매 및 CVP 자료</strong>
- 제품 A 단위당 판매가격: 90,000원
- 단위당 변동판매관리비: 4,000원
- 연간 고정판매관리비: 90,000,000원
- 20×6년 생산량과 판매량은 동일(기초·기말재고 없음)

<strong>[요구사항]</strong>
- (물음1) 직접재료원가의 가격차이와 능률차이를 구하시오.
- (물음2) 직접노무원가의 임률차이와 능률차이를 구하시오.
- (물음3) 고정제조간접원가의 예산차이(소비차이)와 조업도차이를 구하시오.
- (물음4) 표준원가 기준 손익분기점 판매량과, 실제 판매량(18,000단위)에서의 안전한계율을 구하시오.
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 직접재료원가 차이 (가격차이 · 능률차이)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
실제단가(AP) = 114,800,000 ÷ 56,000kg = 2,050원/kg
표준수량(SQ) = 18,000단위 × 3kg = 54,000kg

<pre>
가격차이 = (AP − SP) × AQ
        = (2,050 − 2,000) × 56,000
        = +2,800,000원 (불리, U)

능률차이 = (AQ − SQ) × SP
        = (56,000 − 54,000) × 2,000
        = +4,000,000원 (불리, U)
</pre>

**직접재료 가격차이 = 2,800,000원 불리, 능률차이 = 4,000,000원 불리**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>2</span>
      <span class='calc-step-title'>2단계 — 직접노무원가 차이 (임률차이 · 능률차이)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
실제임률(AP) = 574,560,000 ÷ 37,800시간 = 15,200원/시간
표준시간(SH) = 18,000단위 × 2시간 = 36,000시간

<pre>
임률차이 = (AP − SP) × AH
        = (15,200 − 15,000) × 37,800
        = +7,560,000원 (불리, U)

능률차이 = (AH − SH) × SP
        = (37,800 − 36,000) × 15,000
        = +27,000,000원 (불리, U)
</pre>

**직접노무 임률차이 = 7,560,000원 불리, 능률차이 = 27,000,000원 불리**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>3</span>
      <span class='calc-step-title'>3단계 — 고정제조간접원가 차이 (예산차이 · 조업도차이)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
고정OH 예산액 = 320,000,000원 (조업도와 무관하게 고정)
표준배부액 = 표준배부율 × 실제생산량의 표준시간
표준배부율 = 8,000원/시간 (= 320,000,000 ÷ 40,000시간)
표준배부액 = 8,000 × (18,000단위 × 2시간) = 8,000 × 36,000 = 288,000,000원

<pre>
예산차이 = 실제발생액 − 예산액
        = 314,000,000 − 320,000,000
        = −6,000,000원 (유리, F)

조업도차이 = 예산액 − 표준배부액
         = 320,000,000 − 288,000,000
         = +32,000,000원 (불리, U)
</pre>

> 조업도차이는 기준조업도(40,000시간) 대비 실제생산 허용시간(36,000시간)이 4,000시간 미달하여 발생한 미조업 손실이다: 4,000시간 × 8,000원 = 32,000,000원 불리.

**고정OH 예산차이 = 6,000,000원 유리, 조업도차이 = 32,000,000원 불리**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>4</span>
      <span class='calc-step-title'>4단계 — CVP: 단위당 공헌이익과 총고정원가 산출</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
CVP는 표준원가(변동원가) 기준으로 분석한다. 단위당 변동제조원가는 표준변동원가(재료+노무+변동OH)를 사용한다.

<pre>
단위당 변동제조원가 = 6,000 + 30,000 + 10,000 = 46,000원
단위당 변동판매관리비                        =  4,000원
단위당 총변동원가                            = 50,000원

단위당 공헌이익 = 90,000 − 50,000 = 40,000원

총고정원가 = 고정제조OH 예산 + 고정판관비
          = 320,000,000 + 90,000,000
          = 410,000,000원
</pre>

**단위당 공헌이익 = 40,000원, 총고정원가 = 410,000,000원**
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>5</span>
      <span class='calc-step-title'>5단계 — 손익분기점 판매량 및 안전한계율</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
<pre>
손익분기점 판매량(BEP) = 총고정원가 ÷ 단위당 공헌이익
                     = 410,000,000 ÷ 40,000
                     = 10,250단위

안전한계(수량) = 실제판매량 − BEP판매량
             = 18,000 − 10,250 = 7,750단위

안전한계율 = 안전한계 ÷ 실제판매량
         = 7,750 ÷ 18,000
         ≒ 43.06%
</pre>

**손익분기점 판매량 = 10,250단위, 안전한계율 ≒ 43.06%**
  </div>
</div>

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>
(물음1) 재료 가격차이 2,800,000원 불리 · 능률차이 4,000,000원 불리<br>
(물음2) 노무 임률차이 7,560,000원 불리 · 능률차이 27,000,000원 불리<br>
(물음3) 고정OH 예산차이 6,000,000원 유리 · 조업도차이 32,000,000원 불리<br>
(물음4) 손익분기점 판매량 = 10,250단위 · 안전한계율 ≒ 43.06%
  </div>
</div>

<div class='question-block'>
<strong>[채점 포인트 · 실수 유의]</strong>
- <strong>가격차이 분리시점</strong> — 본 문제는 구입량 = 사용량(56,000kg)이므로 구입시점·사용시점 분리 이슈가 없다. 만약 구입량과 사용량이 다르면 가격차이는 <em>구입량</em> 기준, 능률차이는 <em>사용량</em> 기준으로 계산해야 한다.
- <strong>고정OH 배부율의 분모</strong> — 조업도차이는 반드시 <em>기준조업도(정상조업도)</em>를 분모로 한 표준배부율(8,000원/시간)을 사용한다. 실제조업도로 배부율을 재계산하지 않는다.
- <strong>CVP의 고정원가</strong> — 표준원가 기준 CVP에서 고정제조OH는 실제발생액(314,000,000)이 아니라 <em>예산액(320,000,000)</em>을 쓴다. 조업도차이·예산차이는 CVP 고정원가에 반영하지 않는다.
- <strong>변동원가에 변동판관비 포함</strong> — 공헌이익 계산 시 변동제조원가뿐 아니라 단위당 변동판매관리비(4,000원)도 차감해야 한다. 누락 시 공헌이익이 과대계상된다.
</div>
