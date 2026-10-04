import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "validate_lessons.py"

_spec = importlib.util.spec_from_file_location("validate_lessons", SCRIPT)
validate_lessons = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_lessons)
validate_file = validate_lessons.validate_file

VALID_ID = "N1-M1-L01"
VALID_NAME = f"{VALID_ID}-que-pasa-cuando-escribes-una-url.md"

FRONTMATTER = """---
id: N1-M1-L01
titulo: "¿Qué pasa cuando escribes una URL?"
nivel: 1
duracion_min: 10
estado: borrador
prerequisitos: []
fuentes:
  - https://developer.mozilla.org/es/docs/Learn/Getting_started_with_the_web/How_the_Web_works
  - https://www.cloudflare.com/learning/dns/what-is-dns/
glosario: [DNS, servidor]
---
"""

SECTIONS = {
    "## 1. El gancho": "Escribes una dirección y en un segundo aparece una página.",
    "## 2. La idea en una frase": "El navegador pide la página a un servidor y la dibuja.",
    "## 3. La analogía": "Es como pedir comida a domicilio con una dirección.",
    "## 4. Contraste": (
        "| Sin DNS | Con DNS |\n"
        "| :-- | :-- |\n"
        "| Recuerdas números | Recuerdas nombres |"
    ),
    "## 5. Diagrama": "```mermaid\nflowchart LR\n  A[Navegador] --> B[DNS]\n```",
    "## 6. Bueno vs. malo": "Bueno: usar HTTPS. Malo: ignorar el candado.",
    "## 7. Ponte a prueba": (
        "1. ¿Qué hace el DNS?\n"
        "<details><summary>Respuesta</summary>Traduce nombres a IP.</details>\n\n"
        "2. ¿Quién dibuja la página?\n"
        "<details><summary>Respuesta</summary>El navegador.</details>\n\n"
        "3. ¿Qué protege HTTPS?\n"
        "<details><summary>Respuesta</summary>La conexión.</details>"
    ),
    "## 8. Mini ejercicio": "Abre las herramientas de desarrollo y mira la pestaña Red.",
    "## 9. Cómo te ayuda a revisar a la IA": "Si la IA dice que el DNS guarda páginas, sabrás que se equivoca.",
    "## 10. Fuentes": (
        "- [MDN](https://developer.mozilla.org/)\n"
        "- [Cloudflare](https://www.cloudflare.com/learning/dns/what-is-dns/)"
    ),
}


def build_lesson(sections=None, frontmatter=FRONTMATTER):
    sections = SECTIONS if sections is None else sections
    body = "\n\n".join(f"{heading}\n\n{content}" for heading, content in sections.items())
    return f"{frontmatter}\n# Título\n\n{body}\n"


def write_lesson(root: Path, text: str, folder="N1", name=VALID_NAME) -> Path:
    path = root / "lecciones" / folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def mutate(text: str, old: str, new: str) -> str:
    assert old in text, f"fixture does not contain {old!r}"
    return text.replace(old, new, 1)


def with_section(heading, content):
    return {**SECTIONS, heading: content}


def test_valid_lesson_has_no_errors(tmp_path):
    assert validate_file(write_lesson(tmp_path, build_lesson())) == []


@pytest.mark.parametrize(
    "old, new, expected",
    [
        ("id: N1-M1-L01", "id: N1-M1-L1", "'id' no válido"),
        ("id: N1-M1-L01", "id: N8-M1-L01", "'id' no válido"),
        ("nivel: 1", "nivel: 2", "no coincide con el nivel del id"),
        ("nivel: 1", "nivel: 9", "'nivel' debe ser"),
        ("duracion_min: 10", "duracion_min: 4", "'duracion_min'"),
        ("duracion_min: 10", "duracion_min: 21", "'duracion_min'"),
        ("estado: borrador", "estado: publicada", "'estado' debe ser"),
        ("prerequisitos: []", "prerequisitos: [N1-M1-L01, tema-previo]", "prerrequisito no válido"),
        ("  - https://www.cloudflare.com/learning/dns/what-is-dns/\n", "", "al menos 2 elementos"),
        ("  - https://www.cloudflare.com", "  - www.cloudflare.com", "fuente no válida"),
        ('titulo: "¿Qué pasa cuando escribes una URL?"', 'titulo: ""', "'titulo' no puede estar vacío"),
        ("glosario: [DNS, servidor]\n", "", "falta el campo obligatorio 'glosario'"),
    ],
)
def test_frontmatter_violations(tmp_path, old, new, expected):
    text = mutate(build_lesson(), old, new)
    errors = validate_file(write_lesson(tmp_path, text))
    assert any(expected in error for error in errors), errors


def test_filename_must_start_with_id(tmp_path):
    errors = validate_file(write_lesson(tmp_path, build_lesson(), name="N1-M1-L02-otra.md"))
    assert any("nombre del archivo" in error for error in errors), errors


def test_folder_must_match_level(tmp_path):
    errors = validate_file(write_lesson(tmp_path, build_lesson(), folder="N2"))
    assert any("carpeta 'N1'" in error for error in errors), errors


def test_missing_frontmatter(tmp_path):
    text = build_lesson().split("---\n", 2)[2]
    errors = validate_file(write_lesson(tmp_path, text))
    assert len(errors) == 1 and "frontmatter" in errors[0]


def test_missing_heading(tmp_path):
    sections = {k: v for k, v in SECTIONS.items() if k != "## 8. Mini ejercicio"}
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any("falta el encabezado '## 8. Mini ejercicio'" in error for error in errors), errors


def test_wrong_heading_order(tmp_path):
    items = list(SECTIONS.items())
    items[1], items[2] = items[2], items[1]
    errors = validate_file(write_lesson(tmp_path, build_lesson(dict(items))))
    assert any("orden" in error for error in errors), errors


def test_empty_section(tmp_path):
    sections = with_section("## 6. Bueno vs. malo", "   ")
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any("'## 6. Bueno vs. malo' está vacía" in error for error in errors), errors


@pytest.mark.parametrize(
    "heading, content, expected",
    [
        ("## 4. Contraste", "Sin DNS recuerdas números; con DNS, nombres.", "tabla markdown"),
        ("## 5. Diagrama", "```\nA --> B\n```", "```mermaid"),
        ("## 10. Fuentes", "- [MDN](https://developer.mozilla.org/)", "al menos 2 enlaces"),
    ],
)
def test_section_content_rules(tmp_path, heading, content, expected):
    errors = validate_file(write_lesson(tmp_path, build_lesson(with_section(heading, content))))
    assert any(expected in error for error in errors), errors


def test_bare_urls_count_as_sources(tmp_path):
    content = "- https://developer.mozilla.org/\n- https://www.cloudflare.com/"
    sections = with_section("## 10. Fuentes", content)
    assert validate_file(write_lesson(tmp_path, build_lesson(sections))) == []


def _quiz(count, details=None):
    details = count if details is None else details
    lines = []
    for number in range(1, count + 1):
        lines.append(f"{number}. Pregunta {number}")
        if number <= details:
            lines.append("<details><summary>Respuesta</summary>Sí.</details>")
    lines.extend("<details><summary>Extra</summary>Sí.</details>" for _ in range(details - count))
    return "\n".join(lines)


@pytest.mark.parametrize(
    "quiz, expected",
    [
        (_quiz(2, 3), "exactamente 3 preguntas numeradas (tiene 2)"),
        (_quiz(4), "exactamente 3 preguntas numeradas (tiene 4)"),
        (_quiz(3, 2), "al menos 3 bloques <details>"),
    ],
)
def test_quiz_rules(tmp_path, quiz, expected):
    sections = with_section("## 7. Ponte a prueba", quiz)
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any(expected in error for error in errors), errors


def test_too_many_words(tmp_path):
    sections = with_section("## 1. El gancho", "palabra " * 1400)
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any("palabras; el máximo es 1400" in error for error in errors), errors


def test_fenced_code_does_not_count_as_words(tmp_path):
    long_code = "```mermaid\nflowchart LR\n" + "  A --> B\n" * 600 + "```"
    sections = with_section("## 5. Diagrama", long_code)
    assert validate_file(write_lesson(tmp_path, build_lesson(sections))) == []


def test_collects_all_errors(tmp_path):
    text = mutate(build_lesson(), "estado: borrador", "estado: x")
    text = mutate(text, "duracion_min: 10", "duracion_min: 99")
    assert len(validate_file(write_lesson(tmp_path, text))) == 2


def test_frontmatter_block_and_inline_lists_parse():
    block = (
        "fuentes:\n  - 'https://a.example'\n  - https://b.example\n"
        "glosario: [DNS, \"IP\"]\nprerequisitos: []\ntitulo: 'Hola'"
    )
    meta = validate_lessons.parse_frontmatter(block)
    assert meta["fuentes"] == ["https://a.example", "https://b.example"]
    assert meta["glosario"] == ["DNS", "IP"]
    assert meta["prerequisitos"] == []
    assert meta["titulo"] == "Hola"


def test_inline_sources_list_is_valid(tmp_path):
    frontmatter = mutate(
        FRONTMATTER,
        "fuentes:\n  - https://developer.mozilla.org/es/docs/Learn/Getting_started_with_the_web/How_the_Web_works\n"
        "  - https://www.cloudflare.com/learning/dns/what-is-dns/\n",
        "fuentes: [https://developer.mozilla.org/, https://www.cloudflare.com/]\n",
    )
    assert validate_file(write_lesson(tmp_path, build_lesson(frontmatter=frontmatter))) == []


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)],
        capture_output=True, text=True, cwd=REPO,
    )


def test_cli_exit_zero_on_valid(tmp_path):
    path = write_lesson(tmp_path, build_lesson())
    result = run_cli(path)
    assert result.returncode == 0
    assert result.stdout.startswith("OK ")


def test_cli_exit_one_on_invalid(tmp_path):
    path = write_lesson(tmp_path, mutate(build_lesson(), "estado: borrador", "estado: x"))
    result = run_cli(path)
    assert result.returncode == 1
    assert "ERROR" in result.stdout and "'estado'" in result.stdout


def test_cli_empty_dir_prints_notice(tmp_path):
    result = run_cli(tmp_path)
    assert result.returncode == 0
    assert "No hay lecciones" in result.stdout


def test_repo_lessons_are_valid():
    files = sorted((REPO / "lecciones").glob("**/*.md"))
    if not files:
        pytest.skip("no lesson files in lecciones/ yet")
    failures = {str(path): validate_file(path) for path in files}
    assert {path: errs for path, errs in failures.items() if errs} == {}
