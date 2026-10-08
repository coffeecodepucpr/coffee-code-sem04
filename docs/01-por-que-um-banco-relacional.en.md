# Module 01, Why a Relational Database

🇧🇷 [Português](./01-por-que-um-banco-relacional.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

In Module 00 you saw the problem: the Study Group Finder data lives in arrays and disappears when the page reloads. This module calmly explains what a database solves that an array does not, and introduces the minimum vocabulary the rest of the week will use.

## // The problem: the array belongs to the browser

When `script.js` runs, the `gruposMock` array is created in the browser's memory, and it only exists there. That creates three concrete limitations:

- **It does not persist:** reloading the page, closing the tab or turning off the computer erases everything.
- **It is not shared:** if you open the Dashboard on two computers, each one has its own copy of the array. A change made on one does not show up on the other.
- **It does not protect itself:** nothing stops the array from getting two groups with the same id, or a group pointing to a subject that does not exist.

A database solves all three: the data is kept in a central place, which keeps existing even with everything turned off, and which can enforce rules about what is accepted.

## // Database, DBMS and SQL: three names that get mixed up

> **DATABASE: IN PLAIN WORDS**
> It is an organized set of data stored permanently. In a relational database, that data lives in tables linked to each other.

Three names show up together all the time, and it is common to mix them up:

| Name | What it is | Example this week |
|---|---|---|
| DBMS | The program that stores the data and answers requests | PostgreSQL |
| SQL | The language used to talk to the DBMS | `SELECT * FROM grupos` |
| Platform | A service that hosts the DBMS and offers tools around it | Supabase |

In one sentence: you use the **SQL language** to ask things of **PostgreSQL**, which is hosted on the **Supabase platform**.

## // The minimum vocabulary of a relational database

Almost everything you already know from arrays and objects has an equivalent in a database:

| In JavaScript (Week 03) | In the relational database |
|---|---|
| An array of objects (`gruposMock`) | A **table** (`grupos`) |
| An object inside the array | A **row** (also called a record) |
| A property of the object (`materia`) | A **column** (also called a field) |
| The `id` property | The **primary key** |

The primary key is the column whose value uniquely identifies each row. In `gruposMock`, the `id` already played that role, even without that name.

## // What "relational" means

> **RELATIONAL DATABASE: IN PLAIN WORDS**
> It is a database that stores data in tables and lets you link one table to another through keys, so that each piece of information exists in a single place.

In `gruposMock`, the subject name ("Cálculo I") is written inside each group. If there are three Cálculo I groups, the text is repeated three times. In a relational database, the subject exists in a single table, and each group just points to it through a key. This link between tables is what gives it the name "relational", and it is what this week's modeling will teach you to design.

## // Good example × bad example

**Bad example**: storing a list inside a single field:

| usuario_id | nome_usuario | grupos |
|---|---|---|
| 1 | Ana Martins | Cálculo I, Estrutura de Dados, Banco de Dados |

To find out who takes part in "Banco de Dados", you would have to search for a piece of text inside every field. To remove Ana from a group, you would have to rewrite the whole list.

**Good example**: one row for each link between a person and a group:

| usuario_id | grupo_id |
|---|---|
| 1 | 1 |
| 1 | 2 |
| 1 | 3 |

Now each fact takes one row. Finding out who is in a group, or removing a membership, is a simple and safe operation. This is the format the rest of the week will build.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Saying "the database is SQL" | SQL, PostgreSQL and Supabase always show up together | Remember the three layers: language (SQL), program (PostgreSQL) and platform (Supabase) |
| Treating the database like a huge spreadsheet | Tables look like spreadsheets | In a database, the links between tables and the validation rules are the central point |
| Storing lists inside a text field | It is the fastest way to copy what the array already did | Use one row per item, in its own table |
| Thinking the database makes the page more "complete" by itself | Database and page are separate things | The database only stores data; connecting the page to it is a separate step that comes later |

## // Guided practice

1. Open the `script.js` from the Week 03 example and find the `gruposMock` array and the `usuarioMock` object.
2. On paper or in a text editor, write `gruposMock` as a table: one column for each property, one row for each group.
3. Mark which column would be the primary key.
4. Circle the values that repeat from one row to another.

## // Practice on your own

> **CHALLENGE**
> Look at the `usuarioMock` object from Week 03, which has the properties `nome`, `email` and `materias` (an array of ids). Which of these properties does not fit in a single column of a table? Write an idea of how to store that information using rows.

## // Applying it to the week's project

1. Create, in your repository, the file `docs/arquitetura.md` (if it does not exist yet).
2. Write a section "Data that needs to persist", listing, as bullet points, everything your project currently keeps in arrays that should survive a page reload.
3. Commit: `git commit -m "List the data that needs to persist"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> You open the Dashboard on your computer and, at the same moment, the same page on another computer. Both show the same groups, but if you leave a group in the Profile on the first one, the second keeps showing the membership. Why?

Answer: because each browser runs its own `script.js` and creates its own `gruposMock` array in memory. There is no central place that both of them query. For a change made on one computer to show up on the other, the data needs to live in a shared and permanent place, which is exactly the role of the database.

## // Module summary

- [ ] I can explain three limitations of keeping data in an array in the browser.
- [ ] I can tell DBMS, SQL and platform apart (PostgreSQL, SQL and Supabase).
- [ ] I can relate array, object and property to table, row and column.
- [ ] I know what a primary key is.
- [ ] I can explain what "relational" means and why it avoids repetition.

---

**Next module:** `02-postgresql-e-supabase.en.md`, with the vocabulary ready, it is time to create your database and run the first query.

`Study Material // Coffee & Code`
