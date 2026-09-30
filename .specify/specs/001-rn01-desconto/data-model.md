# Data model — 001 RN01 desconto

Sem tabelas: a RN01 opera sobre variáveis de bloco anônimo. Este é o modelo completo de dados da feature.

| Variável | Tipo Oracle | Papel | Origem | Limite |
|---|---|---|---|---|
| `v_cliente` | `VARCHAR2(40 BYTE)` | nome do cliente | entrada | 40 bytes; estouro → `ORA-06502` |
| `v_qtd_hamburgueres` | `NUMBER(3,0)` | quantidade por pedido | entrada | 0–999 (inteiro); estouro → `ORA-06502` |
| `v_preco_total` | `NUMBER(7,2)` | preço total a pagar (entrada; vira líquido após o desconto) | entrada | até 99999,99 |
| `v_desconto` | `NUMBER(7,2)` | valor do desconto obtido | calculado: `ROUND(preco * 0.10, 2)` se `qtd > 3`, senão `0` | até 99999,99 |

Regra de transformação (RN01):

```
se v_qtd_hamburgueres > 3:
    v_desconto    := ROUND(v_preco_total * 0.10, 2)
    v_preco_total := v_preco_total - v_desconto
senão:
    v_desconto := 0
```

Formato de saída (determinístico, pt-BR): `TO_CHAR(x, 'FM999990D00', 'NLS_NUMERIC_CHARACTERS='',.''')` → vírgula decimal, sem padding, zero inteiro impresso (ex.: `108,00`, `0,00`).
