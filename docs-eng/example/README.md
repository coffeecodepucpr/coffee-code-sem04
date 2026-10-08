# Runnable examples, Week 04

🇧🇷 [Português](../../docs/example/README.md) · 🇺🇸 English

The runnable files for this week live in [`docs/example/`](../../docs/example/); this page is the English guide to them. It is a reference, not a required answer key: your project needs to apply the same concepts, not be identical to this one.

> The code, file names, table names and comments in these files are in Portuguese, to match the rest of the material: `usuarios` (users), `materias` (subjects), `grupos` (groups), `participacoes` (memberships), `encontros` (meetings).

## `sql/`: the main track

Scripts for the Study Group Finder, tested on PostgreSQL 16. Run them in order, in the Supabase SQL Editor:

| File | What it does |
|---|---|
| `01-schema.sql` | Creates the five tables, the constraints and turns on RLS |
| `02-seed.sql` | Inserts the example data (6 subjects, 8 users, 6 groups, 16 memberships, 7 meetings) |
| `03-consultas.sql` | Seven queries, from a simple `select` to `join` with `group by` |
| `04-indices.sql` | Veteran track: foreign key indexes |
| `05-laboratorio-indices.sql` | Veteran track: a 300-thousand-row lab to measure the effect of an index (runs in a separate schema, `lab`) |

## `sqlalchemy/`: veteran track, tested

The model in SQLAlchemy 2.0 and the migration history with Alembic, tested against PostgreSQL 16 (SQLAlchemy 2.0.54, Alembic 1.20, psycopg 3).

```
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://user:password@host:5432/test_database"
alembic upgrade head      # creates the tables through the initial migration
python consultas.py       # runs the queries (needs the seed loaded)
```

## `prisma/`: veteran track, NOT tested by the author

> **WARNING**
> The environment in which this material was produced could not download the Prisma engine, so these files **were never run or validated**. They follow the official Prisma 7 documentation, checked on October 4, 2026. Check them on your machine.

Prisma ORM 8 is still a *release candidate* on that date, and `npm install prisma` already installs the Prisma 8 tool, which has its own flow (no `generate` or `migrate dev`). A Prisma 7 project on PostgreSQL can be imported into Prisma 8 with `npx prisma@latest orm init --from-prisma7-schema prisma/schema.prisma`. That is why `package.json` pins version 7, to keep the examples stable.

```
npm install
cp .env.example .env      # fill in the DATABASE_URL of a test database
npx prisma generate
npx tsx src/consultas.ts
```

## Security rules

- Always use a **test database separate** from your deliverable's database.
- The password goes in `.env`, which never goes into Git. The `.env.example` files have no password.
- Never run `prisma migrate dev` on the deliverable's database: it may propose resetting the database.
