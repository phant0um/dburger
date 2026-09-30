# DBurger — PL/SQL exercises

Didactic PL/SQL project for the Divine Burger (DBurger) case study: a burger chain
whose data lives in Oracle. Each business rule (RNxx) ships as one self-contained
anonymous block, verified by a real Oracle test suite.

This repository currently implements **RN01 — order discount**: if the burger
quantity is greater than 3, a 10% discount is applied to the total price; the
block prints the client name, quantity, final price and discount via
`DBMS_OUTPUT.PUT_LINE`.

## Requirements

- Oracle 18c+ with SQL\*Plus (to run the block), **or** just read `src/rn01_bloco.sql`.
- Docker (Colima/OrbStack/Docker Desktop) for the integration test suite.
- Python 3.9+ (stdlib only) for the test harness.

## Usage

Run the block on any Oracle schema:

```sh
sqlplus user/password@service @src/rn01_bloco.sql
```

## Development

```sh
make test              # structural contract, offline (does NOT prove behavior)
make test-integration  # behavior, real Oracle (starts gvenzl/oracle-free container)
make vet               # quick subset: declarations + golden file
make lint              # gitleaks + text hygiene
make build             # dist/dburger-rn01.sql
make doctor            # environment status by layer
```

Structural tests prove the file contract (four variables with exact types, golden
file against the template, fixture schema). Behavior is only proven by
`make test-integration`, which executes the block inside a disposable Oracle
container and compares the output line by line. There is no fake-green path: no
Oracle, no behavior claim.

## Layout

- `src/rn01_bloco.sql` — the deliverable block (exactly the template rendered with the demo case).
- `src/rn01_bloco_tpl.sql` — parameterized template used by the test harness.
- `testdata/casos.json` — real fixtures: demo, boundary (3/4), type ceilings, planted negatives.
- `tests/` — offline contract suite + Oracle integration harness.
- `.specify/` — constitution, spec, research, plan, tasks (workflow `projeto-novo`).
- `docs/modelagem/dicionario-de-dados.md` — Tabela 1 do material: as 24 tabelas do projeto DBurger (DDL pendente da especificação de colunas).
- `docs/verify-report.md` — per-AC verdict with evidence; `docs/progress.md` — cycle log.

## License

MIT — see [LICENSE](LICENSE).
