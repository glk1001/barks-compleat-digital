#!/bin/bash


declare -r COMPARE_OUT_FILE=/tmp/compare.txt

function do_compare()
{
  local -r file1="$1"
  local -r file2="$2"
  local -r fuzz=$3

  if [[ "${fuzz}" == "0%" ]]; then
    compare -metric MAE "${file1}" "${file2}" NULL: &> "${COMPARE_OUT_FILE}"
    RESULT=$?
    if [[ ${RESULT} != 0 ]]; then
      RESULT=0
      MAE=$(head -n 1 "${COMPARE_OUT_FILE}" | awk '{print $1}')
      if [[ $(echo "1.0 < ${MAE}" | bc) -eq 1 ]]; then
        RESULT=1
      fi
    fi
  else
    # Get a dir to put the diff images
    file_dir=$(dirname "${file1}")
    # Remove "images" from the end
    file_dir=$(dirname "${file_dir}")

    file_dir=${DIFF_DIR}/$(basename "${file_dir}")
    mkdir -p "${file_dir}"

    diff_file=${file_dir}/diff-$(basename "${file1}")

    compare -fuzz ${fuzz} -metric AE "${file1}" "${file2}" "${diff_file}" &> "${COMPARE_OUT_FILE}"
    RESULT=$?
    if [[ ${RESULT} != 0 ]]; then
      RESULT=0
      AE=$(head -n 1 "${COMPARE_OUT_FILE}" | awk '{print $1}')
      AE=$(echo "$AE" | calc -p)
      if [[ $(echo "${AE} > 10000" | bc) -eq 1 ]]; then
        RESULT=1
      fi
    fi
    if [[ ${RESULT} == 0 ]]; then
      rm -f "${diff_file}"
    fi
  fi

  cat /tmp/compare.txt

  return ${RESULT}
}


declare -r DIRECTORY1=$1
declare -r DIRECTORY2=$2
declare -r FUZZ=$3
declare -r DIFF_DIR=$4

if [[ ! -d "${DIRECTORY1}" ]]; then
  echo "Error: Could not find directory1: \"${DIRECTORY1}\"."
  exit 1
fi
if [[ ! -d "${DIRECTORY2}" ]]; then
  echo "Error: Could not find directory2: \"${DIRECTORY2}\"."
  exit 1
fi
if [[ "${FUZZ}" == "" ]]; then
  echo "Error: You must specify a fuzz amount (0 means no fuzz and use MAE)."
  exit 1
fi
if [[ "${FUZZ: -1}" != "%" ]]; then
  echo "Error: The fuzz amount must end with a '%': \"${FUZZ}\"."
  exit 1
fi
if [[ "${FUZZ}" != "0%" ]]; then
  if [[ "${DIFF_DIR}" == "" ]] ; then
    echo "Error: For non-zero fuzz amount \"${FUZZ}\" you must specify a diff dir."
    exit 1
  fi
  if [[ ! -d "${DIFF_DIR}" ]]; then
    echo "Error: Could not find diff directory: \"${DIFF_DIR}\"."
    exit 1
  fi
fi

ERRORS=0

for file in "${DIRECTORY1}"/*; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")

    file1=${DIRECTORY1}/$filename
    file2=${DIRECTORY2}/$filename

    if [[ ! -f "${file2}" ]]; then
      filename_no_extension="${filename%.*}"
      file2=${DIRECTORY2}/${filename_no_extension}.jpg
    fi

    if [[ ! -f "${file2}" ]]; then
      echo ""
      echo "Warning: Could not find file2: \"${file2}\"."
      continue
    fi

    # printf "${filename}: "

    METRIC=$(do_compare "${file1}" "${file2}" ${FUZZ})

    if [[ $? == 0 ]]; then
      : # printf "ok (metric = ${METRIC})\n"
    else
      echo ""
      echo "Error comparing \"${file1}\":"
      echo
      echo ${METRIC}
      echo
      echo
      ERRORS=$((ERRORS+1))
    fi
  fi
done

exit ${ERRORS}
