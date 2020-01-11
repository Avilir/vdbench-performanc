#!/bin/bash

#######################################################
#
# This script is for building the vdbench container.
# it used the 'podman' for the build and accept the build TAG 
# from the user.
# without the tag the script will stop and exit with error.
# the script must be run from the top directory of the vdbench.
#
# the repository that it will create is on quay, but this can be changed.
#
# Author : Avi Liani <alayani@redhat.com>
# Creation date : Jan,11,2020
#

Tag=$1
Repo="quay.io/avili/vdbench"

if [[ ${Tag} -eq "" ]] ; then
	echo "Error: you mast give the tag name for the build !"
	exit 1
fi

echo podman build -t ${Repo}:${Tag} .
