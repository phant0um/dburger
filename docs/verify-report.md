# Verify report — 001 rn01-desconto

> 2026-09-29 · DBurger 0.1.0 · Público: mantenedor

## Resultado

**PASS.** 5 critérios PASS, 0 PARTIAL, 0 FAIL.

Evidência base:
- `make test`: 4 testes, 0 falhas, offline (estrutura — não prova comportamento).
- `make test-integration`: 8 testes, 0 falhas, Oracle real (`gvenzl/oracle-free:slim`, PDB `FREEPDB1`, contêiner `dburger-oracle`), ~1 min de rodada com o banco de pé.
- `gitleaks dir`: sem vazamentos; negativo plantado (chave AWS em formato vivo) reprovado com exit `1`; repo limpo exit `0`.
- `check-project-scaffold.py`: exit 0 (constitution, spec com 5 ACs, tasks, CI, test runner, verify-report).
- Execuções reais: `Ana Souza, 5, 120.00` → `Cliente: Ana Souza / Quantidade de hambúrgueres: 5 / Preço total a pagar: R$ 108,00 / Desconto aplicado: R$ 12,00` (saída real do Oracle, comparada linha a linha).

## Critérios

| AC | Resultado | Evidência |
|---|---|---|
| 1.1 | PASS | `make test` → `declaracoes`: 4 variáveis com `VARCHAR2(40 BYTE)`, `NUMBER(3,0)`, `NUMBER(7,2)`, `NUMBER(7,2)` |
| 1.2 | PASS | Oracle real: `demo` (5 un. → 108,00/12,00), `fronteira-4` (4 un. → 81,00/9,00), `teto-tipos` (999 un. → 89999,99/10000,00) |
| 1.3 | PASS | Oracle real: `fronteira-3` (3 un. → 90,00/0,00), `zerado` (1 un. → 0,00/0,00) |
| 1.4 | PASS | Comparação exata das 4 linhas de `DBMS_OUTPUT.PUT_LINE` em 6 casos com saída; 2 casos de erro verificam a `ORA-` |
| 1.5 | PASS | `teto-tipos` e `nome-40-bytes` executam sem estouro; `nome-41-bytes-erro` e `qtd-1000-erro` reprovam com `ORA-06502` (negativos plantados) |

## Drift da spec

- Primeira rodada real reprovou 3/8 casos: `TO_CHAR(..., 'FM99999D00')` apagava o dígito zero inteiro (`R$ ,00`). Corrigido para `FM999990D00` (ASSUMPTION 4 confirmada com ajuste documentado em `research.md`).
- Escopo do projeto ampliado pelo usuário (2026-09-29): dicionário de dados de 24 tabelas (Tabela 1) registrado em `docs/modelagem/dicionario-de-dados.md`. DDL fica pendente da especificação de colunas — não inventada.

## Observações para a próxima versão

- O `healthcheck.sh` do `gvenzl/oracle-free:slim` não respondeu pronto em 300 s na primeira subida (create DB); o harness ganhou fallback por log ("DATABASE IS READY TO USE") e teto de 600 s.
- Gitleaks allowlista chaves de exemplo documentadas (ex.: AWS `...EXAMPLE`): o gate de segredo precisa de padrão vivo — e o exit code deve ser lido direto do detector, sem pipe no meio.
- CI remoto nunca executou (push requer aprovação): a alegação "CI verde" fica restrita ao que roda local (`make test`/`make lint`).
