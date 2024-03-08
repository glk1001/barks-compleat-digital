#!/bin/bash

set -u

declare -r THIS_SCRIPT_PATH="$(cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

if [[ "${1:-}" == "--list-cmds" ]]; then
    declare -r LIST_ONLY=Y
else
    declare -r LIST_ONLY=N
fi

declare -r CONFIG_DIR="${THIS_SCRIPT_PATH}/Configs"
declare -r CUR_DIR="$(pwd)"
declare -r WORK_DIR="/tmp/barks-clean"

if [[ ! -d "${CONFIG_DIR}" ]]; then
    echo "ERROR: Could not find configs directory \"${CONFIG_DIR}\"."
    exit 1
fi

# declare -r ARGS="--log-level INFO --work-dir ${WORK_DIR} --no-cache"
declare -r ARGS="--log-level INFO --work-dir ${WORK_DIR}"

if [[ "${LIST_ONLY}" == "Y" ]]; then
    echo declare -r THIS_SCRIPT_PATH=\"${THIS_SCRIPT_PATH}\"
    echo declare -r CONFIG_DIR=\"${CONFIG_DIR}\"
    echo declare -r ARGS=\"${ARGS}\"
    echo
fi

for ini_file in ${CONFIG_DIR}/*.ini ; do
    if [[ "${LIST_ONLY}" == "Y" ]]; then
        echo python3 "\${THIS_SCRIPT_PATH}/create_clean_comic.py" \${ARGS} --ini-file \"\${CONFIG_DIR}/$(basename "${ini_file}")\"
    else
        python3 "${THIS_SCRIPT_PATH}/create_clean_comic.py" ${ARGS} --ini-file "${ini_file}" ${1:-}
        if [[ $? != 0 ]]; then
            echo "ERROR: Could not process \"${ini_file}\"."
            exit 1
        fi
    fi
done

