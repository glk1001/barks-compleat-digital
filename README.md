# Barks Fantagraphics Digital Comics Processor

This project is a sophisticated command-line tool designed to process, organize, and archive a digital collection of
Carl Barks' comics, specifically from the Fantagraphics "The Complete Carl Barks Disney Library" series.

It takes raw source directories containing scanned pages, restored images, upscaled versions, and manual fixes, and
intelligently combines them into a structured, consistently named, and reader-friendly digital library in `.cbz` format.

## Features

- **Intelligent Source Management**: Automatically selects the best available version of a page, prioritizing restored
  files, manual fixes, and upscaled images over original scans.
- **Comprehensive Organization**: Generates a clean, browsable library organized in multiple ways:
    - A master chronological directory.
    - Symlinked directories organized by comic book series (e.g., *Uncle Scrooge*, *Walt Disney's Comics and Stories*).
    - Symlinked directories organized by the year the story was submitted.
- **CBZ Archive Creation**: Packages each comic book into a `.cbz` file, the standard format for digital comic readers.
- **Rich Metadata Integration**: Reads and utilizes detailed metadata from the Fantagraphics collection, including
  publication dates, series information, and chronological numbering.
- **Advanced Image Handling**:
    - Supports various image formats (`.jpg`, `.png`, `.svg`).
    - Manages different processing stages: original, upscaled, restored, and OCR'd.
    - Handles special cases for censored pages or known printing errors, incorporating added or modified pages as
      needed.
- **Configuration-Driven**: Uses per-comic `.ini` files to define page order, page types (cover, splash, body, etc.),
  and other specific metadata.

---

## Requirements

- **Python**: 3.12 or newer.
- **Python Dependencies**: All required packages are listed in `requirements.txt`.
- **Source Files**: You must have access to the source comic book files, organized in a specific directory structure (
  see below).

## Installation

1. **Clone the Repository**

   ```bash
   git clone <your-repository-url>
   cd barks-fantagraphics
   ```

2. **Install Dependencies**


You need to use *uv* for package management and a Python virtual environment.

```uv
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the required packages
uv sync

# Create the alias:
alias uvenv='UV_ENV_FILE=.uvenv uv'
```

## Directory Structure

The tool expects a specific input directory structure for your source files. Each comic book should have its own root
folder, which contains an `.ini` file and various subdirectories for different page versions.

```
source_comics/
└── The-Old-Castles-Secret/
    ├── The-Old-Castles-Secret.ini
    ├── srce/
    │   └── images/
    │       ├── 001.jpg
    │       └── 002.jpg
    ├── srce-upscayled/
    │   └── images/
    │       ├── 001.png
    │       └── 002.png
    ├── srce-restored/
    │   └── images/
    │       ├── 001.png
    │       └── 002.png
    └── srce-fixes/
        └── images/
            └── 003.png  # An added or modified page
```

- **`<Comic-Title>.ini`**: The configuration file defining page order and types.
- **`srce/`**: Contains the original, unmodified scanned pages.
- **`srce-upscayled/`**: Contains versions of pages that have been run through an upscaling algorithm.
- **`srce-restored/`**: Contains professionally restored or color-corrected pages.
- **`srce-fixes/`**: Contains manually added or edited pages to correct errors or omissions in the original source.

## Usage

TO BE DONE

The script will then:

1. Scan the source directory for comic book folders.
2. Read the `.ini` file for each comic.
3. Determine the final set of pages for each comic, selecting the best version available.
4. Create a `.cbz` archive for each comic in the output directory.
5. Generate the series and year symlink structures for easy browsing.

## Output Structure

The generated output library will be organized and ready for use in any comic reader application (like YACReader,
CDisplayEx, or Chunky).

```
output_library/
├── Chronological/
│   ├── 001 - The Mummy's Ring [OS 29].cbz
│   └── 002 - The Old Castle's Secret [OS 189].cbz
├── Comics/
│   └── Uncle Scrooge/
│       └── 001 - The Old Castle's Secret [OS 189].cbz (symlink)
└── Years/
    └── 1948/
        └── 002 - The Old Castle's Secret [OS 189].cbz (symlink)
```

## License

This project is licensed under the GPL License.

This project is intended for personal, non-commercial use for managing a legally owned collection of comics. Please
respect all copyright laws.