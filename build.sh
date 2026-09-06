#!/usr/bin/env bash
# Build the public site into dist/ for Cloudflare Pages.
# Only the paths listed below are deployed; everything else in the repo
# (working files, source fonts, variants, exports) stays on GitHub only.
set -euo pipefail

OUT="dist"

# Public files and directories, relative to the repo root.
PUBLIC=(
  index.html
  robots.txt
  sitemap.xml
  _headers
  css
  js
  imgs
  fonts-web
  assets/logos
  resources
  editor
)

# Paths inside the above that must NOT ship (build tooling, notes).
EXCLUDE=(
  editor/README.md
  editor/scripts
)

rm -rf "$OUT"
mkdir -p "$OUT"

for path in "${PUBLIC[@]}"; do
  if [ ! -e "$path" ]; then
    echo "build.sh: missing public path: $path" >&2
    exit 1
  fi
  mkdir -p "$OUT/$(dirname "$path")"
  cp -R "$path" "$OUT/$(dirname "$path")/"
done

for path in "${EXCLUDE[@]}"; do
  rm -rf "${OUT:?}/$path"
done

echo "build.sh: wrote $(find "$OUT" -type f | wc -l | tr -d ' ') files to $OUT/"
