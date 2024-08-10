#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

VENV_PATH='/tmp/.oxl-sphinx-venv'

python3 -m virtualenv "$VENV_PATH"
source "${VENV_PATH}/bin/activate"

pip install -r requirements.txt >/dev/null
