# ☕ Coffee & Code — SEM 04 | Modelagem de Dados

🇧🇷 Português · 🇺🇸 [English](README.en.md)

```text
> module: sem-04
> tema: modelagem de dados
> status: online
> coffee loaded ✓
```

Material da **Semana 04** da trilha do Coffee & Code, o clube de tecnologia da PUCPR.

## Sobre

☕ Coffee & Code PUCPR — Semana 04: Modelagem de Dados. PostgreSQL, Supabase, DER, normalização (1FN a 3FN) e SQL, levando o Buscador de Grupos de Estudo dos arrays da Semana 03 para um banco relacional de verdade.

---

Na Semana 03 as telas ganharam comportamento: o Login valida, o Dashboard renderiza e filtra os cards, o Perfil reage sem recarregar a página. Mas faça um teste: saia de um grupo e recarregue a página. O grupo está de volta. Os dados moram em arrays dentro do `script.js` e somem a cada recarregamento.

A Semana 04 existe para dar um lugar de verdade a esses dados: PostgreSQL, Supabase, DER, normalização (1FN a 3FN) e SQL. No fim da semana o Buscador de Grupos de Estudo tem um banco relacional bem desenhado, ativo e com dados dentro — ainda sem ligar a página a ele, mas com o modelo pronto.

> **Sobre o idioma:** o material em inglês fica em [`docs-eng/`](docs-eng/), com a mesma estrutura de [`docs/`](docs/); os READMEs têm versão em inglês com o sufixo `.en.md`.

## Por onde começar

👉 **[docs/00-comece-aqui.md](docs/00-comece-aqui.md)** — leia este primeiro. Ele explica o caminho da semana e o que vem da Semana 03.

Depois, siga os módulos na ordem. Os módulos `01` a `12` formam a trilha principal:

| # | Módulo | Sobre |
|---|---|---|
| 01 | [Por que um banco relacional](docs/01-por-que-um-banco-relacional.md) | Persistência, tabela, linha, coluna e chave |
| 02 | [PostgreSQL e Supabase](docs/02-postgresql-e-supabase.md) | Criar o projeto, o painel e a primeira consulta |
| 03 | [Entidades e atributos](docs/03-entidades-e-atributos.md) | Descobrir as entidades e os atributos |
| 04 | [Relacionamentos e cardinalidade](docs/04-relacionamentos-e-cardinalidade.md) | 1:1, 1:N, N:N e a notação pé de galinha |
| 05 | [O diagrama DER](docs/05-o-diagrama-der.md) | Desenhar o DER do projeto |
| 06 | [Normalização: anomalias e 1FN](docs/06-normalizacao-anomalias-e-1fn.md) | Anomalias e a 1FN |
| 07 | [Normalização: 2FN e 3FN](docs/07-normalizacao-2fn-e-3fn.md) | 2FN e 3FN |
| 08 | [Tipos de dados e chaves](docs/08-tipos-de-dados-e-chaves.md) | Tipos, chaves e restrições |
| 09 | [SQL: criando as tabelas](docs/09-sql-criando-as-tabelas.md) | `create table` e o script do projeto |
| 10 | [SQL: inserindo e consultando](docs/10-sql-inserindo-e-consultando.md) | `insert`, `select`, `update` e `delete` |
| 11 | [SQL: join e agregações](docs/11-sql-join-e-agregacoes.md) | `join`, `left join`, `count` e `group by` |
| 12 | [Projeto guiado](docs/12-projeto-guiado.md) | Construindo o banco do início ao fim |

Os módulos `13` a `15` são a **trilha veterano**, opcional, para ler depois:

| # | Módulo | Sobre |
|---|---|---|
| 13 | [Índices e desempenho](docs/13-indices-e-desempenho.md) | Índices e `explain analyze` |
| 14 | [Migrations](docs/14-migrations.md) | Migrations com Alembic e Prisma |
| 15 | [ORMs: Prisma e SQLAlchemy](docs/15-orms-prisma-e-sqlalchemy.md) | ORMs |

E, para consultar quando precisar:

- 💻 [Exemplo executável](docs/example/) — os scripts SQL do projeto e os modelos da trilha veterano, para consulta
- 🎯 [Desafios](docs/desafios.md) — opcionais, para ir além do pedido
- ✅ [Entregável](docs/entregavel.md) — checklist final antes de fechar a semana

## O exemplo executável

A pasta [`docs/example/`](docs/example/) tem uma implementação de referência do banco do Buscador de Grupos de Estudo:

- `sql/` — os scripts de criação, dados e consultas, testados em um PostgreSQL 16. Rode na ordem, no SQL Editor do Supabase.
- `sqlalchemy/` — trilha veterano: o modelo em SQLAlchemy com migrations em Alembic (testado).
- `prisma/` — trilha veterano: o mesmo modelo em Prisma (**não testado** pelo autor).

Os detalhes estão no [README da pasta](docs/example/README.md).

É material de **consulta, não gabarito**. O seu projeto tem o seu próprio domínio — o exemplo serve para você ver uma solução possível quando travar, não para copiar.

## O entregável

Ao final da Semana 04, o repositório do **seu projeto** (não este aqui) deve ter, além de tudo o que veio das Semanas 01 a 03:

```text
docs/
├── der.png           ← novo: o DER do projeto
└── arquitetura.md    ← atualizado: modelo, dicionário de dados, ordem dos scripts
sql/                  ← novo
├── 01-schema.sql
├── 02-seed.sql
└── 03-consultas.sql
```

E um banco PostgreSQL **ativo** no Supabase, com as tabelas criadas, o RLS ligado e dados dentro. A senha do banco não pode estar em nenhum arquivo versionado.

O checklist completo está em [docs/entregavel.md](docs/entregavel.md).

> **Um modelo correto vale mais que um banco grande.** Um DER que resolve bem o N:N e um modelo sem repetição, com poucas linhas, valem mais nesta semana do que um banco cheio de dados em uma tabela única mal desenhada.

## Entregas da turma

Ainda não há entregas da Semana 04. Quer ser a primeira pessoa? Veja [como entregar](entregas/README.md).

## O que não entra nesta semana

A página web continua usando os dados mock da Semana 03: ligar o front-end ao banco fica para depois. Também não entram login de verdade nem políticas de acesso por usuário (além de ligar o RLS). Índices, migrations e ORM são da trilha veterano, não do entregável.

## Projeto contínuo

Todos os módulos usam o mesmo projeto fictício das semanas anteriores: o **Buscador de Grupos de Estudo**, agora com os dados em um banco relacional. Se você tem um projeto próprio, o raciocínio de cada módulo se aplica da mesma forma — só troque o nome.

## Como funciona

O Coffee & Code é **100% online**. Cada módulo foi escrito para ser autossuficiente: você estuda no seu ritmo, pode avançar mais rápido, voltar em semanas anteriores e consultar o material durante o projeto.

Os encontros semanais, também online, existem para tirar dúvidas, revisar conceitos, programar junto e mostrar o que você produziu — **não para dar aula**:

- 🗓️ **quarta-feira** — 20h00 às 21h30
- 🗓️ **sábado** — 10h00 às 11h30

Os dois trabalham o mesmo conteúdo. Escolha o que couber melhor na sua semana, e não precisa ficar o horário inteiro na call.

## Travou?

Chega no encontro ou no Discord com uma pergunta específica. `"minha chave estrangeira dá erro ao inserir, já conferi a ordem e o tipo"` costuma ser resolvido muito mais rápido do que `"meu banco não funciona"`.

E lembra: não saber alguma coisa não é problema. Saber pesquisar faz parte da área.

## Diagramas

Todos os diagramas usados nos módulos estão em [`docs/assets/`](docs/assets/), em formato SVG editável.

## Semanas anteriores

- [SEM 01 — Kickoff & Design System](https://github.com/coffeecodepucpr/coffee-code-sem01)
- [SEM 02 — Interface Web (Parte 1: Layout)](https://github.com/coffeecodepucpr/coffee-code-sem02)
- [SEM 03 — Interface Web (Parte 2: Dinâmica)](https://github.com/coffeecodepucpr/coffee-code-sem03)

---

```text
HTTP 418 — I'm a teapot
> ready to code
```
