---
layout: default
title: "개정 브리핑"
---

# 개정 브리핑

매일/매주 개정세법, 신규 예규, 주요 조세 판례를 정리합니다.

<ul class="post-list">
{% assign briefings = site.posts | where_exp: "p", "p.categories contains 'briefing'" %}
{% for post in briefings %}
  <li>
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      <span>{{ post.date | date: "%Y.%m.%d" }}</span>
      {% if post.applied_date %}<span class="applied-date">적용 {{ post.applied_date }}</span>{% endif %}
    </div>
    {% if post.excerpt %}<div class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 25 }}</div>{% endif %}
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">아직 누적된 브리핑이 없습니다.</span></li>
{% endfor %}
</ul>
