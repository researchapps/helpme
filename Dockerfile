FROM continuumio/miniconda3

# docker build -t vanessa/helpme .

LABEL maintainer vsochat@stanford.edu
ENV SHELL /bin/bash
RUN apt-get update && apt-get install -y gcc \
                                        build-essential \ 
                                        libssl-dev \
                                        libffi-dev
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN /opt/conda/bin/conda install -y gxx_linux-64
RUN /opt/conda/bin/pip install setuptools && \
    /opt/conda/bin/pip install pip --upgrade && \
    /opt/conda/bin/pip install -r /code/requirements.txt && \
    cd /code && /opt/conda/bin/pip install .[all]

ENTRYPOINT ["helpme"]

ENV PATH /usr/local/bin:$PATH

WORKDIR /code
