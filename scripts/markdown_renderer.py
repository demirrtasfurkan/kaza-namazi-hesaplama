#!/usr/bin/env python3
"""Small, dependency-free Markdown renderer for CMS-authored article bodies."""

from html import escape
import re
import unicodedata


def slugify(value):
    table = str.maketrans({"ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g", "ü": "u", "Ü": "u", "ö": "o", "Ö": "o", "ç": "c", "Ç": "c"})
    value = unicodedata.normalize("NFKD", value.translate(table)).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "bolum"


def inline(text):
    tokens = []

    def hold(value):
        tokens.append(value)
        return f"\x00{len(tokens) - 1}\x00"

    text = escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", lambda m: hold(f"<code>{m.group(1)}</code>"), text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+|/[^\s)]*|#[^\s)]*)\)",
        lambda m: hold(f'<a href="{escape(m.group(2), quote=True)}">{m.group(1)}</a>'),
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    for index, value in enumerate(tokens):
        text = text.replace(f"\x00{index}\x00", value)
    return text


def _is_table_separator(line):
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def render_markdown(markdown, include_toc=True):
    lines = (markdown or "").replace("\r\n", "\n").split("\n")
    output, paragraph, headings = [], [], []
    list_type = None
    quote_lines = []
    i = 0

    def flush_paragraph():
        if paragraph:
            output.append("<p>" + inline(" ".join(x.strip() for x in paragraph)) + "</p>")
            paragraph.clear()

    def close_list():
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    def flush_quote():
        if quote_lines:
            output.append("<blockquote>" + render_markdown("\n".join(quote_lines), include_toc=False) + "</blockquote>")
            quote_lines.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush_paragraph(); close_list(); flush_quote(); i += 1; continue

        heading = re.match(r"^(#{2,4})\s+(.+?)\s*$", line)
        if heading:
            flush_paragraph(); close_list(); flush_quote()
            level = len(heading.group(1)); label = heading.group(2).strip(); anchor = slugify(re.sub(r"[*_`]", "", label))
            base = anchor; suffix = 2
            while any(existing[1] == anchor for existing in headings):
                anchor = f"{base}-{suffix}"; suffix += 1
            headings.append((level, anchor, re.sub(r"[*_`]", "", label)))
            output.append(f'<h{level} id="{anchor}">{inline(label)}</h{level}>'); i += 1; continue

        if i + 1 < len(lines) and "|" in line and _is_table_separator(lines[i + 1]):
            flush_paragraph(); close_list(); flush_quote()
            headers = [x.strip() for x in line.strip().strip("|").split("|")]
            i += 2; rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([x.strip() for x in lines[i].strip().strip("|").split("|")]); i += 1
            head = "".join(f"<th>{inline(x)}</th>" for x in headers)
            body = "".join("<tr>" + "".join(f"<td>{inline(x)}</td>" for x in row) + "</tr>" for row in rows)
            output.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
            continue

        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        numbered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if bullet or numbered:
            flush_paragraph(); flush_quote(); wanted = "ul" if bullet else "ol"
            if list_type != wanted:
                close_list(); output.append(f"<{wanted}>"); list_type = wanted
            output.append(f"<li>{inline((bullet or numbered).group(1))}</li>"); i += 1; continue

        if line.lstrip().startswith(">"):
            flush_paragraph(); close_list(); quote_lines.append(line.lstrip()[1:].lstrip()); i += 1; continue

        if line.lstrip().startswith("<"):
            flush_paragraph(); close_list(); flush_quote(); output.append(line); i += 1; continue

        paragraph.append(line); i += 1

    flush_paragraph(); close_list(); flush_quote()
    body = "\n".join(output)
    if include_toc and len(headings) >= 2:
        items = "".join(f'<li><a href="#{anchor}">{escape(label)}</a></li>' for level, anchor, label in headings if level == 2)
        if items:
            body = f'<nav class="article-toc" aria-label="İçindekiler"><strong>İçindekiler</strong><ol>{items}</ol></nav>\n' + body
    return body
