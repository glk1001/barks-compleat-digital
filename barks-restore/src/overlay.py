import os.path

from .gmic_exe import run_gmic


def overlay_inpainted_file_with_black_ink(
    inpaint_file: str,
    black_ink_file: str,
    out_file: str,
) -> None:
    if not os.path.exists(inpaint_file):
        msg = f'File not found: "{inpaint_file}".'
        raise FileNotFoundError(msg)
    if not os.path.exists(black_ink_file):
        msg = f'File not found: "{black_ink_file}".'
        raise FileNotFoundError(msg)

    overlay_cmd = [
        inpaint_file,
        black_ink_file,
        "+channels[-1]",
        "100%",
        "+image[0]",
        "[1],0%,0%,0,0,1,[2],255",
        "output[-1]",
        out_file,
    ]

    run_gmic(overlay_cmd)
