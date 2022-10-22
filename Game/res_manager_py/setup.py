from setuptools import setup
from Cython.Build import cythonize

setup(
    name='res_manager',
    ext_modules=cythonize('res_manager.py')
)