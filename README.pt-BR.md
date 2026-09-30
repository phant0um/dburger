# DBurger — exercícios PL/SQL

Projeto didático de PL/SQL do estudo de caso Divine Burger (DBurger): uma
hamburgueria cujos dados vivem no Oracle. Cada regra de negócio (RNxx) é um bloco
anônimo autocontido, verificado por uma suíte de testes em Oracle real.

Este repositório implementa a **RN01 — desconto de pedido**: se a quantidade de
hambúrgueres for maior que 3, aplica-se desconto de 10% sobre o preço total; o
bloco imprime nome do cliente, quantidade, preço final e desconto via
`DBMS_OUTPUT.PUT_LINE`.

## A regra (RN01)

> Crie um bloco PL/SQL que declare quatro variáveis: nome do cliente
> (`VARCHAR2` de até 40 bytes), quantidade de hambúrgueres (até 3 números
> inteiros), preço total (5 números inteiros e 2 casas decimais) e valor do
> desconto (5 números inteiros e 2 casas decimais). Se a quantidade de
> hambúrgueres for maior que 3, aplique desconto de 10% no preço total. Caso
> contrário, mantenha o preço total original. Exiba nome, quantidade, preço total
> (com desconto, se aplicável) e valor do desconto com `DBMS_OUTPUT.PUT_LINE`.

## Requisitos

- Oracle 18c+ com SQL\*Plus (para executar o bloco) — ou apenas ler `src/rn01_bloco.sql`.
- Docker (Colima/OrbStack/Docker Desktop) para a suíte de integração.
- Python 3.9+ (apenas stdlib) para o harness de testes.

## Como executar o bloco

```sh
sqlplus usuario/senha@servico @src/rn01_bloco.sql
```

Saída esperada (caso de demonstração: Ana Souza, 5 hambúrgueres, R$ 120,00):

```
Cliente: Ana Souza
Quantidade de hambúrgueres: 5
Preço total a pagar: R$ 108,00
Desconto aplicado: R$ 12,00
```

## Desenvolvimento

```sh
make test              # contrato estrutural, offline (NÃO prova comportamento)
make test-integration  # comportamento, Oracle real (sobe o contêiner gvenzl/oracle-free)
make vet               # subconjunto rápido: declarações + golden file
make lint              # gitleaks + higiene de texto
make build             # dist/dburger-rn01.sql
make doctor            # estado do ambiente por camada
```

Os testes estruturais provam o contrato do arquivo (quatro variáveis com tipos
exatos, golden file contra o template, schema das fixtures). O comportamento só é
provado por `make test-integration`, que executa o bloco dentro de um contêiner
Oracle descartável e compara a saída linha a linha. Não existe caminho de verde
falso: sem Oracle não há afirmação de comportamento.

## Estrutura

- `src/rn01_bloco.sql` — o bloco entregável (exatamente o template renderizado com o caso demo).
- `src/rn01_bloco_tpl.sql` — template parametrizado usado pelo harness de testes.
- `testdata/casos.json` — fixtures reais: demo, fronteira (3/4), teto dos tipos, negativos plantados.
- `tests/` — suíte de contrato offline + harness de integração Oracle.
- `.specify/` — constitution, spec, research, plan, tasks (workflow `projeto-novo`).
- `docs/modelagem/dicionario-de-dados.md` — Tabela 1 do material: as 24 tabelas do projeto DBurger (DDL pendente da especificação de colunas).
- `docs/verify-report.md` — veredito por AC com evidência; `docs/progress.md` — log do ciclo.

## Licença

MIT — veja [LICENSE](LICENSE).
