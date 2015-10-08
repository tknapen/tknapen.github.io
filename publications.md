---
layout: page
permalink: /publications/
title: publications
description: our publications
---

<!-- {% for project in site.publications %}

{% if project.redirect %}
<div class="project">
    <div class="thumbnail">
        <a href="{{ project.redirect }}" target="_blank">
        {% if project.img %}
        <img class="thumbnail" src="{{ project.img }}"/>
        {% else %}
        <div class="thumbnail blankbox"></div>
        {% endif %}    
        <span>
            <h1>{{ project.title }}</h1>
            <br/>
            <p>{{ project.description }}</p>
        </span>
        </a>
    </div>
</div>
{% else %}

<div class="project ">
    <div class="thumbnail">
        <a href="{{ site.baseurl }}{{ project.url }}">
        {% if project.img %}
        <img class="thumbnail" src="{{ project.img }}"/>
        {% else %}
        <div class="thumbnail blankbox"></div>
        {% endif %}    
        <span>
            <h1>{{ project.title }}</h1>
            <br/>
            <p>{{ project.description }}</p>
        </span>
        </a>
    </div>
</div>

{% endif %}

{% endfor %}
 -->

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