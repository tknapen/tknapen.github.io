---
layout: post
title: Population Receptive Field Mapping
description: Mapping how visual information is encoded in the human brain
img: /img/prf/eccen_quadrant.png
---

With fMRI, we measure thousands of neurons in each voxel. Because neurons with similar receptive fields are close together on the retinotopic map, each population of neurons measured in a single fMRI voxel will have similar receptive fields. This means that it is possible to chart, for each voxel, its population receptive field, or pRF, i.e. the region of visual space that the voxel’s neural tissue analyses. We estimate these population receptive fields to thoroughly understand how the visual system encodes information. Recent studies using this novel encoding-model approach emphasize the flexibility of information encoding in the retinotopic maps, changing due to things such as attention, etc. Thus, they bring us closer to a low-level understanding of the neuronal underpinnings of cognitive phenomena.

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
<!--   <source src="/img/blog/movie/movie.ogv" type='video/ogg; codecs="theora, vorbis"'>
  <source src="/img/blog/movie/movie.webm" type='video/webm; codecs="vp8, vorbis"'>
  <iframe src="http://player.vimeo.com/video/24959362?title=0&amp;byline=0&amp;portrait=0"
   width="400" height="300"></iframe>
 --> </video>
</div>




