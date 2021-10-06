---
layout: page
permalink: /resources/
title: resources
description: We publish our datasets & other stuff here.
---


We are very much devoted to open science. All our analyses appear on GitHub, and here we provide access to our results. This can be in the form of interactive plots, and/or [pycortex-based](https://github.com/gallantlab/pycortex) brain viewers. 
We will also link to [openneuro.org](https://openneuro.org) dataset which we put online.

The first place to look for how-tos that detail how we work with data etc. is on the <a href="https://github.com/tknapen/tknapen.github.io/wiki" target="_blank">lab wiki</a>, where such documents live. 


<ul class="post-list">
{% for item in site.resources %}
    <li>
    {% if item.img %}
            <img class="col two right" src="{{ item.img }}">
    {% endif %}     
        <h4><a class="person-title" href="{{ item.url | prepend: site.baseurl }}">{{ item.title }}</a></h4>
            <p>{{ item.description }}</p>
      </li>
{% endfor %}
</ul>


<img class="col three" src="/img/science/999999/999999_sulcaldepth.png">
