---
layout: default
title: News
permalink: /news/
description: "News from the Knapen Lab: papers, people, positions and datasets."
redirect_from:
  - /blog/
  - /blog/page2/
  - /blog/page3/
  - /blog/page4/
  - /blog/page5/
  - /blog/page6/
  - /blog/page7/
  - /blog/page8/
  - /blog/page9/
---
{%- assign by_year = site.posts | group_by_exp: "p", "p.date | date: '%Y'" -%}
<div class="wrap wrap-text news-page">
  <header class="page-header">
    <h1 class="page-title">News</h1>
    <p class="page-note">Also available as an <a href="{{ '/feed.xml' | relative_url }}">Atom feed</a>.</p>
  </header>
  {%- for group in by_year %}
  <section class="news-year" aria-labelledby="ny{{ group.name }}">
    <h2 id="ny{{ group.name }}">{{ group.name }}</h2>
    <ol class="news-list">
      {%- for post in group.items %}
      <li class="news-item{% if post.img %} has-thumb{% endif %}">
        <div class="news-text">
          <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d" }}</time>
          <h3 class="news-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
          {%- if post.description %}
          <p>{{ post.description }}</p>
          {%- endif %}
        </div>
        {%- if post.img %}
        <img class="news-thumb" src="{{ post.img | relative_url }}" alt="" loading="lazy" decoding="async">
        {%- endif %}
      </li>
      {%- endfor %}
    </ol>
  </section>
  {%- endfor %}
</div>
