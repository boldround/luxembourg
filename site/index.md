---
layout: default
title: "홈"
show_filters: true
---

<div class="dday-strip">
  <div>
    <div class="dday-number" id="dday-count"></div>
    <div class="dday-label">시험까지</div>
  </div>
  <div>
    <div class="dday-exam">2026년 7월 18일</div>
    <div class="dday-date">제63회 세무사 2차</div>
  </div>
</div>

<script>
(function() {
  var exam = new Date(2026, 6, 18);
  var now = new Date();
  now.setHours(0,0,0,0);
  var diff = Math.ceil((exam - now) / (1000*60*60*24));
  var el = document.getElementById('dday-count');
  if (el) el.textContent = 'D-' + diff;
})();
</script>

<div class="stats-strip">
  <div class="stat-item">
    <div class="stat-value" id="post-count">{{ site.posts | size }}</div>
    <div class="stat-label">학습 자료</div>
  </div>
  <div class="stat-item">
    <div class="stat-value">4+1</div>
    <div class="stat-label">2차 과목</div>
  </div>
  <div class="stat-item">
    <div class="stat-value">11주</div>
    <div class="stat-label">남은 기간</div>
  </div>
</div>

<div class="today-card">
  <h3>오늘 학습할 것</h3>
  <ul class="today-list">
    <li><span style="color:var(--text-muted);font-size:0.85rem;">아직 콘텐츠가 없습니다 — 파이프라인 가동 후 자동 채워집니다.</span></li>
  </ul>
</div>

<div class="quick-links">
  <a class="quick-link" href="{{ '/concepts/' | relative_url }}">
    <div class="ql-icon">📖</div>
    <div class="ql-title">개념 정리</div>
    <div class="ql-desc">세법학 핵심 개념</div>
  </a>
  <a class="quick-link" href="{{ '/calculations/' | relative_url }}">
    <div class="ql-icon">🧮</div>
    <div class="ql-title">계산 문제</div>
    <div class="ql-desc">회계학 단계별 풀이</div>
  </a>
  <a class="quick-link" href="{{ '/practice/' | relative_url }}">
    <div class="ql-icon">✏️</div>
    <div class="ql-title">논술 답안</div>
    <div class="ql-desc">세법학 모범답안</div>
  </a>
  <a class="quick-link" href="{{ '/flashcards/' | relative_url }}">
    <div class="ql-icon">🎴</div>
    <div class="ql-title">암기 카드</div>
    <div class="ql-desc">조문·판례 스와이프</div>
  </a>
  <a class="quick-link" href="{{ '/briefings/' | relative_url }}">
    <div class="ql-icon">📰</div>
    <div class="ql-title">개정 브리핑</div>
    <div class="ql-desc">세법·예규·판례</div>
  </a>
  <a class="quick-link" href="{{ '/progress/' | relative_url }}">
    <div class="ql-icon">📊</div>
    <div class="ql-title">회독 트래커</div>
    <div class="ql-desc">진도와 약점 진단</div>
  </a>
</div>

## 최신 자료

<ul class="post-list">
{% for post in site.posts limit:7 %}
  <li data-subjects="{{ post.subject | join: ' ' }}">
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      <span>{{ post.date | date: "%Y.%m.%d" }}</span>
      {% for cat in post.categories %}
        <span class="badge">
          {% case cat %}
            {% when 'briefing' %}브리핑
            {% when 'concept' %}개념
            {% when 'calculation' %}계산
            {% when 'practice' %}논술
            {% when 'flashcard' %}암기카드
            {% when 'weekly' %}주간 회독
            {% else %}{{ cat }}
          {% endcase %}
        </span>
      {% endfor %}
      {% for subj in post.subject %}
        {% case subj %}
          {% when 'accounting1' %}<span class="tag tag-acc1">회계1</span>
          {% when 'accounting2' %}<span class="tag tag-acc2">회계2</span>
          {% when 'tax_law1' %}<span class="tag tag-tax1">세법1</span>
          {% when 'tax_law2' %}<span class="tag tag-tax2">세법2</span>
        {% endcase %}
      {% endfor %}
      {% if post.applied_date %}
        <span class="applied-date">적용 {{ post.applied_date }}</span>
      {% endif %}
    </div>
    {% if post.excerpt %}
      <div class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 25 }}</div>
    {% endif %}
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">파이프라인 가동 전 — 콘텐츠가 누적되면 여기에 표시됩니다.</span></li>
{% endfor %}
</ul>
