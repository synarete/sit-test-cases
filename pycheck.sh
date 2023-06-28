#!/bin/bash
self=$(basename "${BASH_SOURCE[0]}")
basedir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

export LC_ALL=C
unset CDPATH

set -e
cd "${basedir}"

_run_command() {
	command -v "$1" > /dev/null && "$@"
}

_run_black() {
	_run_command black -q -l 79 --preview "${basedir}"
}

_run_flake8() {
	_run_command flake8 "${basedir}"
}

_run_mypy() {
	_run_command mypy --no-color-output "${basedir}" | grep -v "Success: "
}

_run_pylint() {
	_run_command pylint --rcfile="${basedir}/pylintrc" "${basedir}"
}

case "$1" in
	"-b"|"--black")
		_run_black
		;;
	"-f"|"--flake8")
		_run_flake8
		;;
	"-m"|"--mypy")
		_run_mypy
		;;
	"-l"|"--pylint")
		_run_pylint
		;;
	"-a"|"--all")
		_run_black
		_run_flake8
		_run_mypy
		_run_pylint
		;;			
	*)
		echo "${self} [--black|--flake8|--flake8|--pylint|--all]"
		;;
esac

