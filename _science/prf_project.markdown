---
layout: post
title: Population Receptive Field Mapping
description: Mapping how visual information is encoded in the human brain
frontpage: true
img: /img/prf/eccen_quadrant.png
---

With fMRI, we measure a signal related to the activity of thousands of neurons in each voxel. Because neurons with similar receptive fields are close together on the retinotopic map, each population of neurons in a single fMRI voxel will have similar receptive fields. This means that it is possible to chart, for each voxel, its population receptive field, or pRF, i.e. the region of visual space that the voxel’s neural tissue analyses. These mappings of visual preferences in the brain are unique to the specific participant, and give us detailed knowledge about how the visual system encodes visual information. Our lab is interested in finding how this encoding of visual information changes as a function of cognitive factors such as attention and reinforcement.
Recent studies do exactly this - using this novel encoding-model approach emphasize the flexibility of information encoding in the retinotopic maps, changing due to things such as attention, etc. Thus, they bring us closer to a low-level understanding of the neuronal underpinnings of cognitive phenomena.

<div class="img_row">
	<img class="col two" src="{{ site.baseurl }}/img/prf/retmap_flat.png" alt="" title="Retinotopic map"/>
	<img class="col one" src="{{ site.baseurl }}/img/prf/eccen_quadrant.png" alt="" title="Some Data"/>
</div>
<div class="col three caption">
	We're developing novel techniques to investigate the effects of attention on the representation of space in the brain.
</div>

How is the coding of visual space changed as a function of attention? We have developed an open-source Python package to fit these PRF profiles, and are now applying it to an experiment in which we address this question. We use a stimulus similar to the following:

<div class="photo_frame_center" align = "center">
 <video width="600" height="420" controls preload="none">
  <!-- poster="{{ site.baseurl }}/img/prf/retmap_flat.png"> -->
  <source src="{{ site.baseurl }}/img/prf/stim_movie_orig.mov" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'>
</video>
</div>




