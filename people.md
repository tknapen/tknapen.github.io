---
layout: page
permalink: /people/
title: people
description: People in the lab
---

<ul class="post-list">
{% for person in site.people reversed %}
    <li>
        <h4><a class="person-title" href="{{ person.url | prepend: site.baseurl }}">{{ person.title }}</a></h4>
        <!-- <p class="post-meta">{{ person.date | date: '%B %-d, %Y — %H:%M' }}</p> -->
            <p>{{ person.description }}</p>
      </li>
{% endfor %}
</ul>