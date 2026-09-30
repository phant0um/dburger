-- Divine Burger (DBurger) — RN01
-- Bloco PL/SQL: pedido com desconto de 10% para mais de 3 hambúrgueres.
-- Regra de negócio: se a quantidade de hambúrgueres for maior que 3,
-- aplica-se desconto de 10% sobre o preço total; caso contrário,
-- mantém-se o preço total original.
SET SERVEROUTPUT ON
SET FEEDBACK OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE

DECLARE
  v_cliente          VARCHAR2(40 BYTE) := 'Ana Souza';
  v_qtd_hamburgueres NUMBER(3, 0)      := 5;
  v_preco_total      NUMBER(7, 2)      := 120.00;
  v_desconto         NUMBER(7, 2)      := 0;
BEGIN
  IF v_qtd_hamburgueres > 3 THEN
    v_desconto    := ROUND(v_preco_total * 0.10, 2);
    v_preco_total := v_preco_total - v_desconto;
  END IF;

  DBMS_OUTPUT.PUT_LINE('Cliente: ' || v_cliente);
  DBMS_OUTPUT.PUT_LINE('Quantidade de hambúrgueres: ' || TO_CHAR(v_qtd_hamburgueres));
  DBMS_OUTPUT.PUT_LINE('Preço total a pagar: R$ ' ||
    TO_CHAR(v_preco_total, 'FM999990D00', 'NLS_NUMERIC_CHARACTERS='',.'''));
  DBMS_OUTPUT.PUT_LINE('Desconto aplicado: R$ ' ||
    TO_CHAR(v_desconto, 'FM999990D00', 'NLS_NUMERIC_CHARACTERS='',.'''));
END;
/
EXIT
