---
layout: page
permalink: /data/
title: data
description: We publish our data here.
---

<!-- <img class="col one left" src="/img/prf/retmap_flat.png"> -->

We are very much devoted to open science. All our analyses appear on GitHub, and here we provide access to our results. This can be in the form of interactive plots, and/or [pycortex-based](https://github.com/gallantlab/pycortex) brain viewers. 
We will also link to [openneuro.org](https://openneuro.org) dataset which we are about to put online.

**More to come soon!**


<ul class="post-list">
{% for data in site.data %}
    <li>
    {% if data.img %}
            <img class="col one right" src="{{ data.img }}">
    {% endif %}     
        <h4><a class="person-title" href="{{ data.url | prepend: site.baseurl }}">{{ data.title }}</a></h4>
            <p>{{ data.description }}</p>
      </li>
{% endfor %}
</ul>