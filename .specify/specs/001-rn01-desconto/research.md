# Research — 001 RN01 desconto

## Tipos Oracle pedidos pela RN01

- "conteúdos caracteres de até 40 bytes" → `VARCHAR2(40 BYTE)`. O sufixo `BYTE` é explícito de propósito: em banco `AL32UTF8`, `VARCHAR2(40)` pode ser lido como 40 caracteres dependendo do `NLS_LENGTH_SEMANTICS`; a RN01 fala em bytes.
- "até 3 números inteiros" → `NUMBER(3,0)`: escala 0 impede casas decimais; aceita 0..999 e negativos com sinal (−999..999). Fora disso: `ORA-06502` em tempo de execução (atribuição a variável é checada no runtime, não na compilação).
- "5 números inteiros e 2 casas decimais" → `NUMBER(7,2)`: precisão total 7, escala 2 → parte inteira de até 5 dígitos (até 99999,99).

## Comportamento de overflow (validado em execução real)

- `VARCHAR2(40 BYTE)` com 41 bytes → `ORA-06502: PL/SQL: numeric or value error`.
- `NUMBER(3,0) := 1000` → mesmo `ORA-06502`. É o negativo plantado da suíte: se o teste de 41 bytes passar, o gate de limites está falso.

## Desconto

- `ROUND(preco * 0.10, 2)` antes de subtrair: `NUMBER(7,2)` tem escala 2, e `99999.99 * 0.10 = 9999.999` arredondaria implícito; arredondar explícito deixa o resultado auditável (caso-limite: 10000,00).
- `preco * 0.10` cabe em `NUMBER(7,2)` para todo preço admitido pelo tipo (pior caso 10000,00 ≤ 99999,99).

## Saída determinística

- `DBMS_OUTPUT.PUT_LINE` com número "cru" depende de NLS da sessão (vírgula vs ponto). Formato fixo com `TO_CHAR(v, 'FM999990D00', 'NLS_NUMERIC_CHARACTERS='',.''')` → vírgula decimal pt-BR (ex.: `108,00`).
- `FM` remove espaços de preenchimento; a saída fica `R$ 108,00`, sem padding.
- **Armadilha validada em execução real:** `FM99999D00` apaga o dígito inteiro quando o valor é 0 (saída `,00` em vez de `0,00`) — o modelo `9` suprime zeros à esquerda e o `FM` remove o último espaço. O placeholder `0` no final da parte inteira (`FM999990D00`) garante o dígito. 3 dos 8 casos da primeira rodada real reprovaram por isso.

## Oracle de teste

- `gvenzl/oracle-free:slim` (image oficial mantida por Gerald Venzl, ~650 MB, sobe em ~60–90 s) em Docker: contêiner descartável, usuário de teste criado pelo harness, zero instalação de cliente no host (o `sqlplus` já vem no contêiner; o harness fala com ele via `docker exec -i` e stdin).
- PDB de serviço: `FREEPDB1`; senha via `ORACLE_PASSWORD` (variável de ambiente do harness, nunca commitada).
- Sem Docker/Oracle disponível, apenas o contrato estrutural roda — e isso é declarado, nunca vendido como teste de comportamento.

## Referências

- Oracle Database PL/SQL Language Reference — `NUMBER(p,s)`, `VARCHAR2(n BYTE)`, `DBMS_OUTPUT`.
- Oracle Database Error Messages — `ORA-06502`.
