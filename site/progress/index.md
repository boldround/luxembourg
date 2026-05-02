---
layout: default
title: "회독 트래커"
---

# 회독 트래커

8과목 진도와 약점 진단. (실제 데이터 연결은 P1 단계에서 — 현재는 placeholder.)

## 2차 과목 (2026 7/18 시험)

<table>
<thead>
<tr><th>과목</th><th>회독수</th><th>최근 학습</th><th>정답률</th></tr>
</thead>
<tbody>
<tr><td><span class="tag tag-acc1">회계학 1부</span></td><td>0회</td><td>—</td><td>—</td></tr>
<tr><td><span class="tag tag-acc2">회계학 2부</span></td><td>0회</td><td>—</td><td>—</td></tr>
<tr><td><span class="tag tag-tax1">세법학 1부</span></td><td>0회</td><td>—</td><td>—</td></tr>
<tr><td><span class="tag tag-tax2">세법학 2부</span></td><td>0회</td><td>—</td><td>—</td></tr>
</tbody>
</table>

## 1차 과목 (2027 4/24 시험)

<table>
<thead>
<tr><th>과목</th><th>회독수</th><th>최근 학습</th><th>정답률</th></tr>
</thead>
<tbody>
<tr><td>재정학</td><td>0회</td><td>—</td><td>—</td></tr>
<tr><td>세법학개론</td><td>0회</td><td>—</td><td>—</td></tr>
<tr><td>회계학개론</td><td>0회</td><td>—</td><td>—</td></tr>
<tr><td>행정소송법 (선택)</td><td>0회</td><td>—</td><td>—</td></tr>
</tbody>
</table>

## 주간 회독 리포트

<ul class="post-list">
{% assign weekly = site.posts | where_exp: "p", "p.categories contains 'weekly'" %}
{% for post in weekly %}
  <li>
    <div class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></div>
    <div class="post-meta"><span>{{ post.date | date: "%Y.%m.%d" }}</span></div>
  </li>
{% else %}
  <li><span style="color:var(--text-muted);">아직 주간 리포트가 없습니다 — 매주 토요일 자동 생성 예정.</span></li>
{% endfor %}
</ul>
