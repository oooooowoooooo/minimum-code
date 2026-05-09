"""Extract learning sections from source files."""
from pathlib import Path

from app.schemas.module import Section


def read_file(path: Path) -> str:
    """Read a source file safely."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def extract_sections_from_python(filepath: Path) -> list[Section]:
    """Extract teaching sections from a Python file."""
    content = read_file(filepath)
    if not content:
        return []

    sections: list[Section] = []
    current_title = ""
    current_lines: list[str] = []

    for line in content.split("\n"):
        if line.startswith("# ==="):
            _append_code_section(sections, current_title, current_lines, "python")
            current_lines = []
        elif line.startswith("# ") and not current_lines:
            current_title = line[2:].strip()
        else:
            current_lines.append(line)

    _append_code_section(sections, current_title, current_lines, "python")
    return sections[:10]


def extract_sections_from_markdown(filepath: Path) -> list[Section]:
    """Extract sections from a markdown file."""
    content = read_file(filepath)
    if not content:
        return []

    sections: list[Section] = []
    current_title = ""
    current_lines: list[str] = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_title and current_lines:
                sections.append(
                    Section(
                        title=current_title,
                        content="\n".join(current_lines).strip(),
                        type="text",
                    )
                )
            current_title = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title and current_lines:
        sections.append(
            Section(
                title=current_title,
                content="\n".join(current_lines).strip(),
                type="text",
            )
        )

    return sections[:10]


def extract_sections_from_ts(filepath: Path) -> list[Section]:
    """Extract teaching sections from a TypeScript/TSX file."""
    content = read_file(filepath)
    if not content:
        return []

    sections: list[Section] = []
    current_title = ""
    current_lines: list[str] = []
    in_section = False

    for line in content.split("\n"):
        section_match = line.startswith("// SECTION ") and ":" in line

        if line.startswith("// ==="):
            _append_code_section(sections, current_title, current_lines, "typescript")
            current_title = ""
            current_lines = []
            in_section = False
        elif section_match:
            _append_code_section(sections, current_title, current_lines, "typescript")
            current_title = line.split(":", 1)[1].strip()
            current_lines = []
            in_section = True
        elif in_section:
            current_lines.append(line)
        elif not current_title and line.startswith("// "):
            current_title = line[3:].strip()

    _append_code_section(sections, current_title, current_lines, "typescript")
    return sections[:10]


def extract_sections(filepath: Path) -> list[Section]:
    """Dispatch section extraction based on file extension."""
    if filepath.suffix == ".py":
        return extract_sections_from_python(filepath)
    if filepath.suffix in (".ts", ".tsx"):
        return extract_sections_from_ts(filepath)
    if filepath.suffix == ".md":
        return extract_sections_from_markdown(filepath)
    return []


def _append_code_section(
    sections: list[Section],
    title: str,
    lines: list[str],
    language: str,
) -> None:
    if not title or not lines:
        return

    text = "\n".join(lines).strip()
    if not text:
        return

    code_markers = ["def ", "class ", "function ", "interface ", "const ", "import ", "print("]
    sections.append(
        Section(
            title=title,
            content=text,
            type="code" if any(marker in text for marker in code_markers) else "text",
            language=language,
        )
    )
