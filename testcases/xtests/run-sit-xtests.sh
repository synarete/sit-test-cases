#!/bin/bash
CONTAINER_CMD=${CONTAINER_CMD:-podman}
SELF=$0
IMG="$1"
VOL="$2"
CURUID=$(id -u)
CURGID=$(id -g)

_die() { echo "${SELF}:" "$*"; exit 1; }

# Check input directory pathname
[[ -n "${VOL}" ]] || _die "usage: ${SELF} <dirname>"
[[ -d "${VOL}" ]] || _die "not a direcotry ${VOL}"

# Require taget image
# podman build -t ${IMG} -f ./Containerfile
podman inspect ${IMG} > /dev/null 2>&1 || _die "missing image: ${IMG}"

podman run -ti --rm \
  --userns keep-id:uid="${CURUID}",gid="${CURGID}" \
  --user="${CURUID}:${CURGID}" \
  --volume="/etc/group:/etc/group:ro" \
  --volume="/etc/passwd:/etc/passwd:ro" \
  --volume="/etc/shadow:/etc/shadow:ro" \
  --volume="${VOL}:/mnt/test:rw" \
  --volume="/home/${USER}:/home/${USER}:rw" \
  --workdir="/home/${USER}" \
  ${IMG} bash

