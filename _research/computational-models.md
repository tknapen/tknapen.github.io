---
title: Computational models
order: 3
tagline: "Encoding models that connect sensory input, brain responses and behavior."
description: "Population receptive field, connective field and normalization models that explain brain responses with biologically interpretable parameters, and models of learning and the pupil."
img: /assets/img/themes/computational-models.jpg
img_alt: "Connective field model on the cortical surface: changing the field's center and size changes which part of the source map predicts a response."
redirect_from:
  - /science/connective_fields/
  - /science/prf_project/
---
Our encoding models explain a brain response from the sensory input or from activity elsewhere in the brain, using parameters with a biological meaning. We then ask how those parameters vary across brain regions, how they change with attention and neurochemistry, and how they relate to behavior.

## Approach

An fMRI voxel samples hundreds of thousands of neurons. On a retinotopic map, neurons with similar receptive fields lie close together, so each voxel has a preference: its population receptive field (pRF), the region of visual space it responds to. We fit pRF models to responses to mapping stimuli and extend them with computations such as divisive normalization.

### A pRF model in three steps

**From stimulus to signal.** A mapping stimulus, here a bar that sweeps across the visual field, drives a voxel whenever it overlaps the voxel's receptive field. The model turns that overlap into a predicted neural response and then, through the hemodynamic response, into a predicted BOLD time series.

{% include clip.html id="stimulus-to-bold" %}

**A chain of stages.** The prediction comes from a sequence of operations on the stimulus: extracting features, pooling them over space with the receptive field, transforming the pooled signal, neural dynamics and the hemodynamic response. Most stages have parameters of their own, and the pRF models we use differ in what these stages compute.

{% include clip.html id="model-as-chain" %}

**Fitting.** For each voxel we search for the parameters whose prediction best matches the measured time series: first a grid search over candidate positions and sizes, then iterative refinement of the best candidate.

{% include clip.html id="grid-and-fit" %}

### Dividing by a normalization pool

In the divisive normalization pRF model, the transformation stage is a division. A Gaussian activation pool drives the response, and a larger Gaussian normalization pool at the same position divides it ([Aqil et al., 2021](/publications/2021-11-15-PNAS/)). The two animations below are simulations of this model, computed with [prfmodel](/software/) for illustrative parameter values.

**A bar crosses the pRF.** The activation pool responds only while the bar is near the pRF; the normalization pool responds over a wider range. Their ratio peaks at the pRF and falls slightly below baseline on either side, where the bar drives the normalization pool but hardly the activation pool: surround suppression.

{% include clip.html id="dn-bar-sweep" %}

**A disc grows over the pRF.** The response rises while the disc fills the activation pool, and then falls as the disc keeps filling the normalization pool: larger stimuli give smaller responses, known as oversaturation. In the simulation, a larger normalization constant gives a weaker response that falls less, and the fall disappears when the two pools have the same size.

{% include clip.html id="dn-size-tuning" %}

### From brain to brain

Connective field models apply the same idea from brain to brain. They explain a region's responses from a Gaussian patch of activity on a topographic source map such as primary visual cortex (V1). Depending on the source map, the patch's center stands for a location in visual space or a position on the body, and its size, in millimeters of cortex, measures the spatial scale of integration. They need only brain activity, so they can be fit to data from any experiment, including movie watching and rest ([Knapen, 2021](/publications/2021-01-12-PNAS/)). For behavior and the pupil, we use models of learning and decision making to estimate latent processes trial by trial. Our model-fitting software is listed under [software and data](/software/).

## What we have found

**Normalization explains diverse pRF responses.** A pRF model based on divisive normalization captured seemingly disparate response signatures in human visual cortex with a single computation, and outperformed existing pRF models; its parameters varied systematically across the visual hierarchy ([Aqil et al., 2021](/publications/2021-11-15-PNAS/)). Comparing these parameters from 7T fMRI with receptor density maps from positron emission tomography provided evidence that serotonin and GABA receptor densities are a biological substrate for modulations of normalization in the human visual system ([Aqil et al., 2024](/publications/2024-01-03-SA/)).

**Contextual computation under psilocybin.** In humans, psilocybin altered contextual perception in the Ebbinghaus illusion and contextual modulation of visual cortical responses, and a computational model captured and linked both changes ([Aqil et al., 2025](/publications/2025-11-21-NC/)).

**Attention changes how visual cortex samples space.** Spatial and feature-based attention interacted in how human visual cortex resampled space; an attentional gain field of varying precision explains this parsimoniously ([van Es et al., 2018](/publications/2018-12-07-EL/)). Focused attention attracted pRFs toward the attended location more strongly than distributed attention did ([Sheikh Abdirashid et al., 2025](/publications/2025-09-02-JoV/)).

**The pupil tracks learning variables.** In a reinforcement learning task, the human pupil dilated before a choice with trial-by-trial value beliefs. After feedback, early dilation scaled with value uncertainty and later constriction with signed reward prediction errors ([Van Slooten et al., 2018](/publications/2018-11-30-PCB/)).

## Open questions

Can a small set of canonical computations, with parameters set by local neurochemistry, account for responses beyond visual cortex? How should encoding models handle the eye movements and complex input of natural vision? To make these models easier to apply and extend, the Popylar project develops [prfmodel](/software/), a community Python package for pRF and connective field modeling. Version 0.2.0 was released for our [workshop in Coimbra](/2026/11/06/popylar-workshop-coimbra.html) in November 2026.
