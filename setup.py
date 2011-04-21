"""
WOFpy
-------

WOFpy is a python library for serving CUAHSI's WaterOneflow 1.0 web services

CUAHSI is the Consortium of Universities for the
Advancement of Hydrologic Science, Inc.

"""

from setuptools import Command, setup, find_packages

setup(
    name='WOFpy',
    version='0.1-alpha',
    license='BSD',
    author='James Seppi',
    author_email='james.seppi@gmail.com',
    description='a python library for serving WaterOneFlow web services',
    long_description=__doc__,
    keywords='cuahsi his wofpy water waterml cuahsi wateroneflow',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'flask>=0.6.1',
        'sqlalchemy>=0.6.7',
        'pyodbc>=2.1.8',
        'lxml>=2.2',
        'soaplib>=2.0.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

)