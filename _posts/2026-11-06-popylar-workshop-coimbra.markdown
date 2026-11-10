---
layout: post
title: "Popylar workshop on pRF modeling in Coimbra"
description: A two-day hands-on workshop on population receptive field modeling with the new prfmodel Python package, at the University of Coimbra.
date: 2026-11-06 17:00:00
---

On 5 and 6 November 2026 we ran a two-day workshop on population receptive field (pRF) modeling at the Faculty of Psychology and Educational Sciences of the University of Coimbra, Portugal. The workshop was organized by the Popylar team, on behalf of the Spinoza Centre for Neuroimaging and the Netherlands eScience Center, for PhD students, postdocs and faculty with basic Python skills.

Lectures covered the origins of pRF mapping (Serge Dumoulin), the design of pRF experiments and advanced pRF models (Tomas Knapen) and cognitive pRF models (Ben Harvey). Ilona Bloem presented electrophysiological applications and Marcus Daghlian presented neural contrast sensitivity functions. Malte Lüken of the Netherlands eScience Center introduced the package and discussed modeling choices and best practices.

Most of the time went to hands-on practicals with [prfmodel](https://popylar-org.github.io/prfmodel/), the Python package that the Popylar project develops. Participants fitted Gaussian pRF models to 7T fMRI data, cross-validated and compared models (including difference-of-Gaussians, compressive spatial summation and divisive normalization), fitted connective field models, and applied pRF models to electrocorticography, numerosity and contrast sensitivity data. Version 0.2.0 of prfmodel was released for the workshop.

The [workshop materials](https://popylar-org.github.io/2026-11-05_workshop-coimbra/) are public: slides from several of the lectures, and the practicals with their solutions, which run in Google Colab. The source is on [GitHub](https://github.com/popylar-org/2026-11-05_workshop-coimbra). To try prfmodel yourself:

```bash
pip install "prfmodel[tensorflow]"
```

The [documentation](https://popylar-org.github.io/prfmodel/) has tutorials and worked examples. Popylar is supported by the Netherlands eScience Center through its Open eScience Call 2024.
