#!/usr/bin/env python3
"""Validate lesson files under lecciones/ against the lesson contract.

Usage: python scripts/validate_lessons.py [paths...]

Without arguments, every lecciones/**/*.md file (relative to the repo root)
is validated. Directories passed as arguments are searched recursively.
Stdlib only: the frontmatter parser supports the small YAML subset we use.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "lecciones"

ID_RE = re.compile(r"^N([1-7])-M\d+-L\d{2}$")
VALID_STATES = ("borrador", "verificada", "aprobada")
REQUIRED_KEYS = (
    "id", "titulo", "nivel", "duracion_min", "estado",
    "prerequisitos", "fuentes", "glosario",
)
EXPECTED_HEADINGS = (
    "## 1. El gancho",
    "## 2. La idea en una frase",
    "## 3. La analogía",
    "## 4. Contraste",
    "## 5. Diagrama",
    "## 6. Bueno vs. malo",
    "## 7. Ponte a prueba",
    "## 8. Mini ejercicio",
    "## 9. Cómo te ayuda a revisar a la IA",
    "## 10. Fuentes",
)
MAX_WORDS = 1400
MIN_DURATION, MAX_DURATION = 5, 20

FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
QUESTION_RE = re.compile(r"^\d+\.\s")
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*https?://[^)\s]+[^)]*\)")
BARE_URL_RE = re.compile(r"(?<!\()https?://[^\s)>\]]+")


class FrontmatterError(ValueError):
    """Raised when the frontmatter block is missing or malformed."""


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_inline_list(value: str) -> list[str]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    return [_strip_quotes(item) for item in inner.split(",") if item.strip()]


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_text, body). Raise FrontmatterError if absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("falta el bloque de metadatos (frontmatter) entre '---' al inicio del archivo")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1:])
    raise FrontmatterError("el bloque de metadatos (frontmatter) no se cierra con '---'")


def parse_frontmatter(block: str) -> dict[str, object]:
    """Parse `key: value`, inline lists and block lists."""
    data: dict[str, object] = {}
    current_list_key: str | None = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if current_list_key is not None and raw[:1] in (" ", "\t") and stripped.startswith("-"):
            items = data[current_list_key]
            assert isinstance(items, list)
            items.append(_strip_quotes(stripped[1:]))
            continue
        current_list_key = None
        if ":" not in raw:
            raise FrontmatterError(f"línea de metadatos no válida: {stripped!r}")
        key, _, value = raw.partition(":")
        key, value = key.strip(), value.strip()
        if not value:
            data[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            data[key] = _parse_inline_list(value)
        else:
            data[key] = _strip_quotes(value)
    return data


def _as_int(value: object) -> int | None:
    if isinstance(value, str) and re.fullmatch(r"-?\d+", value.strip()):
        return int(value)
    return None


def _validate_frontmatter(meta: dict[str, object], path: Path) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in meta:
            errors.append(f"falta el campo obligatorio '{key}' en los metadatos")

    level_from_id: int | None = None
    lesson_id = meta.get("id")
    if "id" in meta:
        match = ID_RE.match(lesson_id) if isinstance(lesson_id, str) else None
        if not match:
            errors.append(f"'id' no válido ({lesson_id!r}); formato esperado: N1-M1-L01")
        else:
            level_from_id = int(match.group(1))
            if not path.name.startswith(f"{lesson_id}-"):
                errors.append(f"el nombre del archivo debe empezar por '{lesson_id}-'")
            if path.parent.name != f"N{level_from_id}":
                errors.append(
                    f"la lección debe estar en la carpeta 'N{level_from_id}', no en '{path.parent.name}'"
                )

    if "titulo" in meta:
        title = meta["titulo"]
        if not isinstance(title, str) or not title.strip():
            errors.append("'titulo' no puede estar vacío")

    if "nivel" in meta:
        level = _as_int(meta["nivel"])
        if level is None or not 1 <= level <= 7:
            errors.append(f"'nivel' debe ser un número entero entre 1 y 7 (es {meta['nivel']!r})")
        elif level_from_id is not None and level != level_from_id:
            errors.append(f"'nivel' ({level}) no coincide con el nivel del id (N{level_from_id})")

    if "duracion_min" in meta:
        duration = _as_int(meta["duracion_min"])
        if duration is None or not MIN_DURATION <= duration <= MAX_DURATION:
            errors.append(
                f"'duracion_min' debe ser un entero entre {MIN_DURATION} y {MAX_DURATION} "
                f"(es {meta['duracion_min']!r})"
            )

    if "estado" in meta and meta["estado"] not in VALID_STATES:
        errors.append(f"'estado' debe ser uno de {', '.join(VALID_STATES)} (es {meta['estado']!r})")

    if "prerequisitos" in meta:
        prerequisites = meta["prerequisitos"]
        if not isinstance(prerequisites, list):
            errors.append("'prerequisitos' debe ser una lista (puede ser [])")
        else:
            for item in prerequisites:
                if not ID_RE.match(item):
                    errors.append(f"prerrequisito no válido: {item!r}; formato esperado: N1-M1-L01")

    if "fuentes" in meta:
        sources = meta["fuentes"]
        if not isinstance(sources, list):
            errors.append("'fuentes' debe ser una lista")
        else:
            if len(sources) < 2:
                errors.append(f"'fuentes' necesita al menos 2 elementos (tiene {len(sources)})")
            for item in sources:
                if not item.startswith(("http://", "https://")):
                    errors.append(f"fuente no válida: {item!r}; debe empezar por http:// o https://")

    if "glosario" in meta and not isinstance(meta["glosario"], list):
        errors.append("'glosario' debe ser una lista (puede ser [])")

    return errors


def _heading_lines(body_lines: list[str]) -> list[tuple[int, str]]:
    """Return (line_index, heading) for `## ` lines outside fenced blocks."""
    headings: list[tuple[int, str]] = []
    in_fence = False
    for index, line in enumerate(body_lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("## "):
            headings.append((index, line.rstrip()))
    return headings


def _strip_fenced_blocks(text: str) -> str:
    kept: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append(line)
    return "\n".join(kept)


def _validate_sections(sections: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for heading, content in sections.items():
        if not content.strip():
            errors.append(f"la sección '{heading}' está vacía")

    contrast = sections.get(EXPECTED_HEADINGS[3])
    if contrast is not None and contrast.strip():
        lines = contrast.splitlines()
        has_row = any(line.lstrip().startswith("|") for line in lines)
        has_separator = any(TABLE_SEPARATOR_RE.match(line) and "-" in line for line in lines)
        if not (has_row and has_separator):
            errors.append(f"la sección '{EXPECTED_HEADINGS[3]}' debe contener una tabla markdown")

    diagram = sections.get(EXPECTED_HEADINGS[4])
    if diagram is not None and diagram.strip():
        if not any(line.strip().startswith("```mermaid") for line in diagram.splitlines()):
            errors.append(f"la sección '{EXPECTED_HEADINGS[4]}' debe contener un bloque ```mermaid")

    quiz = sections.get(EXPECTED_HEADINGS[6])
    if quiz is not None and quiz.strip():
        questions = sum(1 for line in quiz.splitlines() if QUESTION_RE.match(line))
        if questions != 3:
            errors.append(
                f"la sección '{EXPECTED_HEADINGS[6]}' debe tener exactamente 3 preguntas numeradas "
                f"(tiene {questions})"
            )
        details = quiz.count("<details>")
        if details < 3:
            errors.append(
                f"la sección '{EXPECTED_HEADINGS[6]}' necesita al menos 3 bloques <details> "
                f"con la respuesta (tiene {details})"
            )

    sources = sections.get(EXPECTED_HEADINGS[9])
    if sources is not None and sources.strip():
        links = len(LINK_RE.findall(sources))
        bare = len(BARE_URL_RE.findall(LINK_RE.sub("", sources)))
        if links + bare < 2:
            errors.append(
                f"la sección '{EXPECTED_HEADINGS[9]}' necesita al menos 2 enlaces (tiene {links + bare})"
            )
    return errors


def _validate_body(body: str) -> list[str]:
    errors: list[str] = []
    lines = body.splitlines()
    headings = _heading_lines(lines)
    found = [heading for _, heading in headings]

    missing = [heading for heading in EXPECTED_HEADINGS if heading not in found]
    for heading in missing:
        errors.append(f"falta el encabezado '{heading}'")

    present_expected = [heading for heading in found if heading in EXPECTED_HEADINGS]
    expected_order = [heading for heading in EXPECTED_HEADINGS if heading in present_expected]
    if present_expected != expected_order:
        errors.append("los encabezados de las secciones no están en el orden de la plantilla")

    sections: dict[str, str] = {}
    for position, (index, heading) in enumerate(headings):
        if heading not in EXPECTED_HEADINGS or heading in sections:
            continue
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        sections[heading] = "\n".join(lines[index + 1:end])
    errors.extend(_validate_sections(sections))

    words = len(_strip_fenced_blocks(body).split())
    if words > MAX_WORDS:
        errors.append(f"la lección tiene {words} palabras; el máximo es {MAX_WORDS}")
    return errors


def validate_file(path: Path | str) -> list[str]:
    """Return the list of error messages for one lesson file (empty if valid)."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"no se pudo leer el archivo: {exc}"]
    try:
        block, body = split_frontmatter(text)
        meta = parse_frontmatter(block)
    except FrontmatterError as exc:
        return [str(exc)]
    return _validate_frontmatter(meta, path) + _validate_body(body)


def collect_files(args: list[str]) -> list[Path]:
    if not args:
        return sorted(LESSONS_DIR.glob("**/*.md")) if LESSONS_DIR.is_dir() else []
    files: list[Path] = []
    for arg in args:
        target = Path(arg)
        if target.is_dir():
            files.extend(sorted(target.glob("**/*.md")))
        else:
            files.append(target)
    return files


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    files = collect_files(args)
    if not files:
        print("No hay lecciones que validar.")
        return 0
    has_errors = False
    for file in files:
        errors = validate_file(file)
        if errors:
            has_errors = True
            for message in errors:
                print(f"ERROR {file}: {message}")
        else:
            print(f"OK {file}")
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
