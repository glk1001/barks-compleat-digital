shopt -s expand_aliases
source ${HOME}/.bash_aliases

set -e

uvenv run build-comics/batch-build-comics.py build --title "Good Neighbors"
uvenv run build-comics/batch-build-comics.py build --title "Mystery of the Swamp"
uvenv run build-comics/batch-build-comics.py build --title "Donald Duck's Best Christmas"
uvenv run build-comics/batch-build-comics.py build --title "The Bill Collectors"
uvenv run build-comics/batch-build-comics.py build --title "Donald Duck's Atom Bomb"
uvenv run build-comics/batch-build-comics.py build --title "Lost in the Andes!"
uvenv run build-comics/batch-build-comics.py build --title "Only a Poor Old Man"

