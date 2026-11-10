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
We aim to explain brain responses, not only to locate them. Our encoding models predict a response from the sensory input or from activity elsewhere in the brain, using parameters with a biological meaning. We then ask how those parameters vary across brain regions, how they change with attention and neurochemistry, and how they relate to behavior.

## Approach

An fMRI voxel samples thousands of neurons. On a retinotopic map, neurons with similar receptive fields lie close together, so each voxel has a preference: its population receptive field (pRF), the region of visual space it responds to. We fit pRF models to responses to mapping stimuli and extend them with computations such as divisive normalization.

Connective field models apply the same idea from brain to brain. They explain a region's responses from a Gaussian patch of activity on a topographic source map such as primary visual cortex (V1). Depending on the source map, the patch's center stands for a location in visual space, a sound frequency or a position on the body, and its size, in millimeters of cortex, measures the spatial scale of integration. They need only brain activity, so they can be fit to data from any experiment, including movie watching and rest ([Knapen, 2021](/publications/2021-01-12-PNAS/)). For behavior and the pupil, we use models of learning and decision making to estimate latent processes trial by trial. Our model-fitting software is listed under [software and data](/software/).

## What we have found

- A pRF model based on divisive normalization captured seemingly disparate response signatures in human visual cortex with a single computation, and outperformed existing pRF models; its parameters varied systematically across the visual hierarchy ([Aqil et al., 2021](/publications/2021-11-15-PNAS/)).
- Comparing these parameters from 7T fMRI with receptor density maps from positron emission tomography provided evidence that serotonin and GABA receptor densities are a biological substrate for modulations of normalization in the human visual system ([Aqil et al., 2024](/publications/2024-01-03-SA/)).
- In humans, psilocybin altered contextual perception in the Ebbinghaus illusion and contextual modulation of visual cortical responses, and a computational model captured and linked both changes ([Aqil et al., 2025](/publications/2025-11-21-NC/)).
- Attention changes how human visual cortex samples space. Spatial and feature-based attention interacted in this resampling, which an attentional gain field of varying precision explains parsimoniously ([van Es et al., 2018](/publications/2018-12-07-EL/)). Focused attention attracted pRFs toward the attended location more strongly than distributed attention did ([Sheikh Abdirashid et al., 2025](/publications/2025-09-02-JoV/)).
- During reinforcement learning, the human pupil tracked model variables: before a choice it dilated with trial-by-trial value beliefs, and after feedback early dilation scaled with value uncertainty and later constriction with signed reward prediction errors ([Van Slooten et al., 2018](/publications/2018-11-30-PCB/)).

## Open questions

Can a small set of canonical computations, with parameters set by local neurochemistry, account for responses beyond visual cortex? How should encoding models handle the eye movements and complex input of natural vision? We are also developing Popylar, a community package for pRF modeling, to make these models easier to apply and extend.
