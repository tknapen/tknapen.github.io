---
layout: default
title: Research
permalink: /research/
description: "The four research themes of the Knapen Lab: topographic maps, precision neuroimaging, computational models, and perception and awareness."
redirect_from:
  - /science/
---
<div class="wrap">
  <header class="page-header page-header-wide">
    <h1 class="page-title">Research</h1>
    <p class="page-lead">Our work is organized in four themes that share methods, models and data. Each theme page describes the questions we ask and lists the relevant papers, people and tools.</p>
  </header>
  {%- assign themes = site.research | sort: "order" %}
  <div class="grid grid-themes-large">
    {%- for t in themes %}
    {% include theme-card.html theme=t hlevel=2 large=true eager=forloop.first %}
    {%- endfor %}
  </div>
</div>
