#! /bin/bash

set -u

declare -r RE='^[0-9]+$'


if [[ "${1:-}" != "--dry-run" ]]; then
  declare -r DRY_RUN="N"
else
  declare -r DRY_RUN="Y"
  shift
fi

declare -r TARGET_DIR="$1"
if [[ ! -d "${TARGET_DIR}" ]]; then
    echo "ERROR: Could not find target dir \"${TARGET_DIR}\"." >&2
    exit 1
fi

declare -r FILE_NUM_START="$2"
if ! [[ ${FILE_NUM_START} =~ ${RE} ]] ; then
    echo "ERROR: Expecting file num start \"${FILE_NUM_START}\" to be a number." >&2
    exit 1
fi

pushd "${TARGET_DIR}"

for FILE in *; do
    num="${FILE: -7}"
    num="${num: 0:3}"
    num="${num#0}"
    if ! [[ ${num} =~ ${RE} ]] ; then
        echo "Skipping file \"${FILE}\" - num = \"${num}\"" >&2
        continue
    fi
    new_num=$((10#${num} + ${FILE_NUM_START}))
    new_num=$(printf "%03d" $new_num)
    new_file="${new_num}.jpg"
    if [[ -f "${new_file}" ]]; then
        echo "ERROR: Will not overwrite file \"${new_file}\". Source is \"${FILE}\"."
        exit 1
    fi
    if [[ "${DRY_RUN}" == "Y" ]]; then
        echo mv -vn "${FILE}" "${new_file}"
    else
        mv -vn "${FILE}" "${new_file}"
    fi
done

popd
