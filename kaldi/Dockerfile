FROM ubuntu:latest

ENV CPU_CORE 4

RUN \
  rm -rf /var/lib/apt/lists/* && \
  apt-get update -qq && \
  apt-get install -y \
    git bzip2 wget sox \
    g++ make python python3 \
    zlib1g-dev automake autoconf libtool subversion \
    libatlas-base-dev\
    unzip


WORKDIR /usr/local/
# Use the newest kaldi version
RUN git clone https://github.com/kaldi-asr/kaldi.git


WORKDIR /usr/local/kaldi/tools
RUN extras/check_dependencies.sh
RUN make -j $CPU_CORE

WORKDIR /usr/local/kaldi/src
RUN ./configure && make depend -j $CPU_CORE && make -j $CPU_CORE

ENV KALDI_ROOT=/usr/local/kaldi
ENV PATH="/opt/model/utils:/usr/local/kaldi/src/bin:/usr/local/kaldi/tools/openfst/bin:/usr/local/kaldi/src/fstbin:/usr/local/kaldi/src/gmmbin:/usr/local/kaldi/src/featbin:/usr/local/kaldi/src/lm:/usr/local/kaldi/src/sgmmbin:/usr/local/kaldi/src/sgmm2bin:/usr/local/kaldi/src/fgmmbin:/usr/local/kaldi/src/latbin:/usr/local/kaldi/src/nnetbin:/usr/local/kaldi/src/nnet2bin:/usr/local/kaldi/src/online2bin:/usr/local/kaldi/src/ivectorbin:/usr/local/kaldi/src/lmbin:/usr/local/kaldi/src/chainbin:/usr/local/kaldi/src/nnet3bin:/opt/model:$PATH:/usr/local/kaldi/tools/sph2pipe_v2.5:${PATH}"
ENV LC_ALL C.UTF-8

RUN mkdir /opt/model
COPY ./kaldi/model /opt/model
RUN chmod +x /opt/model/decode.sh

# Init redis workers

RUN apt-get update --fix-missing \
    && apt-get install -y python3.6 python3-pip libsndfile1

RUN mkdir /opt/api-sr
WORKDIR /opt/api-sr
COPY ./web/api-sr/requirements.txt /opt/api-sr
RUN pip3 install -r requirements.txt

COPY ./web/api-sr /opt/api-sr

RUN chmod +x init_workers.sh
CMD ./init_workers.sh

