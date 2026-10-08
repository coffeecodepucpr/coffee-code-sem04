# Module 07, Normalization: 2NF and 3NF

🇧🇷 [Português](./07-normalizacao-2fn-e-3fn.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

In Module 06 you saw why a single table causes problems, and how 1NF solves the first level: each cell holds a single value, with no lists inside a column. But a table can be in 1NF and still repeat a lot of information. This module solves exactly that, with the next two normal forms.

## // The starting point: a 1NF table that still repeats data

This is the `participacoes_planilha` table, which records who takes part in which group:

| usuario_id | grupo_id | nome_usuario | nome_grupo | materia | codigo_materia | entrou_em |
|---|---|---|---|---|---|---|
| 1 | 10 | Ana Martins | Cálculo passo a passo | Cálculo I | MAT101 | 2026-09-01 |
| 1 | 11 | Ana Martins | Estruturas na prática | Estrutura de Dados | INF201 | 2026-09-03 |
| 2 | 10 | Bruno Lima | Cálculo passo a passo | Cálculo I | MAT101 | 2026-09-02 |
| 3 | 11 | Carla Souza | Estruturas na prática | Estrutura de Dados | INF201 | 2026-09-05 |

The primary key here is **composite**: the pair `(usuario_id, grupo_id)` identifies a row, because the same person can take part in several groups and a group has several people.

Notice how much text repeats. The name "Ana Martins" appears in two rows, and so does the code MAT101. If Ana changes her name, you need to remember to update all her rows. If you forget one, the database ends up with two versions of the same person.

## // Functional dependency: the idea behind everything

> **FUNCTIONAL DEPENDENCY: IN PLAIN WORDS**
> We say B depends on A when, knowing the value of A, there is a single possible value for B. We write A → B. Example: knowing the `usuario_id`, there is a single `nome_usuario`.

Applying this question to each column of the example table:

| Column | Depends on | Depends on the whole key? |
|---|---|---|
| `nome_usuario` | `usuario_id` | No, only on part of the key |
| `nome_grupo` | `grupo_id` | No, only on part of the key |
| `materia` | `grupo_id` | No, only on part of the key |
| `codigo_materia` | `materia` | No, it depends on another column that is not a key |
| `entrou_em` | `(usuario_id, grupo_id)` | Yes |

This table is the map of the problems: each "No" points to a repetition that the next sections will remove.

## // 2NF: the whole key

> **2NF: IN PLAIN WORDS**
> A table is in 2NF when it is already in 1NF and every attribute that is not part of the key depends on the **whole** key, not just on a piece of it.

2NF only has something to fix when the key is composite. If the key has a single column, the table is automatically in 2NF, because there is no "piece" of the key.

How to apply it, in four steps:

1. Identify the composite key (here, `usuario_id` and `grupo_id`).
2. For each column outside the key, ask: do I need both pieces of the key to determine it, or just one?
3. Columns that depend on a single piece go to a new table, which has that piece as its key.
4. Only the columns that depend on the whole key stay in the original table.

The result of 2NF is three tables:

| usuario_id | nome_usuario |
|---|---|
| 1 | Ana Martins |
| 2 | Bruno Lima |
| 3 | Carla Souza |

| grupo_id | nome_grupo | materia | codigo_materia |
|---|---|---|---|
| 10 | Cálculo passo a passo | Cálculo I | MAT101 |
| 11 | Estruturas na prática | Estrutura de Dados | INF201 |

| usuario_id | grupo_id | entrou_em |
|---|---|---|
| 1 | 10 | 2026-09-01 |
| 1 | 11 | 2026-09-03 |
| 2 | 10 | 2026-09-02 |
| 3 | 11 | 2026-09-05 |

Each person's name now exists only once. But the `grupos` table still stores `materia` and `codigo_materia` together, and that is where the next problem lies.

## // 3NF: nothing but the key

> **3NF: IN PLAIN WORDS**
> A table is in 3NF when it is already in 2NF and no column outside the key depends on another column outside the key. In other words: no transitive dependencies.

In the `grupos` table, `codigo_materia` does not depend directly on `grupo_id`: it depends on `materia`, and `materia` depends on `grupo_id`. The information reaches the group "passing through" another column, and that is a transitive dependency (`grupo_id` → `materia` → `codigo_materia`). If a subject's code changes, you need to fix every group of that subject.

The fix follows the same logic as 2NF: information that depends on another column goes into its own table.

<div align="center">
<img src="./assets/normalizacao-1fn-2fn-3fn.svg" alt="The single 1NF table splitting into three tables in 2NF and four tables in 3NF" width="640">
</div>

In the end, the project's model has four tables:

```
usuarios(usuario_id PK, nome_usuario)
materias(materia_id PK, nome, codigo)
grupos(grupo_id PK, nome_grupo, materia_id FK)
participacoes(usuario_id PK/FK, grupo_id PK/FK, entrou_em)
```

The `grupos` table now stores only `materia_id`, a reference to the subject. The letters PK and FK stand for primary key and foreign key, which Module 08 explains in detail.

## // What about the mock's `participantes` field?

In Week 03's `gruposMock`, each group had a property `participantes: 5`. Notice that, in the normalized model, this column does not exist, and on purpose. The number of participants can be **calculated** by counting each group's rows in `participacoes`.

Storing the number as a column would create a second source of truth, and the database could say the group has 5 participants while the `participacoes` table shows 4 rows. It is the same out-of-sync problem you saw in Module 13 of Week 03, now in the database. Module 11 shows how to calculate the number with `COUNT`.

## // When not to normalize

Normalizing reduces repetition, but increases the number of tables, and querying scattered data requires combining tables (the `JOIN` from Module 11). In systems heavily focused on reading and reports, data is sometimes duplicated on purpose, to gain speed. This is called denormalization.

This week's rule: normalize up to 3NF, and only denormalize for a measured reason, never on a hunch. Module 13 (veteran track) shows how to measure.

## // Good example × bad example

**Bad example**: the subject code repeated inside each group:

| grupo_id | nome_grupo | materia | codigo_materia |
|---|---|---|---|
| 10 | Cálculo passo a passo | Cálculo I | MAT101 |
| 12 | Revisão de limites | Cálculo I | MAT101 |

If the code changes to MAT102, both rows have to be updated, and forgetting one leaves the database contradicting itself.

**Good example**: the subject in its own table, and the group storing only the reference:

| materia_id | nome | codigo |
|---|---|---|
| 1 | Cálculo I | MAT101 |

| grupo_id | nome_grupo | materia_id |
|---|---|---|
| 10 | Cálculo passo a passo | 1 |
| 12 | Revisão de limites | 1 |

Now the code exists in a single place, and changing it is a change to a single row.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Looking for something to split for 2NF in a table with a single-column key | 2NF only deals with dependency on part of a composite key | If the key has a single column, the table is already in 2NF: move on to 3NF |
| Splitting too much, creating a table for each column | Normalization becomes a goal instead of a tool | Only split when there is real repetition or a dependency that breaks the rule |
| Assuming `materia` always determines `codigo_materia` | The dependency only holds if the subject name is unique | Confirm the business rule: if two subjects with the same name can have different codes, the dependency does not exist |
| Storing a value that can be calculated, like the participant count | It seems faster to read | Calculate it with `COUNT`, and only store it if you measure that you really need to |

## // Guided practice

1. Copy this module's `participacoes_planilha` table into a text editor or onto paper.
2. Write the functional dependencies, one per line, in the format `A → B`.
3. Apply 2NF: which columns depend only on `usuario_id`? Which depend only on `grupo_id`?
4. Apply 3NF to the remaining `grupos` table.
5. Compare your result with this module's diagram and note any difference.

## // Practice on your own

> **CHALLENGE**
> The `encontros_planilha` table stores `encontro_id` (key), `grupo_id`, `nome_grupo`, `dia_semana`, `hora_inicio` and `local`. Is there any transitive dependency? If there is, write how you would split the table.

## // Applying it to the week's project

1. In your `docs/arquitetura.md`, record the project's tables and columns after 3NF, in the same format as the list in this module.
2. Review the ERD you drew in Module 05: does each entity follow 2NF and 3NF? Adjust the drawing where it does not.
3. Commit: `git commit -m "Normalize the project's model up to 3NF"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> The table `grupos(grupo_id, nome_grupo, materia_id, nome_materia)` has a simple key (`grupo_id`). Is it already in 2NF? And in 3NF?

Answer: it is in 2NF, because the key has a single column and, therefore, no column can depend on just "part" of it. But it is not in 3NF: `nome_materia` depends on `materia_id`, which is not the key, forming the transitive dependency `grupo_id` → `materia_id` → `nome_materia`. The fix is to remove `nome_materia` from `grupos` and store it only in the `materias` table.

## // Module summary

- [ ] I can explain what a functional dependency is (A → B).
- [ ] I can identify when a column depends only on part of a composite key (2NF violation).
- [ ] I can identify a transitive dependency (3NF violation).
- [ ] I can split a table to fix each violation.
- [ ] I know why the mock's `participantes` field should not become a column.
- [ ] My project's model is normalized up to 3NF.

---

**Next module:** `08-tipos-de-dados-e-chaves.en.md`, the design is normalized. Time to define each column's type and how the tables connect through keys.

`Study Material // Coffee & Code`
