set dotenv-load

default:
    @echo 'Hello, world!'

show-env:
    env


# Comics commands
info volume:
    uv run barks-cmds/fantagraphics-info.py --log-level WARN --volume {{ volume }}

build title:
    uv run build-comics/batch-build-comics.py build --log-level INFO --title "{{ title }}"

check volume:
    uv run build-comics/batch-build-comics.py check-integrity --log-level WARN --volume {{ volume }}

upscayl volume:
    uv run barks-restore/batch-upscayl.py --volume {{ volume }} |& tee /mnt/2tb_drive/workdir/{{ volume }}-upscayl.log

restore volume:
    uv run barks-restore/batch-restore-pipeline.py --work-dir /mnt/2tb_drive/workdir/barks-restore/restore --volume {{ volume }} |& tee /mnt/2tb_drive/workdir/{{ volume }}-restore.log

panels volume:
    uv run barks-restore/batch-panel-bounds.py --work-dir /mnt/2tb_drive/workdir/barks-restore/panel-bounds --volume {{ volume }}

make-empty-configs volume:
    uv run barks-cmds/make-empty-configs.py --log-level INFO --volume {{ volume }}

# Test commands
test-small:
    bash small-build-test.sh
    bash compare-build-dirs.sh "/media/greg/2tb_drive_backup/Books/Carl Barks/Regression-Tests/Small/aaa-Chronological-dirs" "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs"

compare-all:
    bash compare-build-dirs.sh "/media/greg/2tb_drive_backup/Books/Carl Barks/Regression-Tests/Big/aaa-Chronological-dirs" "/home/greg/Books/Carl Barks/The Comics/aaa-Chronological-dirs"

compare restored-orig:
    bash compare-fanta-image-dirs.sh "$HOME/Books/Carl Barks/Fantagraphics-restored" "$HOME/Books/Carl Barks/Fantagraphics-original" 50% 5000

# Backup commands
backup-to-internal:
    rsync --delete -avh /home/greg/Books/Carl\ Barks/  /mnt/2tb_drive/barks-backup/Carl\ Barks/

backup-to-external:
    rsync --delete -avh /home/greg/Books/Carl\ Barks/  /media/greg/2tb_drive_backup/barks-backup/Carl\ Barks/
    rsync --delete -avh /mnt/2tb_drive/Books/          /media/greg/2tb_drive_backup/Books/

backup-to-1tb-external:
    rsync --delete -avh /home/greg/Books/Carl\ Barks/      /media/greg/1TB_Backup/barks-backup/Carl\ Barks/
    rsync --delete -avh /mnt/2tb_drive/Books/Carl\ Barks/  /media/greg/1TB_Backup/barks-backup/Carl\ Barks-big-dirs/

backup-to-music-external:
    rsync --delete -avh /home/greg/Books/Carl\ Barks/  /media/greg/MusicBarksBackup/Books/Carl\ Barks/

backup-to-restic-external:
    rsync --delete -avh /home/greg/Books/Carl\ Barks/  /media/greg/restic_backup/Books/Carl\ Barks/
