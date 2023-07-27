SELF = $(lastword $(MAKEFILE_LIST))
BASEDIR = $(realpath $(dir $(SELF)))
CONTAINER_CMD ?= podman
IMG ?= sit-xtests
TESTDIR ?= $(BASEDIR)

all: image

.PHONY: image
image:
	$(CONTAINER_CMD) build -t $(IMG) -f $(BASEDIR)/Containerfile

.PHONY: test
test:
	CONTAINER_CMD=$(CONTAINER_CMD) \
	  $(BASEDIR)/run-sit-xtests.sh $(IMG) $(TESTDIR)
