---
layout: default
title: Animations
permalink: /animations/
description: "Short animations that explain the Knapen Lab's models and methods, and lecturekit and manim8, the open-source packages they are made with."
---
{%- assign tools = site.data.software | where: "group", "animations" -%}
<div class="wrap animations-page">
  <header class="page-header page-header-wide">
    <h1 class="page-title">Animations</h1>
    <p class="page-lead">Short animations that explain our models and methods. They are rendered from code, for our lectures and talks and for this site.</p>
  </header>

  <section class="section-block" aria-labelledby="clips-heading">
    <h2 id="clips-heading">Clips</h2>
    <p class="section-note">Each clip plays once when it comes into view. The button under it pauses or replays it.</p>
    <div class="clip-list">
      {%- for c in site.data.clips %}
      <div>
        {% include clip.html id=c.id credit=false hlevel=3 %}
        {%- if c.page %}
        <p class="clip-where">In context: <a href="{{ c.page | relative_url }}">{{ c.page_title | default: c.page }}</a></p>
        {%- endif %}
      </div>
      {%- endfor %}
    </div>
  </section>

  <section class="section-block" aria-labelledby="made-heading">
    <h2 id="made-heading">How they are made</h2>
    <div class="prose">
      <p>The clips come from our lectures. Each lecture is one Markdown file, which <a href="https://github.com/tknapen/lecturekit">lecturekit</a> builds into a Reveal.js deck for the room and a Beamer PDF for study. Figures are drawn from numbers and clips are rendered from code with <a href="https://www.manim.community">Manim</a>, so a lecture can be rebuilt and checked like any other analysis.</p>
      <p><a href="https://github.com/tknapen/manim8">manim8</a> is the animation layer. An animation is specified in versioned YAML, or described in plain language to an assistant that writes the YAML. It is composed from registered components, reviewed through still frames at named checkpoints, and rendered under a versioned style. The look of a lecture is defined once, in a brand file, and the same clip can be rendered for a light and for a dark deck.</p>
      <p>Clips made for this site, such as the two on divisive normalization, live in <a href="https://github.com/tknapen/site-animations">site-animations</a>. Their curves are simulated with <a href="{{ '/software/' | relative_url }}">prfmodel</a>, and each clip is rendered twice from the same scene, for the light and the dark version of the site.</p>
      <p>Both packages are open source under the MIT license and in active development; neither is on PyPI yet. lecturekit installs from GitHub and needs Quarto and a TeX distribution (see its <a href="https://github.com/tknapen/lecturekit/blob/main/docs/INSTALL.md">installation notes</a>):</p>
<pre><code>pip install "lecturekit[review,figures,clips] @ git+https://github.com/tknapen/lecturekit@main"
lk new my-lecture &amp;&amp; cd my-lecture &amp;&amp; lk build</code></pre>
    </div>
    {%- if tools.size > 0 %}
    <div class="grid grid-sw section-note-after">
      {%- for item in tools %}
      {% include software-card.html item=item hlevel=3 %}
      {%- endfor %}
    </div>
    {%- endif %}
  </section>

  <section class="section-block" aria-labelledby="expo-heading">
    <h2 id="expo-heading">Example lectures</h2>
    <div class="prose">
      <p><a href="https://github.com/tknapen/lecturekit-expo">lecturekit-expo</a> collects complete lecture projects built this way. Each carries its storyboard, plan, checked facts and the sources it was built from, with clips made for it:</p>
      <ul>
        <li>Divisive normalization across the hierarchy</li>
        <li>Drift diffusion: evidence to a bound</li>
        <li>A talk from a paper: joint visual and somatotopic tuning</li>
        <li>MRI from spins to k-space</li>
        <li>Signal detection theory in twenty minutes</li>
      </ul>
    </div>
  </section>
</div>
