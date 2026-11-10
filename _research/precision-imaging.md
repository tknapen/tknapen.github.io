---
title: Precision neuroimaging
order: 2
tagline: "Intensive, high-quality measurements in individual brains, and the open datasets they produce."
description: "Many hours of high-quality 7T fMRI in individual brains, fast targeted acquisition, quantitative MRI and combined fMRI and MEG, and the datasets this work produces."
img: /assets/img/themes/precision-imaging.jpg
img_alt: "Inflated cortical surfaces from the Arrow of Time dataset, colored by preferred polar angle (left) and eccentricity (right), estimated from the pRF mapping experiment (top) and from a motion-energy model of responses to the videos (bottom)."
---
Testing a model voxel by voxel takes many hours of high-quality data from one brain. Other questions need a fast measurement at one location, or timing that fMRI alone cannot give. We design experiments, acquisition methods and analyses for these measurements, and share the data.

## Approach

With colleagues, we have described the principles of what we call intensive fMRI: extensive sampling of cognitive phenomena in a few individuals, to support computational modeling of single voxels. More data alone is not enough: it takes experiments designed for a rich hypothesis space and careful optimization of data quality ([Kupers et al., 2024](/publications/2024-10-24-TINS/)).

Our intensive dataset, Arrow of Time, has about 21 hours of 7T fMRI per participant (1.7 mm isotropic, repetition time 1.6 s) during 2,160 brief naturalistic videos, plus retinotopy and motion-energy localizers.

Line-scanning fMRI gives up volume coverage to sample a single line through cortex at very high spatial resolution and sampling rate. MEG adds millisecond timing to fMRI's spatial detail.

## What we have found

**Line-scanning in humans.** Our 7T implementation sampled every 200 ms, and its BOLD responses corresponded well with conventional echo-planar data ([Raimondo et al., 2021](/publications/2021-08-20-JCBFM/)). Multi-echo readouts and denoising raised temporal signal-to-noise ratio from 4.0 to 36.2, and navigators made it more robust to motion ([Raimondo et al., 2022](/publications/2022-11-17-JNM/)). A spin-echo version gave a sharper line profile, at a cost in functional sensitivity ([Raimondo et al., 2023](/publications/2023-01-10-MAGMA/)).

**Targeting a chosen location.** We select a target on each participant's cortical surface from its anatomy and pRF, place the line there in a second session, and tailor the stimuli to it. For most participants, pRF estimates from the line resembled the target's; target and best-matching V1 location were on average about 5.5 mm apart ([Heij et al., 2023](/publications/2023-08-22-HBM/)).

**Timing from fMRI and MEG.** A forward model that predicts MEG responses from each individual's fMRI visual field maps revealed a processing hierarchy across them: V1 captured most of the variance in MEG sensors, earlier than extrastriate areas ([Eickhoff et al., 2026](/publications/2026-07-10-PCB/)).

**Cortical microstructure in depression.** Quantitative 7T MRI of T1 (a proxy for intracortical myelin) and T2\* (a proxy for iron) in 48 patients with major depressive disorder and 10 controls linked diagnosis and symptom severity to lower myelination in lateral orbitofrontal cortex, not to iron ([Heij et al., 2024](/publications/2024-06-20-TP/)).

**Body maps from rest and video data.** In data recorded during rest, a model that maps body-part and visual field tuning at once produced detailed body-part tuning maps; during video watching, it revealed an array of somatotopic body maps across the dorsolateral visual system ([Hedger et al., 2025](/publications/2025-11-26-NAT/)). See also [Topographic maps](/research/topographic-maps/).

## Open questions

How well do models fit to many hours of data in one brain generalize to new stimuli and to other people? Which questions need a dense, multipurpose dataset, and which a fast measurement aimed at one location? We are preparing [Arrow of Time](/2026/04/24/AOT.html) as an open resource; its first release is planned around the turn of the year 2026/27 ([get notified](https://forms.gle/BMmfyWEZKL7vU5Va9)).
