#!/bin/bash
set -e

# Install PostgressSQL dependencies
dnf install -y \
  automake \
  bison \
  diffutils \
  flex \
  gcc \
  git \
  libicu \
  libicu-devel \
  make \
  perl-core \
  readline \
  readline-devel \
  zlib \
  zlib-devel

# Build and install PostgressSQL from source
git clone git://git.postgresql.org/git/postgresql.git
cd postgresql
