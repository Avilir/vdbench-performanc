FROM ubi8

LABEL maintainer.mail="alayani@redhat.com"
LABEL maintainer.name="Avi Liani"
LABEL version="1.0"

#RUN dnf update -y

# Python installation
RUN dnf install --nodocs -y python3 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# Java installation
RUN dnf install --nodocs -y java

RUN dnf clean all

# Python packages installation
RUN pip3 install --user --upgrade pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --user --upgrade-strategy=only-if-needed XlsxWriter

RUN for i in `seq 0 9` ; do mkdir -p /mnt/lun$i ; done
RUN  mkdir /opt/vdbench  /mnt/pvc
COPY vdbench50407 /opt/vdbench
COPY .bashrc /root
USER root
WORKDIR /opt/vdbench
CMD ["/bin/bash"]
