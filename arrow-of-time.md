---
layout: page
title: Arrow of Time
permalink: /arrow-of-time/
description: "An open 7T fMRI dataset of brain responses to over 2,000 brief naturalistic videos, each played forward and backward."
---
{%- assign aot = site.data.lab.aot -%}

Arrow of Time (AOT) is an intensive fMRI dataset. Eight participants each spent 15 hours in a 7 tesla (7T) scanner watching over 2,000 brief naturalistic videos (1.7 mm isotropic resolution, repetition time 1.6 s). Every video was shown four times: twice as recorded and twice played backward. Retinotopy and motion-energy localizers in every participant tie the responses to each person's own visual field maps.

{{ aot.release }}

<p><a class="button" href="{{ aot.signup }}">Get notified about the release</a></p>

## What the dataset is for

Arrow of Time serves two purposes. It is an open resource for studying how the brain processes dynamic, naturalistic visual input, and it is a specific probe of the causal model of the world that the brain applies to that input.

**Dynamic vision in individual brains.** Much of what is known about visual cortex comes from static images, and the largest intensive fMRI dataset, the Natural Scenes Dataset, used photographs ([Allen et al., 2022](https://doi.org/10.1038/s41593-021-00962-x)). Natural vision is dynamic. Responses to natural movies have been modeled with motion-energy filters ([Nishimoto et al., 2011](https://doi.org/10.1016/j.cub.2011.08.031)) and with semantic features ([Huth et al., 2012](https://doi.org/10.1016/j.neuron.2012.10.014)), and the BOLD Moments Dataset provides whole-brain responses to over 1,000 three-second clips in ten people ([Lahner et al., 2024](https://doi.org/10.1038/s41467-024-50310-3)). Arrow of Time adds deep sampling at 7T: over 2,000 clips and 15 hours per participant, enough to fit and compare models voxel by voxel within one brain ([Kupers et al., 2024](/publications/2024-10-24-TINS/)).

**A probe of the brain's world model.** People judge the physical world as if they simulate it ([Battaglia et al., 2013](https://doi.org/10.1073/pnas.1306572110)). Frontal and parietal regions respond selectively when people watch and predict physical events ([Fischer et al., 2016](https://doi.org/10.1073/pnas.1610344113)), and the brain carries an internal model of gravity ([McIntyre et al., 2001](https://doi.org/10.1038/89477); [Indovina et al., 2005](https://doi.org/10.1126/science.1107961)). Playing a video backward is a simple way to violate such a model while keeping the images the same. Observers detect reversal quickly for events such as free fall, diffusion and forward locomotion, and often miss it otherwise ([Hanyu et al., 2023](https://doi.org/10.1098/rsos.230036)), and whether a clip is reversed can be computed from the video itself ([Pickup et al., 2014](https://doi.org/10.1109/CVPR.2014.262); [Wei et al., 2018](https://doi.org/10.1109/CVPR.2018.00840)). The strength of the violation therefore differs from clip to clip in a measurable way.

An earlier fMRI study showed silent films forward and backward: responses in early visual areas were reliable either way, but responses in higher areas were reproducible only for forward films ([Hasson et al., 2008](https://doi.org/10.1523/JNEUROSCI.5487-07.2008)). Arrow of Time asks the same kind of question for brief events, in thousands of clips, at the level of single voxels.

## Design

Reversal leaves every frame of a video intact and keeps the amount of motion, but it turns many clips into events that do not happen: water climbs back into a glass, a fallen object rises. The comparison between the two directions therefore asks which responses depend on how the world unfolds in time, and not only on what is in the image.

Each clip is shown twice in each direction, in random and counterbalanced order, so the difference between directions can be measured against the reliability within a direction. All four presentations of a clip fall within one scanning session, so a difference between directions cannot come from a difference between sessions. The motion-energy localizer gives a model of what reversal changes at the level of local motion, so that what remains can be attributed to the content of the events.

## A first look

A first analysis describes each video in two ways, by its local motion and by its content in words, and asks how much of each location's response the two descriptions explain.

<figure>
  <img src="{{ '/assets/img/aot/encoding-models.webp' | relative_url }}" width="1331" height="1061" loading="lazy" decoding="async" alt="Top: a video frame leads along two paths. In one, a vision-language model writes a description of the video, which a language model turns into a sentence embedding vector. In the other, spatiotemporal filters applied to the video are averaged across its frames into a motion embedding vector. Bottom: flattened cortical surfaces of both hemispheres, colored red, green and blue by which of the two descriptions explains each location's responses.">
  <figcaption>Two descriptions of each video. A vision-language model (Qwen-VL-Max) writes a description, which is embedded as a 2,048-dimensional sentence vector. Spatiotemporal filters give the video's motion energy, averaged over its 61 frames (11,845 dimensions). Banded ridge regression fits both to the responses to the forward-played videos. On the flattened cortical surfaces, red marks variance explained by motion energy, green variance explained by the sentence embedding, and blue the part of the noise ceiling that neither explains.</figcaption>
</figure>

## Data quality

Deep sampling pays off only if the sessions line up. The movie steps through the runs of one participant after registration.

{% include clip.html id="aot-registration-qc" credit=false %}

## Status

The last scanning sessions take place in November 2026, and basic processing of the data is done. A data paper will follow. Earlier news: [Arrow of Time dataset nearing completion]({{ aot.post | relative_url }}).
