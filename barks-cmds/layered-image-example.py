import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR))
import layeredimage.io

# ORA
ora_file = "/home/greg/Books/Carl Barks/Fantagraphics-censorship-fixes/the-golden-fleecing/The-Golden-Fleecing-larkies-to-harpies-LAYERS.ora"
ora = layeredimage.io.openLayerImage(ora_file)

print(ora)
