#!/bin/sh

git clone --recursive --depth 1 --single-branch -b dev_4_4 git://github.com/openmicroscopy/openmicroscopy.git omero-stable

tar -zcf omero-stable.tar.gz --exclude .git omero-stable
#tar -zcf omero-stable.tar.gz \
#	--exclude .git/objects \
#	--exclude .git/modules/docs/sphinx/objects \
#	--exclude .git/modules/components/bioformats/objects \
#	--exclude .git/modules/components/tools/OmeroPy/scripts/objects \
#	omero-stable


