---
layout: page
permalink: /science/
title: science
description: the topics our science covers
---

<!-- <div class="app"> -->
{% assign projects = site.science | sample:120 %}
{% for project in projects %}

{% if project.redirect %}
<div class="project">
    <div class="thumbnail">
        <a href="{{ project.redirect }}" target="_blank">
        {% if project.img %}
        <img class="thumbnailperson" src="{{ project.img }}"/>
        {% else %}
        <div class="thumbnail blankbox"></div>
        {% endif %}    
        <span>
            <h2 class="slide">{{ project.title }}</h2>
            <br/>
            <h3 class="slide">{{ project.description }}</h3>
        </span>
        </a>
    </div>
</div>
{% else %}

<div class="project">
    <div class="thumbnail">
        <a href="{{ site.baseurl }}{{ project.url }}">
        {% if project.img %}
        <img class="thumbnailperson" src="{{ project.img }}"/>
        {% else %}
        <div class="thumbnail blankbox"></div>
        {% endif %}    
        <span>
            <h2 class="slide">{{ project.title }}</h2>
            <br/>
            <h3 class="slide">{{ project.description }}</h3>
        </span>
        </a>
    </div>
</div>

{% endif %}

{% endfor %}
<!-- </div> -->
