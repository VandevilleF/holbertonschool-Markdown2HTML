#!/usr/bin/python3
"""Start a script"""
import sys
import os


def convert_headings(md_text):
    """Convert Mardown title to HTML Tag"""
    html_line = []

    for line in md_text.splitlines():
        if line.startswith('#'):
            header_lvl = len(line.split()[0])
            if 1 <= header_lvl <= 6:
                content = line.strip("#").strip()
                html_line.append(f"<h{header_lvl}>{content}</h{header_lvl}>\n")
    return "".join(html_line)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(md_file):
        sys.stderr.write(f"Missing {md_file}\n")
        exit(1)

    else:
        try:
            with open(md_file, "r") as mardown_f:
                md_content = mardown_f.read()
            with open(html_file, "w") as html_f:
                html_f.write(convert_headings(md_content))
                exit(0)
        except Exception as e:
            exit(1)
