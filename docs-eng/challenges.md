# Challenges, Week 04

🇧🇷 [Português](../docs/desafios.md) · 🇺🇸 English

Optional challenges, organized by the week's modules. None of them is required for the basic submission; see `deliverable.md` for what is required. Use these challenges if you finished the main modules and want to go deeper, or if you want to make the database more robust.

---

## // Entities, relationships and ERD (Modules 03 to 05)

**If you are just starting**
- Add a new entity to the ERD, `avaliacoes` (ratings), in which a person gives a score from 1 to 5 to a group they take part in. Decide the cardinality, the keys and whether it needs an associative table.

**If you already have experience**
- Look up the recursive relationship (a table that points to itself) and propose a case in the project, like "child" groups of a larger group.
- Look up the difference between the conceptual, logical and physical levels of an ERD and identify which level each of this week's diagrams is at.

---

## // Normalization (Modules 06 and 07)

**If you are just starting**
- Take a real spreadsheet of yours (expenses, studies, a collection) and apply 1NF, 2NF and 3NF, writing down the resulting tables.

**If you already have experience**
- Look up Boyce-Codd Normal Form (BCNF) and find a case where 3NF is not enough.
- Look up conscious denormalization and write an example, in the project, in which it would be worth duplicating data on purpose, justifying it with a measurement.

---

## // Types, keys and SQL (Modules 08 to 11)

**If you are just starting**
- Write a query that shows, for each person, how many groups they take part in, including people who are in none.
- Write a query that lists the groups that still have spots, sorted from the one with the most spots to the one with the fewest.

**If you already have experience**
- Look up `window functions` (like `row_number()` and `rank()`) and use one to number each subject's groups by participant count.
- Look up `CTE` (the `with` clause) and rewrite the remaining-spots query in a more readable way.
- Look up `unique` across more than one column and create a constraint that prevents two meetings of the same group on the same day and time.

---

## // Indexes, migrations and ORMs (Modules 13 to 15)

**If you are just starting**
- Take two queries from Module 11 and run `explain analyze` on each one, writing down the scan type the database chose.

**If you already have experience**
- Look up partial indexes (`create index ... where ...`) and create one for a project query that only looks at part of the rows.
- Look up `pg_stat_statements` and find out how to identify, in a real database, which queries consume the most time.
- Rewrite all the queries from Module 11 in SQLAlchemy or in Prisma and compare the generated SQL with the SQL you wrote by hand.

---

## // General challenge (everyone)

Write, in a `docs/decisoes.md` file, the five main modeling decisions of your project, each one in two sentences: what you decided and why. Examples: why `materias` is a separate table, why `participantes` is not a column, why the key of `participacoes` is composite. If you can justify each one without looking at the material, your model is at a good level.
