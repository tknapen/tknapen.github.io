---
layout: default
title: Publications
permalink: /publications/
description: "Publications of the Knapen Lab, with abstracts, links to articles, preprints, code and data."
---
{%- assign lab = site.data.lab -%}
{%- assign pubs = site.publications | sort: "date" | reverse -%}
{%- assign themes = site.research | sort: "order" -%}
<div class="wrap pubs-page">
  <header class="page-header page-header-wide">
    <h1 class="page-title">Publications</h1>
    <p class="page-lead">{{ pubs.size }} publications, newest first.</p>
    {%- assign has_scholar = false -%}{%- if lab.links.scholar and lab.links.scholar != "" -%}{%- assign has_scholar = true -%}{%- endif -%}
    {%- assign has_orcid = false -%}{%- if lab.links.orcid and lab.links.orcid != "" -%}{%- assign has_orcid = true -%}{%- endif -%}
    {%- if has_scholar or has_orcid %}
    <p class="page-note">{{ lab.pi | default: "The PI" }}'s profiles on {% if has_scholar %}<a href="{{ lab.links.scholar }}">Google Scholar</a>{% endif %}{% if has_scholar and has_orcid %} and {% endif %}{% if has_orcid %}<a href="{{ lab.links.orcid }}">ORCID</a>{% endif %} may list papers not yet added here.</p>
    {%- endif %}
  </header>

  <div class="pub-filters" id="pub-filters" hidden>
    <div class="filter-buttons" role="group" aria-label="Filter publications">
      <button type="button" class="filter-btn" data-filter="all" aria-pressed="true">All</button>
      <button type="button" class="filter-btn" data-filter="selected" aria-pressed="false">Selected</button>
      {%- if themes.size > 0 %}
      {%- for t in themes %}
      {%- assign tslug = t.url | split: "/" | last %}
      <button type="button" class="filter-btn" data-filter="theme:{{ tslug }}" aria-pressed="false">{{ t.title }}</button>
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

  {%- assign by_year = pubs | group_by_exp: "p", "p.date | date: '%Y'" %}
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
