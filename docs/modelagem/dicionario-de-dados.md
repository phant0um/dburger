# Tabela 1 — Dicionário de dados das tabelas do projeto DBurger

> Fonte: material do projeto DBurger, fornecido pelo usuário em 2026-09-29.
> Registro fiel (nome + descrição). Colunas/atributos **não** estão neste
> documento — não inventar; aguardar a especificação de colunas (próximas
> tabelas do material) antes de escrever DDL.

| Tabela | Breve Descrição |
|---|---|
| DB_BAIRRO | Tabela que irá receber os bairros onde se encontram as lojas, os clientes e os funcionários do projeto DBurger. |
| DB_CARGO | Tabela que irá receber os principais cargos. Gerente, Caixa e Chapeiro são alguns exemplos de cargos existentes. |
| DB_CATEGORIA_PROD | Tabela que irá receber as categorias dos produtos do projeto DBurger. |
| DB_CIDADE | Tabela que irá receber os dados das principais cidades do Brasil associadas ao endereço das lojas, funcionários e clientes do projeto DBurger. |
| DB_CLIENTE | Tabela que irá receber os dados dos clientes que realizam pedidos no projeto DBurger. Esses clientes podem ser pessoas físicas ou pessoas jurídicas. |
| DB_CLI_FISICA | Tabela que recebem os dados dos clientes pessoa física que realizam pedidos no projeto DBurger. |
| DB_CLI_JURIDICA | Tabela que recebem os dados dos clientes pessoa jurídica que realizam pedidos no projeto DBurger. |
| DB_DEPTO | Tabela que recebe os dados dos departamentos da empresa DBurger. |
| DB_END_CLI | Tabela que recebe os dados dos endereços dos clientes que solicitam entrega dos produtos da empresa DBurger. |
| DB_END_FUNC | Tabela que recebe os dados dos endereços dos funcionários que trabalham na empresa DBurger. |
| DB_END_LOJA | Tabela que recebe os dados dos endereços das lojas da empresa DBurger. |
| DB_ESTADO | Essa tabela irá receber todos os Estados do Brasil. |
| DB_FATURAMENTO_PRODUTO | Essa tabela irá receber o resumo do faturamento das vendas dos produtos realizadas nas lojas DBurger. |
| DB_FORMA_PAGAMENTO | Tabela que irá receber as formas de pagamento oferecidas ao cliente para o projeto DBurger. |
| DB_FUNCIONARIO | Tabela que irá receber todos os funcionários cadastrados na empresa DBurger. |
| DB_FUNC_LOJA | Tabela que associa o funcionário DBurger à sua respectiva loja, permitindo que o funcionário, ao longo do tempo, possa receber promoções na empresa DBurger. |
| DB_ITEM_PEDIDO | Tabela que irá receber os itens pedidos para cada pedido dos 2 últimos anos de vendas da empresa DBurger. |
| DB_LOGRADOURO | Tabela que irá receber os logradouros (endereços) das lojas, funcionários e clientes da empresa DBurger. |
| DB_LOJA | Tabela que irá receber as lojas localizadas nas principais cidades do Brasil da empresa DBurger. |
| DB_PEDIDO | Tabela que irá receber os pedidos criados contendo as vendas dos 2 últimos anos da empresa DBurger. |
| DB_PRODUTO | Tabela que irá receber os produtos do projeto DBurger. |
| DB_PRODUTO_IMAGEM | Tabela que irá receber futuramente as imagens dos produtos do projeto DBurger. |
| DB_PRODUTO_LOJA | Tabela que associa os produtos existentes em determinada loja do projeto DBurger. |
| DB_SUB_CATEGORIA_PROD | Tabela que irá receber as subcategorias dos produtos do projeto DBurger. |

**Total: 24 tabelas.**

## Famílias observadas (leitura estrutural, não normativa)

- **Endereço:** DB_ESTADO → DB_CIDADE → DB_LOGRADOURO → DB_BAIRRO → DB_END_LOJA / DB_END_FUNC / DB_END_CLI.
- **Pessoas:** DB_CLIENTE (PF/PJ) → DB_CLI_FISICA / DB_CLI_JURIDICA; DB_FUNCIONARIO → DB_CARGO / DB_DEPTO / DB_FUNC_LOJA → DB_LOJA.
- **Catálogo:** DB_CATEGORIA_PROD → DB_SUB_CATEGORIA_PROD → DB_PRODUTO → DB_PRODUTO_IMAGEM / DB_PRODUTO_LOJA.
- **Venda:** DB_PEDIDO → DB_ITEM_PEDIDO → DB_PRODUTO; DB_FORMA_PAGAMENTO; DB_FATURAMENTO_PRODUTO (resumo).

## Pendência explícita

- Especificação de colunas, PKs, FKs e constraints de cada tabela: **não fornecida até aqui**. O DDL (`db/ddl/`) só será escrito quando o material com os atributos chegar — ver `docs/progress.md`.
