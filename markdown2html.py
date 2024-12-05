#!/usr/bin/python3
"""Start a script"""
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(md_file):
        sys.stderr.write("Missing {md_file}\n")
        exit(1)

    else:
        with open(html_file, "w") as f:
            f.write("")
            exit(0)
