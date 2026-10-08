# Module 11, SQL: JOIN and Aggregations

🇧🇷 [Português](./11-sql-join-e-agregacoes.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

Normalizing spread the data across five tables. That removes repetition, but creates a new problem: almost every interesting question needs data from more than one table. `join` is the command that puts the tables back together, and aggregations are what calculate numbers like the participant count, the field that disappeared from `gruposMock`.

## // The problem: the Dashboard needs data from several places

To show a Dashboard card, Week 03 used an object with everything together: group name, subject and participant count. In the database, the group name is in `grupos`, the subject name is in `materias`, and the participant count does not even exist as data: it has to be calculated from `participacoes`. Bringing that together is the job of `join` and `count`.

## // `join`: combining tables by key

> **JOIN: IN PLAIN WORDS**
> It is the operation that combines rows from two tables when a condition is true. Almost always, the condition compares a foreign key with the primary key it points to.

<div align="center">
<img src="./assets/join-visual.svg" alt="The grupos and materias tables linked by materia_id, producing a result table with the group name and the subject name" width="640">
</div>

```sql
select g.nome_grupo, m.nome as materia, m.codigo
from grupos g
join materias m on m.materia_id = g.materia_id
order by m.nome;
```

```
       nome_grupo       |        materia         | codigo
------------------------+------------------------+--------
 Modelagem e SQL        | Banco de Dados         | INF301
 Cálculo passo a passo  | Cálculo I              | MAT101
 Requisitos e histórias | Engenharia de Software | INF305
 Estruturas na prática  | Estrutura de Dados     | INF201
 Redes na unha          | Redes de Computadores  | INF310
 Processos e memória    | Sistemas Operacionais  | INF315
```

Three details of the syntax:

- `join materias m on ...`: joins the `materias` table, which is now called `m` (an **alias**, to type less).
- `on m.materia_id = g.materia_id`: the condition that links the two tables, the primary key on one side and the foreign key on the other.
- `m.nome as materia`: `as` gives the column a new name in the result.

## // `join` and `left join`: what happens without a match

A regular `join` only returns the rows that have a match on both sides. `left join` keeps **all the rows from the left table**, even when there is no match, and fills whatever is missing with empty values.

Imagine there is a subject "Cálculo II", still with no group. Counting groups per subject:

```sql
-- join: the subject with no group disappears from the result
select m.nome as materia, count(g.grupo_id) as grupos
from materias m
join grupos g on g.materia_id = m.materia_id
group by m.nome order by m.nome;
```

```sql
-- left join: the subject with no group shows up, with 0
select m.nome as materia, count(g.grupo_id) as grupos
from materias m
left join grupos g on g.materia_id = m.materia_id
group by m.nome order by m.nome;
```

In the second result, there is one more row: `Cálculo II` with `0` groups. If the question is "how many groups does each subject have, including those with none", `left join` is the right one.

## // Aggregations: calculating numbers

> **AGGREGATION: IN PLAIN WORDS**
> It is a calculation that summarizes several rows into a single value, like counting, adding up or finding the largest. The most used functions are `count`, `sum`, `avg`, `min` and `max`.

```sql
select count(*) as total, min(entrou_em) as primeira, max(entrou_em) as ultima
from participacoes;
```

```
 total |  primeira  |   ultima
-------+------------+------------
    16 | 2026-09-01 | 2026-09-13
```

### > `group by`: one result per group

To calculate a value for each group, instead of just one for the whole table, use `group by`. This is the query that brings back the `participantes` field that disappeared from the mock:

```sql
select g.grupo_id, g.nome_grupo, count(p.usuario_id) as participantes
from grupos g
left join participacoes p on p.grupo_id = g.grupo_id
group by g.grupo_id, g.nome_grupo
order by participantes desc, g.nome_grupo;
```

```
 grupo_id |       nome_grupo       | participantes
----------+------------------------+---------------
        3 | Modelagem e SQL        |             6
        1 | Cálculo passo a passo  |             3
        2 | Estruturas na prática  |             2
        5 | Redes na unha          |             2
        4 | Requisitos e histórias |             2
        6 | Processos e memória    |             1
```

The `group by` rule: every column in the `select` that is not inside an aggregate function must also appear in the `group by`.

### > `having`: filtering after aggregating

`where` filters rows **before** grouping. To filter by the result of the calculation, like "only groups with 3 or more participants", use `having`:

```sql
select g.nome_grupo, count(p.usuario_id) as participantes
from grupos g
left join participacoes p on p.grupo_id = g.grupo_id
group by g.grupo_id, g.nome_grupo
having count(p.usuario_id) >= 3;
```

## // Remaining spots: the calculation the Dashboard needs

Putting it all together, this query returns, for each group, the limit, how many take part and how many spots are left:

```sql
select g.nome_grupo,
       g.max_participantes,
       count(p.usuario_id) as participantes,
       g.max_participantes - count(p.usuario_id) as vagas
from grupos g
left join participacoes p on p.grupo_id = g.grupo_id
group by g.grupo_id, g.nome_grupo, g.max_participantes
order by vagas desc, g.nome_grupo;
```

```
       nome_grupo       | max_participantes | participantes | vagas
------------------------+-------------------+---------------+-------
 Redes na unha          |                 6 |             2 |     4
 Cálculo passo a passo  |                 6 |             3 |     3
 Estruturas na prática  |                 5 |             2 |     3
 Processos e memória    |                 4 |             1 |     3
 Requisitos e histórias |                 5 |             2 |     3
 Modelagem e SQL        |                 8 |             6 |     2
```

## // The Profile in SQL: three tables together

The Week 03 Profile screen showed a person's groups, with each one's subject. In SQL, that is a chained `join`, going through the four tables:

```sql
select u.nome_usuario, g.nome_grupo, m.nome as materia, p.entrou_em
from usuarios u
join participacoes p on p.usuario_id = u.usuario_id
join grupos g        on g.grupo_id   = p.grupo_id
join materias m      on m.materia_id = g.materia_id
where u.email = 'ana.martins@exemplo.com'
order by p.entrou_em;
```

```
 nome_usuario |      nome_grupo       |      materia       | entrou_em
--------------+-----------------------+--------------------+------------
 Ana Martins  | Cálculo passo a passo | Cálculo I          | 2026-09-01
 Ana Martins  | Estruturas na prática | Estrutura de Dados | 2026-09-03
 Ana Martins  | Modelagem e SQL       | Banco de Dados     | 2026-09-05
```

## // What `map`, `reduce` and friends become in SQL

| JavaScript (Week 03) | SQL |
|---|---|
| `grupos.map(g => g.materia)` (pick fields) | `select coluna1, coluna2` |
| Looking up each group's subject in another array | `join ... on ...` |
| `lista.length` or `reduce` to count | `count(...)` |
| Adding up or finding the largest value | `sum(...)`, `max(...)` |
| Grouping items by a property | `group by ...` |

## // Good example × bad example

**Bad example**: `count(*)` together with `left join`:

```sql
select g.nome_grupo, count(*) as participantes
from grupos g
left join participacoes p on p.grupo_id = g.grupo_id
group by g.nome_grupo;
```

For a group with no participants, `left join` returns **one** row (with `p` empty), and `count(*)` counts that row. The result is `1`, when it should be `0`.

**Good example**: count a column from the right table:

```sql
select g.nome_grupo, count(p.usuario_id) as participantes
from grupos g
left join participacoes p on p.grupo_id = g.grupo_id
group by g.nome_grupo;
```

`count(column)` ignores empty values, so the group with no participants shows up with `0`. Tested with an empty group, `count(*)` returned `1`, and `count(p.usuario_id)`, `0`.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Forgetting `on` and getting 36 rows instead of 6 | Without a condition, the database combines each row of one table with every row of the other (6 groups times 6 subjects) | Every `join` needs its `on` |
| `column "g.nome_grupo" must appear in the GROUP BY clause or be used in an aggregate function` | A column outside the aggregation is not in the `group by` | Add the column to the `group by` |
| `column reference "materia_id" is ambiguous` | The column exists in both tables of the `join` | Write `g.materia_id` or `m.materia_id`, with the alias |
| Using `count(*)` with `left join` | It counts the "empty" row generated by `left join` | Count a column from the right table |
| Swapping `where` for `having` | Both filter, but at different moments | `where` filters rows before grouping, `having` filters the groups after |

## // Guided practice

1. Run the `join` query between `grupos` and `materias` and check the result.
2. Run the participants-per-group query and compare it with `gruposMock`'s `participantes`: the numbers are different on purpose, and why?
3. Run the remaining-spots query.
4. Write the Profile query for another person, changing the email.
5. Remove the `on` from a `join` and look at the size of the result.

## // Practice on your own

> **CHALLENGE**
> Write a query that shows, for each subject, how many memberships it has in total (adding up all its groups). Hint: you will need to join `materias`, `grupos` and `participacoes`.

## // Applying it to the week's project

1. Save your project's queries in `sql/03-consultas.sql`, with a comment explaining each one.
2. Include at least one query with `join`, one with `group by` and one with `left join`.
3. Commit: `git commit -m "Add the project's queries"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> A new group has no participants yet. Your "participants per group" query uses a regular `join`, instead of `left join`. What will the Dashboard show for that group?

Answer: nothing, the group disappears from the result. A regular `join` only returns rows that have a match on both sides, and a group with no memberships has no row in `participacoes`. For it to show up with `0` participants, the query needs a `left join` starting from the `grupos` table.

## // Module summary

- [ ] I can combine tables with `join` and write the `on` condition with primary and foreign keys.
- [ ] I know the difference between `join` and `left join`.
- [ ] I can use `count`, `sum`, `min` and `max`, and `group by`.
- [ ] I can filter the result of an aggregation with `having`.
- [ ] I know why `count(*)` is misleading when there is a `left join`.
- [ ] I have already written my project's queries.

---

**Next module:** `12-projeto-guiado.en.md`, the tools are complete. Time to put everything together and get the database active on Supabase.

`Study Material // Coffee & Code`
