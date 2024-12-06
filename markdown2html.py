#!/usr/bin/python3
"""Start a script"""
import sys
import os
import re
import hashlib


def formating_inline(line):
    """Formate text for bold and italics tag"""
    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
    return line


def but_why(line):
    """Why ???"""
    def convert_to_md5(match):
        content = match.group(1)
        md5_hash = hashlib.md5(content.encode()).hexdigest()
        return md5_hash

    line = re.sub(r"\[\[(.+?)\]\]", convert_to_md5, line)

    def remove_c(match):
        content = match.group(1)
        return re.sub(r"[cC]", "", content)
    line = re.sub(r"\(\((.+?)\)\)", remove_c, line)
    return line


def convert_to_html(md_text):
    """Convert Mardown to HTML Tag"""
    html_line = []
    in_list = False
    in_ord_list = False
    current_paragraph = []

    for line in md_text.splitlines():
        line = formating_inline(line)
        line = but_why(line)
        # Headings
        if line.startswith('#'):
            header_lvl = len(line.split()[0])
            if 1 <= header_lvl <= 6:
                content = line.strip("#").strip()
                html_line.append(f"<h{header_lvl}>{content}</h{header_lvl}>")

        # Unordered list
        elif line.startswith("- "):
            content = line[2:].strip()
            if in_ord_list:
                html_line.append("</ol>")
                in_ord_list = False
            if not in_list:
                html_line.append("<ul>")
                in_list = True
            html_line.append(f"\t<li>{content}</li>")

        # Ordered list
        elif line.startswith("* "):
            content = line[2:].strip()
            if in_list:
                html_line.append("</ul>")
                in_list = False
            if not in_ord_list:
                html_line.append("<ol>")
                in_ord_list = True
            html_line.append(f"\t<li>{content}</li>")

        # Simple text
        elif line.strip():
            if current_paragraph:
                current_paragraph.append(f"<br/>\n\t{line.strip()}")
            else:
                current_paragraph.append(line.strip())

        else:
            if current_paragraph:
                html_line.append("<p>\n\t" + '\n'.join(current_paragraph)
                                 + "\n</p>")
                current_paragraph = []

            if in_list:
                html_line.append("</ul>")
                in_list = False
            if in_ord_list:
                html_line.append("</ol>")
                in_ord_list = False

    if current_paragraph:
        html_line.append("<p>\n\t" + '\n'.join(current_paragraph) + "\n</p>\n")

    if in_list:
        html_line.append("</ul>\n")
    if in_ord_list:
        html_line.append("</ol>\n")

    return "\n".join(html_line)


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
            with open(md_file, "r") as markdown_f:
                md_content = markdown_f.read()

            html_content = convert_to_html(md_content)
            with open(html_file, "w") as html_f:
                html_f.write(html_content)
                exit(0)
        except Exception as e:
            exit(1)
