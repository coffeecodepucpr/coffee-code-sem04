# Module 00, Start Here

🇧🇷 [Português](../docs/00-comece-aqui.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Welcome to Week 04

If you followed Week 03, the Study Group Finder screens already react, validate and render lists. Now try this: open the Profile, leave a group and then reload the page. The group is back. Nothing the person did was saved.

This is not a flaw in what you built, and it is exactly where Week 03 said it would stop. The data lives in arrays inside `script.js`, in the browser's memory, and disappears every time the page reloads. To truly last, it needs to live in a database.

## // What changes from now on

<div align="center">
<img src="../docs/assets/mock-para-tabela.svg" alt="An array of JavaScript objects becoming the rows of a database table" width="640">
</div>

Each object in the array becomes a row in a table, and each property becomes a column. But that "becomes" hides the hard part: which tables should exist, how they connect to each other, and how to avoid storing the same information in two places. That is what a week of data modeling is about.

## // What you will build by the end of the week

- An ERD (entity-relationship diagram) of the Study Group Finder, showing the tables and how they relate to each other.
- The model reviewed against the normalization rules (1NF, 2NF and 3NF), so that no information is repeated.
- SQL scripts that create the tables and insert the data that used to live in `gruposMock`.
- A PostgreSQL database hosted on Supabase, with the tables created and data inside, visible in the dashboard.

## // What is still left out

> **NOT THIS WEEK YET**
> The web page keeps using the mock data from Week 03: connecting the front end to the database comes later. Real login and per-user access rules (the database security policies) are not included either. This week is about designing and creating the database, not about consuming it from an application.

## // Why a relational database, and why PostgreSQL

> **RELATIONAL DATABASE: IN PLAIN WORDS**
> It is a database that stores data in tables (rows and columns) and lets you link one table to another through keys, so that each piece of information exists in a single place.

**PostgreSQL** is an open-source relational database, widely used in the industry. **Supabase** is a platform that gives you a ready-to-use PostgreSQL in the cloud, with a visual dashboard to create and query tables, so you do not need to install anything on your computer.

> **A WARNING ABOUT THE FREE PLAN**
> On Supabase's free plan, a project with no activity for a week is paused, and someone has to reactivate it manually in the dashboard. The data is not lost, but the database stays offline until it is reactivated. If you are going to submit your work after a few idle days, open the project first and confirm it is active. Module 02 shows how.

## // The two tracks

**If you are just starting**, you have never written a line of SQL or drawn a database diagram. The main track assumes that: Modules 01 to 12 introduce each concept before it is needed, focusing on drawing the ERD and writing the SQL scripts for the tables.

**If you already have experience**, you have worked with databases before. Modules 13 to 15, clearly marked as the veteran track and placed after the essential content, cover indexes, migrations and ORMs (Prisma and SQLAlchemy).

You model the data of the Study Group Finder, the same project as in previous weeks. What changes between the two tracks is the depth.

## // Week 04 map

| Module | Content | You will be able to |
|---|---|---|
| 01 | Why a relational database | Explain what a database solves that an array does not |
| 02 | PostgreSQL and Supabase | Create the project and run the first query |
| 03 | Entities and attributes | Find out which tables the project needs |
| 04 | Relationships and cardinality | Connect entities with 1:1, 1:N and N:N |
| 05 | The ER diagram | Draw the complete model of the project |
| 06 | Normalization: anomalies and 1NF | Recognize the problems of a single table |
| 07 | Normalization: 2NF and 3NF | Remove repetition by splitting tables |
| 08 | Data types and keys | Choose each column's type and the keys |
| 09 | SQL: creating the tables | Turn the ERD into `CREATE TABLE` scripts |
| 10 | SQL: inserting and querying | Store and fetch data with `INSERT` and `SELECT` |
| 11 | SQL: JOIN and aggregations | Combine tables and count results |
| 12 | Guided project | Have the database active on Supabase, with data |
| 13 | Indexes and performance (veteran) | Speed up queries and understand the execution plan |
| 14 | Migrations (veteran) | Version changes to the database schema |
| 15 | ORMs: Prisma and SQLAlchemy (veteran) | Map tables to code objects |

Each module is a standalone file, but they were written to be read in this order: the design (ERD and normalization) comes before SQL, as in a real project, because creating tables without designing them first usually ends with tables being redone later.

---

**Next module:** `01-why-a-relational-database.md`, before drawing any table, understand what a database solves that an array does not.

`Study Material // Coffee & Code`
