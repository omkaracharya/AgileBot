#!/bin/bash

export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

if ! rpm -q docker >/dev/null 2>&1 ; then
  echo ""
  echo ""
  echo "#########################################"
  echo "###         Installing docker.         ##"
  echo "#########################################"
  echo ""
  yum install docker -y >/dev/null
fi

if ! service docker status >/dev/null 2>&1 ; then
  echo ""
  echo ""
  echo "#########################################"
  echo "###     starting docker service.       ##"
  echo "#########################################"
  echo ""
  service docker start
fi


if ! rpm -q git >/dev/null 2>&1 ; then
  echo ""
  echo ""
  echo "#########################################"
  echo "###         Installing git.            ##"
  echo "#########################################"
  echo ""
  yum install git -y >/dev/null
fi

if [ ! -d CSC-510-Project ] ; then
  echo ""
  echo ""
  echo "#########################################"
  echo "###         Cloning git repo.          ##"
  echo "#########################################"
  echo ""
  git clone https://github.ncsu.edu/oachary/CSC-510-Project.git
fi

cd CSC-510-Project/

if [ ! -f Deploy/docker/DockerFile ] ; then
  echo ""
  echo "DockerFile is  missing"
  exit 1
else
  cp Deploy/docker/DockerFile .
fi

echo ""
echo ""
echo "#########################################"
echo "###      Builing docker image.         ##"
echo "#########################################"
echo ""
docker build -f DockerFile .
