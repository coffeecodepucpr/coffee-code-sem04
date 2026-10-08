# ☕ Coffee & Code — WEEK 04 | Data Modeling

🇧🇷 [Português](README.md) · 🇺🇸 English

```text
> module: sem-04
> topic: data modeling
> status: online
> coffee loaded ✓
```

Material for **Week 04** of the Coffee & Code track, the technology club at PUCPR.

## About

☕ Coffee & Code PUCPR — Week 04: Data Modeling. PostgreSQL, Supabase, ER diagrams, normalization (1NF to 3NF) and SQL, moving the Study Group Finder from Week 03's arrays into a real relational database.

---

In Week 03 the screens got behavior: Login validates, the Dashboard renders and filters the cards, the Profile reacts without reloading the page. But try this: leave a group and reload the page. The group is back. The data lives in arrays inside `script.js` and disappears on every reload.

Week 04 exists to give that data a real home: PostgreSQL, Supabase, ERD, normalization (1NF to 3NF) and SQL. By the end of the week the Study Group Finder has a well-designed relational database, active and with data inside — still without connecting the page to it, but with the model ready.

> **About the language:** every `.md` file in this repository has an English version with the `.en.md` suffix. The diagrams, the code and the example project's table and column names stay in Portuguese, so they match the SQL scripts: `usuarios` (users), `materias` (subjects), `grupos` (groups), `participacoes` (memberships), `encontros` (meetings).

## Where to start

👉 **[docs/00-comece-aqui.en.md](docs/00-comece-aqui.en.md)** — read this one first. It explains the week's path and what comes from Week 03.

Then follow the modules in order. Modules `01` to `12` make up the main track:

| # | Module | About |
|---|---|---|
| 01 | [Why a relational database](docs/01-por-que-um-banco-relacional.en.md) | Persistence, table, row, column and key |
| 02 | [PostgreSQL and Supabase](docs/02-postgresql-e-supabase.en.md) | Creating the project, the dashboard and the first query |
| 03 | [Entities and attributes](docs/03-entidades-e-atributos.en.md) | Finding the entities and the attributes |
| 04 | [Relationships and cardinality](docs/04-relacionamentos-e-cardinalidade.en.md) | 1:1, 1:N, N:N and crow's foot notation |
| 05 | [The ER diagram](docs/05-o-diagrama-der.en.md) | Drawing the project's ERD |
| 06 | [Normalization: anomalies and 1NF](docs/06-normalizacao-anomalias-e-1fn.en.md) | Anomalies and 1NF |
| 07 | [Normalization: 2NF and 3NF](docs/07-normalizacao-2fn-e-3fn.en.md) | 2NF and 3NF |
| 08 | [Data types and keys](docs/08-tipos-de-dados-e-chaves.en.md) | Types, keys and constraints |
| 09 | [SQL: creating the tables](docs/09-sql-criando-as-tabelas.en.md) | `create table` and the project script |
| 10 | [SQL: inserting and querying](docs/10-sql-inserindo-e-consultando.en.md) | `insert`, `select`, `update` and `delete` |
| 11 | [SQL: join and aggregations](docs/11-sql-join-e-agregacoes.en.md) | `join`, `left join`, `count` and `group by` |
| 12 | [Guided project](docs/12-projeto-guiado.en.md) | Building the database from start to finish |

Modules `13` to `15` are the **veteran track**, optional, to read afterwards:

| # | Module | About |
|---|---|---|
| 13 | [Indexes and performance](docs/13-indices-e-desempenho.en.md) | Indexes and `explain analyze` |
| 14 | [Migrations](docs/14-migrations.en.md) | Migrations with Alembic and Prisma |
| 15 | [ORMs: Prisma and SQLAlchemy](docs/15-orms-prisma-e-sqlalchemy.en.md) | ORMs |

And, to look up whenever you need:

- 💻 [Runnable example](docs/example/README.en.md) — the project's SQL scripts and the veteran track models, for reference
- 🎯 [Challenges](docs/desafios.en.md) — optional, to go beyond what is asked
- ✅ [Deliverable](docs/entregavel.en.md) — final checklist before closing the week

## The runnable example

The [`docs/example/`](docs/example/) folder has a reference implementation of the Study Group Finder database:

- `sql/` — the creation, data and query scripts, tested on PostgreSQL 16. Run them in order, in the Supabase SQL Editor.
- `sqlalchemy/` — veteran track: the model in SQLAlchemy with migrations in Alembic (tested).
- `prisma/` — veteran track: the same model in Prisma (**not tested** by the author).

The details are in the [folder's README](docs/example/README.en.md).

It is **reference material, not an answer key**. Your project has its own domain — the example is there for you to see one possible solution when you get stuck, not to copy.

## The deliverable

At the end of Week 04, **your project's** repository (not this one) should have, in addition to everything from Weeks 01 to 03:

```text
docs/
├── der.png           ← new: the project's ERD
└── arquitetura.md    ← updated: model, data dictionary, script order
sql/                  ← new
├── 01-schema.sql
├── 02-seed.sql
└── 03-consultas.sql
```

And an **active** PostgreSQL database on Supabase, with the tables created, RLS on and data inside. The database password cannot be in any versioned file.

The complete checklist is in [docs/entregavel.en.md](docs/entregavel.en.md).

> **A correct model is worth more than a big database.** An ERD that solves the N:N well and a model without repetition, with few rows, are worth more this week than a database full of data in a single badly designed table.

## Class submissions

There are no Week 04 submissions yet. Want to be the first? See [how to submit](entregas/README.en.md).

## What is not part of this week

The web page keeps using the mock data from Week 03: connecting the front end to the database comes later. Real login and per-user access policies (beyond turning RLS on) are not included either. Indexes, migrations and ORMs are part of the veteran track, not the deliverable.

## Ongoing project

All modules use the same fictional project from previous weeks: the **Study Group Finder** (*Buscador de Grupos de Estudo*), now with its data in a relational database. If you have your own project, each module's reasoning applies the same way — just change the name.

## How it works

Coffee & Code is **100% online**. Each module was written to be self-contained: you study at your own pace, can move ahead faster, go back to previous weeks and look up the material while working on your project.

The weekly meetings, also online, exist to answer questions, review concepts, code together and show what you produced — **not to give lectures**:

- 🗓️ **Wednesday** — 8:00 pm to 9:30 pm
- 🗓️ **Saturday** — 10:00 am to 11:30 am

Both cover the same content. Pick whichever fits your week best, and you don't need to stay on the call the whole time.

## Stuck?

Bring a specific question to the meeting or to Discord. `"my foreign key gives an error when inserting, I already checked the order and the type"` usually gets solved much faster than `"my database doesn't work"`.

And remember: not knowing something is not a problem. Knowing how to search is part of the field.

## Diagrams

All diagrams used in the modules are in [`docs/assets/`](docs/assets/), in editable SVG format.

## Previous weeks

- [WEEK 01 — Kickoff & Design System](https://github.com/coffeecodepucpr/coffee-code-sem01)
- [WEEK 02 — Web Interface (Part 1: Layout)](https://github.com/coffeecodepucpr/coffee-code-sem02)
- [WEEK 03 — Web Interface (Part 2: Dynamic)](https://github.com/coffeecodepucpr/coffee-code-sem03)

---

```text
HTTP 418 — I'm a teapot
> ready to code
```
