#!/bin/sh

git clone --recursive --depth 1 --single-branch -b dev_4_4 git://github.com/openmicroscopy/openmicroscopy.git omero-stable

tar -zcf omero-stable.tar.gz --exclude .git omero-stable


