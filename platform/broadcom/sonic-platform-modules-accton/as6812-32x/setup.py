import os
import sys
from setuptools import setup
os.listdir

setup(
   name='as6812_32x',
   version='1.0',
   description='Module to initialize Accton AS6812-32X platforms',
   
   packages=['as6812_32x'],
   package_dir={'as6812_32x': 'as6812-32x/classes'},
)
