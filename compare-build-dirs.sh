#!/bin/bash

set -u

# shellcheck disable=SC2155
# shellcheck disable=SC2164
declare -r THIS_SCRIPT_PATH="$(cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

BUILD_DIR1=$1
BUILD_DIR2=$2

if [[ ! -d "${BUILD_DIR1}" ]]; then
  echo "Error: Could not find build directory1: \"${BUILD_DIR1}\"."
  exit 1
fi
if [[ ! -d "${BUILD_DIR2}" ]]; then
  echo "Error: Could not find build directory2: \"${BUILD_DIR2}\"."
  exit 1
fi

ERRORS=0

for dir in "${BUILD_DIR1}"/*; do
  DIR_TO_COMPARE=$(basename "$dir")
  echo
  echo "Comparing \"${DIR_TO_COMPARE}\"..."
  bash "${THIS_SCRIPT_PATH}"/compare-build.sh "${BUILD_DIR1}/${DIR_TO_COMPARE}" "${BUILD_DIR2}/${DIR_TO_COMPARE}"
  if [[ $? != 0 ]]; then
      ERRORS=$((ERRORS+1))
  fi
done

if [[ ${ERRORS} != 0 ]]; then
  echo
  echo "There were compare errors."
fi