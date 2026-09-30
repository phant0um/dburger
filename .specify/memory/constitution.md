# Constitution — DBurger (DBurger PL/SQL)

Estas regras valem para toda feature. Mudar este arquivo exige issue própria, nunca dentro de uma feature.

## 1. Escopo

- DBurger resolve regras de negócio da hamburgueria em blocos PL/SQL didáticos; cada bloco executa uma regra de negócio (RN) por vez e imprime o resultado via `DBMS_OUTPUT.PUT_LINE`.
- O que fica fora: aplicativo mobile, plataforma web, modelagem completa do banco (clientes, vendas, produtos). O projeto nunca escreve fora de `src/`, `dist/` e `testdata/`.

## 2. Código

- PL/SQL (Oracle 18c+), SQL*Plus como executor. Nenhuma dependência de terceiros dentro dos `.sql`.
- O harness de teste (Python 3 stdlib apenas) orquestra o Oracle em contêiner Docker; a lógica de negócio vive só em PL/SQL.
- Um arquivo por RN; a variável de saída é sempre formatada com `TO_CHAR` explícito (formato determinístico, independente de NLS de sessão).
- Erros carregam contexto: bloco que falha deve deixar a `ORA-` visível na saída do harness, nunca silenciada.

## 3. Segurança (modelo de ameaça curto)

- Entrada não confiável: valores de teste vêm de `testdata/casos.json`. Validação: schema rígido no harness (tipos e limites conferidos antes de renderizar).
- Valores nunca são interpolados em shell: o bloco renderizado entra no `sqlplus` por stdin, sem `sh -c`.
- Segredo: senha do usuário de teste só em variável de ambiente do harness (padrão local, documentado). Nunca em log, saída ou mensagem de erro. Nenhuma credencial de produção existe neste projeto.
- gitleaks no pre-commit e no CI desde o primeiro commit.

## 4. Testes

- O contrato estrutural (4 variáveis, tipos exatos, golden file) roda offline, sem Oracle.
- O comportamento (regra de desconto) só é considerado verificado com execução real em Oracle (`integration`); teste offline nunca prova comportamento.
- Teste primeiro (red → green → refactor) em cada seam.
- Todo gate novo prova que reprova um negativo plantado (ex.: nome de 41 bytes deve estourar `VARCHAR2(40 BYTE)` com `ORA-06502`).

## 5. Arquivos e estado

- Os `.sql` de entrega são didáticos: sem colateral, sem DDL, sem `COMMIT`. Blocos anônimos autocontidos.
- Idempotência: rodar o harness duas vezes não altera `src/`; o harness recria apenas o usuário de teste se necessário.

## 6. UX da CLI (harness)

- Exit `0` sucesso, `1` erro de execução ou teste reprovado, `2` uso inválido, `3` dependência ausente (Docker/Oracle).
- Progresso em stderr; stdout só recebe o resultado dos testes.
- Mensagem de erro diz o próximo passo (ex.: "rode `make doctor`").

## 7. Performance

- Suíte completa (8 casos, incluindo subida do Oracle Free) em menos de 4 min em MacBook Apple Silicon; casos individuais em < 5 s cada com o banco de pé.
