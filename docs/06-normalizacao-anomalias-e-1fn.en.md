# Module 06, Normalization: Anomalies and 1NF

🇧🇷 [Português](./06-normalizacao-anomalias-e-1fn.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

In Module 05 you finished the ERD. Before turning it into tables, there is a verification step: checking whether the design avoids repetition and consistency problems. This check is called **normalization**, and this is the first of two modules about it. Here you see what goes wrong in a badly designed table, and apply the first level of correction, 1NF.

> **A NOTE ON THE NAMES**
> In Portuguese, the normal forms are written 1FN, 2FN and 3FN (*Forma Normal*), which is why the file names in this repository use "fn". In English they are 1NF, 2NF and 3NF.

## // The problem: the "single spreadsheet"

Imagine that, instead of five tables, someone stored everything in a single spreadsheet, one row per person in each group:

| usuario | grupo | materia | codigo_materia |
|---|---|---|---|
| Ana Martins | Cálculo passo a passo | Cálculo I | MAT101 |
| Bruno Lima | Cálculo passo a passo | Cálculo I | MAT101 |
| Ana Martins | Estruturas na prática | Estrutura de Dados | INF201 |
| Carla Souza | Estruturas na prática | Estrutura de Dados | INF201 |
| Diego Rocha | Processos e memória | Sistemas Operacionais | INF315 |

At first glance it works. But everything that repeats here is a trap waiting to go off.

## // The three anomalies

> **ANOMALY: IN PLAIN WORDS**
> It is a problem that shows up when changing the data of a badly designed table, caused by repeated or mixed information. There are three classic types.

<div align="center">
<img src="./assets/anomalias-tabela-unica.svg" alt="The single spreadsheet with the repeated data highlighted and the three anomalies: update, deletion and insertion" width="640">
</div>

**Update anomaly.** The code MAT101 appears in two rows. If the university changes the code of Cálculo I, both have to be changed, and forgetting one leaves the spreadsheet saying two different things.

**Deletion anomaly.** Diego is the only person in the group "Processos e memória". If he leaves the group and the row is deleted, the group, the subject and its code disappear along with it. Deleting a membership destroyed information that had nothing to do with it.

**Insertion anomaly.** To register the subject "Redes de Computadores", someone would already have to be taking part in a group for it, because each row is a membership. A subject with no participant has nowhere to be stored.

## // What normalization is

> **NORMALIZATION: IN PLAIN WORDS**
> It is a method for organizing tables so that each piece of information is stored in a single place, removing the anomalies. The method has levels, called normal forms (1NF, 2NF, 3NF and others).

Each normal form is a rule. A table that follows the rules of a level is "at that level". You already did a good part of the normalization by intuition in the previous modules, when you split Subject into its own entity. Now you will learn the method that explains why.

## // 1NF: atomic values

> **1NF: IN PLAIN WORDS**
> A table is in First Normal Form when each cell holds a single (atomic) value, with no lists or repeating groups, and when each row can be uniquely identified.

To be in 1NF, a table needs to meet four conditions:

1. Each cell has a **single value**, never a list.
2. There are no **repeated columns** for the same kind of data (such as `grupo1`, `grupo2`, `grupo3`).
3. Each row has a **key** that uniquely identifies it.
4. All rows have the **same structure**.

## // Fixing a table that violates 1NF

Look at a table in which each user has their groups in a single cell:

| usuario_id | nome_usuario | grupos |
|---|---|---|
| 1 | Ana Martins | Cálculo passo a passo, Estruturas na prática |
| 2 | Bruno Lima | Cálculo passo a passo |
| 3 | Carla Souza | Estruturas na prática |

The `grupos` column violates 1NF: Ana's cell holds two values. The fix is to give each fact its own row, and to use as the key the pair of columns that identifies each row:

| usuario_id | grupo_id | nome_usuario | nome_grupo |
|---|---|---|---|
| 1 | 10 | Ana Martins | Cálculo passo a passo |
| 1 | 11 | Ana Martins | Estruturas na prática |
| 2 | 10 | Bruno Lima | Cálculo passo a passo |
| 3 | 11 | Carla Souza | Estruturas na prática |

Now each cell has a single value, and the pair `(usuario_id, grupo_id)` is the key. The table is in 1NF.

## // 1NF does not solve everything

Compare the table above with the spreadsheet at the start of the module. Even in 1NF, the name "Ana Martins" appears in two rows, and each group's name repeats. 1NF only guarantees that values are atomic, and the update, deletion and insertion anomalies are still possible. The next module shows the two normal forms that remove the remaining repetition: 2NF and 3NF.

## // Good example × bad example

**Bad example**: repeated columns to simulate a list:

| usuario_id | nome_usuario | grupo1 | grupo2 | grupo3 |
|---|---|---|---|---|
| 1 | Ana Martins | Cálculo passo a passo | Estruturas na prática | |

What if Ana joins a fourth group? The structure of the whole table has to change, and most cells stay empty.

**Good example**: one row per membership:

| usuario_id | grupo_id |
|---|---|
| 1 | 10 |
| 1 | 11 |

Joining a fourth group just means adding a row, without changing the structure of anything.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Thinking 1NF is the whole of normalization | 1NF fixes the most visible problem, the list in a cell | Keep going to 2NF and 3NF to remove repetition |
| Separating values with commas inside a column | It is the fastest way to copy the array | Use one row per value |
| Creating numbered columns (`grupo1`, `grupo2`) | It looks organized | Replace them with rows in a link table |
| Forgetting the key for each row | The spreadsheet did not ask for one | Define the column or pair of columns that identifies each row |

## // Guided practice

1. Copy the spreadsheet from the start of the module into a text editor.
2. For each of the three anomalies, write a concrete example using the spreadsheet's data.
3. Take the table with the `grupos` column (a list in a cell) and rewrite it in 1NF.
4. Identify the table's key after the fix.

## // Practice on your own

> **CHALLENGE**
> A table stores `encontro_id`, `grupo_id` and a `dias` column with values like "Tuesday, Thursday". Is it in 1NF? Rewrite it so that it is.

## // Applying it to the week's project

1. Reread the ERD you drew in Module 05 and check: does any column store a list, or are there numbered columns?
2. If there are, fix the ERD and update the drawing in `docs/der.png`.
3. Record the result of the 1NF check in `docs/arquitetura.md`.
4. Commit: `git commit -m "Check 1NF in the project's ERD"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> A `grupos` table has a `participantes` column with values like "Ana, Bruno, Carla". Which 1NF rule does it break, and which ERD structure you already know solves this problem?

Answer: it breaks the first rule, which requires a single value per cell, because the cell holds a list of names. The problem is solved with a link table (Membership), which stores one row for each person in each group, exactly as the ERD from Module 05 already does.

## // Module summary

- [ ] I can explain the three anomalies: update, deletion and insertion.
- [ ] I know what normalization is and why it exists.
- [ ] I know the four conditions of 1NF.
- [ ] I can fix a table that stores lists in a cell.
- [ ] I know that 1NF alone does not remove all repetition.

---

**Next module:** `07-normalizacao-2fn-e-3fn.en.md`, 1NF solved the lists, but repetition remains. The next two levels take care of it.

`Study Material // Coffee & Code`
