# Module 02, PostgreSQL and Supabase

🇧🇷 [Português](../docs/02-postgresql-e-supabase.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

In Module 01 you saw the difference between DBMS, SQL and platform. Now you will get your hands on them: create your project on Supabase, get to know the dashboard and run the first query. Designing the database comes in the next modules, but it is better to have the environment working already, so that nothing is new when it is time to create the tables.

## // What Supabase provides

> **SUPABASE: IN PLAIN WORDS**
> It is a platform that hosts a ready-to-use PostgreSQL database in the cloud and offers, around it, a visual dashboard and an API generated automatically from your tables.

<div align="center">
<img src="../docs/assets/supabase-visao-geral.svg" alt="A Supabase project: the dashboard and the API accessing the same PostgreSQL database" width="640">
</div>

Each Supabase project has its own PostgreSQL. The dashboard is where you look at and edit data with clicks; the API is what, later on, lets an application talk to the database. This week you only use the dashboard and SQL.

## // Creating your project

> **ABOUT BUTTON NAMES**
> Platforms change their interface often. The names below were correct on the date this material was checked (October 4, 2026). If something is somewhere else, the path stays the same: create an account, create a project, set the database password, wait for it to be created.

1. Go to `supabase.com` and create a free account.
2. In the dashboard, click **New project** and choose the organization (one is created along with the account).
3. Fill in the project name (for example, `buscador-de-grupos`).
4. Set the **database password** and keep it somewhere safe. If you forget it, you can reset it in the project's database settings.
5. Choose the region closest to you and the **Free** plan.
6. Click to create and wait. Creation usually takes one or two minutes.

## // Getting to know the dashboard

In the project's side menu, two areas are the most used this week:

| Area | What it is for |
|---|---|
| Table Editor | Viewing, creating and editing tables and rows visually, like in a spreadsheet |
| SQL Editor | Writing and running SQL commands, and saving the queries you want to reuse |

The rule of this guide is: **design on paper, create with SQL, check in the Table Editor.** The Table Editor is great for looking at and fixing data, but an SQL script can be versioned in Git, repeated and reviewed, and a sequence of clicks cannot.

## // The first query

Open the **SQL Editor**, create a new query and run:

```sql
select version();
select now();
```

The first returns the PostgreSQL version your project uses; the second, the server's date and time. If both answered, your database is alive.

## // A test table, to get a feel for the tool

```sql
create table teste (
  id    integer,
  texto text
);

insert into teste (id, texto) values (1, 'hello, database');

select * from teste;

drop table teste;
```

What each command did: created a table, stored a row, read the whole table and, finally, deleted the table. Modules 09 and 10 explain each of these commands in detail. For now, what matters is seeing that the flow works end to end, and deleting the test table at the end, so you do not leave junk in the database.

## // The free plan and the inactivity pause

> **WARNING: FREE PROJECTS ARE PAUSED**
> On the free plan, a project that stays a week without activity is paused. The data is kept, but the database stays offline until someone reactivates it from the dashboard. The free plan limits include 500 MB of database space per project. These numbers were checked on October 4, 2026, and it is worth confirming them on Supabase's pricing page before relying on them.

In practice, this means one simple precaution: **before submitting your work, go to the dashboard and check that the project is active.** If it is paused, the dashboard warns you and offers the option to restore it.

## // Two security precautions from day one

> **BE CAREFUL WITH THE PASSWORD AND WITH RLS**
> The database password never goes into the repository. As for the API that Supabase generates automatically (the Data API), access to a table depends on **two layers**: the permissions (*grants*) given to the API roles, such as `anon` and `authenticated`, and *Row Level Security* (RLS), which decides which rows those roles can see. In projects created since May 30, 2026, new tables in the `public` schema do not receive those permissions automatically, and Supabase announced that the same behavior applies to older projects starting October 30, 2026 (information checked on October 7, 2026). Even so, for safety, enable RLS on every table that may be exposed: a table with permissions and without RLS is open to the API roles. With RLS on and no policy created, regular API requests see no rows at all, and this week that is exactly what we want. Real access rules, with permissions and policies, come later, when there is authentication.

## // Good example × bad example

**Bad example**: the database password written inside a file that goes into Git:

```
DATABASE_URL=postgresql://postgres:my-password@db.example.supabase.co:5432/postgres
```

In a versioned file, anyone who sees the repository sees the password, and it stays in the history forever.

**Good example**: the password in a `.env` file that Git ignores:

```
# .gitignore file
.env
```

This way the `.env` exists on your computer, but never goes into a commit.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Forgetting the database password | It is only shown when the project is created | Reset it in the project's database settings and keep it in a password manager |
| The project "disappeared" after a few days | Free projects are paused after a week without use | Go to the dashboard and restore the project |
| Creating tables and forgetting RLS | The database accepts the table without it | Run `alter table ... enable row level security` right after each `create table` |
| Running a command without knowing which project it is on | Accounts can have more than one project | Check the project name at the top of the dashboard before running |

## // Guided practice

1. Create your account and the project, following the steps in this section.
2. In the SQL Editor, run `select version();` and write down the PostgreSQL version.
3. Run the whole `teste` table block, command by command.
4. Open the Table Editor between the `insert` and the `drop table` and check that the table and the row show up there.
5. Confirm, at the end, that the `teste` table was deleted.

## // Practice on your own

> **CHALLENGE**
> Run `select current_database(), current_user;` and find out the database name and the role the SQL Editor is connected with. Then, look up what a "role" is in PostgreSQL and write one sentence explaining it.

## // Applying it to the week's project

1. In your `docs/arquitetura.md`, record the project name on Supabase and the chosen region. **Do not record the password.**
2. Add `.env` to your `.gitignore`, if it is not there yet.
3. Commit: `git commit -m "Document the Supabase project and protect .env"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Your free Supabase project went ten days without anyone accessing it. When you come back, the database does not respond. What probably happened, and what do you need to do?

Answer: the project was paused due to inactivity, which is the free plan's behavior after a week without use. The data is still stored; just go to the dashboard and restore the project. That is why it is worth checking that it is active before any submission.

## // Module summary

- [ ] I have a Supabase project created, with the password kept somewhere safe.
- [ ] I know where the Table Editor and the SQL Editor are.
- [ ] I ran the first query and the test table successfully.
- [ ] I know Free projects are paused after a week without use, and that I need to check this before submitting.
- [ ] I know why the password does not go into the repository and what RLS does.

---

**Next module:** `03-entities-and-attributes.md`, the environment is ready. Time to find out which tables the project really needs.

`Study Material // Coffee & Code`
