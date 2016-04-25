FROM ubuntu:14.04

MAINTAINER Craig Citro <craigcitro@google.com>

# Pick up some TF dependencies
RUN apt-get update && apt-get install -y \
        bc \
        curl \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python-numpy \
        python-pip \
        python-scipy \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Install TensorFlow CPU version.
ENV TENSORFLOW_VERSION 0.8.0rc0
RUN pip --no-cache-dir install \
    http://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-${TENSORFLOW_VERSION}-cp27-none-linux_x86_64.whl

COPY server /server
WORKDIR /server
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
