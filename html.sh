#!/bin/bash

if [ -z "$1" ]
then
  DEST_DIR='build'
else
  DEST_DIR="$1"
fi

set -euo pipefail

function log() {
  msg="$1"
  echo ''
  echo "### ${msg} ###"
  echo ''
}

cd "$(dirname "$0")"

SRC_DIR="$(pwd)"

TS="$(date +%s)"
TMP_DIR="/tmp/${TS}"
mkdir -p "${TMP_DIR}/en"
mkdir -p "${TMP_DIR}/de"

VENV_BIN='/tmp/.oxl-sphinx-venv/bin/activate'
if [ -f "$VENV_BIN" ]
then
  source "$VENV_BIN"
fi

log 'COPYING STATICS'
cp -r "${SRC_DIR}/static/"* "${SRC_DIR}/en/_static/"
cp -r "${SRC_DIR}/static/"* "${SRC_DIR}/de/_static/"

log 'BUILDING DOCS'
sphinx-build -b html en/ "${TMP_DIR}/en/" >/dev/null
sphinx-build -b html de/ "${TMP_DIR}/de/" >/dev/null

log 'PATCHING METADATA'
cp "${SRC_DIR}/meta/"* "${TMP_DIR}/en/"
cp "${SRC_DIR}/meta/"* "${TMP_DIR}/de/"
cp "${SRC_DIR}/en/_meta/"* "${TMP_DIR}/en/"
cp "${SRC_DIR}/de/_meta/"* "${TMP_DIR}/de/"

HTML_META_SRC="<meta charset=\"utf-8\" />"
HTML_META="${HTML_META_SRC}<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; img-src 'self' https://files.oxl.at; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval';\">"
HTML_META="${HTML_META}<link rel=\"icon\" type=\"image/svg\" href=\"https://files.oxl.at/img/oxl.svg\">"
HTML_META_EN="${HTML_META}<link rel=\"alternate\" href=\"https://docs.o-x-l.at\" hreflang=\"de\">"
HTML_META_DE="${HTML_META}<link rel=\"alternate\" href=\"https://docs.o-x-l.com\" hreflang=\"en\">"
HTML_LOGO_LINK_SRC='href=".*Go to homepage"'
HTML_LOGO_LINK_DE='href="https://www.oxl.at" title="OXL IT Services Website"'
HTML_LOGO_LINK_EN='href="https://www.o-x-l.com" title="OXL IT Services Website"'

cd "${TMP_DIR}/en/"

sed -i "s|$HTML_META_SRC|$HTML_META_EN|g" *.html
sed -i "s|$HTML_META_SRC|$HTML_META_EN|g" */*.html
sed -i "s|$HTML_LOGO_LINK_SRC|$HTML_LOGO_LINK_EN|g" *.html
sed -i "s|$HTML_LOGO_LINK_SRC|$HTML_LOGO_LINK_EN|g" */*.html

cd "${TMP_DIR}/de/"

sed -i "s|$HTML_META_SRC|$HTML_META_DE|g" *.html
sed -i "s|$HTML_META_SRC|$HTML_META_DE|g" */*.html
sed -i "s|$HTML_LOGO_LINK_SRC|$HTML_LOGO_LINK_DE|g" *.html
sed -i "s|$HTML_LOGO_LINK_SRC|$HTML_LOGO_LINK_DE|g" */*.html

HTML_LANG_EN='html lang="en"'
HTML_LANG_DE='html lang="de"'

sed -i "s|$HTML_LANG_EN|$HTML_LANG_DE|g" *.html
sed -i "s|$HTML_LANG_EN|$HTML_LANG_DE|g" */*.html





log 'ACTIVATING'
cd "$SRC_DIR"
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

log 'FINISHED'
