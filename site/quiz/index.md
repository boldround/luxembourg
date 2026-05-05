---
layout: default
title: "1차 모의고사"
permalink: /quiz/
---

<style>
  .exam1-tabs {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    margin: 0.5rem 0 1.2rem;
  }
  .exam1-tab {
    font-size: 0.74rem;
    padding: 0.4rem 0.8rem;
    border-radius: 16px;
    background: var(--pill-bg);
    color: var(--text-secondary);
    cursor: pointer;
    border: 1px solid transparent;
    user-select: none;
    min-height: 32px;
    display: inline-flex;
    align-items: center;
  }
  .exam1-tab:hover { border-color: var(--border); }
  .exam1-tab.active {
    background: var(--pill-active);
    color: var(--pill-active-text);
    border-color: var(--pill-active);
  }
</style>

# 1차 모의고사 / 단권화

세무사 1차 객관식 학습 자료. 4과목 (재정학·세법학개론·회계학개론·행정소송법)을 출퇴근 5-10분 단위로.

<div class="exam1-tabs">
  <span class="exam1-tab active" data-filter="all">전체</span>
  <span class="exam1-tab" data-filter="quiz">모의고사</span>
  <span class="exam1-tab" data-filter="summary">단권화</span>
  <span class="exam1-tab" data-filter="public_finance">재정학</span>
  <span class="exam1-tab" data-filter="tax_intro">세법학개론</span>
  <span class="exam1-tab" data-filter="accounting_intro">회계학개론</span>
  <span class="exam1-tab" data-filter="admin_litigation">행정소송법</span>
</div>

<ul class="post-list" id="exam1-list">
{% assign exam1_posts = site.posts | where_exp: "p", "p.categories contains 'quiz' or p.categories contains 'summary'" %}
{% for post in exam1_posts %}
  <li data-cats="{{ post.categories | join: ' ' }}" data-subjects="{{ post.subject | join: ' ' }}">
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      <span>{{ post.date | date: "%Y.%m.%d" }}</span>
      {% for cat in post.categories %}
        {% case cat %}
          {% when 'quiz' %}<span class="badge">모의고사</span>
          {% when 'summary' %}<span class="badge">단권화</span>
        {% endcase %}
      {% endfor %}
      {% for subj in post.subject %}
        {% case subj %}
          {% when 'public_finance' %}<span class="tag tag-acc1">재정학</span>
          {% when 'tax_intro' %}<span class="tag tag-tax1">세법학개론</span>
          {% when 'accounting_intro' %}<span class="tag tag-acc2">회계학개론</span>
          {% when 'admin_litigation' %}<span class="tag" style="background:var(--tag-default);color:#fff;">행정소송법</span>
        {% endcase %}
      {% endfor %}
      {% if post.questions %}<span class="badge">{{ post.questions | size }}문제</span>{% endif %}
      {% if post.applied_date %}<span class="applied-date">적용 {{ post.applied_date }}</span>{% endif %}
    </div>
    {% if post.excerpt %}<div class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 25 }}</div>{% endif %}
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">아직 누적된 1차 콘텐츠가 없습니다 — 일요일 파이프라인이 가동되면 자동 채워집니다.</span></li>
{% endfor %}
</ul>

<script>
(function() {
  var tabs = document.querySelectorAll('.exam1-tab');
  var items = document.querySelectorAll('#exam1-list li[data-cats]');
  tabs.forEach(function(tab) {
    tab.addEventListener('click', function() {
      tabs.forEach(function(t) { t.classList.remove('active'); });
      tab.classList.add('active');
      var f = tab.getAttribute('data-filter');
      items.forEach(function(li) {
        if (f === 'all') { li.style.display = ''; return; }
        var cats = li.getAttribute('data-cats') || '';
        var subs = li.getAttribute('data-subjects') || '';
        var hit = (cats.indexOf(f) !== -1) || (subs.indexOf(f) !== -1);
        li.style.display = hit ? '' : 'none';
      });
    });
  });
})();
</script>
