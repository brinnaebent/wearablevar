from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    ld = f.read()
    

setup(name='wearablevar',
      version='0.1',
      description='Variability Metrics from Longitudinal Wearable Sensors',
      long_description= ld,
      long_description_content_type= 'text/markdown',
      url='https://github.com/brinnaebent/wearablevar',
      author='Brinnae Bent',
      author_email='runsdata@gmail.com',
      license='MIT',
      packages=['wearablevar'],
      install_requires=['pandas','numpy','datetime',
                        ],
      zip_safe=False)
