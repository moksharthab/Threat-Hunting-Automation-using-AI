#!/usr/bin/env python3
"""Render an IOC Analysis Markdown report to a branded Wayfair PDF.

Uses reportlab as the primary renderer. Falls back to pandoc if reportlab
is unavailable. The --logo flag places the Wayfair header image on every page.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        help="Path to a Markdown file. If omitted, read Markdown from stdin.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output PDF file.",
    )
    parser.add_argument(
        "--title",
        help="Optional PDF metadata title. Defaults to the output filename stem.",
    )
    parser.add_argument(
        "--logo",
        help="Path to a logo image to display as a header on every page.",
    )
    return parser.parse_args()


def read_markdown(input_path: str | None) -> str:
    if input_path:
        return Path(input_path).read_text(encoding="utf-8")
    if sys.stdin.isatty():
        raise SystemExit("No Markdown input provided. Use --input or pipe content on stdin.")
    return sys.stdin.read()


def split_table_row(line: str) -> list[str]:
    content = line.strip().strip("|")
    return [cell.strip() for cell in content.split("|")]


def is_separator_row(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-+:?", cell) for cell in cells)


def paragraph_text(lines: list[str]) -> str:
    return " ".join(part.strip() for part in lines if part.strip())


def markdown_to_htmlish(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", escaped)
    escaped = escaped.replace("\n", "<br/>")
    return escaped


def parse_blocks(markdown: str) -> list[tuple[str, object]]:
    lines = markdown.splitlines()
    blocks: list[tuple[str, object]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append(("code", "\n".join(code_lines).rstrip()))
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            blocks.append(("heading", (level, title)))
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = [stripped]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = [split_table_row(row) for row in table_lines if row.strip()]
            if len(rows) >= 2 and is_separator_row(table_lines[1]):
                header = rows[0]
                body = rows[2:]
            else:
                header = rows[0]
                body = rows[1:]
            blocks.append(("table", [header] + body))
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            items: list[str] = []
            while i < len(lines):
                current = lines[i].strip()
                if current.startswith("- ") or current.startswith("* "):
                    items.append(current[2:].strip())
                    i += 1
                    continue
                if not current:
                    i += 1
                break
            blocks.append(("list", items))
            continue

        if re.match(r"\d+\.\s", stripped):
            items = []
            while i < len(lines):
                current = lines[i].strip()
                if re.match(r"\d+\.\s", current):
                    items.append(re.sub(r"^\d+\.\s+", "", current))
                    i += 1
                    continue
                if not current:
                    i += 1
                break
            blocks.append(("olist", items))
            continue

        para_lines = [line]
        i += 1
        while i < len(lines):
            current = lines[i]
            current_stripped = current.strip()
            if not current_stripped:
                i += 1
                break
            if (
                current_stripped.startswith("#")
                or current_stripped.startswith("```")
                or current_stripped.startswith("|")
                or current_stripped.startswith("- ")
                or current_stripped.startswith("* ")
                or re.match(r"\d+\.\s", current_stripped)
            ):
                break
            para_lines.append(current)
            i += 1
        blocks.append(("paragraph", paragraph_text(para_lines)))

    return blocks


def render_with_reportlab(
    markdown: str, output_path: Path, title: str, logo_path: str | None = None
) -> None:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        Image,
        ListFlowable,
        ListItem,
        PageTemplate,
        Paragraph,
        Preformatted,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    logo_file = None
    logo_w = 0
    logo_h = 0
    if logo_path:
        logo_file = Path(logo_path).expanduser().resolve()
        if logo_file.exists():
            from PIL import Image as PILImage

            with PILImage.open(logo_file) as pil_img:
                orig_w, orig_h = pil_img.size
            max_logo_width = 2.5 * inch
            max_logo_height = 0.6 * inch
            scale = min(max_logo_width / orig_w, max_logo_height / orig_h, 1.0)
            logo_w = orig_w * scale
            logo_h = orig_h * scale
        else:
            logo_file = None

    page_width, page_height = letter
    left_margin = 0.65 * inch
    right_margin = 0.65 * inch
    top_margin = 0.7 * inch
    bottom_margin = 0.7 * inch
    frame_width = page_width - left_margin - right_margin

    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#6B7280"),
    )
    footer_style = ParagraphStyle(
        "Footer",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#9CA3AF"),
    )

    def _header_footer(canvas, doc):
        canvas.saveState()
        if logo_file:
            canvas.drawImage(
                str(logo_file),
                left_margin,
                page_height - top_margin + 0.05 * inch,
                width=logo_w,
                height=logo_h,
                preserveAspectRatio=True,
                mask="auto",
            )
            sub = Paragraph(
                "Security Operations | IOC Investigation Report", subtitle_style
            )
            sub_w, sub_h = sub.wrap(frame_width - logo_w - 0.3 * inch, 0.5 * inch)
            sub.drawOn(
                canvas,
                left_margin + logo_w + 0.15 * inch,
                page_height - top_margin + 0.15 * inch,
            )

        footer_text = f"CONFIDENTIAL | Wayfair Security Operations | Page {doc.page}"
        footer = Paragraph(footer_text, footer_style)
        fw, fh = footer.wrap(frame_width, 0.3 * inch)
        footer.drawOn(canvas, left_margin, 0.4 * inch)
        canvas.restoreState()

    header_space = (logo_h + 0.25 * inch) if logo_file else 0
    frame = Frame(
        left_margin,
        bottom_margin,
        frame_width,
        page_height - top_margin - bottom_margin - header_space,
        id="main",
    )

    doc = BaseDocTemplate(
        str(output_path),
        pagesize=letter,
        title=title,
        author="Wayfair SOC Automation - IOC Analysis Agent",
    )
    doc.addPageTemplates(
        [PageTemplate(id="all_pages", frames=[frame], onPage=_header_footer)]
    )

    stylesheet = getSampleStyleSheet()
    normal = stylesheet["BodyText"]
    normal.fontName = "Helvetica"
    normal.fontSize = 9
    normal.leading = 12
    normal.spaceAfter = 6

    h1 = ParagraphStyle(
        "H1",
        parent=stylesheet["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceBefore=8,
        spaceAfter=10,
        textColor=colors.HexColor("#111827"),
    )
    h2 = ParagraphStyle(
        "H2",
        parent=stylesheet["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=8,
        spaceAfter=8,
        textColor=colors.HexColor("#111827"),
    )
    h3 = ParagraphStyle(
        "H3",
        parent=stylesheet["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=6,
        spaceAfter=6,
        textColor=colors.HexColor("#1F2937"),
    )
    h4 = ParagraphStyle(
        "H4",
        parent=stylesheet["Heading4"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        spaceBefore=4,
        spaceAfter=4,
        textColor=colors.HexColor("#374151"),
    )
    code_style = ParagraphStyle(
        "CodeBlock",
        parent=normal,
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        leftIndent=10,
        rightIndent=10,
        borderPadding=8,
        borderColor=colors.HexColor("#D1D5DB"),
        borderWidth=0.5,
        borderRadius=2,
        backColor=colors.HexColor("#F3F4F6"),
        spaceBefore=6,
        spaceAfter=8,
        alignment=TA_LEFT,
    )

    story: list = []

    for kind, payload in parse_blocks(markdown):
        if kind == "heading":
            level, text = payload
            if level == 1:
                style = h1
            elif level == 2:
                style = h2
            elif level == 3:
                style = h3
            else:
                style = h4
            story.append(Paragraph(markdown_to_htmlish(text), style))
            continue

        if kind == "paragraph":
            story.append(Paragraph(markdown_to_htmlish(payload), normal))
            continue

        if kind == "list":
            items = [
                ListItem(Paragraph(markdown_to_htmlish(item), normal), leftIndent=12)
                for item in payload
            ]
            story.append(ListFlowable(items, bulletType="bullet"))
            story.append(Spacer(1, 4))
            continue

        if kind == "olist":
            items = [
                ListItem(Paragraph(markdown_to_htmlish(item), normal), leftIndent=12)
                for item in payload
            ]
            story.append(ListFlowable(items, bulletType="1"))
            story.append(Spacer(1, 4))
            continue

        if kind == "code":
            code_text = payload if payload else " "
            story.append(Preformatted(code_text, code_style))
            continue

        if kind == "table":
            rows = payload
            if not rows:
                continue
            column_count = max(len(row) for row in rows)
            normalized = [row + [""] * (column_count - len(row)) for row in rows]
            col_width = frame_width / column_count
            table = Table(
                [
                    [Paragraph(markdown_to_htmlish(cell), normal) for cell in row]
                    for row in normalized
                ],
                colWidths=[col_width] * column_count,
                repeatRows=1,
                hAlign="LEFT",
            )
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("LEADING", (0, 0), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D1D5DB")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.HexColor("#F9FAFB")],
                        ),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 8))
            continue

    if not story:
        raise SystemExit("Markdown input was empty; nothing to render.")

    doc.build(story)


def render_with_pandoc(markdown: str, output_path: Path, title: str) -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise RuntimeError("pandoc is not installed")

    with tempfile.TemporaryDirectory(prefix="ioc-analysis-") as tmpdir:
        input_path = Path(tmpdir) / "report.md"
        input_path.write_text(markdown, encoding="utf-8")
        command = [
            pandoc,
            str(input_path),
            "-o",
            str(output_path),
            "--metadata",
            f"title={title}",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "pandoc failed to produce a PDF")


def main() -> int:
    args = parse_args()
    markdown = read_markdown(args.input)
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    title = args.title or output_path.stem

    errors: list[str] = []
    logo = getattr(args, "logo", None)

    try:
        import reportlab  # noqa: F401

        render_with_reportlab(markdown, output_path, title, logo_path=logo)
        print(str(output_path))
        return 0
    except Exception as exc:
        errors.append(f"reportlab renderer failed: {exc}")

    try:
        render_with_pandoc(markdown, output_path, title)
        print(str(output_path))
        return 0
    except Exception as exc:
        errors.append(f"pandoc renderer failed: {exc}")

    lines = [
        "Unable to render PDF locally.",
        "Tried the following renderer paths:",
        *[f"- {error}" for error in errors],
        "Install reportlab or pandoc with a working PDF engine, then rerun.",
    ]
    raise SystemExit("\n".join(lines))


if __name__ == "__main__":
    raise SystemExit(main())
