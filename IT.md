---
layout: page
permalink: /IT/
title: IT
description: lab computer stuff
---

<img class="col two right" src="/img/IT/innards.jpg">

This section of the website is a wiki-like collection of instructions on how we do computer stuff. In order to create a reproducible data analysis pipeline, we only use open-source software, and track our own programming on [GitHub](github.com). 

We have two data analysis servers, Aeneas (general purpose, CUDA) and Ascanius (Xeon Phi). 


<ul class="post-list">
{% for IT in site.IT reversed %}
    <li>
    {% if IT.img %}
            <img class="col one right" src="{{ IT.img }}">
    {% endif %}     
        <h4><a class="person-title" href="{{ IT.url | prepend: site.baseurl }}">{{ IT.title }}</a></h4>
        <p class="post-meta">{{ IT.date | date: '%B %-d, %Y — %H:%M' }}</p>
            <p>{{ IT.description }}</p>
      </li>
{% endfor %}
</ul>