---
layout: page
title: Contact
permalink: /contact/
description: "Email, addresses and online profiles of the Knapen Lab."
hide_description: true
---
{%- assign lab = site.data.lab -%}
{%- assign l = lab.links -%}

The best way to reach us is by email to Tomas Knapen: [{{ lab.email }}](mailto:{{ lab.email }}). For positions and student projects, see [Join the lab](/join/).

## Addresses

<ul class="contact-affiliations">
{%- for a in lab.affiliations %}
<li><a href="{{ a.url }}">{{ a.name }}</a>{% if a.unit and a.unit != "" %}<br>{{ a.unit }}{% endif %}{% if a.address and a.address != "" %}<br>{{ a.address }}{% endif %}</li>
{%- endfor %}
</ul>

We acquire our imaging data at the Spinoza Centre for Neuroimaging.

## Online

<ul class="contact-links">
{%- if l.github_org and l.github_org != "" %}
<li><a href="{{ l.github_org }}">GitHub: lab repositories (VU-Cog-Sci)</a></li>
{%- endif %}
{%- if l.github and l.github != "" %}
<li><a href="{{ l.github }}">GitHub: Tomas Knapen</a></li>
{%- endif %}
{%- if l.scholar and l.scholar != "" %}
<li><a href="{{ l.scholar }}">Google Scholar</a></li>
{%- endif %}
{%- if l.orcid and l.orcid != "" %}
<li><a href="{{ l.orcid }}">ORCID</a></li>
{%- endif %}
{%- if l.x and l.x != "" %}
<li><a href="{{ l.x }}">X</a></li>
{%- endif %}
{%- if l.bluesky and l.bluesky != "" %}
<li><a href="{{ l.bluesky }}">Bluesky</a></li>
{%- endif %}
{%- if l.linkedin and l.linkedin != "" %}
<li><a href="{{ l.linkedin }}">LinkedIn</a></li>
{%- endif %}
{%- if l.wiki and l.wiki != "" %}
<li><a href="{{ l.wiki }}">Lab wiki</a></li>
{%- endif %}
</ul>
