---
id: 001
feature: rn01-desconto
status: verify   # draft → clarify → plan → tasks → implement → verify
created: 2026-09-29
---

# Spec 001 — RN01: bloco de pedido com desconto

## Por quê

Exercício inicial de PL/SQL do estudo de caso DBurger (hamburgueria com 30+ anos de operação, dados em Oracle): resolver a regra de negócio RN01 com um bloco anônimo, primeira pedra da jornada didática. Quem sente: aluno que precisa entregar o bloco correto e o instrutor que precisa conferi-lo mecanicamente.

## O quê

Entrada (nome do cliente, quantidade de hambúrgueres, preço total) → saída impressa via `DBMS_OUTPUT.PUT_LINE` com nome, quantidade, preço total já com desconto e valor do desconto; desconto de 10% quando a quantidade for maior que 3.

## User stories

### US1 — Bloco RN01

Como aluno, quero um bloco PL/SQL que declare as quatro variáveis da RN01 e aplique o desconto, para entregar o exercício correto.

Critérios de aceitação (cada um verificável por comando):
- AC1.1 O bloco declara exatamente 4 variáveis, com os tipos da RN01: `VARCHAR2(40 BYTE)`, `NUMBER(3,0)`, `NUMBER(7,2)`, `NUMBER(7,2)` — verificado por teste estrutural offline (`make test`).
- AC1.2 Com quantidade > 3, o desconto é 10% do preço total e o preço exibido é o total já líquido do desconto — verificado por execução real em Oracle (`make test-integration`).
- AC1.3 Com quantidade ≤ 3 (inclusive 3), o desconto é 0 e o preço exibido é o preço original — verificado por execução real em Oracle.
- AC1.4 A saída usa `DBMS_OUTPUT.PUT_LINE` e traz as 4 informações: nome do cliente, quantidade de hambúrgueres, preço total com desconto, valor do desconto — verificado por comparação exata da saída real.
- AC1.5 Os limites dos tipos são honrados: 999 hambúrgueres e preço 99999,99 executam sem estouro; nome de 40 bytes cabe; nome de 41 bytes reprova com `ORA-06502` (negativo plantado) — verificado por execução real em Oracle.

## Fora de escopo

- Preço unitário × quantidade (a RN01 não define preço unitário; o preço total é dado).
- Outras RNs (receitas, despesas, cadastro de clientes), tabelas, triggers, packages.
- Aplicativo mobile e plataforma web do estudo de caso.

## ASSUMPTIONS

| # | Suposição | Como validar (spike) | Estado |
|---|---|---|---|
| 1 | "Preço total" da RN01 é entrada do bloco (não derivado de preço unitário) — a RN01 lista 4 variáveis e nenhuma é preço unitário | releitura da RN01 + comparação com o enunciado | confirmed (2026-09-29) |
| 2 | O desconto incide sobre o preço total (não sobre subtotal de itens) e o preço exibido é o valor já líquido | enunciado: "preço total (considerando o desconto, se aplicável)" | confirmed (2026-09-29) |
| 3 | "5 números inteiros e 2 casas decimais" = `NUMBER(7,2)` (5 dígitos inteiros + 2 decimais) e "até 3 números inteiros" = `NUMBER(3,0)` | convenção Oracle `NUMBER(p,s)` | confirmed (2026-09-29) |
| 4 | Saída numérica com formato fixo (vírgula decimal pt-BR via `TO_CHAR` + override NLS) para comparação determinística nos testes | execução real em Oracle | confirmed (2026-09-29) |

## Clarificações

- Nenhuma pendente: o enunciado da RN01 foi fornido completo pelo usuário em 2026-09-29 (F0 fechado pelo próprio enunciado, sem necessidade de grill — decisão registrada em `docs/progress.md`).
