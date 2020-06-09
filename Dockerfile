FROM ubi8

LABEL maintainer.mail="alayani@redhat.com"
LABEL maintainer.name="Avi Liani"
LABEL version="1.0"

RUN dnf update -y

# Python & Java installation
RUN dnf install --nodocs -y python3 python3-pip java
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN dnf clean all

# Python packages installation
RUN pip3 install --upgrade  pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip
#USER 1001010000
#USER 1001

COPY --chown=1001 requirements.txt /home/requirements.txt

#RUN umask 022
RUN pip install --upgrade-strategy=only-if-needed -r /home/requirements.txt

RUN for i in `seq 0 9` ; do mkdir -p /mnt/lun$i ; done
RUN  mkdir /opt/vdbench /opt/vdbench/bin /opt/vdbench/logs \
     mkdir /opt/vdbench/scripts /opt/vdbench/outputs /opt/vdbench/conf /mnt/pvc

COPY bin /opt/vdbench/bin/
COPY scripts /opt/vdbench/scripts/
COPY conf /opt/vdbench/conf/

COPY .bashrc /root

WORKDIR /opt/vdbench
CMD ["/bin/bash"]
