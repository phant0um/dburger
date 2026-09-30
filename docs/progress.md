# Progress — DBurger

Atualizar no fim de toda sessão (File-as-Bus). A próxima sessão começa lendo este arquivo.

## 2026-09-29 — sessão 1 (F0 → F11, criação do projeto)

- **Fase / checkpoint:** F0–F11 fechados nesta sessão; F12/F13 em aberto.
- **Feito:** scaffold completo via workflow `projeto-novo` — constitution (F1),
  spec/research/plan/tasks/data-model (F2), fixtures reais (F3), esqueleto com
  Makefile/CI/pre-commit (F5), bloco RN01 + template + golden file (F6),
  harness de integração Oracle + doctor (F7), rodada real 8 casos + negativos
  plantados (F8), docs F10, verify-report F11. Commits por task ID (T001–T061).
- **Evidência:** `make test` 4/4 offline · `make lint` gitleaks ok + texto ok ·
  `check-project-scaffold.py` exit 0 · `make test-integration` — ver
  `docs/verify-report.md` para os números exatos da rodada real · gitleaks
  reprova segredo plantado (exit 1) e aprova repo limpo (exit 0).
- **Decisão de F0:** grill-me dispensado — a RN01 veio completa do usuário
  (enunciado fechado, 4 variáveis, regra e saída definidas). Registrado aqui em
  vez de inventar perguntas que o enunciado já responde.
- **Bloqueio:** push/CI remoto e release exigem aprovação humana (Contrato #2);
  CI está escrito (`.github/workflows/ci.yml`) mas nunca foi verde "num commit
  vazio" em remoto — alegação fica local até o push.
- **Próximo passo:** T062 (F12 pós-release: lições) e aprovação para push.
- **Lição:** negativo plantado de segurança precisa de segredo que o detector NÃO
  allowlista: a chave de exemplo documentada da AWS (`...EXAMPLE`) passa
  silenciosa no gitleaks e o gate falso-verde só cai com chave em formato real.
  Regra: todo gate de segredo prova reprovação com padrão vivo, e o exit code é
  medido direto do detector (nunca de um `| tail`). (vira gate em
  `scripts/lint.sh` já coberto pelo teste manual registrado no verify-report.)

## 2026-09-29 — sessão 1b (correção do usuário + rodada real)

- **Fase / checkpoint:** F8 refetado (bug real encontrado e corrigido), F11 fechado.
- **Feito:** (1) correção do usuário: o projeto inclui o dicionário de dados de
  24 tabelas (Tabela 1) → registrado em `docs/modelagem/dicionario-de-dados.md`,
  DDL adiado até a especificação de colunas (não inventar); (2) rodada real
  reprovou 3/8 casos — `FM99999D00` apagava o zero inteiro (`R$ ,00`) — corrigido
  para `FM999990D00`; (3) harness ganhou fallback de prontidão por log e teto de
  600 s (o `healthcheck.sh` não respondeu em 300 s na primeira subida).
- **Evidência:** `make test-integration` → 8 testes, 0 falhas (Oracle real);
  `docs/verify-report.md` com o veredito por AC; `check-project-scaffold.py` exit 0.
- **Bloqueio:** colunas/PKs/FKs das 24 tabelas não fornecidas — DDL bloqueado
  até o material chegar. Push/release continuam exigindo aprovação humana.
- **Próximo passo:** aguardar a especificação de colunas (próximas tabelas do
  material) para F2 da modelagem; aprovação de push.
- **Lição:** formato numérico `FM` com modelo `9` suprime o dígito zero inteiro;
  a execução real é o único oráculo disso — 3 casos "óbvios" passariam em
  qualquer revisão por leitura. Regra: saída formatada sempre com placeholder
  `0` na parte inteira (`FM999990D00`) e teste de caso zero obrigatório.
