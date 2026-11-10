---
layout: page
title: Join the lab
permalink: /join/
description: "How to get in touch about master's projects, PhD and postdoctoral positions, and fellowship applications."
---
{%- assign lab = site.data.lab -%}

We have no open positions at the moment. We are glad to hear from people who would like to work with us, and new vacancies will be announced under [News](/news/).

## How to get in touch

Email Tomas Knapen at [{{ lab.email }}](mailto:{{ lab.email }}) with your CV and a short statement of your research interests. If you are a student, please also say when you would like to do your project and for how long.

## Master's research projects

Students from the Vrije Universiteit Amsterdam and other Amsterdam programs, in psychology, neuroscience, artificial intelligence or related fields, can do their master's research project in the lab. [Robert Satzger](/people/2023-08-25-rs/), for example, did his research internship here as part of the VU's MSc Artificial Intelligence.

## Fellowships

If you have your own fellowship funding, or plan to apply for it, you are welcome to discuss an application with us. Examples are Marie Skłodowska-Curie fellowships, NWO Veni grants and PhD scholarships from the China Scholarship Council. Lab members have joined on a Marie Curie fellowship and on a Chinese PhD scholarship.

## What you learn and do here

We acquire our imaging data at the Spinoza Centre for Neuroimaging in Amsterdam, where much of our work uses ultra-high-field (7T) fMRI. Many studies also use eye tracking and pupillometry.

Analysis happens in Python. A large part of it is computational modeling: models that link brain responses to the sensory input and to behavior, such as population receptive field and connective field models. We write open-source software for this work and share it, including [prfpy](https://github.com/VU-Cog-Sci/prfpy) and [nideconv](https://github.com/VU-Cog-Sci/nideconv); the [Software & data](/software/) page lists the rest.

## How we work

We want our results to remain a valid contribution far into the future, so we would rather do our science well than fast. That means not cutting corners, and building analyses and code that others in the lab, and later the wider research community, can reuse. We also take the feeling of not being sure seriously: it shows where our understanding falls short, and it often points to a good research question.

The same applies to code. We write it so that someone less experienced can read it two years from now, and we use git, docstrings and tests to keep it that way.

Read more in [Lab culture: research dos and don'ts](/resources/culture/) and [Programming dos and don'ts](/resources/pythonic/).{% if lab.links.wiki and lab.links.wiki != "" %} Practical how-tos for working in the lab are on the [lab wiki]({{ lab.links.wiki }}).{% endif %}
