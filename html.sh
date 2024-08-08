#!/bin/bash

if [ -z "$1" ]
then
  DEST_DIR='build'
else
  DEST_DIR="$1"
fi

set -euo pipefail

cd "$(dirname "$0")"

TS="$(date +%s)"
TMP_DIR="/tmp/${TS}"
mkdir -p "${TMP_DIR}/en"
mkdir -p "${TMP_DIR}/de"

VENV_BIN='/tmp/.oxl-docs-venv/bin/activate'
if [ -f "$VENV_BIN" ]
then
  source "$VENV_BIN"
fi

sphinx-build -b html en/ "${TMP_DIR}/en/"
sphinx-build -b html de/ "${TMP_DIR}/de/"

if [ -d "$DEST_DIR" ]
then
  rm -r "$DEST_DIR"
fi
mkdir -p "${DEST_DIR}/en/"
mkdir -p "${DEST_DIR}/de/"

mv "${TMP_DIR}/en/"* "${DEST_DIR}/en/"
mv "${TMP_DIR}/de/"* "${DEST_DIR}/de/"
touch "${DEST_DIR}/en/${TS}"
touch "${DEST_DIR}/de/${TS}"
