---
layout: page
permalink: /IT/
title: IT
description: lab computer stuff
---


This section of the website is a wiki-like collection of instructions on how we do computer stuff. We have multiple in-house data analysis servers, and use the Lisa and Cartesius clusters of the surfsara organization. 

In order to create a reproducible data analysis pipeline, we only use open-source software. We track our own programming on [GitHub](github.com), our collection of tools is on [our lab github page](https://github.com/VU-Cog-Sci). There, you can find the tools we use to [create experiments](https://github.com/VU-Cog-Sci/exptools), [perform finite impulse response fitting](https://github.com/VU-Cog-Sci/nideconv), or [set up reproducible science docker images](https://github.com/VU-Cog-Sci/docker_images), and many others. 

<img class="col one right" src="/img/IT/python-logo.png">

All of our data analysis and experiment programming is done in python. Not only is the open nature of the python science ecosystem vital to how we do science, it is also a beautiful thing to be able to contribute to this ecosystem. 


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