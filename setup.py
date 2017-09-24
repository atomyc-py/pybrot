from setuptools import setup

l_desc = '''pybrot is a simple, yet powerful Python3 implementation of
    the buddhabrot and nebulabrot methods, allowing users to create, modify, and
    display brots derived from the Mandelbrot Set. pybrot quickly renders deep,
    complex point orbits and gives users stunning, meaningful visual insights
    into fractal sets. pybrot even supports the use of PyPy3 for faster render
    times.'''

setup(name='pybrot',
      version='0.1',
      description='''Create, Modify, and Display Buddhabrots and Nebulabrots
                     Derived From the Mandelbrot Set.''',
      long_description = l_desc,
      url='http://github.com/atomyc-py/pybrot',
      author='Steven K.Terry.',
      author_email='stkterry@gmail.com',
      license='GNU GPLv3.0',
      packages=['pybrot'],
      install_requires=['psutil', 'pypng', 'Pillow'],
      zip_safe=False)
