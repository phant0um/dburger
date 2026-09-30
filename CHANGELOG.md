# Changelog

## [0.1.0] — 2026-09-29

### Added

- `src/rn01_bloco.sql`: bloco PL/SQL da RN01 (4 variáveis, desconto de 10% para
  quantidade > 3, saída via `DBMS_OUTPUT.PUT_LINE`).
- `src/rn01_bloco_tpl.sql`: template parametrizado; golden file impede drift.
- `testdata/casos.json`: 8 casos reais (demo, fronteira 3/4, teto dos tipos,
  preço zerado, nome de 40 bytes, 2 negativos plantados de `ORA-06502`).
- `docs/modelagem/dicionario-de-dados.md`: Tabela 1 do material — dicionário
  das 24 tabelas do projeto DBurger (colunas a chegar; DDL pendente delas).
- `tests/`: contrato estrutural offline + harness de integração em Oracle real.
- `Makefile` (`test`, `test-integration`, `vet`, `lint`, `build`, `doctor`),
  CI no dia 1, pre-commit com formatter e gitleaks.
- Constitution, spec, research, plan e tasks em `.specify/`.
