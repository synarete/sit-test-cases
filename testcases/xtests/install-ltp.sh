#!/bin/bash
set -e

# Install LTP dependencies
dnf install -y \
  automake \
  fio \
  gcc \
  git \
  libaio-devel \
  libattr-devel \
  libcap-devel \
  libcurl-devel \
  libtool \
  libunwind-devel \
  libuuid-devel \
  lz4 \
  lz4-devel \
  make \
  openssl-devel \
  perl-core \
  perl-libwww-perl \
  zlib \
  zlib-devel

# Build and install LTP from source
git clone https://github.com/linux-test-project/ltp
cd ltp
make autotools
./configure --disable-metadata
make
make install
cd -

