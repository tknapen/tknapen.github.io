---
layout: page
permalink: /people/
title: people
description: People in the lab
---
<img class="col one right" src="/img/people/lab_wine.jpg">

<ul class="post-list">
{% for person in site.people %}
    <li>
        <h4><a class="person-title" href="{{ person.url | prepend: site.baseurl }}">{{ person.title }}</a></h4>
        <!-- <p class="post-meta">{{ person.date | date: '%B %-d, %Y — %H:%M' }}</p> -->
            <p>{{ person.description }}</p>
      </li>
{% endfor %}
</ul>
<hr />
<br />

<header class="post-header">
    <h1 class="post-title">close collaborators</h1>
    <br />
    <h4 class="post-description">Nationally</h4>
 </header>
<ul class="post-list">
    <li>
        <h5>University of Amsterdam</h5>
            <p><a href="http://www.cognitiveneuroscience.nl/index.php?p=1" target="_blank">Scholte & Lamme Labs</a></p>
    </li>
    <li>
        <h5>Netherlands Institute for Neuroscience (Royal Academy of Sciences)</h5>
            <p><a href="http://www.herseninstituut.knaw.nl/ResearchGroups/RoelfsemaGroup/Research/tabid/417/Default.aspx" target="_blank">Roelfsema Group</a></p>
    </li>
</ul>

<header class="post-header">
    <h4 class="post-description">Internationally</h4>
 </header>
 <ul class="post-list">
    <li>
        <h5>University Medical Center Hamburg</h5>
            <p><a href="http://www.tobiasdonner.net" target="_blank">Donner Lab</a></p>
    </li>
    <li>
        <h5>Michigan State University</h5>
            <p><a href="https://psychology.msu.edu/brascamplab/" target="_blank">Brascamp Lab</a></p>
    </li>
    <li>
        <h5>Vanderbilt University</h5>
            <p><a href="http://www.psy.vanderbilt.edu/faculty/blake/blake.html" target="_blank">Blake Lab</a></p>
    </li>
</ul>
