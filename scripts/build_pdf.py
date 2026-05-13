#!/usr/bin/env python3
"""
Build the Agent Skills Architecture Guide PDF from the Markdown source.

Purpose:
    This script turns `src_docs/Agent-Skills-Architecture-Guide.md` into the
    repo's distributable PDF, `Agent-Skills-Architecture-Guide-v1.pdf`.

Why this exists:
    The repository ships the PDF, but the original repo did not include a
    repeatable build command. Keeping the renderer in-repo lets future agents
    and humans update the Markdown source and regenerate the PDF without
    reverse-engineering the artifact.

Inputs:
    --source:
        Markdown source file. Defaults to:
        src_docs/Agent-Skills-Architecture-Guide.md

    --output:
        PDF destination. Defaults to:
        Agent-Skills-Architecture-Guide-v1.pdf

Outputs:
    A searchable PDF with headings, paragraphs, bullets, tables, code blocks,
    and footer page numbers.

Operational notes:
    - Requires Python 3 and reportlab.
    - Does not call external services.
    - Does not modify the Markdown source.
    - Uses simple Markdown parsing deliberately; this guide only needs stable
      headings, lists, tables, and fenced code blocks.
"""

from __future__ import annotations

import argparse
import html
import re
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


DEFAULT_SOURCE = Path("src_docs/Agent-Skills-Architecture-Guide.md")
DEFAULT_OUTPUT = Path("Agent-Skills-Architecture-Guide-v1.pdf")
DEFAULT_COVER_IMAGE = Path("assets/title-cover.png")


def build_styles() -> dict[str, ParagraphStyle]:
    """Create the small style system used by the PDF renderer."""
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="GuideTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1x",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            spaceBefore=16,
            spaceAfter=8,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2x",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor("#1f2937"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="H3x",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            spaceBefore=9,
            spaceAfter=4,
            textColor=colors.HexColor("#374151"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Bodyx",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=12.8,
            spaceAfter=5,
            textColor=colors.HexColor("#1f2937"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Smallx",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9.2,
            spaceAfter=2,
            textColor=colors.HexColor("#1f2937"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Bulletx",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.4,
            leftIndent=16,
            firstLineIndent=-8,
            spaceAfter=3,
            textColor=colors.HexColor("#1f2937"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Quotex",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=12,
            leftIndent=14,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=6,
            textColor=colors.HexColor("#4b5563"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Codex",
            fontName="Courier",
            fontSize=6.8,
            leading=8.1,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMeta",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=8,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMetaStrong",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceBefore=10,
            spaceAfter=2,
        )
    )
    return styles


def inline_markdown(raw: str) -> str:
    """Convert the subset of inline Markdown needed by this guide."""
    escaped = html.escape(raw)
    escaped = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", escaped)
    return escaped


def wrap_code_line(line: str, width: int = 92) -> list[str]:
    """Wrap long code lines so diagrams do not run off the PDF page."""
    if len(line) <= width:
        return [line]
    return textwrap.wrap(
        line,
        width=width,
        replace_whitespace=False,
        drop_whitespace=False,
    ) or [""]


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    """Parse a simple GitHub-style Markdown table."""
    rows: list[list[str]] = []
    cursor = start
    while (
        cursor < len(lines)
        and lines[cursor].strip().startswith("|")
        and lines[cursor].strip().endswith("|")
    ):
        raw = lines[cursor].strip()
        rows.append([cell.strip() for cell in raw.strip("|").split("|")])
        cursor += 1

    if len(rows) >= 2:
        separator_cells = rows[1]
        is_separator = all(
            set(cell.replace(":", "").replace("-", "").strip()) == set()
            for cell in separator_cells
        )
        if is_separator:
            rows.pop(1)

    max_cols = max(len(row) for row in rows)
    for row in rows:
        while len(row) < max_cols:
            row.append("")
    return rows, cursor


def column_widths(column_count: int) -> list[float]:
    """Choose practical table widths for the guide's common table shapes."""
    usable_width = letter[0] - 1.2 * inch
    if column_count <= 2:
        return [usable_width * 0.33, usable_width * 0.67]
    if column_count == 3:
        return [usable_width * 0.24, usable_width * 0.31, usable_width * 0.45]
    if column_count == 4:
        return [
            usable_width * 0.21,
            usable_width * 0.26,
            usable_width * 0.26,
            usable_width * 0.27,
        ]
    return [usable_width / column_count] * column_count


def add_code_block(story: list, code_lines: list[str], styles: dict[str, ParagraphStyle]) -> None:
    """Add a fenced code block to the PDF story."""
    if not code_lines:
        return
    wrapped: list[str] = []
    for line in code_lines:
        wrapped.extend(wrap_code_line(line))
    story.append(
        KeepTogether(
            [
                Preformatted("\n".join(wrapped), styles["Codex"], maxLineLength=96),
                Spacer(1, 6),
            ]
        )
    )


def add_table(story: list, rows: list[list[str]], styles: dict[str, ParagraphStyle]) -> None:
    """Add a Markdown table to the PDF story with explicit geometry."""
    if not rows:
        return
    data = [
        [Paragraph(inline_markdown(cell), styles["Smallx"]) for cell in row]
        for row in rows
    ]
    table = Table(data, colWidths=column_widths(len(rows[0])), hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f8fafc")],
                ),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8))


def markdown_to_story(markdown_text: str, styles: dict[str, ParagraphStyle]) -> list:
    """Convert the guide's Markdown subset into a ReportLab story."""
    story: list = []
    lines = markdown_text.splitlines()
    index = 0
    in_code = False
    code_buffer: list[str] = []
    first_title = True

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_buffer = []
            else:
                add_code_block(story, code_buffer, styles)
                in_code = False
                code_buffer = []
            index += 1
            continue

        if in_code:
            code_buffer.append(line.rstrip())
            index += 1
            continue

        if stripped == "---":
            story.append(Spacer(1, 8))
            index += 1
            continue

        if not stripped:
            story.append(Spacer(1, 3))
            index += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            rows, index = parse_table(lines, index)
            add_table(story, rows, styles)
            continue

        if stripped.startswith("# "):
            content = stripped[2:].strip()
            if first_title:
                story.append(Paragraph(inline_markdown(content), styles["GuideTitle"]))
                first_title = False
            else:
                story.append(Paragraph(inline_markdown(content), styles["H1x"]))
            index += 1
            continue

        if stripped.startswith("## "):
            story.append(Paragraph(inline_markdown(stripped[3:].strip()), styles["H1x"]))
            index += 1
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(inline_markdown(stripped[4:].strip()), styles["H2x"]))
            index += 1
            continue

        if stripped.startswith("#### "):
            story.append(Paragraph(inline_markdown(stripped[5:].strip()), styles["H3x"]))
            index += 1
            continue

        if stripped.startswith(">"):
            story.append(
                Paragraph(inline_markdown(stripped.lstrip(">").strip()), styles["Quotex"])
            )
            index += 1
            continue

        if re.match(r"^[-*]\s+", stripped):
            story.append(
                Paragraph(
                    inline_markdown(stripped[2:].strip()),
                    styles["Bulletx"],
                    bulletText="•",
                )
            )
            index += 1
            continue

        numbered = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if numbered:
            story.append(
                Paragraph(
                    inline_markdown(numbered.group(2)),
                    styles["Bulletx"],
                    bulletText=f"{numbered.group(1)}.",
                )
            )
            index += 1
            continue

        story.append(Paragraph(inline_markdown(stripped), styles["Bodyx"]))
        index += 1

    if in_code:
        add_code_block(story, code_buffer, styles)

    return story


def cover_story(cover_image: Path, styles: dict[str, ParagraphStyle]) -> list:
    """Create the image-led cover page and curator credit block."""
    if not cover_image.exists():
        return []

    max_width = letter[0] - 1.2 * inch
    max_height = 5.65 * inch
    image = Image(str(cover_image))
    scale = min(max_width / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    image.hAlign = "CENTER"

    return [
        Spacer(1, 0.18 * inch),
        image,
        Spacer(1, 0.18 * inch),
        Paragraph("Agent Skills Architecture Guide", styles["CoverMetaStrong"]),
        Paragraph("Curated by Shane Coy", styles["CoverMeta"]),
        Paragraph("@shaneswrld_ | github.com/shane9coy", styles["CoverMeta"]),
        Paragraph(
            "Codex-first orchestration for Codex, Claude, Hermes Agent, KiloCode, and OpenClaw",
            styles["CoverMeta"],
        ),
        PageBreak(),
    ]


def draw_footer(canvas, doc) -> None:
    """Draw consistent footer text and page numbers."""
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(0.6 * inch, 0.38 * inch, "Agent Skills Architecture Guide")
    canvas.drawRightString(letter[0] - 0.6 * inch, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(source: Path, output: Path, cover_image: Path | None = DEFAULT_COVER_IMAGE) -> None:
    """Build the PDF from source Markdown."""
    styles = build_styles()
    story = []
    if cover_image is not None:
        story.extend(cover_story(cover_image, styles))
    story.extend(markdown_to_story(source.read_text(encoding="utf-8"), styles))
    document = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.6 * inch,
        title="Agent Skills Architecture Guide",
        pageCompression=0,
    )
    document.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the guide PDF from Markdown.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--cover-image",
        type=Path,
        default=DEFAULT_COVER_IMAGE,
        help="Optional cover image path. Use an empty string to skip the cover.",
    )
    args = parser.parse_args()

    cover_image = args.cover_image if str(args.cover_image) else None
    build_pdf(args.source, args.output, cover_image)
    print(f"wrote {args.output} from {args.source}")


if __name__ == "__main__":
    main()
