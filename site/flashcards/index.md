---
layout: default
title: "암기 카드"
---

# 암기 카드

조문 / 판례 핵심구절 / 통칙·예규를 카드로 누적합니다. 카드 탭 또는 스와이프로 답 확인.

<ul class="post-list">
{% assign fc_list = site.posts | where_exp: "p", "p.categories contains 'flashcard'" %}
{% for post in fc_list %}
  <li>
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta">
      <span>{{ post.date | date: "%Y.%m.%d" }}</span>
      <span class="badge">{{ post.cards | size }}장</span>
      {% for subj in post.subject %}
        {% case subj %}
          {% when 'accounting1' %}<span class="tag tag-acc1">회계1</span>
          {% when 'accounting2' %}<span class="tag tag-acc2">회계2</span>
          {% when 'tax_law1' %}<span class="tag tag-tax1">세법1</span>
          {% when 'tax_law2' %}<span class="tag tag-tax2">세법2</span>
        {% endcase %}
      {% endfor %}
    </div>
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">아직 누적된 암기 카드가 없습니다.</span></li>
{% endfor %}
</ul>
