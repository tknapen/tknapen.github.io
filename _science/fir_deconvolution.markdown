---
layout: post
title: Finite Impulse Response Fitting
description: Estimating event-related responses from time series signals
frontpage: true
img: /img/science/more_time_signals.png
---

# Event-related responses in pupil size and fMRI measurements

<br />

It's essential to understand the signals you're looking at. The standard approaches to fMRI analysis assume the haemodynamic impulse-response function has a specific shape. Although slight changes in its timing and shape can be accounted for, it is nonetheless important to inspect the shapes of the event-related responses in one's data. One way to correctly fit these event-related responses is to use linear regression to estimate the finite impulse-response caused by specific types of events. 

<img class="col one right" src="/img/science/more_time_signals.png">

Finite impulse response fitting has some advantages over and above event-related averages. If the impulse-response your data were filtered by is slow, i.e. a low-pass filter, it may be the case that responses to multiple events overlap. This causes problems for epoch-based event-related averaging, since some parts of the data will end up in the event-related responses of several different event types. Provided enough events of all types are present in the experiment (aided even more when <a href="http://www.stat.wisc.edu/~mchung/teaching/MIA/reading/fMRI.dale.HBM.1999.pdf" target="_blank">inter-event periods are randomly drawn from an exponential distribution</a>), deconvolution can take into account this overlap and correctly attribute the signal to specific types of events. 

We have created a python class package, <a href="http://tknapen.github.io/FIRDeconvolution/" target="_blank">fir</a>, to do this. This package makes it very easy to perform quite sophisticated analyses, distilling event-related responses from timeseries signals. See below for a brief example, for more elaborate examples, see <a href="https://github.com/tknapen/FIRDeconvolution/blob/master/src/test/FIRDeconvolution_test.ipynb" target="_blank">this IPython notebook on GitHub</a> 

The package can be installed by issuing ```pip install fir --pre```, where the ```--pre``` allows you to install software that's still in development -- as fir is. 

<hr />
<br />
{% highlight python %}

from fir import FIRDeconvolution

# input_data is a numpy array sampled at signal_sample_frequency, for each of the separate signals (such as fMRI voxels). 
#     type: numpy array, (nr_signals x nr_samples)
# events are numpy arrays with event onsets in seconds. 
#     type: list of numpy arrays, (nr_event_types x nr_events_per_type)
# sample_frequency (Hz) is the frequency at which the original data are sampled (for example, 0.5 Hz for fMRI)
# deconvolution_frequency (Hz) is the frequency at which to perform the fit of the event-related signals
# the data will be resampled to this frequency before estimation.
# deconvolution_interval is a tuple, the interval in seconds over which to estimate the curves.

fd = FIRDeconvolution(
            signal = input_data, 								
            events = [events_1, events_2],						
            event_names = ['event_1', 'event_2'], 			
            sample_frequency = signal_sample_frequency,		
            deconvolution_frequency = deconv_sample_frequency,	
            deconvolution_interval = (-5,15)		
            )

# we then tell it to create its design matrix
fd.create_design_matrix()

# perform the actual regression, in this case with the standard numpy.linalg backend
fd.regress(method = 'lstsq')

# and partition the resulting betas according to the different event types
fd.betas_for_events()

fd.calculate_rsq()

{% endhighlight %}
<hr />
<br />

And this code might return the type of curves shown in the above figure. We encourage you to give this package a try when you have fMRI data from voxels, ROIs, or pupil size timeseries data. 

<!-- <div class="img_row">
	<img class="col two" src="{{ site.baseurl }}/img/prf/retmap_flat.png" alt="" title="Retinotopic map"/>
	<img class="col one" src="{{ site.baseurl }}/img/prf/eccen_quadrant.png" alt="" title="Some Data"/>
</div>
<div class="col three caption">
	We're developing novel techniques to investigate the effects of attention on the representation of space in the brain.
</div>
 -->

