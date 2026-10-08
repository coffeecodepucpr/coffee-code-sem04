# Module 15, ORMs: Prisma and SQLAlchemy

🇧🇷 [Português](./15-orms-prisma-e-sqlalchemy.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

> **VETERAN TRACK**
> This module is part of the veteran track: it comes after the essential content and is not needed for the week's deliverable. If you follow the main track, you can skip to `entregavel.en.md`.

Up to here you talked to the database by writing SQL in the Supabase dashboard. A real application talks to it from code, in Python, TypeScript or another language. This module introduces the tool that builds that bridge, the ORM, and shows the same project model in two of them: SQLAlchemy and Prisma.

## // The problem: the gap between objects and tables

In code, data is objects: a `Grupo` with properties and methods. In the database, it is rows in tables. Translating from one to the other by hand, writing SQL as text inside the code, is laborious and error-prone, and every column name typed wrong only fails when the code runs.

## // What an ORM is

> **ORM: IN PLAIN WORDS**
> *Object-Relational Mapping* is a library that represents the database tables as classes in your code, the rows as objects, and translates operations on objects into SQL commands.

<div align="center">
<img src="./assets/orm-camadas.svg" alt="The layers between the code and the database: the ORM translates objects into SQL, which PostgreSQL runs" width="640">
</div>

The gains are real: the editor completes column names, typos show up earlier, and the relationships between tables become navigable properties (`ana.participacoes`). But the ORM does **not replace** SQL. It writes SQL for you, and understanding SQL, as you did in Modules 09 to 11, is what lets you check whether it wrote it right, and solve what it does not solve on its own.

## // The two tools

| | SQLAlchemy | Prisma |
|---|---|---|
| Language | Python | TypeScript and JavaScript |
| Where the model is described | Python classes (`models.py`) | Its own file (`schema.prisma`) |
| Migrations | Alembic | Prisma Migrate |
| Version used in this guide | SQLAlchemy 2.0 (tested with 2.0.54) | Prisma 7 |

> **MIND THE PRISMA VERSION**
> On the date this material was checked (October 7, 2026), Prisma's official status page says that **Prisma ORM 8 is still a release candidate**, with a release planned for October 2026, and that `npm install prisma` already installs the Prisma 8 command-line tool. Prisma 8's normal flow uses its own schema format (the *contract*) and does not have the `generate` and `migrate dev` commands used in this guide. Prisma 7 projects on PostgreSQL can, however, be imported into Prisma 8 through a migration command (`npx prisma@latest orm init --from-prisma7-schema prisma/schema.prisma`), which lets you run both versions side by side. That command renames the Prisma 7 tool to `prisma7` and its configuration to `prisma7.config.ts`. Prisma 7 keeps receiving fixes for 18 months after version 8 is released. That is why this guide uses **Prisma 7, with the version pinned** (`npm install --save-dev prisma@7`), to keep the examples stable. Check Prisma's status page before you start, because this may have changed.

## // SQLAlchemy 2.0

### > The model

Each table becomes a class, and each column becomes an attribute annotated with its type. Here is the `grupos` table, the same one from Module 09, in Python:

```python
class Grupo(Base):
    __tablename__ = "grupos"

    grupo_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome_grupo: Mapped[str] = mapped_column(Text)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.materia_id"))
    max_participantes: Mapped[int] = mapped_column(Integer, server_default=text("10"))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    materia: Mapped["Materia"] = relationship(back_populates="grupos")
    participacoes: Mapped[list["Participacao"]] = relationship(back_populates="grupo")
```

Compare it with the `create table` from Module 09: each line has its counterpart. `Mapped[str]` without `None` is equivalent to `not null`; `ForeignKey(...)` is equivalent to `references`; and `relationship(...)` is new, because it does not create any column: it only tells SQLAlchemy how to navigate between the tables.

The complete model, with the five tables, is in `example/sqlalchemy/models.py`.

### > Querying

SQLAlchemy 2.0 builds queries with the `select` function, and the result reads almost like SQL:

```python
consulta = (
    select(Grupo.nome_grupo, Grupo.max_participantes,
           func.count(Participacao.usuario_id).label("participantes"))
    .join(Participacao, Participacao.grupo_id == Grupo.grupo_id, isouter=True)
    .group_by(Grupo.grupo_id)
    .order_by(Grupo.nome_grupo)
)
```

This is the spots query from Module 11, with a left `join`, `count` and `group by`. Run against the seeded database, it returned:

```
Cálculo passo a passo      3/6
Estruturas na prática      2/5
Modelagem e SQL            6/8
Processos e memória        1/4
Redes na unha              2/6
Requisitos e histórias     2/5
```

The same numbers as the plain SQL query. To see the SQL the ORM wrote, the query `select(Grupo).where(Grupo.max_participantes >= 6).order_by(Grupo.nome_grupo)` becomes:

```
SELECT grupos.grupo_id, grupos.nome_grupo, grupos.materia_id, grupos.max_participantes, grupos.criado_em
FROM grupos
WHERE grupos.max_participantes >= %(max_participantes_1)s ORDER BY grupos.nome_grupo
```

`%(max_participantes_1)s` is a **parameter**: the value (6) travels separately from the SQL text, and that protects against a famous security flaw, SQL injection.

### > Navigating the relationships

A person's groups, which in Module 11 required a `join` chained across three tables, become navigation through properties:

```python
ana = session.scalars(select(Usuario).where(Usuario.email == "ana.martins@exemplo.com")).one()
for p in ana.participacoes:
    print(f"{p.grupo.nome_grupo} ({p.grupo.materia.nome}), since {p.entrou_em}")
```

```
Cálculo passo a passo (Cálculo I), since 2026-09-01
Estruturas na prática (Estrutura de Dados), since 2026-09-03
Modelagem e SQL (Banco de Dados), since 2026-09-05
```

### > Inserting, and undoing

```python
novo = Grupo(nome_grupo="Cálculo II na prática", materia=materia, max_participantes=5)
session.add(novo)
session.flush()          # sends the insert, and the database returns the generated id
session.rollback()       # undoes everything, the database stays as it was
```

The file `example/sqlalchemy/consultas.py` gathers the three examples and can be run with the `DATABASE_URL` variable pointing to the test database (in the format `postgresql+psycopg://user:password@host:5432/database`).

## // Prisma 7

> **WARNING: THIS PART WAS NOT RUN BY THE AUTHOR**
> The environment in which this material was produced could not download the Prisma engine, so nothing in this section was run, and `schema.prisma` was not validated. The content follows the official Prisma 7 documentation, checked on October 4, 2026. Run it on your machine and, if anything differs, the official documentation is the reference.

### > Installation and setup

```
npm install --save-dev prisma@7 dotenv typescript tsx
npm install @prisma/client@7 @prisma/adapter-pg pg
```

In Prisma 7, the database is configured in a `prisma.config.ts` file at the project root, and no longer inside `schema.prisma`:

```ts
import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: { url: process.env["DATABASE_URL"] },
});
```

Two differences compared to older tutorials: the database URL **moved out** of `schema.prisma`, and Prisma 7 requires a *driver adapter* when creating the client (for PostgreSQL, `@prisma/adapter-pg`).

### > The model

Prisma describes the tables in a file with its own syntax. Here is `Grupo`, the same table from the previous examples:

```
model Grupo {
  id               BigInt         @id @default(autoincrement()) @map("grupo_id")
  nome             String         @map("nome_grupo")
  materiaId        BigInt         @map("materia_id")
  maxParticipantes Int            @default(10) @map("max_participantes")
  criadoEm         DateTime       @default(now()) @map("criado_em") @db.Timestamptz(6)
  materia          Materia        @relation(fields: [materiaId], references: [id])
  participacoes    Participacao[]
  encontros        Encontro[]

  @@index([materiaId])
  @@map("grupos")
}
```

`@map` and `@@map` link the names in the code (`maxParticipantes`) to the database column names (`max_participantes`), and that is what lets you keep the naming conventions from Module 08. The complete model is in `example/prisma/prisma/schema.prisma`.

One detail to check on your machine: Prisma usually creates automatic identifiers with `@default(autoincrement())`, which may generate a `serial` column, not the `generated always as identity` from this guide's SQL script. The practical effect for the project is the same, but the generated structure is not identical, and you can compare it with `\d grupos` in `psql`.

### > Generating the client and querying

```
npx prisma generate
```

And, in the code, the client is created by passing the adapter:

```ts
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "./generated/prisma/client";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL! });
const prisma = new PrismaClient({ adapter });
```

The spots query, and a person's groups:

```ts
const grupos = await prisma.grupo.findMany({
  include: { materia: true, _count: { select: { participacoes: true } } },
  orderBy: { nome: "asc" },
});

const ana = await prisma.usuario.findUnique({
  where: { email: "ana.martins@exemplo.com" },
  include: { participacoes: { include: { grupo: { include: { materia: true } } } } },
});
```

`include` is the equivalent of `join`: it asks Prisma to bring, along with the object, the related records. The file `example/prisma/src/consultas.ts` gathers the examples.

## // The two side by side

| I want... | SQL (Module 11) | SQLAlchemy | Prisma |
|---|---|---|---|
| The groups with their subject | `join materias` | `.join(Materia)` or `grupo.materia` | `include: { materia: true }` |
| Count participants | `count(...)` with `group by` | `func.count(...)` | `_count: { select: { participacoes: true } }` |
| Filter | `where` | `.where(...)` | `where: { ... }` |
| Sort | `order by` | `.order_by(...)` | `orderBy: { ... }` |
| A person's groups | Chained `join` | `ana.participacoes` | Nested `include` |

## // When to use an ORM, and when to write SQL

An ORM shines in an application's day-to-day: simple read, create and update operations, with type safety and navigable relationships. But there are cases where direct SQL is better: reports with complicated aggregations, queries that need very specific performance, or PostgreSQL-specific features the ORM does not expose. The two main ORMs in this module let you run plain SQL when needed, and your knowledge from Modules 09 to 13 is valuable in both worlds.

## // Good example × bad example

**Bad example**: building SQL by joining text with the person's input:

```python
email = input("Email: ")
session.execute(text(f"select * from usuarios where email = '{email}'"))
```

If someone types `' or '1'='1`, the condition becomes always true and the query returns **all** users. That is SQL injection.

**Good example**: let the ORM (or the parameter) take care of the value:

```python
session.scalars(select(Usuario).where(Usuario.email == email))
```

The value travels as a parameter, separate from the SQL text, and is never interpreted as a command.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Forgetting `relationship` and trying to navigate `ana.participacoes` | The foreign key alone does not create the property | Declare the `relationship` on both sides of the link |
| Thinking the ORM means you do not need to know SQL | It hides SQL, but does not eliminate it | Look at the generated SQL and check it with `explain analyze` when something is slow |
| `npm install prisma` and the `generate` and `migrate dev` commands disappear | Today that installs the Prisma 8 tool | Install `prisma@7` and pin the version in `package.json` |
| Building SQL with concatenated text | It is the shortest path | Use parameters or the ORM's methods |
| Running the ORM against the deliverable's database with `migrate dev` | Prisma may propose resetting the database | Use a separate test database |

## // Guided practice

1. In `example/sqlalchemy/`, point the `DATABASE_URL` variable to your test database and run `consultas.py`.
2. Compare the numbers in the result with the spots query from Module 11.
3. Write, in `consultas.py` itself, an ORM query that returns a group's meetings (hint: use the `grupo.encontros` relationship).
4. If you are going to use Prisma, set up `.env`, run `npx prisma generate` and run `src/consultas.ts`.

## // Practice on your own

> **CHALLENGE**
> Pick one of the queries from Module 11 that you have not yet rewritten with an ORM (for example, "the subjects with their total memberships") and rewrite it in SQLAlchemy or in Prisma. Then check the result against the plain SQL one.

## // Applying it to the week's project

1. Record in `docs/arquitetura.md` which ORM you chose and why, in two or three sentences.
2. Add the model (`models.py` or `schema.prisma`) and a `.env.example` file without the password to the repository.
3. Commit: `git commit -m "Add the project's ORM model"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> You read on a forum that "with an ORM you don't even need to learn SQL". Which two arguments from this module show the problem with that idea?

Answer: first, the ORM just writes the SQL for you, and to know whether it wrote an efficient query (or to diagnose a slow one) you need to read the generated SQL and the execution plan, as in Module 13. Second, there are cases, like complex reports or PostgreSQL-specific features, in which the right path is to write SQL directly. The ORM saves work day to day, but it depends on whoever uses it understanding what happens underneath.

## // Module summary

- [ ] I know what an ORM is and the problem it solves.
- [ ] I can describe a table as a class in SQLAlchemy and as a model in Prisma.
- [ ] I can write a query with `join`, aggregation and filter in at least one of the two.
- [ ] I know Prisma 8 is still a release candidate and that this guide uses Prisma 7 with the version pinned.
- [ ] I know why the ORM does not replace SQL.

---

**Next step:** `entregavel.en.md`, the final review of everything Week 04 asked for.

`Study Material // Coffee & Code`
