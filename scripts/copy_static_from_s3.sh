#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

aws s3 sync \
    s3://${V0_BUCKET}/cli \
    ./docs/static/cli
