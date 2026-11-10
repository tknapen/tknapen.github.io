---
title: Precision neuroimaging
order: 2
tagline: "Dense, high-resolution measurements of brain activity, from cortical layers and columns to large naturalistic datasets."
description: "Ultra-high-field fMRI methods that resolve cortical layers and columns, and intensive datasets that support computational modeling in individual brains."
img: /assets/img/themes/precision-imaging.jpg
img_alt: "Schematic of the layers of visual cortex, showing where thalamic input arrives and where feedforward output and top-down feedback connect."
---
Much of the brain's processing happens at scales conventional fMRI blurs. Input from the thalamus and feedback from other areas arrive in different cortical layers, and neighboring columns can carry signals from different eyes. Other questions need many hours of data from one brain to test a model voxel by voxel. We develop acquisition and analysis methods for both kinds of question.

## Approach

We use ultra-high-field (7T) fMRI to measure responses across cortical depth and within ocular dominance columns, correcting for draining-vein effects. With line-scanning, we give up volume coverage to sample a single line through cortex at 250 µm resolution along cortical depth, every 105 to 200 ms. We estimate hemodynamic responses from the data rather than assume their shape, and combine fMRI with MEG when timing matters. With colleagues, we have described the principles of what we call intensive fMRI: extensive sampling of cognitive phenomena in a few individuals, designed for computational modeling at the level of single voxels ([Kupers et al., 2024](/publications/2024-10-24-TINS/)).

## What we have found

**Columns and layers separate input from attention.** We imaged ocular dominance columns in human V1 across cortical depth; the column patterns were stable across sessions and across scanners on different continents. Separating input by eye let us compare attention conditions with an identical stimulus. Monocular stimulation had its largest effect at deep and middle depths, whereas spatial attention affected BOLD activity only near the pial surface ([de Hollander et al., 2020](/publications/2021-03-12-NI/)).

**Line-scanning in humans.** We implemented line-scanning at 7T ([Raimondo et al., 2021](/publications/2021-08-20-JCBFM/)), improved its sensitivity with multi-echo readouts and denoising, added motion correction ([Raimondo et al., 2022](/publications/2022-11-17-JNM/)), and built a framework that places the line on a cortical location selected by its anatomy and pRF ([Heij et al., 2023](/publications/2023-08-22-HBM/)). Line-scanning also showed that depth-resolved hemodynamic responses in V1 are similar in young and middle-aged adults ([Raimondo et al., 2025](/publications/2025-02-28-BT/)).

**A laminar signature of context.** In line-scanning data, stimuli in the center of a participant's pRF evoked responses that increased toward the pial surface with a small peak at middle depths, consistent with feedforward input. Large stimuli in the surround evoked activity in superficial and deep layers, where descending connections terminate ([Heij et al., 2025](/publications/2025-06-19-IS/)).

**Timing from fMRI and MEG.** In humans, a forward model that predicts MEG responses from fMRI-defined visual field maps showed that V1 captured most of the variance in MEG sensors, and did so earlier than extrastriate areas ([Eickhoff et al., 2026](/publications/2026-07-10-PCB/)).

## Open questions

Can laminar signals separate feedforward from feedback processing during natural viewing, as they can with tailored stimuli? How well do models fit to many hours of data in one brain generalize to new stimuli and to other people? For such questions, we are preparing the public release of [Arrow of Time](/2026/04/24/AOT.html), an intensive 7T fMRI dataset of brain responses to 2,160 brief naturalistic videos, with about 21 hours of scanning per participant at 1.7 mm isotropic resolution. The first release is planned around the turn of the year ([get notified](https://forms.gle/BMmfyWEZKL7vU5Va9)).
