"""
Title: Render Cpp
Author: Sovereign Shahid
Date: 2025-04-21
Description: This file is used as a pre-render script to extract cpp codeblocks from the qmd files
             and compile them to wasm for use in quarto web pages.
"""

import ctypes
import os
import shutil
import subprocess
import sys

import exdown

# --- CONSTANTS --- #
CFLAGS = [
    "-Wall",
    "--target=wasm32",
    "-I./scripts/includes/",  # this includes the wasm.h file
    "-Os",
    "-flto",
    "--no-standard-libraries",
    "-fvisibility=hidden",
    "-std=c++14",
    "-ffunction-sections",  # This makes the function names normal
    "-fdata-sections",
]

LDFLAGS = [
    "--no-entry",
    "--strip-all",
    "--export-dynamic",
    "--allow-undefined",  # This allows for external definitions in js
    "--initial-memory=131072",
    "--error-limit=0",
    "--lto-O3",
    "-O3",
    "--gc-sections",
]

file_str = os.getenv("QUARTO_PROJECT_INPUT_FILES")
if file_str is None:
    print("Error: needs to be run as a pre-render script", file=sys.stderr)
    sys.exit(1)

files = file_str.splitlines(keepends=False)


def has_cpp(filename: str) -> bool:
    with open(filename, "r", encoding="UTF-8") as f:
        for line in f:
            if r"```cpp" in line:
                print(f"{filename} has cpp")
                return True
    return False


# Get all the files to be compiled to
cpp_files = [file for file in files if has_cpp(file)]

if cpp_files == []:
    print("Note: No cpp code blocks to render")
    sys.exit(0)


def compile_cpp(filepath: str) -> None:
    command = (
        ["clang"]
        + CFLAGS
        + [f"-Wl,{flag}" for flag in LDFLAGS]
        + [
            "-o",
            f"{filepath}.wasm",
            f"{filepath}.cpp",
        ]
    )
    subprocess.run(command, check=True)


for file in cpp_files:
    print(f"Parsing: {file}")

    # check if the file exists and get the filename
    if file is not None:
        # Extract cpp code from qmd codeblocks
        cpp_code = "\n".join(
            line[0] for line in exdown.extract(file, syntax_filter="cpp")
        )
        filename = file.split(".")[0]

        with open(f"{filename}.cpp", "w", encoding="UTF-8") as f:
            f.write(cpp_code)
        compile_cpp(filename)
