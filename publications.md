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
        <p class="pub-meta">{{ publication.date | date: '%Y' }}, {{publication.journal }}</p>
            <p class="post-meta">{{ publication.description }}</p>
      <hr />
      </li>
{% endfor %}
</ul>