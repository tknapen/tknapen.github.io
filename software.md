---
layout: default
title: Software & data
permalink: /software/
description: "Open-source software and datasets from the Knapen Lab, and the lab handbook."
redirect_from:
  - /resources/
  - /science/deconvolution/
---
{%- assign lab = site.data.lab -%}
{%- assign sw = site.data.software | where: "kind", "software" -%}
{%- assign ds = site.data.software | where: "kind", "dataset" -%}
<div class="wrap software-page">
  <header class="page-header page-header-wide">
    <h1 class="page-title">Software &amp; data</h1>
    <p class="page-lead">We share the code and data behind our papers.{% if lab.links.github_org and lab.links.github_org != "" %} Lab repositories are on GitHub in the <a href="{{ lab.links.github_org }}">VU-Cog-Sci organization</a>.{% endif %}</p>
  </header>

  {%- if sw.size > 0 %}
  <section class="section-block" aria-labelledby="sw-heading">
    <h2 id="sw-heading">Software</h2>
    <div class="grid grid-sw">
      {%- for item in sw %}
      {% include software-card.html item=item hlevel=3 %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  {%- if ds.size > 0 %}
  <section class="section-block" aria-labelledby="ds-heading">
    <h2 id="ds-heading">Datasets</h2>
    <div class="grid grid-sw">
      {%- for item in ds %}
      {% include software-card.html item=item hlevel=3 %}
      {%- endfor %}
    </div>
  </section>
  {%- endif %}

  <section class="section-block" aria-labelledby="handbook-heading">
    <h2 id="handbook-heading">Lab handbook</h2>
    {%- if lab.links.wiki and lab.links.wiki != "" %}
    <p class="section-note">How-tos for our data, analysis and lab procedures are on the <a href="{{ lab.links.wiki }}">lab wiki</a>. The pages below cover how we work together and write code.</p>
    {%- endif %}
    <ul class="handbook-list">
      {%- assign resources = site.resources | sort: "title" %}
      {%- for r in resources %}
      <li>
        <a href="{{ r.url | relative_url }}">{{ r.title }}</a>
        {%- if r.description %}<p>{{ r.description }}</p>{% endif %}
      </li>
      {%- endfor %}
    </ul>
  </section>
</div>
