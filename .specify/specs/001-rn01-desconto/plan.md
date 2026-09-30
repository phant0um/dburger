# Plan — 001 RN01 desconto

## Decisões de implementação

1. **Um arquivo entregável**: `src/rn01_bloco.sql` é literalmente o bloco pedido pela RN01 (4 variáveis, regra do desconto, 4 `DBMS_OUTPUT.PUT_LINE`). Nada além do que a RN01 pede entra nele.
2. **Testabilidade sem contaminar o exercício**: `src/rn01_bloco_tpl.sql` é o mesmo bloco com 3 placeholders (`{{CLIENTE}}`, `{{QTD}}`, `{{PRECO}}`). O teste de golden file garante que o arquivo entregável é exatamente o template renderizado com o caso-demo — impede drift entre o que se testa e o que se entrega.
3. **Comportamento só é provado em Oracle real**: `tests/run_tests.py` (Python 3 stdlib) renderiza cada caso de `testdata/casos.json`, executa via `sqlplus` dentro do contêiner `gvenzl/oracle-free:slim` e compara a saída linha a linha. Marcado como `integration`.
4. **Contrato estrutural offline**: `tests/test_offline.py` prova golden file, os 4 tipos declarados e o schema dos casos. Ele prova estrutura, nunca comportamento — isso está escrito na saída do próprio teste.
5. **Sem dependências de terceiro**: nenhum pacote Python, nenhuma extensão SQL*Plus. O único requisito externo é Docker para a suíte de integração.
6. **Segurança**: senha de teste via `DBURGER_SYS_PASSWORD` (padrão local documentado); bloco entra no `sqlplus` por stdin, sem interpolação em shell; gitleaks no hook e no CI.

## Orçamento de tokens/execução

- Fases mecânicas (scaffold, testes) feitas em uma sessão; a subida do Oracle Free é o passo mais caro em tempo (~2 min), não em token.

## Riscos

| Risco | Mitigação |
|---|---|
| Encoding de saída (acentos) variar entre host e contêiner | `NLS_LANG=AMERICAN_AMERICA.AL32UTF8` fixo no `docker exec`; comparação exata reprova variação |
| Oracle Free não subir no CI público | CI roda apenas offline; integração é local e documentada como tal |
| Drift template × arquivo entregável | golden file check no `make test` |
