# Module 12, Guided Project: The Study Group Finder Database

🇧🇷 [Português](../docs/12-projeto-guiado.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // What this module is for

No new concept appears here. This module brings together, in order, everything Modules 01 to 11 taught, and ends with the week's deliverable: a relational database on Supabase, with the tables created and data inside.

## // Step 1, Confirm the Supabase project (Module 02)

Go to the dashboard and confirm three things: the project is **active** (not paused), the database password is kept somewhere safe, and the `.env` file is listed in the repository's `.gitignore`.

## // Step 2, Review the design (Modules 03 to 08)

Before creating anything, check your project's ERD and data dictionary:

- [ ] Each entity became a table, and the N:N was solved with an associative table.
- [ ] Every table has a primary key, and every 1:N relationship has the foreign key on the "many" side.
- [ ] No column stores a list, and no derived data (like the participant count) became a column.
- [ ] The tables follow 2NF and 3NF.
- [ ] All columns have a defined type, and the constraints (`not null`, `unique`, `check`) are written down.

## // Step 3, Create the tables (Module 09)

Run your `sql/01-schema.sql` in the SQL Editor and check, in the Table Editor, that the five tables exist and that RLS is on for all of them.

## // Step 4, Insert the data (Module 10)

Run your `sql/02-seed.sql`. Then check that every table received the expected rows with this query, which gathers the counts in a single result:

```sql
select 'materias' as tabela, count(*) as linhas from materias
union all select 'usuarios',      count(*) from usuarios
union all select 'grupos',        count(*) from grupos
union all select 'participacoes', count(*) from participacoes
union all select 'encontros',     count(*) from encontros;
```

With this guide's example data, the expected result is 6 subjects, 8 users, 6 groups, 16 memberships and 7 meetings. `union all` is a new command that simply stacks the results of several queries, and here it only serves to check everything at once.

## // Step 5, Query (Module 11)

Save in `sql/03-consultas.sql` the queries your project would need: the groups with remaining spots (what the Dashboard showed) and a person's groups (what the Profile showed). Run each one and check that the result makes sense.

## // Step 6, Document

In `docs/arquitetura.md`, gather: the ERD (image), the data dictionary, the order in which the scripts must be run and the project name on Supabase. **Do not include the password or the connection URL with the password.**

## // Step 7, Final check and commit

1. Run `git status` and confirm that `.env` does **not** show up in the list of new files.
2. Confirm that the `sql/` folder has the three scripts and that the `docs/` folder has the ERD and the architecture document.
3. Commit: `git commit -m "Finish the project's relational database"`.

## // Extra step for the veteran track

If you followed Modules 13 to 15, the database can now take three more things: the indexes from `04-indices.sql` (Module 13), the migration history (Module 14) and the equivalent model in Prisma or SQLAlchemy (Module 15). They are optional and come **after** the database is working.

## // Closing checklist

- [ ] The Supabase project is active, and the password is out of the repository.
- [ ] The five tables exist, with types and constraints matching the data dictionary.
- [ ] RLS is on for all tables.
- [ ] The tables contain the initial data, and the counts match what is expected.
- [ ] The queries with `join`, `group by` and `left join` work.
- [ ] The ERD and the data dictionary are in the repository.
- [ ] The SQL scripts are versioned, in execution order.

## // Common mistakes when putting it all together

| Mistake | Why it happens | How to fix it |
|---|---|---|
| `relation "..." does not exist` when running the seed | The schema was not created first, or the table was created in another project | Check the project name at the top of the dashboard and run the schema first |
| `duplicate key value violates unique constraint` when running the seed again | The rows already exist, and the constraints are protecting the database | This is the expected behavior. To start over from scratch, delete the tables in reverse order and recreate them |
| The tables show up, but the Table Editor shows 0 rows | The seed failed halfway, or ran in another query | Run the counts from Step 4 and reread the SQL Editor error message |
| The project "disappeared" on submission day | Inactivity pause on the free plan | Go to the dashboard and restore the project before submitting |
| The password ended up in a commit | `.env` was not in `.gitignore` | Change the database password in the project settings, and add `.env` to `.gitignore` |

## // Applying it to the week's project

This is the application: there is no separate activity. At the end of this module, your database should pass the checklist in `deliverable.md`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> You run the seed twice in a row and the second run ends with a duplicate key error. Does that mean something is broken?

Answer: no, it means the constraints are working. The `nome` column in `materias` and the `email` column in `usuarios` are `unique`, so the database refuses the same data the second time and prevents your database from having duplicate rows. To redo it from scratch, delete the tables in the reverse order of creation (encontros, participacoes, grupos, usuarios, materias) and run the schema and the seed again.

## // Module summary

- [ ] I can repeat, from memory, the sequence: design, normalize, create, populate, query and document.
- [ ] My database is active on Supabase, with tables and data.
- [ ] The closing checklist is complete.

---

**Next module:** `13-indexes-and-performance.md` for the veteran track, or `deliverable.md` for the final review if you follow the main track.

`Study Material // Coffee & Code`
