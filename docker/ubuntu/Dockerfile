FROM uphy/ubuntu-desktop-jp

# Common softs install
RUN apt-get update && \
    apt-get install -y sudo wget gcc make zlib1g-dev libssl-dev

# Python3 Install
ARG PYTHON_VER
RUN wget https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tgz && \
    tar zxvf Python-${PYTHON_VER}.tgz && \
    cd Python-${PYTHON_VER} && \
    ./configure --prefix=/usr/local/python && \
    make && make install

# Google Chrome Install
RUN curl https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Useradd for GoogleChrome user
# remove?
ARG UBUNTU_USER
ARG UBUNTU_PASS
RUN useradd -m ${UBUNTU_USER} && \
    echo ${UBUNTU_USER}:${UBUNTU_PASS} | chpasswd && \
    echo "${UBUNTU_USER} ALL=(ALL) ALL" >> /etc/sudoers