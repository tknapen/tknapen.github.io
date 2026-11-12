---
layout: default
title: Publications
permalink: /publications/
description: "Publications of the Knapen Lab, with abstracts, links to articles, preprints, code and data."
---
{%- assign lab = site.data.lab -%}
{%- assign pubs = site.publications | sort: "date" | reverse -%}
{%- assign themes = site.research | sort: "order" -%}
{%- assign by_year = pubs | group_by_exp: "p", "p.date | date: '%Y'" %}
{%- comment -%} Publications per year for the small bar chart: oldest to newest year, including years without papers. {%- endcomment -%}
{%- assign first_year = by_year.last.name | plus: 0 -%}
{%- assign last_year = by_year.first.name | plus: 0 -%}
{%- assign max_count = 0 -%}{%- assign max_year = last_year -%}
{%- for g in by_year -%}{%- if g.items.size > max_count -%}{%- assign max_count = g.items.size -%}{%- assign max_year = g.name -%}{%- endif -%}{%- endfor -%}
{%- assign mid_year = first_year | plus: last_year | divided_by: 2 -%}
<div class="wrap pubs-page">
  <div class="pubs-intro">
  <header class="page-header page-header-wide">
    <h1 class="page-title">Publications</h1>
    <p class="page-lead">{{ pubs.size }} publications, newest first.</p>
    {%- assign has_scholar = false -%}{%- if lab.links.scholar and lab.links.scholar != "" -%}{%- assign has_scholar = true -%}{%- endif -%}
    {%- assign has_orcid = false -%}{%- if lab.links.orcid and lab.links.orcid != "" -%}{%- assign has_orcid = true -%}{%- endif -%}
    {%- if has_scholar or has_orcid %}
    <p class="page-note">{{ lab.pi | default: "The PI" }}'s profiles on {% if has_scholar %}<a href="{{ lab.links.scholar }}">Google Scholar</a>{% endif %}{% if has_scholar and has_orcid %} and {% endif %}{% if has_orcid %}<a href="{{ lab.links.orcid }}">ORCID</a>{% endif %} may list papers not yet added here.</p>
    {%- endif %}
  </header>
  {%- if max_count > 0 and last_year > first_year %}
  <figure class="pub-hist">
    <div class="pub-hist-bars" role="img" aria-label="Bar chart of publications per year from {{ first_year }} to {{ last_year }}; the most in one year is {{ max_count }}, in {{ max_year }}.">
      {%- for y in (first_year..last_year) %}
      {%- assign y_name = y | append: "" %}
      {%- assign g = by_year | where: "name", y_name | first %}
      {%- if g %}{% assign n = g.items.size %}{% else %}{% assign n = 0 %}{% endif %}
      <span style="--h: {{ n | times: 100 | divided_by: max_count }}%" title="{{ y }}: {{ n }}"></span>
      {%- endfor %}
    </div>
    <div class="pub-hist-axis" aria-hidden="true"><span>{{ first_year }}</span><span>{{ mid_year }}</span><span>{{ last_year }}</span></div>
    <figcaption>Publications per year</figcaption>
  </figure>
  {%- endif %}
  </div>

  <div class="pub-filters" id="pub-filters" hidden>
    <div class="filter-buttons" role="group" aria-label="Filter publications">
      <button type="button" class="filter-btn" data-filter="all" aria-pressed="true">All</button>
      <button type="button" class="filter-btn" data-filter="selected" aria-pressed="false">Selected</button>
      {%- if themes.size > 0 %}
      {%- for t in themes %}
      {%- assign tslug = t.url | split: "/" | last %}
      <button type="button" class="filter-btn" data-filter="theme:{{ tslug }}" data-hue="{{ tslug }}" aria-pressed="false">{{ t.title }}</button>
      {%- endfor %}
      {%- else %}
      <button type="button" class="filter-btn" data-filter="theme:topographic-maps" aria-pressed="false">Topographic maps</button>
      <button type="button" class="filter-btn" data-filter="theme:precision-imaging" aria-pressed="false">Precision neuroimaging</button>
      <button type="button" class="filter-btn" data-filter="theme:computational-models" aria-pressed="false">Computational models</button>
      <button type="button" class="filter-btn" data-filter="theme:perception-awareness" aria-pressed="false">Perception and awareness</button>
      {%- endif %}
      {%- assign preprints = pubs | where: "type", "preprint" %}
      {%- if preprints.size > 0 %}
      <button type="button" class="filter-btn" data-filter="type:preprint" aria-pressed="false">Preprints</button>
      {%- endif %}
    </div>
    <div class="filter-search">
      <label for="pub-search">Search titles, authors and journals</label>
      <input type="search" id="pub-search" autocomplete="off" spellcheck="false" placeholder="e.g. rivalry, Hedger, eLife">
    </div>
    <p class="filter-status" id="pub-status" aria-live="polite"></p>
  </div>

  <div class="pub-years">
    {%- for group in by_year %}
    <section class="pub-year" aria-labelledby="y{{ group.name }}">
      <h2 class="pub-year-label" id="y{{ group.name }}">{{ group.name }}</h2>
      <ol class="pub-list">
        {%- for pub in group.items %}
        {% include pub-entry.html pub=pub hlevel=3 %}
        {%- endfor %}
      </ol>
    </section>
    {%- endfor %}
  </div>
  <p class="filter-empty" id="pub-empty" hidden>No publications match this filter.</p>
</div>
