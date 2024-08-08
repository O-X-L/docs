#!/usr/bin/env bash

set -euo pipefail

VENV_PATH='/tmp/.oxl-docs-venv'

python3 -m virtualenv "$VENV_PATH"
source "${VENV_PATH}/bin/activate"
