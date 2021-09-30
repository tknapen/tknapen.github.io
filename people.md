---
layout: page
permalink: /people/
title: people
description: Knapen Lab Team
---

{% for person in site.people %}

{% if person.redirect %}
<div class="person">
    <div class="thumbnail">
        <a href="{{ person.redirect }}" target="_blank">
        {% if person.img %}
        <img class="thumbnailperson" src="{{ person.img }}"/>
        {% else %}
        <div class="thumbnail blankbox"></div>
        {% endif %}    
        <span>
            <h2 class="slide">{{ person.title }}</h2>
            <br/>
            <h3 class="slide">{{ person.description }}</h3>
        </span>
        </a>
    </div>
</div>
{% else %}

<div class="person">
    <div class="thumbnail">
        <a href="{{ site.baseurl }}{{ person.url }}">
        {% if person.img %}
        <img class="thumbnailperson" src="{{ person.img }}"/>
        {% else %}
        <div class="thumbnail blankbox"></div>
        {% endif %}    
        <span>
            <h2 class="slide">{{ person.title }}</h2>
            <br/>
            <h3 class="slide">{{ person.description }}</h3>
        </span>
        </a>
    </div>
</div>

{% endif %}

{% endfor %}