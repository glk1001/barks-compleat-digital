set -e

declare -r COMIC_CLEAN="python3 ${HOME}/Prj/github/mcomix-barks-tools/create_clean_comic.py"
declare -r INI_DIR="${HOME}/Prj/github/mcomix-barks-tools/Configs"
declare -r WORK_DIR="/tmp/barks-clean"

mkdir -p ${WORK_DIR}

# Fix missing dest image file
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}"'/Seals Are So Smart!.ini'

# Fix missing zip file
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}"'/Turkey Raffle.ini'

# Fix missing symlinks
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}"'/Swimming Swindlers.ini' --just-symlinks
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}"'/Fireman Donald.ini' --just-symlinks

# Fix missing additional file
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}"'/The Gold-Finder.ini'

# Fix out of date ini file
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}"'/Adventure Down Under.ini' --just-zip --no-cache

# Fix out of date zip file
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}/Playin' Hookey.ini"

# Fix out of date zip symlinks
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}"'/Spoil the Rod.ini'
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}/Santa's Stormy Visit.ini"

# Fix out of date dest image file
${COMIC_CLEAN} build-single --work-dir ${WORK_DIR} --ini-file "${INI_DIR}/A Christmas for Shacktown.ini"

# Fix unexpected dest images
rm -f "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/054 The Gold-Finder/images/2-10-SHOULD-NOT-HERE.jpg"
rm -f "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/059 Donald Duck's Atom Bomb/images/2-07-SHOULD-NOT-HERE.jpg"

# Fix unexpected main file
rm -f "/home/greg/Books/Carl Barks/The Comics/MAIN-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/MAIN-SHOULD-NOT-HERE-file"

# Fix unexpected aaa-Chronological-dirs files
rm -f "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/056 Turkey Raffle/aaa-CHRON-SUBDIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/056 Turkey Raffle/aaa-CHRON-SUBDIR-SHOULD-NOT-HERE-file"
rm -f "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/aaa-CHRON-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/aaa-CHRON-DIR-SHOULD-NOT-HERE-file"

# Fix unexpected Chronological files
rm -f "/home/greg/Books/Carl Barks/The Comics/Chronological/CHRON-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Chronological/CHRON-DIR-SHOULD-NOT-HERE-file"

# Fix unexpected series files
rm -f "/home/greg/Books/Carl Barks/The Comics/Comics and Stories/SERIES-CS-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Comics and Stories/SERIES-CS-DIR-SHOULD-NOT-HERE-file"
rm -f "/home/greg/Books/Carl Barks/The Comics/Donald Duck Adventures/SERIES-DDA-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Donald Duck Adventures/SERIES-DDA-DIR-SHOULD-NOT-HERE-file"
rm -f "/home/greg/Books/Carl Barks/The Comics/Donald Duck Short Stories/SERIES-DDS-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Donald Duck Short Stories/SERIES-DDS-DIR-SHOULD-NOT-HERE-file"
rm -f "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Adventures/SERIES-USA-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Adventures/SERIES-USA-DIR-SHOULD-NOT-HERE-file"
rm -f "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Short Stories/SERIES-USS-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Short Stories/SERIES-USS-DIR-SHOULD-NOT-HERE-file"

# Fix unexpected year files
rm -f "/home/greg/Books/Carl Barks/The Comics/Chronological Years/YEARS-MAIN-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Chronological Years/YEARS-MAIN-DIR-SHOULD-NOT-HERE-file"
rm -f "/home/greg/Books/Carl Barks/The Comics/Chronological Years/1947/YEARS-1947-DIR-SHOULD-NOT-HERE-dir"
rm -f "/home/greg/Books/Carl Barks/The Comics/Chronological Years/1947/YEARS-1947-DIR-SHOULD-NOT-HERE-file"
