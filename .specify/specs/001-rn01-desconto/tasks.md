# Tasks — 001 rn01-desconto

Legenda: `[P]` = paralelizável com as outras `[P]` do mesmo bloco. `→` = depende de. Teste sempre antes da implementação. Um commit por task, com o ID na mensagem.

## Fase 0 — Spike (valida ASSUMPTIONS)

- [x] T001 Spike de tipos e overflow em Oracle real: confirmar `NUMBER(7,2)`, `VARCHAR2(40 BYTE)` e o `ORA-06502` dos limites (precisa do contêiner Oracle — dependência local via Docker, sem instalação de sistema).
- [x] T002 → T001. Fixtures reais em `testdata/casos.json` (caso-demo, fronteira qtd=3/4, teto de tipos, negativos plantados).
- [x] T003 → T002. Registrar resultado das ASSUMPTIONS na spec. Se alguma falhar, parar e voltar para Clarify.

Checkpoint: fixtures reais em `testdata/`, ASSUMPTIONS validadas.

## Fase 1 — Esqueleto

- [x] T010 → T003. Repo, identidade git, `src/rn01_bloco.sql` (saída determinística), contrato estrutural com teste.
- [x] T011 → T010. `Makefile` com `test`, `vet`, `lint`, `build`; CI no dia 1; pre-commit com formatter e gitleaks.

Checkpoint: CI verde num commit vazio (pendente de push — requer aprovação); gitleaks reprova segredo plantado.

## Fase 2 — Núcleo puro

- [x] T020 [P] → T010. Testes do contrato das 4 variáveis (tipos exatos) e do golden file. `tests/test_offline.py`.
- [x] T021 → T020. Implementar o bloco e o template. `src/rn01_bloco_tpl.sql`, `src/rn01_bloco.sql`.

Checkpoint: suíte offline verde, sem rede e sem binário externo.

## Fase 3 — Orquestração + adapters reais

- [x] T040 → T021. Harness de integração: renderiza caso → `sqlplus` via stdin → compara saída. `tests/run_tests.py`.
- [x] T041 → T040. Adapter Oracle: contêiner `gvenzl/oracle-free:slim`, usuário de teste, espera de healthcheck. `scripts/doctor.sh`.

Checkpoint: todos os AC verdes com execução real (ver `docs/verify-report.md`).

## Fase 4 — Verificação

- [x] T050 → T041. Rodada real ponta a ponta (8 casos) e negativo plantado reprovado.
- [x] T051 → T050. Auditoria de segurança (sem segredo em repo/log) e revisão 2 eixos (spec × código); corrigir bloqueantes.
- [x] T052 → T051. `docs/verify-report.md` por AC; scaffold checker verde.

## Fase 5 — Docs e pós-release

- [x] T060 → T052. README (EN + pt-BR), CHANGELOG, LICENSE; comandos do README rodando como escritos.
- [x] T061 → T060. `docs/progress.md` do ciclo + lição.
