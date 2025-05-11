#!/bin/bash

DIRECTORY1=$1
DIRECTORY2=$2

if [[ ! -d "${DIRECTORY1}" ]]; then
  echo "Error: Could not find directory1: \"${DIRECTORY1}\"."
  exit 1
fi
if [[ ! -d "${DIRECTORY2}" ]]; then
  echo "Error: Could not find directory2: \"${DIRECTORY2}\"."
  exit 1
fi

ERRORS=0

for file in "${DIRECTORY1}"/*; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")

    file1=${DIRECTORY1}/$filename
    file2=${DIRECTORY2}/$filename

    if [[ ! -f "${file2}" ]]; then
      echo ""
      echo "Error: Could not find file2: \"${file2}\"."
      exit 1
    fi

    #printf "${filename}: "
	
    compare -metric MAE "${file1}" "${file2}" NULL: &> /tmp/compare.txt
    if [[ $? != 0 ]]; then
      MAE=$(head -n 1 /tmp/compare.txt | awk '{print $1}')
      if [[  $(echo "1.0 < ${MAE}" | bc) -eq 1 ]]; then
        echo ""
        echo "Error comparing \"${file1}\":"
        echo
        cat /tmp/compare.txt
        echo
        echo
        ERRORS=$((ERRORS+1))
      fi
    fi
  fi
done

exit ${ERRORS}
