---
layout: default
title: People
permalink: /people/
description: "Members and alumni of the Knapen Lab."
---
{%- assign people = site.people | sort: "order" -%}
{%- assign pis = people | where: "status", "pi" -%}
{%- assign current = people | where: "status", "current" -%}
{%- assign unsorted = people | where_exp: "p", "p.status == nil" -%}
{%- assign alumni = people | where: "status", "alumni" -%}
<div class="wrap people-page">
  <header class="page-header page-header-wide">
    <h1 class="page-title">People</h1>
  </header>

  {%- for p in pis %}
  {%- assign parts = p.title | split: " " %}
  {%- assign body = p.content | strip_html | strip %}
  <section class="pi-block" aria-label="Principal investigator">
    <div class="person-photo person-photo-large">
      {%- if p.photo %}
      <img src="{{ p.photo | relative_url }}" alt="Portrait of {{ p.title }}" width="400" height="500" decoding="async">
      {%- else %}
      <span class="initials" aria-hidden="true">{{ parts.first | slice: 0 }}{{ parts.last | slice: 0 }}</span>
      {%- endif %}
    </div>
    <div class="pi-text">
      <h2 class="pi-name">{% if body != "" %}<a href="{{ p.url | relative_url }}">{{ p.title }}</a>{% else %}{{ p.title }}{% endif %}</h2>
      {%- if p.role and p.role != "" %}<p class="person-role-large">{{ p.role }}</p>{% endif %}
      {%- if p.description %}<p class="pi-desc">{{ p.description }}</p>{% endif %}
      {% include person-links.html links=p.links label="Links" %}
      {%- if body != "" %}
      <p><a class="more-link" href="{{ p.url | relative_url }}">Biography and publications<span class="visually-hidden"> of {{ p.title }}</span></a></p>
      {%- endif %}
    </div>
  </section>
  {%- endfor %}

  {%- assign members = current | concat: unsorted %}
  {%- if members.size > 0 %}
  <section class="section-block" aria-labelledby="current-heading">
    <h2 id="current-heading">Current members</h2>
    <div class="grid grid-people">
      {%- for p in members %}
      {% include person-card.html person=p hlevel=3 %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  {%- if alumni.size > 0 %}
  <section class="section-block" aria-labelledby="alumni-heading">
    <h2 id="alumni-heading">Alumni</h2>
    <table class="alumni-table">
      <thead>
        <tr><th scope="col">Name</th><th scope="col">Role in the lab</th><th scope="col">Years</th><th scope="col">Now</th></tr>
      </thead>
      <tbody>
        {%- for p in alumni %}
        {%- assign body = p.content | strip_html | strip %}
        <tr>
          <th scope="row">{% if body != "" %}<a href="{{ p.url | relative_url }}">{{ p.title }}</a>{% else %}{{ p.title }}{% endif %}</th>
          <td data-label="Role">{{ p.role }}</td>
          <td data-label="Years">{% if p.start %}{{ p.start }}{% if p.end and p.end != "" %}–{{ p.end }}{% endif %}{% endif %}</td>
          <td data-label="Now">{{ p.now }}</td>
        </tr>
        {%- endfor %}
      </tbody>
    </table>
  </section>
  {%- endif %}

  <p class="people-join">Interested in joining? See <a href="{{ '/join/' | relative_url }}">Join the lab</a>.</p>
</div>
