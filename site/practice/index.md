---
layout: default
title: "논술 답안"
show_filters: true
---

# 논술 답안

세법학 1·2부 논술형 모범답안을 누적합니다. 판례·통칙 핵심구절 인용 중심.

<ul class="post-list">
{% assign p_list = site.posts | where_exp: "p", "p.categories contains 'practice'" %}
{% for post in p_list %}
  <li data-subjects="{{ post.subject | join: ' ' }}">
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      <span>{{ post.date | date: "%Y.%m.%d" }}</span>
      {% for subj in post.subject %}
        {% case subj %}
          {% when 'tax_law1' %}<span class="tag tag-tax1">세법1</span>
          {% when 'tax_law2' %}<span class="tag tag-tax2">세법2</span>
        {% endcase %}
      {% endfor %}
      {% if post.applied_date %}<span class="applied-date">적용 {{ post.applied_date }}</span>{% endif %}
    </div>
    {% if post.excerpt %}<div class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 25 }}</div>{% endif %}
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">아직 누적된 논술 답안이 없습니다.</span></li>
{% endfor %}
</ul>
