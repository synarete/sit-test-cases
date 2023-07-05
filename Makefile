SELF = $(lastword $(MAKEFILE_LIST))
ROOT_DIR = $(realpath $(dir $(SELF)))

PYTHONPATH := .
TEST_INFO_FILE := test-info.yml
PATH := $(PATH):/usr/local/bin
export PYTHONPATH TEST_INFO_FILE PATH

define runtox
	@cd "$(ROOT_DIR)" && tox -e $1
endef

test:
	@pytest -v `cat testcases/tests|sed 's/^/testcases\//'`

sanity_test:
	@pytest -v testcases/consistency

.PHONY: test sanity_test

.PHONY: check-mypy
check-mypy:
	$(call runtox, "mypy")

.PHONY: check-flake8
check-flake8:
	$(call runtox, "flake8")

PHONY: check-black
check-black:
	$(call runtox, "black")

