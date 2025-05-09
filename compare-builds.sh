#!/bin/bash

set -u

declare -r THIS_SCRIPT_PATH="$(cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

DIRECTORY1=$1
DIRECTORY2=$2

if [[ ! -d "${DIRECTORY1}" ]]; then
  echo "Error: Could not find build directory1: \"${DIRECTORY1}\"."
  exit 1
fi
if [[ ! -d "${DIRECTORY2}" ]]; then
  echo "Error: Could not find build directory2: \"${DIRECTORY2}\"."
  exit 1
fi

diff -r --exclude=images -I "time of run" -I "Created:" -I "timestamp" "${DIRECTORY1}" "${DIRECTORY2}"
if [[ $? != 0 ]]; then
  echo "Error in diff"
  exit 1
fi

bash ${THIS_SCRIPT_PATH}/compare-images.sh "${DIRECTORY1}/images" "${DIRECTORY2}/images"
