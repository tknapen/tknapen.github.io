---
layout: page
permalink: /data/
title: data
description: page on which we publish data
---

<!-- <img class="col one left" src="/img/prf/retmap_flat.png"> -->

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