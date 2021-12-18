#!/usr/bin/env python3

from pdf2image import convert_from_path
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
input_dir = Path("input")

if __name__ == "__main__":
    for file in Path("input").glob(pattern="*.pdf"):
        images = convert_from_path(file, size=1920)
        for image in images:
            image.save(str(output_dir) + "/" + file.stem + ".png")
