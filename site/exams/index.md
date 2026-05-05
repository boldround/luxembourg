---
layout: default
title: "기출문제 + 풀이"
show_filters: true
---

# 기출문제 + 풀이

세무사 2차 시험 4과목(회계학 1·2부, 세법학 1·2부)의 연도별 기출문제와 단계별 풀이·모범답안.

기출 원본은 한국산업인력공단 Q-Net 자료실에서 다운로드한 hwp/hwpx를 파싱한 것이며, 풀이는 Claude로 자동 생성 후 팩트체커 통과한 콘텐츠만 누적됨.

<div style="margin: 1.5rem 0; padding: 1rem; background: var(--pill-bg); border-radius: 8px; border: 1px dashed var(--border);">
<strong>학습 가이드</strong>
<ul style="margin-top: 0.5rem; margin-bottom: 0;">
  <li>각 연도별로 과목 4종 → 문제별 풀이</li>
  <li>풀이는 단계별 토글 — 답 보기 전 본인이 풀어보고 비교</li>
  <li>틀린 문제는 회독 트래커에 자동 기록 (P1 예정)</li>
</ul>
</div>

## 연도별

<ul class="post-list">
{% assign exams = site.posts | where_exp: "p", "p.categories contains 'exam'" | sort: 'exam_year' | reverse %}
{% for post in exams %}
  <li data-subjects="{{ post.subject | join: ' ' }}">
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      {% if post.exam_year %}<span class="badge">{{ post.exam_year }}년</span>{% endif %}
      {% if post.exam_round %}<span class="badge">제{{ post.exam_round }}회</span>{% endif %}
      {% if post.exam_type %}<span class="badge">{{ post.exam_type }}</span>{% endif %}
      {% for subj in post.subject %}
        {% case subj %}
          {% when 'accounting1' %}<span class="tag tag-acc1">회계1</span>
          {% when 'accounting2' %}<span class="tag tag-acc2">회계2</span>
          {% when 'tax_law1' %}<span class="tag tag-tax1">세법1</span>
          {% when 'tax_law2' %}<span class="tag tag-tax2">세법2</span>
        {% endcase %}
      {% endfor %}
      {% if post.problem_count %}<span class="badge">{{ post.problem_count }}문</span>{% endif %}
      {% if post.applied_date %}<span class="applied-date">적용 {{ post.applied_date }}</span>{% endif %}
    </div>
    {% if post.excerpt %}<div class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 30 }}</div>{% endif %}
  </li>
{% else %}
  <li>
    <span style="color:var(--text-muted);">
      아직 누적된 기출 풀이가 없습니다. <br>
      <code>data/exams/raw/{연도}/</code>에 hwp/hwpx 파일을 두고 파이프라인을 실행하면 자동으로 채워집니다.
    </span>
  </li>
{% endfor %}
</ul>

## 다운로드 안내

기출 원본 파일은 <a href="https://www.q-net.or.kr/cst003.do?id=cst00309&gSite=L&gId=22">한국산업인력공단 Q-Net 자료실</a>에서 받을 수 있습니다 (회차/연도별 hwp/hwpx).

받은 파일은 다음 위치에 두면 됩니다:

```
luxembourg/data/exams/raw/2024년/2024-2차-회계학1부.hwpx
                              /2024-2차-회계학2부.hwpx
                              /2024-2차-세법학1부.hwpx
                              /2024-2차-세법학2부.hwpx
                       /2023년/...
```

이후 파이프라인이 자동으로:
1. hwp/hwpx → markdown 파싱 (`hwpx_parser`)
2. 문제별로 분리
3. Claude CLI로 단계별 풀이·모범답안 생성
4. 팩트체커 통과 시 사이트 publish
