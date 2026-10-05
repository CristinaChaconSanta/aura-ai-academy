#!/usr/bin/env python3
"""Validate lesson files under lecciones/ against the lesson contract.

Usage: python scripts/validate_lessons.py [paths...]

Without arguments, every lecciones/**/*.md file (relative to the repo root)
is validated. Directories passed as arguments are searched recursively.
Stdlib only: the frontmatter parser supports the small YAML subset we use.
"""
from __future__ import annotations

import bisect
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "lecciones"
BANNED_PHRASES_PATH = REPO_ROOT / "docs" / "frases-prohibidas.txt"

ID_RE = re.compile(r"^N([1-7])-M\d+-L\d{2}$")
VALID_STATES = ("borrador", "verificada", "aprobada")
REQUIRED_KEYS = (
    "id", "titulo", "nivel", "duracion_min", "estado",
    "prerequisitos", "fuentes", "glosario",
)
EXPECTED_HEADINGS = (
    "## 1. El gancho",
    "## 2. La idea en una frase",
    "## 3. Las palabras nuevas",
    "## 4. La analogía",
    "## 5. Diagrama",
    "## 6. Contraste",
    "## 7. ¿Cuál falla?",
    "## 8. Ponte a prueba",
    "## 9. Mini ejercicio",
    "## 10. Cómo te ayuda a revisar a la IA",
    "## 11. Cómo se conecta",
    "## 12. Ya puedes",
    "## 13. Fuentes",
)
(
    HOOK_SECTION, GLOSSARY_SECTION, DIAGRAM_SECTION, CONTRAST_SECTION, WHICH_FAILS_SECTION,
    QUIZ_SECTION, REVIEW_AI_SECTION, CONNECTIONS_SECTION, SOURCES_SECTION,
) = (
    EXPECTED_HEADINGS[0], EXPECTED_HEADINGS[2], EXPECTED_HEADINGS[4], EXPECTED_HEADINGS[5],
    EXPECTED_HEADINGS[6], EXPECTED_HEADINGS[7], EXPECTED_HEADINGS[9], EXPECTED_HEADINGS[10],
    EXPECTED_HEADINGS[12],
)
# Section 11 is mandatory from this level on; optional below it.
CONNECTIONS_MIN_LEVEL = 2
GLOSSARY_LABELS = ("**Qué es:**", "**Ejemplo:**")
ETYMOLOGY_LABEL = "Por qué se llama así"
CONNECTIONS_LABELS = ("Viene de:", "Lleva a:", "Si lo combinas con")
AI_OUTPUT_QUOTE = "> Salida de IA:"
EXPLAIN_PROMPT = "Explícalo con tus palabras"
MAX_WORDS = 2200
MIN_DURATION, MAX_DURATION = 15, 32
MIN_GLOSSARY_TERMS, MAX_GLOSSARY_TERMS = 1, 5
MALLA_PATH = REPO_ROOT / "curriculum" / "malla.md"

TIMER = "\u23F1"  # ⏱, the time marker every heading carries (except Fuentes).
TIMER_RE = re.compile("\u23F1\uFE0F?")
DETAILS_RE = re.compile(r"<details>.*?</details>", re.DOTALL)
LESSON_REF_RE = re.compile(r"\bN\d+-M\d+-L\d{2}\b")

FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
QUESTION_RE = re.compile(r"^\d+\.\s")
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*https?://[^)\s]+[^)]*\)")
BARE_URL_RE = re.compile(r"(?<!\()https?://[^\s)>\]]+")

MAX_PARAGRAPH_WORDS = 80
MAX_SENTENCE_WORDS = 40
MAX_EM_DASHES = 3
MAX_EXCLAMATIONS = 1
MAX_EMOJIS = 3
SOURCES_HEADING = SOURCES_SECTION
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]\s|\d+\.\s)")
HTML_TAG_RE = re.compile(r"<[^>]*>")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
ANY_URL_RE = re.compile(r"https?://\S+")
SENTENCE_END_RE = re.compile(r"[.?!]+(?=\s|$)")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u231A\u231B\u23E9-\u23FA]")


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

    if "glosario" in meta:
        glossary = meta["glosario"]
        if not isinstance(glossary, list):
            errors.append("'glosario' debe ser una lista")
        else:
            count = len([item for item in glossary if item.strip()])
            if not MIN_GLOSSARY_TERMS <= count <= MAX_GLOSSARY_TERMS:
                errors.append(
                    f"'glosario' debe tener entre {MIN_GLOSSARY_TERMS} y {MAX_GLOSSARY_TERMS} "
                    f"términos (tiene {count}); si necesitas más, divide la lección"
                )

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


def section_key(heading: str) -> str:
    """Drop the time marker: '## 1. El gancho ⏱ 1 min' -> '## 1. El gancho'."""
    return TIMER_RE.split(heading, maxsplit=1)[0].rstrip(" (")


def load_lesson_ids(path: Path | None = None) -> set[str] | None:
    """Lesson IDs listed in the malla, or None if it cannot be read."""
    path = MALLA_PATH if path is None else path
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return set(LESSON_REF_RE.findall(text))


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


def _normalize_term(text: str) -> str:
    """Lowercase, strip accents (NFD minus combining marks) and collapse spaces."""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(stripped.lower().split())


def _glossary_entries(content: str) -> list[tuple[str, str]]:
    """Split section 3 into (term, entry_text) by `### ` headings outside fences."""
    entries: list[tuple[str, list[str]]] = []
    in_fence = False
    for line in content.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence and line.startswith("### "):
            entries.append((line[4:].strip(), []))
            continue
        if entries:
            entries[-1][1].append(line)
    return [(term, "\n".join(lines)) for term, lines in entries]


def _validate_glossary(content: str, glossary: list[str]) -> list[str]:
    entries = _glossary_entries(content)
    if not entries:
        return ["sección 3: necesita al menos una entrada con encabezado '### <término>'"]
    errors: list[str] = []
    for term, text in entries:
        for label in GLOSSARY_LABELS:
            if label not in text:
                errors.append(f'sección 3: a "{term}" le falta "{label}"')
        folded = any(ETYMOLOGY_LABEL in block for block in DETAILS_RE.findall(text))
        if not folded:
            errors.append(
                f'sección 3: a "{term}" le falta "{ETYMOLOGY_LABEL}" plegado en '
                f"<details><summary>{ETYMOLOGY_LABEL}</summary>...</details>"
            )
    headings = [_normalize_term(term) for term, _ in entries]
    for item in glossary:
        wanted = _normalize_term(item)
        if not wanted or not any(heading.startswith(wanted) for heading in headings):
            errors.append(f'sección 3: el término del glosario "{item}" no tiene explicación')
    return errors


def _has_fence(content: str, language: str = "") -> bool:
    return any(line.strip().startswith("```" + language) for line in content.splitlines())


def _validate_connections(content: str, malla_ids: set[str] | None) -> list[str]:
    errors: list[str] = []
    for label in CONNECTIONS_LABELS:
        if label not in content:
            errors.append(f"la sección '{CONNECTIONS_SECTION}' debe incluir la etiqueta \"{label}\"")
    if not _has_fence(content, "mermaid"):
        errors.append(f"la sección '{CONNECTIONS_SECTION}' debe contener un mini mapa ```mermaid")
    cited = sorted(set(LESSON_REF_RE.findall(content)))
    if cited and malla_ids is None:
        errors.append(f"no se pudo leer la malla para comprobar los IDs citados en '{CONNECTIONS_SECTION}'")
    elif malla_ids is not None:
        for lesson_id in cited:
            if lesson_id not in malla_ids:
                errors.append(
                    f"la sección '{CONNECTIONS_SECTION}' cita {lesson_id}, que no existe en la malla"
                )
    return errors


def _validate_sections(
    sections: dict[str, str], glossary: list[str], malla_ids: set[str] | None
) -> list[str]:
    errors: list[str] = []
    for heading, content in sections.items():
        if not content.strip():
            errors.append(f"la sección '{heading}' está vacía")

    def filled(heading: str) -> str | None:
        content = sections.get(heading)
        return content if content is not None and content.strip() else None

    hook = filled(HOOK_SECTION)
    if hook is not None and "?" not in hook:
        errors.append(
            f"la sección '{HOOK_SECTION}' debe terminar con una pregunta de predicción (falta '?')"
        )

    glossary_section = filled(GLOSSARY_SECTION)
    if glossary_section is not None:
        errors.extend(_validate_glossary(glossary_section, glossary))

    contrast = filled(CONTRAST_SECTION)
    if contrast is not None:
        lines = contrast.splitlines()
        has_row = any(line.lstrip().startswith("|") for line in lines)
        has_separator = any(TABLE_SEPARATOR_RE.match(line) and "-" in line for line in lines)
        if not (has_row and has_separator):
            errors.append(f"la sección '{CONTRAST_SECTION}' debe contener una tabla markdown")

    diagram = filled(DIAGRAM_SECTION)
    if diagram is not None and not _has_fence(diagram, "mermaid"):
        errors.append(f"la sección '{DIAGRAM_SECTION}' debe contener un bloque ```mermaid")

    which_fails = filled(WHICH_FAILS_SECTION)
    if which_fails is not None and not DETAILS_RE.search(which_fails):
        errors.append(f"la sección '{WHICH_FAILS_SECTION}' debe tener la respuesta dentro de <details>")

    quiz = filled(QUIZ_SECTION)
    if quiz is not None:
        questions = sum(1 for line in quiz.splitlines() if QUESTION_RE.match(line))
        if questions != 3:
            errors.append(
                f"la sección '{QUIZ_SECTION}' debe tener exactamente 3 preguntas numeradas "
                f"(tiene {questions})"
            )
        details = quiz.count("<details>")
        if details < 3:
            errors.append(
                f"la sección '{QUIZ_SECTION}' necesita al menos 3 bloques <details> "
                f"con la respuesta (tiene {details})"
            )
        if EXPLAIN_PROMPT not in quiz:
            errors.append(f"la sección '{QUIZ_SECTION}' debe incluir \"{EXPLAIN_PROMPT}\"")

    review_ai = filled(REVIEW_AI_SECTION)
    if review_ai is not None:
        quoted = any(line.strip().startswith(AI_OUTPUT_QUOTE) for line in review_ai.splitlines())
        if not (_has_fence(review_ai) or quoted):
            errors.append(
                f"la sección '{REVIEW_AI_SECTION}' debe mostrar un fragmento de salida de IA "
                f"(bloque de código o línea que empiece por '{AI_OUTPUT_QUOTE}')"
            )

    connections = filled(CONNECTIONS_SECTION)
    if connections is not None:
        errors.extend(_validate_connections(connections, malla_ids))

    sources = filled(SOURCES_SECTION)
    if sources is not None:
        links = len(LINK_RE.findall(sources))
        bare = len(BARE_URL_RE.findall(LINK_RE.sub("", sources)))
        if links + bare < 2:
            errors.append(
                f"la sección '{SOURCES_SECTION}' necesita al menos 2 enlaces (tiene {links + bare})"
            )
        if not DETAILS_RE.search(sources):
            errors.append(
                f"la sección '{SOURCES_SECTION}' debe ir plegada en "
                "<details><summary>Fuentes</summary>...</details>"
            )
    return errors


def _validate_body(
    body: str, glossary: list[str], level: int | None, malla_ids: set[str] | None
) -> list[str]:
    errors: list[str] = []
    lines = body.splitlines()
    headings = _heading_lines(lines)
    keys = [section_key(heading) for _, heading in headings]

    required = [
        heading for heading in EXPECTED_HEADINGS
        if heading != CONNECTIONS_SECTION or (level is not None and level >= CONNECTIONS_MIN_LEVEL)
    ]
    for heading in required:
        if heading not in keys:
            note = (
                f" (obligatorio desde el nivel {CONNECTIONS_MIN_LEVEL})"
                if heading == CONNECTIONS_SECTION else ""
            )
            errors.append(f"falta el encabezado '{heading}'{note}")

    present_expected = [key for key in keys if key in EXPECTED_HEADINGS]
    expected_order = [heading for heading in EXPECTED_HEADINGS if heading in present_expected]
    if present_expected != expected_order:
        errors.append("los encabezados de las secciones no están en el orden de la plantilla")

    for (_, heading), key in zip(headings, keys):
        if key != SOURCES_SECTION and TIMER not in heading:
            errors.append(f"el encabezado '{heading}' necesita la marca de tiempo (ej. '⏱ 2 min')")

    sections: dict[str, str] = {}
    for position, ((index, _), key) in enumerate(zip(headings, keys)):
        if key not in EXPECTED_HEADINGS or key in sections:
            continue
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        sections[key] = "\n".join(lines[index + 1:end])
    errors.extend(_validate_sections(sections, glossary, malla_ids))

    words = len(_strip_fenced_blocks(body).split())
    if words > MAX_WORDS:
        errors.append(f"la lección tiene {words} palabras; el máximo es {MAX_WORDS}")
    return errors


def load_banned_phrases(path: Path | None = None) -> list[str]:
    """Read the banned phrases file; return [] if it is missing or unreadable."""
    path = BANNED_PHRASES_PATH if path is None else path
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    phrases: list[str] = []
    for line in raw.splitlines():
        phrase = " ".join(line.split()).lower()
        if phrase and not phrase.startswith("#") and phrase not in phrases:
            phrases.append(phrase)
    return phrases


def _prose_lines(body_lines: list[str], first_line: int) -> list[tuple[int, str, str, str]]:
    """Classify body lines as (line_number, kind, text, section).

    kind is one of: "text", "list", "quote", "html", "break". "break" covers
    blank lines, headings, tables and fenced code: none of them is prose, and
    all of them end a paragraph. "html" lines (e.g. `<details>...</details>`)
    keep their text without tags: it counts for phrases, dashes, exclamations
    and emojis, but it is ignored for paragraph and sentence length.
    """
    result: list[tuple[int, str, str, str]] = []
    in_fence = False
    section = ""
    for index, line in enumerate(body_lines):
        number = first_line + index
        stripped = line.strip()
        if FENCE_RE.match(line):
            in_fence = not in_fence
            result.append((number, "break", "", section))
            continue
        if in_fence or not stripped or stripped.startswith("|"):
            result.append((number, "break", "", section))
            continue
        if stripped.startswith("#"):
            if line.startswith("## "):
                section = section_key(line.rstrip())
            result.append((number, "break", "", section))
            continue
        if stripped.startswith("<"):
            kind, text = "html", HTML_TAG_RE.sub(" ", stripped)
        elif stripped.startswith(">"):
            kind, text = "quote", stripped.lstrip(">").strip()
        elif LIST_ITEM_RE.match(line):
            kind, text = "list", LIST_ITEM_RE.sub("", line, count=1).strip()
        else:
            kind, text = "text", stripped
        result.append((number, kind, text, section))
    return result


def _clean_for_counting(text: str) -> str:
    text = INLINE_CODE_RE.sub(" ", text)
    text = MD_LINK_RE.sub(r"\1", text)
    return ANY_URL_RE.sub(" ", text)


def _join_with_offsets(lines: list[tuple[int, str]]) -> tuple[str, list[int], list[int]]:
    """Join (line_number, text) with spaces; return text, start offsets, line numbers."""
    parts: list[str] = []
    starts: list[int] = []
    numbers: list[int] = []
    position = 0
    for number, text in lines:
        starts.append(position)
        numbers.append(number)
        parts.append(text)
        position += len(text) + 1
    return " ".join(parts), starts, numbers


def _line_at(offset: int, starts: list[int], numbers: list[int]) -> int:
    return numbers[bisect.bisect_right(starts, offset) - 1]


def _check_banned_phrases(prose: list[tuple[int, str]]) -> list[str]:
    phrases = load_banned_phrases()
    if not phrases or not prose:
        return []
    normalized = [(number, " ".join(text.split()).lower()) for number, text in prose]
    joined, starts, numbers = _join_with_offsets(normalized)
    errors: list[str] = []
    for phrase in phrases:
        position = joined.find(phrase)
        if position >= 0:
            line = _line_at(position, starts, numbers)
            errors.append(f'estilo: frase prohibida "{phrase}" (línea {line})')
    return errors


def _check_sentences(block: list[tuple[int, str]]) -> list[str]:
    cleaned = [(number, _clean_for_counting(text)) for number, text in block]
    joined, starts, numbers = _join_with_offsets(cleaned)
    errors: list[str] = []
    begin = 0
    boundaries = [match.end() for match in SENTENCE_END_RE.finditer(joined)] + [len(joined)]
    for end in boundaries:
        sentence = joined[begin:end]
        words = len(sentence.split())
        if words > MAX_SENTENCE_WORDS:
            offset = begin + len(sentence) - len(sentence.lstrip())
            line = _line_at(offset, starts, numbers)
            errors.append(f"estilo: frase de {words} palabras (máx. {MAX_SENTENCE_WORDS}) en línea {line}")
        begin = end
    return errors


def _check_lengths(lines: list[tuple[int, str, str, str]]) -> list[str]:
    """Paragraph and sentence length. Paragraphs = runs of plain "text" lines;
    list items and blockquotes are checked one by one for sentence length only."""
    errors: list[str] = []
    paragraph: list[tuple[int, str]] = []

    def flush() -> None:
        if not paragraph:
            return
        words = sum(len(_clean_for_counting(text).split()) for _, text in paragraph)
        if words > MAX_PARAGRAPH_WORDS:
            errors.append(
                f"estilo: párrafo de {words} palabras (máx. {MAX_PARAGRAPH_WORDS}) en línea {paragraph[0][0]}"
            )
        errors.extend(_check_sentences(paragraph))
        paragraph.clear()

    for number, kind, text, _ in lines:
        if kind == "text":
            paragraph.append((number, text))
            continue
        flush()
        if kind in ("list", "quote"):
            errors.extend(_check_sentences([(number, text)]))
    flush()
    return errors


def _validate_style(body: str, first_line: int) -> list[str]:
    lines = _prose_lines(body.splitlines(), first_line)
    prose = [(number, text) for number, kind, text, _ in lines if kind != "break"]
    errors = _check_banned_phrases(prose)
    errors.extend(_check_lengths(lines))

    dashes = sum(
        text.count("—") for _, kind, text, section in lines
        if kind != "break" and section != SOURCES_HEADING
    )
    if dashes > MAX_EM_DASHES:
        errors.append(f"estilo: {dashes} rayas (—); máx. {MAX_EM_DASHES}. Usa punto o coma.")
    exclamations = sum(text.count("¡") for _, text in prose)
    if exclamations > MAX_EXCLAMATIONS:
        errors.append(f"estilo: {exclamations} exclamaciones; máx. {MAX_EXCLAMATIONS}")
    emojis = sum(len(EMOJI_RE.findall(TIMER_RE.sub(" ", text))) for _, text in prose)
    if emojis > MAX_EMOJIS:
        errors.append(f"estilo: {emojis} emojis; máx. {MAX_EMOJIS}")
    return errors


def _body_first_line(text: str) -> int:
    """1-based file line number of the first body line (after the closing '---')."""
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index + 2
    return 1


def validate_file(path: Path | str, malla_path: Path | str | None = None) -> list[str]:
    """Return the list of error messages for one lesson file (empty if valid).

    malla_path overrides curriculum/malla.md (used to check cited lesson IDs).
    """
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
    glossary = meta.get("glosario")
    glossary = [item for item in glossary if item.strip()] if isinstance(glossary, list) else []
    level = _as_int(meta.get("nivel"))
    malla_ids = load_lesson_ids(None if malla_path is None else Path(malla_path))
    return (
        _validate_frontmatter(meta, path)
        + _validate_body(body, glossary, level, malla_ids)
        + _validate_style(body, _body_first_line(text))
    )


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
