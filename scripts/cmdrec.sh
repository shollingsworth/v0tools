#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

srcscript="${1?"testing script"}"
shift
# srcscript=./bin/dnsrebind.py
destfile="./docs/static/cli/$(basename "${srcscript}").webm"
echo "${srcscript} -> ${destfile}"
echo "Look at ${srcscript} then press enter to continue"
read
cmdrec.py  \
    -y -k 1 \
    -g 0,0,1920,850 \
    "${destfile}" $*
open "${destfile}"
