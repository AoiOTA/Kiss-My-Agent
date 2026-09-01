#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd -P)
exec python3 "$script_dir/validate.py" --root "$script_dir/.." "$@"
