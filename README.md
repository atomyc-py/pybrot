# *Atomyc:* pybrot

<img src="/images/logos/hydrogen_logo_cropped.png" align="left" hspace="4" vspace="0" height=100>


<!--
<h1>
  <small>Atomyc:</small> pybrot
</h1>
-->

**pybrot** is a simple, yet powerful Python3 implementation of the buddhabrot
and nebulabrot methods, allowing users to create, modify, and display brots
derived from the Mandelbrot Set.  pybrot quickly renders deep, complex point
orbits and gives users stunning, meaningful visual insights into fractal sets.  pybrot even supports the use of PyPy3 for faster render times.


___

<html>
<body>

<img width=400 height=450 overflow="hidden" src="/images/examples/example_buddha_2.png" alt="" title="" /><img
    width=400 height=450 overflow="hidden" src="/images/examples/example_nebula_2_3.png" alt="" title="" />

<img width=200 height=225 overflow="hidden" src="/images/examples/example_buddha_1.png" alt="" title="" /><img
    width=200 height=225 overflow="hidden" src="/images/examples/example_buddha_3.png" alt="" title="" /><img
    width=200 height=225 overflow="hidden" src="/images/examples/example_nebula_1.png" alt="" title="" /><img
    width=200 height=225 overflow="hidden" src="/images/examples/example_nebula_3.png" alt="" title="" />
    
</body>
</html>

## Contents
 - [Code Examples](#code-examples)
 - [About](#about)
 - [Download and Installation](#download-and-installation)
 - [Important Notes](#important-notes)
 - [Forthcoming | To Do | Musings](#forthcoming-|-to-do-|-musings)
 - [Future Forks](#future-forks)
 - [References](#references)
 - [License](#license)

## Code Examples
```python
# Create an instance of a buddhabrot
>>> buddha = pybrot.Buddha(min_orbit=1000, orbit=750000, size=[2000,2000])
# Run three passes to generate some image data and view the updated
# image on each pass
>>> buddha.brot(passes=5, show=True)
# Compare the normalized image with a reduced/compressed range image
>>> buddha.display(type='n')
>>> buddha.display(type='r', powr=1/4, kill_old=False)
# Increase the nsamples per pass and run the brot several more times to fill it
# in a bit
>>> buddha.brot(passes=10, nsamples=1500000)
# Check the image once more to make sure it's something you like
>>> buddha.display()
# Set the bitdepth to 16 bits and save a png of the image
>>> buddha.savepng(name='my_first_brot.png', bits=16)
# Pickle the raw tally data for use elsewhere or to pickup where you left off
# at a later time
>>> buddha.saveraw(name='brots_are_fun.p')
# Play with con_img and use the output elsewhere
>>> r_img, n_img = buddha.con_img(powr=1/5, bits=8)

# Creating and rendering nebulabrots is just as easy, and you can
# edit the orbits of each color and minimum orbit any way you'd like
>>> nebula = pybrot.Nebula(min_orbit=0, blue_orbit=500, green_orbit=5000,
                           red_orbit=50000)
```

## About
Pybrot creates instances of Buddhabrots and Nebulabrots as described by Melinda
Green, discoverer of the methods.  The brots are derived from the Mandelbrot set
and the mathematics are mostly similar.  Check these [links](#references) out
for more details on this.  

The current buddha and nebula classes have been optimized for deep rendering and
as such users may find there are faster implementations (forthcoming in pybrot!)
for smaller bailout values/iterations.  What's more, pybrot was born of a
curiosity of how quickly the core algorithm could be in Python, without
the use of NumPy or CUDA.  It goes without saying then that this is not *the
fastest* brot algorithm.  For what it's worth, future forks of pybrot, or
perhaps entirely new projects, will include the NumPy/CUDA improvements I have
laying about.

Pybrot returns an image plotting the paths of C orbits on their way to infinity.
Users looking for the raw C values may look to future versions of pybrot with
expanded functionality.


## Download and Installation
To use, you can clone or download directly.  From your command line:  
```shell
# Clone the repository to your active directory
$ git clone https://github.com/atomyc-py/pybrot

# Get into the repository
$ cd pybrot

# Install
$ python3 setup.py install
```
###### pybrot works with:  
 - Python3, PyPy3  
 *Using PyPy3 is strongly suggested because of the significant increase in
 performance.*

###### pybrot requires and will attempt to install the following Python3 packages:  
* psutil, PyPNG, Pillow

## Important Notes
 * Because pybrot doesn't use NumPy, it's very memory inefficient.  Full color
   nebulabrots at 5k by 5k pixels easily exceed 8Gb in memory during raw
   conversion after the passes of a brot are complete.  The display function
   built in using Pillow actually starts throwing errors due to the large sizes
   of lists being stuffed in at this resolution.  You can still save images just
   fine however.
 * You should seriously use PyPy3 over Python3 for this.  It's just so much
   faster.


### Forthcoming | To Do | Musings

* seed values
* docstrings
* exceptions and safe-guards
* small orbit optimizations
* save-segmentation / snapshots
* meta-data saving with png and raw data
* extras tool-set
  * return plain C values within orbit limits
  * individual orbit viewer
  * view and build images by hand selecting C values and their orbits
* custom image editor and viewer to replace currently hackish/garbage solution
* hp5 database for extremely large images

### Future Forks
* NumPy implementation
* CUDA implementation for face-melting performance

## References
[The Buddhabrot Technique](http://superliminal.com/fractals/bbrot/bbrot.htm)  
*Discover Melinda Green's page.  Some history behind the buddhabrot method and basic explanations.*  
[Buddhabrot Wiki](https://en.wikipedia.org/wiki/Buddhabrot)  
*Mathematics and basic implementations of the method.*  
[Mandelbrot Wiki](https://en.wikipedia.org/wiki/Mandelbrot_set)  
*More general overview and mathematics from which the buddhabrot is derived.*  


### License
[GNU GPLv3](/LICENSE)
