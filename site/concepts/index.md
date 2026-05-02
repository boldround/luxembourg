---
layout: default
title: "개념 정리"
show_filters: true
---

# 개념 정리

세법학 1·2부의 핵심 개념을 과목별로 누적합니다.

<ul class="post-list">
{% assign concepts = site.posts | where_exp: "p", "p.categories contains 'concept'" %}
{% for post in concepts %}
  <li data-subjects="{{ post.subject | join: ' ' }}">
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      <span>{{ post.date | date: "%Y.%m.%d" }}</span>
      {% for subj in post.subject %}
        {% case subj %}
          {% when 'tax_law1' %}<span class="tag tag-tax1">세법1</span>
          {% when 'tax_law2' %}<span class="tag tag-tax2">세법2</span>
          {% when 'accounting1' %}<span class="tag tag-acc1">회계1</span>
          {% when 'accounting2' %}<span class="tag tag-acc2">회계2</span>
        {% endcase %}
      {% endfor %}
      {% if post.applied_date %}<span class="applied-date">적용 {{ post.applied_date }}</span>{% endif %}
    </div>
    {% if post.excerpt %}<div class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 25 }}</div>{% endif %}
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">아직 누적된 개념 정리가 없습니다.</span></li>
{% endfor %}
</ul>
