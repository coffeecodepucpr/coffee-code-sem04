# Deliverable, Week 04

🇧🇷 [Português](./entregavel.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

Use this file as the final checklist before considering Week 04 done. It gathers what is **required**; the extra challenges in `desafios.en.md` and Modules 13 to 15 of the veteran track are optional.

## // What you should have in hand now

If you followed the modules in order, your repository should now have, in addition to everything from previous weeks: the project's ERD, the data dictionary, the versioned SQL scripts and an active PostgreSQL database on Supabase, with the tables created and data inside.

## // Deliverable checklist

### > Active database on Supabase

- [ ] The Supabase project is **active** (not paused) on submission day.
- [ ] The project's five tables exist (or the equivalent ones, if your domain is different).
- [ ] RLS is on for all tables.
- [ ] The tables contain initial data, and the counts match your data script.

### > Modeling

- [ ] The ERD is in the repository (for example, in `docs/der.png`), with entities, keys and cardinality at the ends.
- [ ] Every N:N is solved with an associative table.
- [ ] The model follows 1NF, 2NF and 3NF, and no calculable data (like the participant count) became a column.
- [ ] The data dictionary describes the type and constraints of each column.

### > SQL

- [ ] The `sql/` folder has the table creation script and the data script, in execution order.
- [ ] Every foreign key has `references`, and each one has its `on delete` decided.
- [ ] There is at least one query with `join`, one with `group by` and one with `left join`.

### > Security and organization

- [ ] The database password is **not** in any versioned file, and `.env` is in `.gitignore`.
- [ ] `docs/arquitetura.md` describes the model, the order in which the scripts run and the project name on Supabase.

## // What is NOT expected this week

- You are not expected to connect the web page to the database: the front end keeps using mock data.
- You are not expected to have real login or per-user access policies (RLS rules, beyond turning it on).
- You are not expected to have indexes, migrations or an ORM: that is the veteran track.
- You are not expected to have a lot of data in the database: a few dozen rows are enough.

> **A CORRECT MODEL IS WORTH MORE THAN A BIG DATABASE**
> An ERD that solves the N:N well and a model without repetition, with few rows, are worth more in this evaluation than a database full of data in a single badly designed table. What is being evaluated this week is the quality of the design.

## // How to review before submitting

> **THE MOST IMPORTANT TEST THIS WEEK**
> Go to the Supabase dashboard and confirm, with your own eyes, that the project is active and that the tables show up with data in the Table Editor. Then, on an empty test database, run your scripts from scratch, in order, and check that they all pass without errors.

If both tests pass, your database is reproducible and your submission is on the right track. If one of them fails, the error message almost always points to the exact table or line: go back to the corresponding module.

## // Where to ask questions

The weekly Coffee & Code meetings exist for this. "My foreign key gives an error when inserting, I already checked the order and the type" is much faster to solve than "my database doesn't work".

If you want to go deeper than what was asked, see `desafios.en.md` and the veteran track, in Modules 13 to 15.

## // What comes in Week 05

Week 04 ends with a well-designed database, active and with data, but still isolated: the Week 03 web page keeps using mock data. That bridge, connecting the interface to the database, is what the club's next weeks start to build.

Good work so far.

`Study Material // Coffee & Code`
