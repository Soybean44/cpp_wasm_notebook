"""
Title: Render Cpp
Author: Sovereign Shahid
Date: 2025-04-21
Description: This file is used as a pre-render script to extract cpp codeblocks from the qmd files
             and compile them to wasm for use in quarto web pages.
"""

import os
import subprocess
import sys

import exdown

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


cpp_files = [file for file in files if has_cpp(file)]

if cpp_files == []:
    print("Note: No cpp code blocks to render")
    sys.exit(0)


def compile_cpp(filepath: str) -> None:
    command = [
        "clang",
        "-Wall",
        "--target=wasm32",
        "-I./scripts/includes/",
        "-Os",
        "-flto",
        "--no-standard-libraries",
        "-fvisibility=hidden",
        "-std=c++14",
        "-ffunction-sections",
        "-fdata-sections",
        "-Wl,--no-entry",
        "-Wl,--strip-all",
        "-Wl,--export-dynamic",
        "-Wl,--allow-undefined",
        "-Wl,--initial-memory=131072",
        "-Wl,--error-limit=0",
        "-Wl,--lto-O3",
        "-Wl,-O3",
        "-Wl,--gc-sections",
        "-o",
        f"{filepath}.wasm",
        f"{filepath}.cpp",
    ]
    print(" ".join(command))
    subprocess.run(command, check=True)


for file in cpp_files:
    print(f"Parsing: {file}")
    cpp_code = "\n".join(line[0] for line in exdown.extract(file, syntax_filter="cpp"))
    if (filename := os.path.basename(file)) is not None:
        filename = filename.split(".")[0]
    directory = os.path.dirname(file)
    filepath = f"{directory}/{filename}" if directory != "" else filename
    with open(f"{filepath}.cpp", "w", encoding="UTF-8") as f:
        f.write(cpp_code)
    # TODO: Implement compilation to wasm
    compile_cpp(filepath)
