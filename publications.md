---
layout: page
permalink: /publications/
title: publications
description: our publications
---

<!-- <img class="col one left" src="/img/prf/retmap_flat.png"> -->

<ul class="post-list">
{% for publication in site.publications reversed %}
    <li>
    {% if publication.img %}
            <img class="col one right" src="{{ publication.img }}">
    {% endif %}     
        <h4><a class="person-title" href="{{ publication.url | prepend: site.baseurl }}">{{ publication.title }}</a></h4>
        <p class="post-meta">{{ publication.date | date: '%B %-d, %Y — %H:%M' }}</p>
            <p>{{ publication.description }}</p>
      </li>
{% endfor %}
</ul>