---
title: Topographic maps
order: 1
tagline: "How maps of the sensory world and of the body organize processing throughout the brain."
description: "How maps of visual space and of the body organize processing well beyond sensory cortex, and how they change with what the brain is doing."
img: /assets/img/themes/topographic-maps.jpg
img_alt: "Inflated cortical surfaces colored by preferred visual field position, with visual areas from V1 to the intraparietal sulcus outlined."
---
Early sensory cortex is laid out as maps: neighboring neurons respond to neighboring points on the retina or the skin. We ask how far this organization reaches beyond the classical sensory areas, how it changes with cognitive state and with eye movements, and what maps contribute to memory, to action and to perceiving other people's bodies.

## Approach

We estimate each brain location's preferred position in visual space with population receptive field (pRF) [models](/research/computational-models/). Topographic connectivity derives preferred positions in visual space or on the body from the pattern of activity on a source map, such as primary visual cortex (V1) or primary somatosensory cortex (S1). It needs only brain activity, so it also works during movie watching and rest. We analyze large public datasets, such as the Human Connectome Project (HCP) retinotopy data, alongside individuals scanned over many runs.

Fitting a pRF to every voxel gives each one a preferred position in the visual field. Across the cortical surface these preferences change smoothly from voxel to voxel, and that orderly progression is the map.

{% include clip.html id="prf-map" %}

## What we have found

**The cerebellum contains maps of visual space.** In the HCP retinotopy data we found five ipsilateral retinotopic maps in three clusters of the human cerebellum (oculomotor vermis, lobule VIIb and lobule VIIIb), and released an atlas of them ([van Es et al., 2019](/publications/2019-05-20-CB/)). Connectivity with V1 later revealed an eccentricity gradient in the oculomotor vermis during movie watching, absent in a simple mapping experiment, and a new topographic area in Crus II that appeared during movies but not at rest ([Zuiderbaan et al., 2026](/publications/2025-11-25-JoN/)).

**Visual coding extends into the default network and hippocampus.** In the human brain, the default network deactivates selectively depending on where a visual stimulus appears: it encodes spatial vision through deactivation ([Szinte and Knapen, 2020](/publications/2020-05-18-CC/)). Connectivity with V1 revealed stable visual organization in the default-mode network and hippocampus, warped by cognitive state ([Knapen, 2021](/publications/2021-01-12-PNAS/)). In the human hippocampus, pRF mapping showed strong biases for the contralateral visual field ([Silson et al., 2021](/publications/2021-03-17-JoN/)).

**Body maps in visual cortex.** A model that maps body-part tuning and visual field tuning at once revealed an array of somatotopic body maps across the human dorsolateral visual system during video watching. Their body-position tuning aligns with their visual tuning and predicts both visual field preferences and preferences for seeing particular body parts ([Hedger et al., 2025](/publications/2025-11-26-NAT/)).

**Maps across eye movements.** Motion and tilt aftereffects are tied to retinal position, not to world- or head-centered position ([Knapen et al., 2009](/publications/2009-05-15-JoV/); [Knapen et al., 2010](/publications/2010-01-19-JoV/)). Around a saccade, information about its target reaches foveal retinotopic cortex. In human fMRI, activity matching the target's orientation and size was remapped to the fovea, but not when observers only attended the target ([Knapen et al., 2016](/publications/2016-06-21-FSN/)), and peripheral targets could be decoded from foveal cortex without foveal stimulation ([Kämmer et al., 2026](/publications/2025-08-20-EL/)).

## Open questions

With colleagues, we have proposed that visuospatial coding gives cognition a common reference frame ([Groen et al., 2021](/publications/2021-11-16-TiCS/)). What do maps in memory and default-network regions compute, and how do they reorganize during free viewing? How do aligned visual and bodily maps support action and social perception, and how similar is this organization across primate species?
