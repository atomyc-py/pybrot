import pickle
import time
from cmath import isfinite as c_isfinite
from math import floor as m_floor
from random import random as rand
import psutil
from PIL import Image
import png

def get_max(data):
    return max(x for row in data for x in row)

class _Brot:
    def __init__(self, **kwargs):

        self.min_orbit = kwargs.get('min_orbit', 100)
        self.size = kwargs.get('size', [2000, 2000])
        self.xbounds = kwargs.get('xbounds', [-2.25, 1.25])
        self.ybounds = kwargs.get('ybounds', [-1.75, 1.75])
        self.nsamples = kwargs.get('nsamples', 1000000)

        # Convenient variables and setup for scaling complex bounds to pixels
        self.xpush = self.xbounds[1] - self.xbounds[0]
        self.ypush = self.ybounds[1] - self.ybounds[0]
        self.xdiv = self.xbounds[0]/self.xpush*self.size[0]
        self.ydiv = self.ybounds[0]/self.ypush*self.size[1]
        self.zxdiv = self.size[0]/self.xpush
        self.zydiv = self.size[1]/self.ypush

    # Gets the current date and time for saving raw and png files without first
    # specifying a name while also ensure you don't write over older data.
    def _moment_name(self):
        moment=time.strftime("%Y-%b-%d_%H:%M:%S",time.localtime())
        return 'temp_'+moment

    # Once a valid C point has been discovered, this method simply reiterates
    # back through the orbit and sends the array back to be appended to the
    # current collection.
    def _subcollect(self, j, C):
        sub_collection = [0]*j
        sub_collection[0] = C
        for k in range(1, j):
            sub_collection[k] = sub_collection[k-1]**2 + C
        return sub_collection

    # Takes in a collection of points, checks each to see if it falls within the
    # image bounds, and if so tallies the corresponding pixel.
    def _refine_img(self, img, collection):
        for Z in collection:
            if (self.xbounds[0] <= Z.real <= self.xbounds[1]
                and self.ybounds[0] <= Z.imag <= self.ybounds[1]):
                l = int(m_floor(Z.real*self.zxdiv - self.xdiv))
                m = int(m_floor(Z.imag*self.zydiv - self.ydiv))
                img[l][m] += 1
                img[l][-m] += 1
        return img

    def con_img(self, img, **kwargs):
        bits = kwargs.get('bits', 8)
        powr = kwargs.get('powr', 1/3)
        self_update = kwargs.get('self_update', False)
        bit_range = 2**bits - .001

        #reduced = [[x**powr for x in Y] for Y in img]
        n_max = get_max(img)
        r_max = n_max**powr

        r_max = r_max if r_max > 0 else 1.0
        n_max = n_max if n_max > 0 else 1.0

        r_img = [[int((bit_range*x**powr)/r_max) for x in Y] for Y in img]
        n_img = [[int((bit_range*x)/n_max) for x in Y] for Y in img]

        if self_update is True:
            self.r_img = r_img
            self.n_img = n_img
        return r_img, n_img

    # Displays the current 'r' or 'n' image.
    def display(self, mode, r_img, n_img, **kwargs):
        typ = kwargs.get('type', 'r')
        size = kwargs.get('size', [800, 800])
        kill_old = kwargs.get('kill_old', True)
        #Bizarre workaround for killing a window before showing a new one.
        if kill_old is True:
            for proc in psutil.process_iter():
                if proc.name() == 'display':
                    proc.kill()

        shw_img = Image.new(mode, (len(r_img), len(r_img[0])), None)
        if typ == 'r':
            shw_img.putdata([j for i in r_img for j in i])
        elif typ == 'n':
            shw_img.putdata([j for i in n_img for j in i])
        shw_img = shw_img.resize(size=size,resample=Image.BICUBIC)
        shw_img.show()

    # Save the raw data to a pickle.
    def saveraw(self, **kwargs):
        name = kwargs.get('name', self._moment_name() + '.p')
        with open(name, 'wb') as f:
            pickle.dump(self.img, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Save a png file
    def savepng(self, mode, r_img, n_img, **kwargs):
        typ = kwargs.get('type', 'r')
        bits = kwargs.get('bits', 8)
        size = kwargs.get('size', self.size)
        name = kwargs.get('name', self._moment_name() + '.png')

        info={'size':size, 'bitdepth':bits}
        if typ == 'r':
            png.from_array(r_img, mode=mode, info=info).save(name)
        elif typ == 'n':
            png.from_array(n_img, mode=mode, info=info).save(name)

################################################################################
class Buddha(_Brot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orbit = kwargs.get('orbit', 1000000)

        # Initialize raw, r, and n image data as zero arrays
        self.img = [[0]*self.size[0] for i in range(self.size[1])]
        self.r_img = [[0]*self.size[0] for i in range(self.size[1])]
        self.n_img = [[0]*self.size[0] for i in range(self.size[1])]

    def display(self, **kwargs):
        r_img, n_img = self.con_img(self.img, **kwargs)
        super().display('L', r_img, n_img, **kwargs)

    def savepng(self, **kwargs):
        r_img, n_img = self.con_img(self.img, **kwargs)
        super().savepng('L', r_img, n_img, **kwargs)


    # THE method.  Complete description of this method can be found in more
    # reasonable reference materials.  Just note the unconvential use of a
    # while-loop to collect nsamples of orbits rather than a more random amount
    # based solely on an n-length set of intial random C values.
    def brot(self, **kwargs):
        passes = kwargs.get('passes', 1)
        show = kwargs.get('show', False)
        saveraw_on_pass = kwargs.get('saveraw_on_pass', False)
        savepng_on_pass = kwargs.get('savepng_on_pass', False)
        nsamples = kwargs.get('nsamples', self.nsamples)
        orbit = kwargs.get('orbit', self.orbit)
        min_orbit = kwargs.get('min_orbit', self.min_orbit)

        for pas in range(passes):
            # Shows current iteration image during each pass
            if show:
                self.display()

            print('Pass ' + str(pas+1) + ' of ' + str(passes))
            i = 0
            collection = []
            while i < nsamples:
                C = complex(rand()*self.xpush + self.xbounds[0],
                            rand()*self.ypush + self.ybounds[0])
                p = ((C.real - 0.25)**2 + C.imag**2)**0.5
                if C.real < p-2*p**2 + 0.25 or \
                   (C.real+1)**2 + C.imag**2 < 0.0625:
                    continue

                Z = complex(0)
                for j in range(orbit):
                    Z = Z*Z + C
                    if not c_isfinite(Z):
                        if j < min_orbit:
                            break

                        if min_orbit < j < orbit:
                            collection += self._subcollect(j, C)
                            i += j
                            print('{0:.2f}'.format(100*i/nsamples)+'%', end='\r')
                        break

            self._refine_img(self.img, collection)
            if saveraw_on_pass:
                self.saveraw()
            if savepng_on_pass:
                self.savepng()

        self.con_img(self.img, self_update = True)
        if show:
            self.display()

################################################################################
class Nebula(_Brot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blue_orbit = kwargs.get('blue_orbit', 500)
        self.green_orbit = kwargs.get('green_orbit', 5000)
        self.red_orbit = kwargs.get('red_orbit', 50000)

        # Initialize raw, r, and n image data as zero arrays
        self.blue_img = [[0]*self.size[0] for i in range(self.size[1])]
        self.green_img = [[0]*self.size[0] for i in range(self.size[1])]
        self.red_img = [[0]*self.size[0] for i in range(self.size[1])]
        self.img = [[0,0,0]*self.size[0] for i in range(self.size[1])]
        self.r_img = [[0,0,0]*self.size[0] for i in range(self.size[1])]
        self.n_img = [[0,0,0]*self.size[0] for i in range(self.size[1])]

    def _refine_img(self, imgs, collections):
        for img, collection in zip(imgs, collections):
            self.img = super()._refine_img(img, collection)

    # Takes the raw image data and converts to both a reduced and normalized
    # form for display, to be saved as a png, or output elsewhere for whatever.
    def con_img(self, img, **kwargs):
        self_update = kwargs.get('self_update', False)
        kwargs.pop('self_update', False)
        r_img_set = []
        n_img_set = []
        for im in img:
            r_img, n_img = super(Nebula, self).con_img(im, **kwargs)
            r_img_set.append(r_img)
            n_img_set.append(n_img)
        r_img = [[(r,g,b) for r,g,b in zip(R,G,B)] for R,G,B in zip(r_img_set[2], r_img_set[1], r_img_set[0])]
        n_img = [[(r,g,b) for r,g,b in zip(R,G,B)] for R,G,B in zip(n_img_set[2], n_img_set[1], n_img_set[0])]

        if self_update is True:
            self.r_img = r_img
            self.n_img = n_img
        return r_img, n_img

    def display(self, **kwargs):

        r_img, n_img = self.con_img([self.blue_img, self.green_img, self.red_img], **kwargs)
        super().display('RGB', r_img, n_img, **kwargs)

    def savepng(self, **kwargs):
        r_img, n_img = self.con_img([self.blue_img, self.green_img, self.red_img], **kwargs)
        super().savepng('RGB', r_img, n_img, **kwargs)

    # THE method.  Complete description of this method can be found in more
    # reasonable reference materials.  Just note the unconvential use of a
    # while-loop to collect nsamples of orbits rather than a more random amount
    # based solely on an n-length set of intial random C values.
    def brot(self, **kwargs):
        passes = kwargs.get('passes', 1)
        show = kwargs.get('show', False)
        saveraw_on_pass = kwargs.get('saveraw_on_pass', False)
        savepng_on_pass = kwargs.get('savepng_on_pass', False)
        nsamples = kwargs.get('nsamples', self.nsamples)
        blue_orbit = kwargs.get('blue_orbit', self.blue_orbit)
        green_orbit = kwargs.get('green_orbit', self.green_orbit)
        red_orbit = kwargs.get('red_orbit', self.red_orbit)
        min_orbit = kwargs.get('min_orbit', self.min_orbit)

        for pas in range(passes):
            # Shows current iteration image during each pass
            if show:
                self.display()

            print('Pass ' + str(pas+1) + ' of ' + str(passes))
            i = 0
            j = 0
            k = 0
            samp = nsamples*3
            collection_blue = []
            collection_green = []
            collection_red = []
            while i < nsamples or j < nsamples or k < nsamples:
                C = complex(rand()*self.xpush + self.xbounds[0],
                            rand()*self.ypush + self.ybounds[0])
                p = ((C.real - 0.25)**2 + C.imag**2)**0.5
                if C.real < p-2*p**2 + 0.25 or \
                   (C.real+1)**2 + C.imag**2 < 0.0625:
                    continue

                Z = complex(0)
                for m in range(red_orbit):
                    Z = Z*Z + C
                    if not c_isfinite(Z):
                        if m < min_orbit:
                            break

                        if min_orbit < m < blue_orbit and i < nsamples:
                            collection_blue += self._subcollect(m, C)
                            i += m
                        elif blue_orbit < m < green_orbit and j < nsamples:
                            collection_green += self._subcollect(m, C)
                            j += m
                        elif green_orbit < m < red_orbit and k < nsamples:
                            collection_red += self._subcollect(m, C)
                            k += m
                        print('RGB: (' + '{0:.2f}'.format(100*(k)/nsamples) + ', '
                              + '{0:.2f}'.format(100*(j)/nsamples)+ ', '
                              + '{0:.2f}'.format(100*(i)/nsamples)+')%',
                              end='\r')
                        break
            print('Refining raw image data...')
            self._refine_img([self.blue_img,
                              self.green_img,
                              self.red_img],
                             [collection_blue,
                              collection_green,
                              collection_red])

            if saveraw_on_pass:
                self.saveraw()
            if savepng_on_pass:
                self.savepng()
        print('Converting image data...')
        self.con_img([self.blue_img, self.green_img, self.red_img],
                     self_update=True)
        if show:
            self.display()
        print('Complete')
