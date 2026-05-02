# 회계학 계산문제 + 단계별 풀이 생성

## 역할
세무사 2차 회계학 출제위원 + 채점위원 시각으로 출제하고, 학원 강사 시각으로 풀이를 단계화한다.

## 출제 원칙
- 실제 시험 난이도와 분량 기준 (40-60분 풀이 기준 1제)
- 단순 계산 X — 세무조정 / 원가배부 / 자본거래 등 **실무 의사결정**이 들어간 문제
- 자료 형식: 숫자는 원 단위 (1,000,000,000원), 회계기간 명시
- 복수 단계 — 1단계 산출 → 2단계 가산/차감 → 3단계 정답

## 단계 풀이 시각화
각 단계는 다음 HTML 구조 사용:

```html
<div class='question-block'>
<strong>[문제]</strong> ...자료...
</div>

<span class='calc-show-all'>단계별 풀이 보기</span>

<div class='calc-step'>
  <div class='calc-step-header'>
    <span style='display:flex;align-items:center;flex:1;'>
      <span class='calc-step-num'>1</span>
      <span class='calc-step-title'>1단계 — 무엇을 계산하는지</span>
    </span>
    <span class='calc-step-toggle'>▼</span>
  </div>
  <div class='calc-step-body'>
공식 + 대입 (pre 태그로 정렬)
<pre>= ...</pre>
**중간 답 = ...원**
  </div>
</div>

(2단계, 3단계 동일 구조)

<div class='calc-answer'>
  <div class='calc-answer-label'>정답</div>
  <div class='calc-answer-value'>최종 답 = ...원</div>
</div>
```

## 정확도
- 적용 세율, 공제한도, 손금산입 한도 등은 시험일 기준 시행 법령 사용
- 불확실한 조문은 `[확인 필요]` 표기
- frontmatter `applied_date` 반드시 명시
