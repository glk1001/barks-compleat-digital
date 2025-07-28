#!/bin/bash

set -u

# shellcheck disable=SC2155
# shellcheck disable=SC2164
declare -r THIS_SCRIPT_PATH="$(cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

declare -r FANTA_DIR1=$1
declare -r FANTA_DIR2=$2
declare -r COMPARE_FUZZ=$3
declare -r AE_CUTOFF=$4
declare -r DIFF_DIR=/tmp/fanta

if [[ ! -d "${FANTA_DIR1}" ]]; then
  echo "Error: Could not find directory1: \"${FANTA_DIR1}\"."
  exit 1
fi
if [[ ! -d "${FANTA_DIR2}" ]]; then
  echo "Error: Could not find directory2: \"${FANTA_DIR2}\"."
  exit 1
fi
if [[ "${COMPARE_FUZZ}" == "" ]]; then
  echo "Error: You must specify a fuzz amount."
  exit 1
fi
if [[ "${AE_CUTOFF}" == "" ]]; then
  echo "Error: You must specify an \"AE_CUTOFF\"."
  exit 1
fi

mkdir -p "${DIFF_DIR}"
rm -rf ${DIFF_DIR}/*

ERRORS=0

for dir in "${FANTA_DIR1}"/*; do
  DIR_TO_COMPARE=$(basename "$dir")/images
  #[[ $DIR_TO_COMPARE == $'Carl Barks Vol. 4 '* ]] || continue
  echo
  echo "Comparing \"${DIR_TO_COMPARE}\"..."
  bash "${THIS_SCRIPT_PATH}"/compare-images.sh "${FANTA_DIR1}/${DIR_TO_COMPARE}" "${FANTA_DIR2}/${DIR_TO_COMPARE}" ${COMPARE_FUZZ} ${AE_CUTOFF} "${DIFF_DIR}"
  if [[ $? != 0 ]]; then
      ERRORS=$((ERRORS+1))
  fi
done

if [[ ${ERRORS} != 0 ]]; then
  echo
  echo "There were compare errors."
fi
