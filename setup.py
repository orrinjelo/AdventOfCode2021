#!/usr/bin/env python3

import os
import setuptools
import shutil
import pathlib

current_path = os.path.split(os.path.realpath(__file__))[0]
this_dir = pathlib.PurePath(current_path).name 
dist_package_name = "aoc2021"

with open(current_path + "/requirements.txt") as f:
    requirements = f.read().splitlines()

def find_ns_packages(searchdir):
    pkgs = []
    path = searchdir.replace(".", "/")
    l = setuptools.find_packages(path)
    for p in l:
        pkgs.append(searchdir + "." + p)
    return pkgs


setuptools.setup(
    name=dist_package_name,
    author='Orrin Jelo',
    author_email='orrinjelo@gmail.com',
    version='1.0',
    url='https://github.com/orrinjelo/AdventOfCode2021',
    packages=find_ns_packages("orrinjelo"),
    install_requires=requirements,
    license='MIT',
    description='Advent of Code 2021',
    long_description=open(current_path + "/README.md").read(),
    python_requires='>=3.5',
    entry_points = {
      'console_scripts': [
        'aoc=orrinjelo.aoc2021.run:main',
      ]
    }
)
