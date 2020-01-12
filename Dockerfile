FROM ubi8

LABEL maintainer.mail="alayani@redhat.com"
LABEL maintainer.name="Avi Liani"
LABEL version="1.0"

RUN dnf update -y

# Python installation
RUN dnf install -y python3 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# Java installation
RUN dnf install -y java

RUN dnf clean all

# Python packages installation
RUN pip3 install --upgrade pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --user XlsxWriter

#    && pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# create and copy the vdbench to the conatiner
RUN for i in `seq 0 9` ; do mkdir -p /mnt/lun$i ; done
RUN  mkdir /opt/vdbench  /mnt/pvc
COPY vdbench50407 /opt/vdbench
COPY .bashrc /root
USER root
WORKDIR /opt/vdbench
CMD ["/bin/bash"]
