#!/usr/bin/env bash

##############################################################################
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
##############################################################################

Tag=$1

# This is the repository that the container will push into.
# This need to be change if you want to use a different repository.
#Repo="docker-registry.upshift.redhat.com/vdbench/vdbench"
Repo="quay.io/avili/vdbench"

CMD_TOOL='podman'  # if you want this can be replace with : 'docker'

zip_file="vdbench50407.zip"

if [[ ! -f ${zip_file} ]] ; then
  echo "The source file from Oracle (${zip_file}) is not present."
  echo "Pleas download it and rerun again."
  exit 1
fi

if [[ ${Tag} == "" ]] ; then
	echo "Error: you mast give the tag name for the build !"
	exit 1
fi

echo "Creating Bin Directory : bin"
mkdir bin
if [[ $? -ne 0 ]] ; then
  echo "can not create directory !"
  exit 1
fi

echo "Moving the zip file (${zip_file}) to bin directory"
mv ${zip_file} bin/
cd bin

echo "Unzip the zip file"
unzip -q ${zip_file}

echo "Delete unnecessary files"
rm -rf aix windows hp mac sol* example* *.txt *.bat *.pdf
rm -rf linux/config.sh linux/linux32.so linux/sparc64.so

echo "Return zip file to parent directory"
mv vdbench50407.zip ../
cd classes/Vdb

echo "Downloading needed class file"
curl -Os https://community.oracle.com/servlet/JiveServlet/downloadBody/1025084-102-1-177296/CollectSlaveStats.class
if [[ $? -ne 0 ]] ; then
  echo "Can not retrieve class file"
  exit 1
fi

cd ../../../

echo "Build the container image"
${CMD_TOOL} build -t ${Repo}:${Tag} .

echo "Cleanup....."
rm -rf bin
