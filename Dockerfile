FROM centos:7

RUN yum update -y \
    && yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y java screen which openssh-server openssh-clients\
    && yum install -y python36u python36u-libs python36u-devel python36u-pip \
#    && yum install -y which gcc \
#    && yum install -y openldap-devel \ 
    && yum clean all

# pipenv installation
#RUN pip install pipenv
#RUN ln -s /usr/bin/pip3 /bin/pip
#RUN pip install --upgrade pip \
#    && pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#RUN rm /usr/bin/python
## python must be pointing to python3.6
RUN ln -s /usr/bin/python3.6 /usr/bin/python3 \
    && ln -s /usr/bin/pip3.6 /usr/bin/pip3

RUN pip3 install --upgrade pip
RUN pip3 install XlsxWriter

# create and copy the vdbench to the conatiner
RUN for i in `seq 0 9` ; do mkdir -p /mnt/lun$i ; done \
    && mkdir /opt/vdbench
COPY vdbench50407 /opt/vdbench

WORKDIR /opt/vdbench

CMD ["/bin/bash"]
