#!/usr/bin/env python3
"""Suíte de integração RN01 contra Oracle real (marcador: integration).

Renderiza cada caso de testdata/casos.json, executa o bloco via sqlplus dentro
do contêiner Oracle Free e compara a saída linha a linha. Sem Oracle não há
suíte: o script falha com exit 3 e diz o próximo passo, nunca finge sucesso.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from typing import NoReturn

from common import TEMPLATE, CaseError, load_cases, render

CONTAINER = os.environ.get("DBURGER_ORACLE_CONTAINER", "dburger-oracle")
IMAGE = os.environ.get("DBURGER_ORACLE_IMAGE", "gvenzl/oracle-free:slim")
SYS_PWD = os.environ.get("DBURGER_SYS_PASSWORD", "dburger_dev_only")
APP_USER = "dburger"
APP_PWD = "dburger_dev_only"
CONNECT = f"{APP_USER}/{APP_PWD}@//localhost:1521/FREEPDB1"
SYS_CONNECT = f"system/{SYS_PWD}@//localhost:1521/FREEPDB1"
NLS_ENV = ["-e", "NLS_LANG=AMERICAN_AMERICA.AL32UTF8"]
READY_TIMEOUT_S = 600
CASE_TIMEOUT_S = 90


def sh(args: list[str], input_text: str | None = None, timeout: int = 120):
    return subprocess.run(
        args,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def die(code: int, msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(code)


def ensure_container() -> None:
    if not sh(["which", "docker"]).returncode == 0:
        die(3, "Docker ausente. Instale o Docker e rode `make doctor`.")
    inspect = sh(["docker", "inspect", "-f", "{{.State.Status}}", CONTAINER])
    if inspect.returncode != 0:
        print(f"subindo {IMAGE} como {CONTAINER} (primeira vez demora)...", file=sys.stderr)
        run = sh([
            "docker", "run", "-d", "--name", CONTAINER,
            "-e", f"ORACLE_PASSWORD={SYS_PWD}",
            "-p", "1521:1521",
            IMAGE,
        ])
        if run.returncode != 0:
            die(1, f"falha ao criar contêiner: {run.stderr.strip()}\n"
                   "Próximo passo: confira `docker images` e rode `make doctor`.")
    elif inspect.stdout.strip() != "running":
        if sh(["docker", "start", CONTAINER]).returncode != 0:
            die(1, f"contêiner {CONTAINER} existe mas não sobe. Próximo passo: `make doctor`.")


def is_ready() -> bool:
    probe = sh(["docker", "exec", CONTAINER, "/home/oracle/healthcheck.sh"], timeout=30)
    if probe.returncode == 0:
        return True
    # Fallback: o create DB do gvenzl escreve esta linha quando o PDB abre.
    logs = sh(["docker", "logs", CONTAINER], timeout=30)
    return "DATABASE IS READY TO USE" in (logs.stdout + logs.stderr)


def wait_ready() -> None:
    deadline = time.time() + READY_TIMEOUT_S
    while time.time() < deadline:
        if is_ready():
            return
        time.sleep(5)
    die(1, f"Oracle não ficou pronto em {READY_TIMEOUT_S}s. Próximo passo: `make doctor`.")


def ensure_user() -> None:
    setup = (
        "WHENEVER SQLERROR CONTINUE\n"
        f"CREATE USER {APP_USER} IDENTIFIED BY {APP_PWD} QUOTA UNLIMITED ON USERS;\n"
        f"GRANT CREATE SESSION TO {APP_USER};\n"
        "EXIT\n"
    )
    sh(["docker", "exec", "-i", *NLS_ENV, CONTAINER, "sqlplus", "-s", SYS_CONNECT],
       input_text=setup, timeout=60)


def run_block(block_text: str) -> tuple[int, str]:
    proc = sh(
        ["docker", "exec", "-i", *NLS_ENV, CONTAINER, "sqlplus", "-s", CONNECT],
        input_text=block_text,
        timeout=CASE_TIMEOUT_S,
    )
    return proc.returncode, proc.stdout


def output_lines(raw: str) -> list[str]:
    noise = ("PL/SQL procedure successfully completed.", "Connected.", "Elapsed:")
    return [ln.strip() for ln in raw.replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.strip().startswith(noise)]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Testes de integração RN01 (Oracle real).")
    ap.add_argument("--only", help="roda apenas o caso com este id")
    args = ap.parse_args(argv)

    try:
        data = load_cases()
    except (CaseError, OSError) as exc:
        die(2, f"casos inválidos: {exc}")

    ensure_container()
    wait_ready()
    ensure_user()

    tpl = TEMPLATE.read_text(encoding="utf-8")
    cases = [c for c in data["casos"] if not args.only or c["id"] == args.only]
    if not cases:
        die(2, f"nenhum caso com id '{args.only}'")

    failures = 0
    for case in cases:
        cid = case["id"]
        code, raw = run_block(render(tpl, case))
        got = output_lines(raw)
        if "esperar_erro" in case:
            want = case["esperar_erro"]
            ok = any(want in ln for ln in raw.split("\n"))
            detail = "" if ok else f"esperava {want}; saída: {got or raw.strip()[:200]!r}"
        else:
            ok = got == case["esperado"]
            detail = "" if ok else f"esperado {case['esperado']}; obtido {got}"
        if ok:
            print(f"PASS {cid}")
        else:
            failures += 1
            print(f"FAIL {cid}: {detail}")
        if code not in (0,) and "esperar_erro" not in case:
            failures += 1
            print(f"FAIL {cid}: sqlplus exit {code} (esperado 0)")

    print(f"\n{len(cases)} testes, {failures} falhas (integration — Oracle real, "
          f"contêiner {CONTAINER})")
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except subprocess.TimeoutExpired as exc:
        die(1, f"timeout em {exc.cmd}: aumente CASE_TIMEOUT_S ou rode `make doctor`.")
