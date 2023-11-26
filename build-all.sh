#!/bin/bash

set -u

declare -r THIS_SCRIPT_PATH="$(cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

declare -r CONFIG_DIR="${THIS_SCRIPT_PATH}/Configs"
declare -r CUR_DIR=$(pwd)

cd "${CONFIG_DIR}"
if [[ "$(pwd)" != "${CONFIG_DIR}" ]]; then
    echo "ERROR: Could not cd to \"${CONFIG_DIR}\"."
    exit 1
fi

for ini_file in *.ini ; do
    python3 "${THIS_SCRIPT_PATH}/create-clean-comic.py" --ini-file "${ini_file}" ${1:-}
done

cd "${CUR_DIR}"
