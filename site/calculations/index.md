---
layout: default
title: "계산 문제"
show_filters: true
---

# 계산 문제

회계학 1·2부 계산문제를 단계별 풀이와 함께 누적합니다.

<ul class="post-list">
{% assign calcs = site.posts | where_exp: "p", "p.categories contains 'calculation'" %}
{% for post in calcs %}
  <li data-subjects="{{ post.subject | join: ' ' }}">
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      <span>{{ post.date | date: "%Y.%m.%d" }}</span>
      {% for subj in post.subject %}
        {% case subj %}
          {% when 'accounting1' %}<span class="tag tag-acc1">회계1</span>
          {% when 'accounting2' %}<span class="tag tag-acc2">회계2</span>
        {% endcase %}
      {% endfor %}
      {% if post.difficulty %}<span class="badge">{{ post.difficulty }}</span>{% endif %}
      {% if post.applied_date %}<span class="applied-date">적용 {{ post.applied_date }}</span>{% endif %}
    </div>
    {% if post.excerpt %}<div class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 25 }}</div>{% endif %}
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">아직 누적된 계산 문제가 없습니다.</span></li>
{% endfor %}
</ul>
