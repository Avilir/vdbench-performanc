#!/bin/bash

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

#Repo="quay.io/avili/vdbench"
# This is the repository that the container will push into.
# This need to be change if you want to use a different repository.
Repo="docker-registry.upshift.redhat.com/vdbench/vdbench"

CMD_TOOL='podman'  # if you want this can be replace with : 'docker'

zip_file="vdbench50407.zip"

if [[ ! -f ${zip_file} ]] ; then
  echo "The source file from Oracle (${zip_file}) is not present."
  echo "Pleas download it and reun again."
  exit 1
fi

if [[ ${Tag} == "" ]] ; then
	echo "Error: you mast give the tag name for the build !"
	exit 1
fi

mkdir bin
if [[ $? -ne 0 ]] ; then
  echo "can not create directory !"
  exit 1
fi

mv ${zip_file} bin/
cd bin
unzip -q ${zip_file}
rm -rf aix windows hp mac sol* example* *.txt *.bat *.pdf
rm -rf linux/config.sh linux/linux32.so linux/sparc64.so

mv vdbench50407.zip ../
cd classes/Vdb
curl -Os https://community.oracle.com/servlet/JiveServlet/downloadBody/1025084-102-1-177296/CollectSlaveStats.class
if [[ $? -ne 0 ]] ; then
  echo "Can not retrive class file"
  exit 1
fi

cd ../../../

${CMD_TOOL} build -t ${Repo}:${Tag} .

rm -rf bin
