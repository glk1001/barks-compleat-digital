#!/bin/bash

set -u

declare -r THIS_SCRIPT_PATH="$(cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

declare -r CONFIG_DIR="${THIS_SCRIPT_PATH}/Configs"
declare -r CUR_DIR=$(pwd)

if [[ ! -d "${CONFIG_DIR}" ]]; then
    echo "ERROR: Could not find configs directory \"${CONFIG_DIR}\"."
    exit 1
fi

for ini_file in ${CONFIG_DIR}/*.ini ; do
    python3 "${THIS_SCRIPT_PATH}/create-clean-comic.py" --ini-file "${ini_file}" ${1:-}
    if [[ $? != 0 ]]; then
        echo "ERROR: Could process \"${ini_file}\"."
        exit 1
    fi
done

