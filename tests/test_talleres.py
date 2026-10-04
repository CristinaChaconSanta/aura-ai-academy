"""Run every taller's tests against its reference solution."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
TALLERES = REPO / "talleres"
NODE = shutil.which("node")

if NODE is None:
    pytest.skip("node is not on PATH", allow_module_level=True)

REQUIRED_FILES = [
    "README.md",
    "solucion.js",
    "index.html",
    "pruebas.js",
    ".referencia/solucion.js",
]


def _taller_dirs():
    return sorted(
        p.parent
        for p in TALLERES.glob("*/pruebas.js")
        if not p.parent.name.startswith("_")
    )


TALLER_DIRS = _taller_dirs()
IDS = [d.name for d in TALLER_DIRS]


def test_at_least_one_taller_exists():
    assert TALLER_DIRS, "no talleres/*/pruebas.js found"


@pytest.mark.parametrize("taller", TALLER_DIRS, ids=IDS)
def test_taller_has_required_files(taller):
    missing = [f for f in REQUIRED_FILES if not (taller / f).is_file()]
    assert not missing, f"{taller.name} is missing: {missing}"


@pytest.mark.parametrize("taller", TALLER_DIRS, ids=IDS)
def test_reference_solution_passes(taller):
    env = dict(os.environ, TALLER_SOLUCION=str(taller / ".referencia" / "solucion.js"))
    result = subprocess.run(
        [NODE, str(taller / "pruebas.js")],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
