#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

dfile="${1?"dockerfile"}"
name="v0tools_$(echo $(basename "${dfile}" | sed 's/\.Dockerfile//'))"
cd "$(dirname "$0")/.."
docker build -t "${name}" -f "${dfile}" .
docker run -it --rm \
    --hostname "${name}" \
    --name "${name}-run" \
    "${name}" make test
