---
layout: page
permalink: /data/
title: data
description: We publish our datasets here.
---


We are very much devoted to open science. All our analyses appear on GitHub, and here we provide access to our results. This can be in the form of interactive plots, and/or [pycortex-based](https://github.com/gallantlab/pycortex) brain viewers. 
We will also link to [openneuro.org](https://openneuro.org) dataset which we put online.

<img class="col three" src="/img/science/999999/999999_sulcaldepth.png">


<ul class="post-list">
{% for item in site.data %}
    <li>
    {% if item.img %}
            <img class="col two right" src="{{ item.img }}">
    {% endif %}     
        <h4><a class="person-title" href="{{ item.url | prepend: site.baseurl }}">{{ item.title }}</a></h4>
            <p>{{ item.description }}</p>
      </li>
{% endfor %}
</ul>