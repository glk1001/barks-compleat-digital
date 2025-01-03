set -e

# Test missing dest image file
rm -vf '/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/048 Seals Are So Smart!/images/2-04.jpg'

# Test missing zip file
rm -vf '/home/greg/Books/Carl Barks/The Comics/Chronological/056 Turkey Raffle [WDCS 75].cbz'

# Test missing symlinks
rm -vf '/home/greg/Books/Carl Barks/The Comics/Comics and Stories/040 Swimming Swindlers [WDCS 71].cbz'
rm -vf '/home/greg/Books/Carl Barks/The Comics/Chronological Years/1947/074 Fireman Donald [WDCS 86].cbz'

# Test missing additional file
rm -vf '/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/054 The Gold-Finder/clean_summary.txt'

# Test out of date ini file
touch --no-create "Configs/Adventure Down Under.ini"

# Test out of date zip file
touch --no-create --date "2004-07-21 20:01" "/home/greg/Books/Carl Barks/The Comics/Chronological/053 Playin' Hookey [WDCS 72].cbz"

# Test out of date zip symlinks
touch --no-create -h --date "2004-07-21 20:01" "/home/greg/Books/Carl Barks/The Comics/Comics and Stories/061 Spoil the Rod [WDCS 92].cbz"
touch --no-create -h --date "2004-07-21 20:01" "/home/greg/Books/Carl Barks/The Comics/Chronological Years/1946/051 Santa's Stormy Visit [FG 46].cbz"

# Test out of date dest image file
touch --no-create --date "2004-07-21 20:01" "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/134 A Christmas for Shacktown/images/1-00.jpg"

# Test unexpected dest images
touch "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/054 The Gold-Finder/images/2-10-SHOULD-NOT-HERE.jpg"
touch "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/059 Donald Duck's Atom Bomb/images/2-07-SHOULD-NOT-HERE.jpg"

# Test unexpected main file
touch "/home/greg/Books/Carl Barks/The Comics/MAIN-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/MAIN-SHOULD-NOT-HERE-file"

# Test unexpected aaa-Chronological-dirs files
touch "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/056 Turkey Raffle/aaa-CHRON-SUBDIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/056 Turkey Raffle/aaa-CHRON-SUBDIR-SHOULD-NOT-HERE-file"
touch "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/aaa-CHRON-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs/aaa-CHRON-DIR-SHOULD-NOT-HERE-file"

# Test unexpected Chronological files
touch "/home/greg/Books/Carl Barks/The Comics/Chronological/CHRON-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Chronological/CHRON-DIR-SHOULD-NOT-HERE-file"

# Test unexpected series files
touch "/home/greg/Books/Carl Barks/The Comics/Comics and Stories/SERIES-CS-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Comics and Stories/SERIES-CS-DIR-SHOULD-NOT-HERE-file"
touch "/home/greg/Books/Carl Barks/The Comics/Donald Duck Adventures/SERIES-DDA-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Donald Duck Adventures/SERIES-DDA-DIR-SHOULD-NOT-HERE-file"
touch "/home/greg/Books/Carl Barks/The Comics/Donald Duck Short Stories/SERIES-DDS-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Donald Duck Short Stories/SERIES-DDS-DIR-SHOULD-NOT-HERE-file"
touch "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Adventures/SERIES-USA-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Adventures/SERIES-USA-DIR-SHOULD-NOT-HERE-file"
touch "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Short Stories/SERIES-USS-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Uncle Scrooge Short Stories/SERIES-USS-DIR-SHOULD-NOT-HERE-file"

# Test unexpected year files
touch "/home/greg/Books/Carl Barks/The Comics/Chronological Years/YEARS-MAIN-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Chronological Years/YEARS-MAIN-DIR-SHOULD-NOT-HERE-file"
touch "/home/greg/Books/Carl Barks/The Comics/Chronological Years/1947/YEARS-1947-DIR-SHOULD-NOT-HERE-dir"
touch "/home/greg/Books/Carl Barks/The Comics/Chronological Years/1947/YEARS-1947-DIR-SHOULD-NOT-HERE-file"
