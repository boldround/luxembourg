---
layout: calculation
title: "[원가관리] 결합원가 배부 + 추가가공 의사결정"
date: 2026-05-19 06:30:00 +0900
categories: [calculation]
subject: [accounting1]
topics: [원가관리, 결합원가, 순실현가치법, 추가가공의사결정]
difficulty: 상
applied_date: "2026-05-19"
---

<div class='question-block'>
<strong>[문제]</strong> ㈜한라는 단일 공정에서 결합원료를 투입하여 결합제품 A, B, C를 동시에 생산한다. 2026년 5월 한 달 동안의 자료는 다음과 같다.

<br><br>
<strong>(1) 결합공정 자료</strong>
<ul>
<li>직접재료원가: 240,000,000원</li>
<li>직접노무원가: 180,000,000원</li>
<li>제조간접원가: 180,000,000원</li>
<li>분리점까지의 결합원가 합계: 600,000,000원</li>
</ul>

<strong>(2) 분리점 시점의 생산량 및 단위당 판매가격</strong>
<table>
<tr><th>제품</th><th>생산량(kg)</th><th>분리점 단위당 판매가</th><th>추가가공원가 총액</th><th>최종 단위당 판매가</th></tr>
<tr><td>A</td><td>100,000</td><td>3,000원</td><td>120,000,000원</td><td>5,000원</td></tr>
<tr><td>B</td><td>200,000</td><td>2,500원</td><td>200,000,000원</td><td>3,500원</td></tr>
<tr><td>C</td><td>150,000</td><td>1,200원</td><td>50,000,000원</td><td>1,600원</td></tr>
</table>

<strong>(3) 추가 정보</strong>
<ul>
<li>회사는 분리점 이후 모든 제품을 추가가공하여 판매하는 방안을 검토 중이다.</li>
<li>5월 중 생산량은 전량 판매되며, 기초·기말재공품 및 재고자산은 없다.</li>
<li>결합원가는 <strong>순실현가치법(NRV)</strong>으로 배부한다.</li>
</ul>

<strong>[요구사항]</strong>
<ol>
<li>모든 제품을 추가가공하여 판매한다고 가정할 때, 순실현가치법에 따라 제품 A, B, C에 배부될 결합원가를 각각 계산하시오.</li>
<li>각 제품에 대하여 추가가공 여부 의사결정을 수행하고, 회사 전체의 최적 영업이익을 계산하시오.</li>
</ol>
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 제품별 순실현가치(NRV) 산출</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
NRV = (최종판매가 × 생산량) − 추가가공원가
<pre>
A : 5,000 × 100,000 − 120,000,000
  = 500,000,000 − 120,000,000 = 380,000,000원
B : 3,500 × 200,000 − 200,000,000
  = 700,000,000 − 200,000,000 = 500,000,000원
C : 1,600 × 150,000 − 50,000,000
  = 240,000,000 − 50,000,000  = 190,000,000원
─────────────────────────────────────────
NRV 합계                       1,070,000,000원
</pre>
<strong>중간 답 = NRV 합계 1,070,000,000원</strong>
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>2</span>
      <span class='calc-step-title'>2단계 — 순실현가치법에 따른 결합원가 배부</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
배부액 = 결합원가 600,000,000 × (개별 NRV ÷ NRV 합계)
<pre>
A : 600,000,000 × (380,000,000 / 1,070,000,000)
  = 600,000,000 × 0.355140 ≒ 213,084,112원
B : 600,000,000 × (500,000,000 / 1,070,000,000)
  = 600,000,000 × 0.467290 ≒ 280,373,832원
C : 600,000,000 × (190,000,000 / 1,070,000,000)
  = 600,000,000 × 0.177570 ≒ 106,542,056원
─────────────────────────────────────────
배부액 합계                        600,000,000원
</pre>
<strong>중간 답 = A 213,084,112 / B 280,373,832 / C 106,542,056원</strong>
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>3</span>
      <span class='calc-step-title'>3단계 — 추가가공 여부 의사결정 (증분분석)</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
의사결정 핵심: 결합원가는 매몰원가이므로 무관. <br>
증분이익 = 추가가공 후 매출 − 분리점 매출 − 추가가공원가
<pre>
A : (5,000−3,000) × 100,000 − 120,000,000
  = 200,000,000 − 120,000,000 = +80,000,000원 → 추가가공 ○
B : (3,500−2,500) × 200,000 − 200,000,000
  = 200,000,000 − 200,000,000 =          0원 → 무차별(현 상태 유지/즉시판매)
C : (1,600−1,200) × 150,000 − 50,000,000
  =  60,000,000 − 50,000,000 = +10,000,000원 → 추가가공 ○
</pre>
<strong>중간 답: A 추가가공, B 즉시판매(또는 무차별), C 추가가공</strong>
  </div>
</div>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>4</span>
      <span class='calc-step-title'>4단계 — 최적 의사결정 하의 회사 전체 영업이익</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
B는 추가가공·즉시판매 모두 매출 700,000,000원으로 동일한 결과지만, 위험·자원 절약 측면에서 분리점 즉시판매를 선택한다고 가정한다.
<pre>
매출 합계
 A(추가가공) : 5,000 × 100,000 = 500,000,000
 B(즉시판매) : 2,500 × 200,000 = 500,000,000
 C(추가가공) : 1,600 × 150,000 = 240,000,000
 ─────────────────────────────────────────
 매출 합계                    1,240,000,000원

총원가
 결합원가              600,000,000
 추가가공원가 A        120,000,000
 추가가공원가 C         50,000,000
 ─────────────────────────────────────────
 총원가                      770,000,000원

영업이익 = 1,240,000,000 − 770,000,000 = 470,000,000원
</pre>
<strong>중간 답 = 영업이익 470,000,000원</strong>
  </div>
</div>

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>
[요구사항 1] 결합원가 배부액 — A 213,084,112원 / B 280,373,832원 / C 106,542,056원<br>
[요구사항 2] 최적 의사결정 — A·C는 추가가공, B는 분리점 즉시판매(추가가공 시 무차별)<br>
회사 전체 최적 영업이익 = <strong>470,000,000원</strong>
  </div>
</div>
