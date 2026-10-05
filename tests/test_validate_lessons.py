import importlib.util
import re
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
duracion_min: 18
estado: borrador
prerequisitos: []
fuentes:
  - https://developer.mozilla.org/es/docs/Learn/Getting_started_with_the_web/How_the_Web_works
  - https://www.cloudflare.com/learning/dns/what-is-dns/
glosario: [DNS, servidor]
---
"""

def glossary_entry(term, labels=("Qué es", "Ejemplo"), etymology="folded"):
    texts = {"Qué es": "una pieza del sistema.", "Ejemplo": "lo usas cada día."}
    lines = [f"### {term}"] + [f"**{label}:** {texts[label]}" for label in labels]
    if etymology == "folded":
        lines.append(
            "<details><summary>Por qué se llama así</summary>\n"
            "Viene de una palabra en inglés.\n</details>"
        )
    elif etymology == "open":
        lines.append("**Por qué se llama así:** viene de una palabra en inglés.")
    return "\n\n".join(lines)


GLOSSARY_SECTION = "\n\n".join([
    glossary_entry("DNS (Domain Name System)"),
    glossary_entry("Servidor (server)"),
])

TIMES = {
    "## 1. El gancho": "1 min",
    "## 2. La idea en una frase": "30 s",
    "## 3. Las palabras nuevas": "4 min",
    "## 4. La analogía": "2 min",
    "## 5. Diagrama": "2 min",
    "## 6. Contraste": "2 min",
    "## 7. ¿Cuál falla?": "3 min",
    "## 8. Ponte a prueba": "3 min",
    "## 9. Mini ejercicio": "5–10 min",
    "## 10. Cómo te ayuda a revisar a la IA": "2 min",
    "## 11. Cómo se conecta": "2 min",
    "## 12. Ya puedes": "10 s",
}

QUIZ = (
    "Explícalo con tus palabras (2 frases) antes de abrir la respuesta.\n\n"
    "1. ¿Qué hace el DNS?\n"
    "<details><summary>Respuesta</summary>Traduce nombres a IP.</details>\n\n"
    "2. ¿Quién dibuja la página?\n"
    "<details><summary>Respuesta</summary>El navegador.</details>\n\n"
    "3. ¿Qué protege HTTPS?\n"
    "<details><summary>Respuesta</summary>La conexión.</details>"
)

SOURCES = (
    "<details><summary>Fuentes</summary>\n\n"
    "- [MDN](https://developer.mozilla.org/)\n"
    "- [Cloudflare](https://www.cloudflare.com/learning/dns/what-is-dns/)\n\n"
    "</details>"
)

CONNECTIONS = (
    "**Viene de:** N1-M1-L01, que explica la URL.\n\n"
    "**Lleva a:** N1-M1-L03, que usa esta idea.\n\n"
    "**Si lo combinas con…:** N1-M1-L04 puedes publicar tu dominio.\n\n"
    "```mermaid\nflowchart LR\n  A[N1-M1-L01] --> B[N1-M1-L02]\n```"
)

# Section 11 is optional at level 1, so the base fixture leaves it out.
SECTIONS = {
    "## 1. El gancho": "Escribes una dirección. ¿Qué crees que pasa cuando pulsas Enter?",
    "## 2. La idea en una frase": "El navegador pide la página a un servidor y la dibuja.",
    "## 3. Las palabras nuevas": GLOSSARY_SECTION,
    "## 4. La analogía": "Es como pedir comida a domicilio con una dirección.",
    "## 5. Diagrama": "Mira primero el navegador.\n\n```mermaid\nflowchart LR\n  A[Navegador] --> B[DNS]\n```",
    "## 6. Contraste": (
        "| Sin DNS | Con DNS |\n"
        "| :-- | :-- |\n"
        "| Recuerdas números | Recuerdas nombres |"
    ),
    "## 7. ¿Cuál falla?": (
        "**A** `https://a.com` y **B** `https//a.com`. ¿Cuál falla y por qué?\n\n"
        "<details><summary>Respuesta</summary>B: le faltan los dos puntos.</details>"
    ),
    "## 8. Ponte a prueba": QUIZ,
    "## 9. Mini ejercicio": "Abre las herramientas de desarrollo y mira la pestaña Red.",
    "## 10. Cómo te ayuda a revisar a la IA": (
        "> Salida de IA: el DNS guarda las páginas.\n\nSabrás que se equivoca."
    ),
    "## 12. Ya puedes": "Explicar qué pasa al escribir una URL.",
    "## 13. Fuentes": SOURCES,
}

MALLA_IDS = ("N1-M1-L01", "N1-M1-L02", "N1-M1-L03", "N1-M1-L04", "N2-M1-L01")


@pytest.fixture(autouse=True)
def malla_file(tmp_path_factory, monkeypatch):
    """Point the validator at a small malla so tests don't depend on the real one."""
    path = tmp_path_factory.mktemp("curriculum") / "malla.md"
    path.write_text("\n".join(f"| {lesson_id} | Lección |" for lesson_id in MALLA_IDS), encoding="utf-8")
    monkeypatch.setattr(validate_lessons, "MALLA_PATH", path)
    return path


def full_heading(key):
    return f"{key} ⏱ {TIMES[key]}" if key in TIMES else key


def build_lesson(sections=None, frontmatter=FRONTMATTER):
    sections = SECTIONS if sections is None else sections
    body = "\n\n".join(f"{full_heading(key)}\n\n{content}" for key, content in sections.items())
    return f"{frontmatter}\n# Título\n\n{body}\n"


def with_connections(content=CONNECTIONS):
    """Base sections plus section 11, kept in template order."""
    items = list(SECTIONS.items())
    items.insert(10, ("## 11. Cómo se conecta", content))
    return dict(items)


LEVEL2_FRONTMATTER = FRONTMATTER.replace("id: N1-M1-L01", "id: N2-M1-L01").replace("nivel: 1", "nivel: 2")
LEVEL2_NAME = "N2-M1-L01-control-de-versiones.md"


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
        ("duracion_min: 18", "duracion_min: 14", "'duracion_min'"),
        ("duracion_min: 18", "duracion_min: 33", "'duracion_min'"),
        ("estado: borrador", "estado: publicada", "'estado' debe ser"),
        ("prerequisitos: []", "prerequisitos: [N1-M1-L01, tema-previo]", "prerrequisito no válido"),
        ("  - https://www.cloudflare.com/learning/dns/what-is-dns/\n", "", "al menos 2 elementos"),
        ("  - https://www.cloudflare.com", "  - www.cloudflare.com", "fuente no válida"),
        ('titulo: "¿Qué pasa cuando escribes una URL?"', 'titulo: ""', "'titulo' no puede estar vacío"),
        ("glosario: [DNS, servidor]\n", "", "falta el campo obligatorio 'glosario'"),
        ("glosario: [DNS, servidor]", "glosario: []", "entre 1 y 5 términos (tiene 0)"),
        ("glosario: [DNS, servidor]", "glosario: [a, b, c, d, e, f]", "entre 1 y 5 términos (tiene 6)"),
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
    sections = {k: v for k, v in SECTIONS.items() if k != "## 9. Mini ejercicio"}
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any("falta el encabezado '## 9. Mini ejercicio'" in error for error in errors), errors


def test_wrong_heading_order(tmp_path):
    items = list(SECTIONS.items())
    items[1], items[2] = items[2], items[1]
    errors = validate_file(write_lesson(tmp_path, build_lesson(dict(items))))
    assert any("orden" in error for error in errors), errors


def test_empty_section(tmp_path):
    sections = with_section("## 4. La analogía", "   ")
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any("'## 4. La analogía' está vacía" in error for error in errors), errors


@pytest.mark.parametrize(
    "heading, content, expected",
    [
        ("## 6. Contraste", "Sin DNS recuerdas números; con DNS, nombres.", "tabla markdown"),
        ("## 5. Diagrama", "```\nA --> B\n```", "```mermaid"),
        (
            "## 13. Fuentes",
            "<details><summary>Fuentes</summary>\n\n- [MDN](https://developer.mozilla.org/)\n\n</details>",
            "al menos 2 enlaces",
        ),
    ],
)
def test_section_content_rules(tmp_path, heading, content, expected):
    errors = validate_file(write_lesson(tmp_path, build_lesson(with_section(heading, content))))
    assert any(expected in error for error in errors), errors


def test_glossary_section_needs_an_entry(tmp_path):
    sections = with_section("## 3. Las palabras nuevas", "Aquí no hay entradas.")
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any("sección 3: necesita al menos una entrada" in error for error in errors), errors


@pytest.mark.parametrize("missing", ["Qué es", "Ejemplo"])
def test_glossary_entry_missing_label(tmp_path, missing):
    labels = [label for label in ("Qué es", "Ejemplo") if label != missing]
    content = "\n\n".join([glossary_entry("DNS", labels), glossary_entry("Servidor")])
    errors = validate_file(write_lesson(tmp_path, build_lesson(with_section("## 3. Las palabras nuevas", content))))
    assert errors == [f'sección 3: a "DNS" le falta "**{missing}:**"'], errors


def test_glossary_term_without_entry(tmp_path):
    content = glossary_entry("DNS (Domain Name System)")
    errors = validate_file(write_lesson(tmp_path, build_lesson(with_section("## 3. Las palabras nuevas", content))))
    assert errors == ['sección 3: el término del glosario "servidor" no tiene explicación'], errors


def test_glossary_match_ignores_case_and_accents(tmp_path):
    frontmatter = mutate(FRONTMATTER, "glosario: [DNS, servidor]", 'glosario: ["Dirección IP"]')
    content = glossary_entry("direccion ip (IP address)")
    sections = with_section("## 3. Las palabras nuevas", content)
    assert validate_file(write_lesson(tmp_path, build_lesson(sections, frontmatter))) == []


def test_glossary_heading_in_code_fence_is_not_an_entry(tmp_path):
    content = glossary_entry("DNS") + "\n\n```text\n### servidor\n```"
    errors = validate_file(write_lesson(tmp_path, build_lesson(with_section("## 3. Las palabras nuevas", content))))
    assert 'sección 3: el término del glosario "servidor" no tiene explicación' in errors, errors


def test_bare_urls_count_as_sources(tmp_path):
    content = "<details><summary>Fuentes</summary>\n\n- https://developer.mozilla.org/\n- https://www.cloudflare.com/\n\n</details>"
    sections = with_section("## 13. Fuentes", content)
    assert validate_file(write_lesson(tmp_path, build_lesson(sections))) == []


def _quiz(count, details=None):
    details = count if details is None else details
    lines = ["Explícalo con tus palabras (2 frases) antes de abrir la respuesta."]
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
    sections = with_section("## 8. Ponte a prueba", quiz)
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any(expected in error for error in errors), errors


def test_too_many_words(tmp_path):
    sections = with_section("## 1. El gancho", "palabra " * 2200)
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert any("palabras; el máximo es 2200" in error for error in errors), errors


def test_words_under_cap_are_ok(tmp_path):
    sections = with_section("## 1. El gancho", "palabra " * 1800)
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    assert not any("el máximo es" in error for error in errors), errors


@pytest.mark.parametrize("duration, ok", [(15, True), (32, True), (33, False)])
def test_duration_bounds(tmp_path, duration, ok):
    text = mutate(build_lesson(), "duracion_min: 18", f"duracion_min: {duration}")
    errors = validate_file(write_lesson(tmp_path, text))
    assert (errors == []) is ok, errors


def test_fenced_code_does_not_count_as_words(tmp_path):
    long_code = "```mermaid\nflowchart LR\n" + "  A --> B\n" * 600 + "```"
    sections = with_section("## 5. Diagrama", long_code)
    assert validate_file(write_lesson(tmp_path, build_lesson(sections))) == []


def test_collects_all_errors(tmp_path):
    text = mutate(build_lesson(), "estado: borrador", "estado: x")
    text = mutate(text, "duracion_min: 18", "duracion_min: 99")
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
    malla = REPO / "curriculum" / "malla.md"
    failures = {str(path): validate_file(path, malla_path=malla) for path in files}
    assert {path: errs for path, errs in failures.items() if errs} == {}


# --- T20 rules: new skeleton -------------------------------------------------


def errors_for(tmp_path, sections=None, frontmatter=FRONTMATTER, **kwargs):
    return validate_file(write_lesson(tmp_path, build_lesson(sections, frontmatter), **kwargs))


def test_hook_needs_a_prediction_question(tmp_path):
    errors = errors_for(tmp_path, with_section("## 1. El gancho", "Escribes una dirección y aparece una página."))
    assert errors == [
        "la sección '## 1. El gancho' debe terminar con una pregunta de predicción (falta '?')"
    ], errors


def test_heading_without_timer_is_rejected(tmp_path):
    text = mutate(build_lesson(), "## 4. La analogía ⏱ 2 min", "## 4. La analogía")
    errors = validate_file(write_lesson(tmp_path, text))
    assert errors == [
        "el encabezado '## 4. La analogía' necesita la marca de tiempo (ej. '⏱ 2 min')"
    ], errors


def test_timer_with_variation_selector_is_accepted(tmp_path):
    text = mutate(build_lesson(), "## 4. La analogía ⏱ 2 min", "## 4. La analogía \u23f1\ufe0f 2 min")
    assert validate_file(write_lesson(tmp_path, text)) == []


def test_sources_heading_needs_no_timer(tmp_path):
    text = build_lesson()
    assert "## 13. Fuentes\n" in text
    assert validate_file(write_lesson(tmp_path, text)) == []


def test_unexpected_heading_also_needs_timer(tmp_path):
    sections = with_section("## 12. Ya puedes", "Explicar una URL.\n\n## Extra\n\nTexto.")
    errors = errors_for(tmp_path, sections)
    assert "el encabezado '## Extra' necesita la marca de tiempo (ej. '⏱ 2 min')" in errors, errors


def test_timer_does_not_count_as_emoji(tmp_path, banned_file):
    content = "Lee esto ⏱ y esto ⏱ y esto ⏱ y esto ⏱️. ¿Qué crees que pasa?"
    assert style_errors(tmp_path, with_section("## 1. El gancho", content)) == []


def test_other_clock_emojis_still_count(tmp_path, banned_file):
    content = "Corre ⏰ ⏳ ⌛ ⏩ ya. ¿Qué crees que pasa?"
    errors = style_errors(tmp_path, with_section("## 1. El gancho", content))
    assert errors == ["estilo: 4 emojis; máx. 3"], errors


def test_glossary_etymology_must_be_folded(tmp_path):
    content = "\n\n".join([glossary_entry("DNS", etymology="open"), glossary_entry("Servidor")])
    errors = errors_for(tmp_path, with_section("## 3. Las palabras nuevas", content))
    assert errors == [
        'sección 3: a "DNS" le falta "Por qué se llama así" plegado en '
        "<details><summary>Por qué se llama así</summary>...</details>"
    ], errors


def test_glossary_etymology_missing(tmp_path):
    content = "\n\n".join([glossary_entry("DNS", etymology=None), glossary_entry("Servidor")])
    errors = errors_for(tmp_path, with_section("## 3. Las palabras nuevas", content))
    assert len(errors) == 1 and 'a "DNS" le falta "Por qué se llama así"' in errors[0], errors


def test_which_fails_answer_must_be_folded(tmp_path):
    content = "**A** `https://a.com` y **B** `https//a.com`. ¿Cuál falla y por qué? Falla B."
    errors = errors_for(tmp_path, with_section("## 7. ¿Cuál falla?", content))
    assert errors == ["la sección '## 7. ¿Cuál falla?' debe tener la respuesta dentro de <details>"], errors


def test_quiz_needs_explain_prompt(tmp_path):
    quiz = QUIZ.replace("Explícalo con tus palabras (2 frases) antes de abrir la respuesta.\n\n", "")
    errors = errors_for(tmp_path, with_section("## 8. Ponte a prueba", quiz))
    assert errors == ["la sección '## 8. Ponte a prueba' debe incluir \"Explícalo con tus palabras\""], errors


@pytest.mark.parametrize(
    "content, ok",
    [
        ("> Salida de IA: el DNS guarda páginas.\n\nEstá mal.", True),
        ("```python\nprint('hola')\n```\n\nEstá mal.", True),
        ("> El DNS guarda páginas.\n\nEstá mal.", False),
        ("La IA diría que el DNS guarda páginas.", False),
    ],
)
def test_review_ai_needs_ai_output_fragment(tmp_path, content, ok):
    errors = errors_for(tmp_path, with_section("## 10. Cómo te ayuda a revisar a la IA", content))
    assert (errors == []) is ok, errors
    if not ok:
        assert "fragmento de salida de IA" in errors[0]


def test_sources_must_be_folded(tmp_path):
    content = "- [MDN](https://developer.mozilla.org/)\n- [Cloudflare](https://www.cloudflare.com/)"
    errors = errors_for(tmp_path, with_section("## 13. Fuentes", content))
    assert errors == [
        "la sección '## 13. Fuentes' debe ir plegada en <details><summary>Fuentes</summary>...</details>"
    ], errors


# Section 11 "Cómo se conecta"


def test_connections_optional_at_level_1(tmp_path):
    assert "## 11. Cómo se conecta" not in build_lesson()
    assert errors_for(tmp_path) == []


def test_connections_valid_at_level_1(tmp_path):
    assert errors_for(tmp_path, with_connections()) == []


def test_connections_required_from_level_2(tmp_path):
    errors = errors_for(tmp_path, frontmatter=LEVEL2_FRONTMATTER, folder="N2", name=LEVEL2_NAME)
    assert errors == ["falta el encabezado '## 11. Cómo se conecta' (obligatorio desde el nivel 2)"], errors


def test_connections_present_at_level_2_is_valid(tmp_path):
    errors = errors_for(
        tmp_path, with_connections(), frontmatter=LEVEL2_FRONTMATTER, folder="N2", name=LEVEL2_NAME
    )
    assert errors == [], errors


@pytest.mark.parametrize("label", ["Viene de:", "Lleva a:", "Si lo combinas con"])
def test_connections_needs_each_label(tmp_path, label):
    content = CONNECTIONS.replace(label, "Otra cosa:")
    errors = errors_for(tmp_path, with_connections(content))
    assert errors == [f"la sección '## 11. Cómo se conecta' debe incluir la etiqueta \"{label}\""], errors


def test_connections_needs_mermaid_map(tmp_path):
    content = CONNECTIONS.split("```mermaid")[0]
    errors = errors_for(tmp_path, with_connections(content))
    assert errors == ["la sección '## 11. Cómo se conecta' debe contener un mini mapa ```mermaid"], errors


def test_connections_rejects_ids_missing_from_malla(tmp_path):
    content = CONNECTIONS.replace("N1-M1-L03", "N1-M9-L42")
    errors = errors_for(tmp_path, with_connections(content))
    assert errors == ["la sección '## 11. Cómo se conecta' cita N1-M9-L42, que no existe en la malla"], errors


def test_malla_path_argument_overrides_default(tmp_path):
    other = tmp_path / "otra-malla.md"
    other.write_text("| N1-M1-L01 |\n| N1-M1-L02 |", encoding="utf-8")
    path = write_lesson(tmp_path, build_lesson(with_connections()))
    errors = validate_file(path, malla_path=other)
    assert sorted(errors) == [
        "la sección '## 11. Cómo se conecta' cita N1-M1-L03, que no existe en la malla",
        "la sección '## 11. Cómo se conecta' cita N1-M1-L04, que no existe en la malla",
    ], errors


def test_unreadable_malla_is_reported_when_ids_are_cited(tmp_path):
    path = write_lesson(tmp_path, build_lesson(with_connections()))
    errors = validate_file(path, malla_path=tmp_path / "no-existe.md")
    assert errors == [
        "no se pudo leer la malla para comprobar los IDs citados en '## 11. Cómo se conecta'"
    ], errors


def test_load_lesson_ids_reads_real_malla():
    ids = validate_lessons.load_lesson_ids(REPO / "curriculum" / "malla.md")
    assert ids and "N1-M1-L01" in ids


def test_template_skeleton_passes_validator(tmp_path):
    """docs/plantilla-leccion.md must stay a valid lesson (against the real malla)."""
    template = (REPO / "docs" / "plantilla-leccion.md").read_text(encoding="utf-8")
    match = re.search(r"````markdown\n(.*?)\n````", template, re.DOTALL)
    assert match, "the template has no ````markdown skeleton block"
    path = write_lesson(tmp_path, match.group(1) + "\n", name="N1-M1-L01-plantilla.md")
    assert validate_file(path, malla_path=REPO / "curriculum" / "malla.md") == []


# --- Style checks -----------------------------------------------------------

BANNED = ["en el mundo actual", "sin lugar a dudas"]


@pytest.fixture
def banned_file(tmp_path, monkeypatch):
    path = tmp_path / "frases.txt"
    path.write_text("# comentario\n\n" + "\n".join(BANNED) + "\n", encoding="utf-8")
    monkeypatch.setattr(validate_lessons, "BANNED_PHRASES_PATH", path)
    return path


def style_errors(tmp_path, sections):
    errors = validate_file(write_lesson(tmp_path, build_lesson(sections)))
    return [error for error in errors if error.startswith("estilo: ")]


def line_of(text, needle):
    return next(i for i, line in enumerate(text.splitlines(), 1) if needle in line)


def test_valid_lesson_has_no_style_errors(tmp_path, banned_file):
    assert style_errors(tmp_path, SECTIONS) == []


def test_banned_phrase_case_insensitive_with_line(tmp_path, banned_file):
    content = "Hoy, EN EL   MUNDO Actual, todo usa la web. Y en el mundo actual también."
    sections = with_section("## 1. El gancho", content)
    text = build_lesson(sections)
    errors = style_errors(tmp_path, sections)
    expected = f'estilo: frase prohibida "en el mundo actual" (línea {line_of(text, "EN EL")})'
    assert errors == [expected]


def test_banned_phrase_across_line_break(tmp_path, banned_file):
    sections = with_section("## 1. El gancho", "Es así sin lugar\na dudas.")
    errors = style_errors(tmp_path, sections)
    assert any('"sin lugar a dudas"' in error for error in errors), errors


def test_banned_phrase_in_code_fence_is_ignored(tmp_path, banned_file):
    content = "Mira el ejemplo.\n\n```text\nsin lugar a dudas\n```"
    assert style_errors(tmp_path, with_section("## 9. Mini ejercicio", content)) == []


def test_missing_banned_file_does_not_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(validate_lessons, "BANNED_PHRASES_PATH", tmp_path / "no-existe.txt")
    assert validate_lessons.load_banned_phrases() == []
    assert validate_file(write_lesson(tmp_path, build_lesson())) == []


def test_long_paragraph(tmp_path, banned_file):
    content = "Una frase corta aquí. " * 21  # 84 words, short sentences
    errors = style_errors(tmp_path, with_section("## 4. La analogía", content))
    assert any(e.startswith("estilo: párrafo de 84 palabras (máx. 80)") for e in errors), errors
    assert not any("frase de" in e for e in errors), errors


def test_long_sentence(tmp_path, banned_file):
    content = "Corto. " + "palabra " * 41 + "final."
    sections = with_section("## 4. La analogía", content)
    errors = style_errors(tmp_path, sections)
    line = line_of(build_lesson(sections), "Corto.")
    assert errors == [f"estilo: frase de 42 palabras (máx. 40) en línea {line}"]


def test_long_sentence_in_list_item(tmp_path, banned_file):
    content = "- Uno corto.\n- " + "palabra " * 45 + "fin."
    errors = style_errors(tmp_path, with_section("## 4. La analogía", content))
    assert any("frase de 46 palabras" in e for e in errors), errors
    assert not any("párrafo" in e for e in errors), errors


def test_urls_and_inline_code_do_not_count_as_words(tmp_path, banned_file):
    content = "Mira " + "`a b c d e` " * 20 + "y https://example.com/x " * 15 + "fin."
    assert style_errors(tmp_path, with_section("## 9. Mini ejercicio", content)) == []


def test_too_many_em_dashes(tmp_path, banned_file):
    content = "Uno — dos — tres — cuatro — cinco."
    errors = style_errors(tmp_path, with_section("## 1. El gancho", content))
    assert errors == ["estilo: 4 rayas (—); máx. 3. Usa punto o coma."]


def test_em_dashes_in_sources_are_ignored(tmp_path, banned_file):
    content = (
        "<details><summary>Fuentes</summary>\n\n"
        "- [MDN — Web](https://developer.mozilla.org/) — guía — base\n"
        "- [Cloudflare — DNS](https://www.cloudflare.com/) — intro\n\n"
        "</details>"
    )
    assert style_errors(tmp_path, with_section("## 13. Fuentes", content)) == []


def test_too_many_exclamations(tmp_path, banned_file):
    content = "¡Hola! Escribes una dirección. ¡Y aparece!"
    errors = style_errors(tmp_path, with_section("## 1. El gancho", content))
    assert errors == ["estilo: 2 exclamaciones; máx. 1"]


def test_too_many_emojis(tmp_path, banned_file):
    content = "Escribes una dirección 🚀 🔥 ✨ 🎉 y aparece."
    errors = style_errors(tmp_path, with_section("## 1. El gancho", content))
    assert errors == ["estilo: 4 emojis; máx. 3"]


def test_emojis_in_table_are_ignored(tmp_path, banned_file):
    content = (
        "| Sin DNS | Con DNS |\n"
        "| :-- | :-- |\n"
        "| ❌ ❌ | ✅ ✅ |\n"
        "| ⚠️ ⚠️ | ✅ ✅ |"
    )
    assert style_errors(tmp_path, with_section("## 6. Contraste", content)) == []
