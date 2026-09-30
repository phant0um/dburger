#!/usr/bin/env python3
"""Contrato estrutural da RN01 — roda OFFLINE, sem Oracle.

Este script prova ESTRUTURA (golden file, tipos declarados, schema dos casos).
Ele NUNCA prova comportamento: a regra de desconto só é provada pela suíte de
integração (`make test-integration`), contra Oracle real.
"""

from __future__ import annotations

import re
import sys

from common import BLOCK, TEMPLATE, CaseError, demo_case, load_cases, render

VAR_RE = re.compile(
    r"^\s*(v_cliente|v_qtd_hamburgueres|v_preco_total|v_desconto)\s+"
    r"(VARCHAR2\(\s*\d+\s*BYTE\s*\)|NUMBER\(\s*\d+\s*,\s*\d+\s*\))",
    re.MULTILINE,
)
EXPECTED_TYPES = {
    "v_cliente": "VARCHAR2(40 BYTE)",
    "v_qtd_hamburgueres": "NUMBER(3, 0)",
    "v_preco_total": "NUMBER(7, 2)",
    "v_desconto": "NUMBER(7, 2)",
}


def test_golden_file() -> str | None:
    """src/rn01_bloco.sql é exatamente o template renderizado com o caso demo."""
    tpl = TEMPLATE.read_text(encoding="utf-8")
    expected = render(tpl, demo_case())
    actual = BLOCK.read_text(encoding="utf-8")
    if actual != expected:
        return (
            "src/rn01_bloco.sql difere do template renderizado com o caso demo "
            "(drift entre o que se testa e o que se entrega)"
        )
    return None


def test_declaracoes() -> str | None:
    """O bloco declara exatamente as 4 variáveis da RN01, com os tipos exigidos."""
    tpl = TEMPLATE.read_text(encoding="utf-8")
    decls = {m.group(1): m.group(2) for m in VAR_RE.finditer(tpl)}
    if set(decls) != set(EXPECTED_TYPES):
        return f"variáveis declaradas: {sorted(decls)}; esperado: {sorted(EXPECTED_TYPES)}"
    for name, want in EXPECTED_TYPES.items():
        got = re.sub(r"\s+", "", decls[name])
        if got != re.sub(r"\s+", "", want):
            return f"{name}: tipo '{decls[name]}' != '{want}'"
    n_decl = len(re.findall(r"^\s*v_\w+\s+(VARCHAR2|NUMBER)", tpl, re.MULTILINE))
    if n_decl != 4:
        return f"{n_decl} declarações no bloco; a RN01 pede exatamente 4"
    return None


def test_casos() -> str | None:
    """testdata/casos.json é válido e cobre as fronteiras exigidas pela spec."""
    data = load_cases()
    ids = []
    for case in data["casos"]:
        cid = case.get("id", "?")
        ids.append(cid)
        erro = case.get("esperar_erro")
        if erro:
            if not isinstance(erro, str) or not erro.startswith("ORA-"):
                return f"caso {cid}: 'esperar_erro' deve ser código ORA-"
            continue
        if not isinstance(case.get("esperado"), list) or len(case["esperado"]) != 4:
            return f"caso {cid}: 'esperado' deve ter 4 linhas (RN01 imprime 4)"
        if not isinstance(case.get("qtd"), int):
            return f"caso {cid}: 'qtd' deve ser inteiro"
        if len(str(case.get("cliente", "")).encode("utf-8")) > 40:
            return f"caso {cid}: cliente com mais de 40 bytes (só casos de erro podem estourar)"
    for obrig in ("demo", "fronteira-3", "fronteira-4", "teto-tipos", "nome-41-bytes-erro"):
        if obrig not in ids:
            return f"caso obrigatório ausente: {obrig}"
    if len(ids) != len(set(ids)):
        return "ids de caso duplicados"
    return None


def test_spec_acs() -> str | None:
    """spec.md traz critérios de aceitação numerados (ACn.m) verificáveis."""
    spec = (BLOCK.parent.parent / ".specify" / "specs" / "001-rn01-desconto" / "spec.md")
    text = spec.read_text(encoding="utf-8")
    acs = re.findall(r"AC(\d+)\.(\d+)", text)
    if len(acs) < 5:
        return f"spec.md com apenas {len(acs)} referências AC; esperado >= 5"
    return None


TESTS = {
    "golden_file (estrutura)": test_golden_file,
    "declaracoes (estrutura)": test_declaracoes,
    "casos (schema)": test_casos,
    "spec_acs": test_spec_acs,
}


def main(argv: list[str]) -> int:
    vet_only = "--vet" in argv
    tests = {
        k: v
        for k, v in TESTS.items()
        if not vet_only or k.startswith(("golden", "declaracoes"))
    }
    failures = 0
    for name, fn in tests.items():
        try:
            err = fn()
        except (CaseError, OSError) as exc:  # falha de setup é falha de teste
            err = str(exc)
        if err:
            failures += 1
            print(f"FAIL {name}: {err}")
        else:
            print(f"PASS {name}")
    print(f"\n{len(tests)} testes, {failures} falhas (offline — estrutura; "
          f"comportamento só em 'make test-integration')")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
