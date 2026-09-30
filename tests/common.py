"""Utilitários compartilhados da suíte DBurger (apenas stdlib)."""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "rn01_bloco_tpl.sql"
BLOCK = ROOT / "src" / "rn01_bloco.sql"
CASES = ROOT / "testdata" / "casos.json"

PLACEHOLDERS = ("{{CLIENTE}}", "{{QTD}}", "{{PRECO}}")


class CaseError(ValueError):
    """Caso de teste malformado."""


def load_cases() -> dict:
    with CASES.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict) or not isinstance(data.get("casos"), list):
        raise CaseError(f"{CASES}: esperado objeto com lista 'casos'")
    return data


def render(template_text: str, case: dict) -> str:
    """Renderiza o template do bloco com os valores do caso.

    Interpolação é estritamente textual e só em placeholders fixos;
    nenhum valor é passado a shell.
    """
    for key in ("id", "cliente", "qtd", "preco"):
        if key not in case:
            raise CaseError(f"caso sem campo obrigatório '{key}': {case.get('id', '?')}")
    text = template_text
    text = text.replace("{{CLIENTE}}", str(case["cliente"]))
    text = text.replace("{{QTD}}", str(case["qtd"]))
    text = text.replace("{{PRECO}}", str(case["preco"]))
    return text


def demo_case() -> dict:
    for case in load_cases()["casos"]:
        if case["id"] == "demo":
            return case
    raise CaseError("caso 'demo' ausente em testdata/casos.json")
