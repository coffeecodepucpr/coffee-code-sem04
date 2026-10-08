# Module 04, Relationships and Cardinality

🇧🇷 [Português](./04-relacionamentos-e-cardinalidade.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

In Module 03 you found the project's entities: User, Subject, Group and Meeting. But isolated entities still say nothing about how the information connects. This module solves exactly that: which entities connect, and in what way.

## // The problem: which subject does a group belong to?

With the four entities on their own, the model cannot answer basic questions about the project. What is a group's subject? Who takes part in a group? When does the group meet? The answers are in the **links** between the entities, and they need to be drawn precisely, because the way they are linked decides how the tables will be created.

## // Relationship

> **RELATIONSHIP: IN PLAIN WORDS**
> It is a link between two entities, usually described by a verb. Examples: a Subject *has* Groups; a User *takes part in* Groups.

To find the relationships, try forming sentences with two entities and a verb:

- A subject **has** groups.
- A group **has** meetings.
- A user **takes part in** groups.

## // Cardinality: how many on each side

> **CARDINALITY: IN PLAIN WORDS**
> It says how many instances of one entity can be linked to one instance of the other. Cardinality is read **in both directions**.

Take the relationship between Subject and Group and read it in both directions:

- A subject can have **many** groups (or none, if none has been created yet).
- A group belongs to **exactly one** subject.

Since on one side the maximum is "one" and on the other it is "many", this relationship is of type **1:N** (one to many).

## // The three types of relationship

| Type | Reading | Example |
|---|---|---|
| 1:1 | Each instance on one side links to at most one on the other | A person and their ID document |
| 1:N | One instance on one side links to many on the other | A subject and its groups |
| N:N | Many on each side link to many on the other | Users and groups |

The 1:1 type is rare and does not appear in this week's project. The other two do: Subject and Group is 1:N, Group and Meeting is 1:N, and User and Group is N:N.

## // Minimum cardinality: required or optional?

Besides the maximum (one or many), it is worth asking about the **minimum**: is the link required or optional?

- A group **must** have a subject: the link is required on that side (minimum 1).
- A subject **can** exist without any group: the link is optional on that side (minimum 0).

This answer will become a concrete database rule in Module 08: the required reference will be a column that does not accept an empty value.

## // Crow's foot notation

To draw cardinalities, this guide uses **crow's foot** notation, very common in modeling tools. Each end of the relationship line has a symbol that states the minimum and maximum on that side:

<div align="center">
<img src="./assets/cardinalidade-pe-de-galinha.svg" alt="The four crow's foot symbols: exactly one, zero or one, one or many, zero or many" width="640">
</div>

| Symbol at the end of the line | Means |
|---|---|
| Two bars | Exactly one |
| Circle and one bar | Zero or one |
| Crow's foot and one bar | One or many |
| Crow's foot and a circle | Zero or many |

The trick to reading it: the symbol **closest to the entity** is the maximum (a bar for "one", the crow's foot for "many"), and the **farthest one** is the minimum (a bar for "required", the circle for "optional").

## // The N:N relationship and the associative table

User and Group are N:N: one person takes part in several groups, and one group has several people. The problem is that a relational database **cannot** represent N:N directly between two tables. The solution is to create a third entity in the middle, the **associative entity**, which breaks the N:N into two 1:N relationships.

In the project, this entity is called **Membership** (`participacoes`): each instance of it represents one person taking part in one group.

| usuario_id | grupo_id | entrou_em |
|---|---|---|
| 1 | 1 | 2026-09-01 |
| 1 | 2 | 2026-09-03 |
| 2 | 1 | 2026-09-02 |

Notice two things. First, each row links one person to one group. Second, the `entrou_em` (joined at) column belongs neither to the user nor to the group: it belongs to the **link** between the two. That is a classic sign that the relationship deserves its own entity.

Now Week 03's `usuarioMock.materias: [1, 2, 3]` makes sense: that array was a disguised way of storing the N:N, which the database stores in a link table.

## // The project's relationships

| Relationship | Left side | Right side | Type |
|---|---|---|---|
| Subject has Group | Exactly one subject | Zero or many groups | 1:N |
| Group has Meeting | Exactly one group | Zero or many meetings | 1:N |
| User has Membership | Exactly one user | Zero or many memberships | 1:N |
| Group has Membership | Exactly one group | Zero or many memberships | 1:N |

The last two together form the N:N between User and Group, solved by Membership.

## // Good example × bad example

**Bad example**: trying to store the N:N inside one of the entities:

| Entity | Attributes |
|---|---|
| User | name, email, list of groups |

A list inside an attribute brings back the problem from Module 01: no good way to query, no safe way to remove a membership, and no place for `entrou_em`.

**Good example**: an associative entity in the middle:

| Entity | Attributes |
|---|---|
| User | name, email |
| Group | group name, participant limit |
| Membership | join date (linking a user to a group) |

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Reading the relationship in one direction only | Hearing "a subject has groups" seems enough | Always read in both directions before fixing the cardinality |
| Drawing N:N directly between two tables | Paper allows it, the database does not | Create the associative entity and use two 1:N relationships |
| Swapping the side of the crow's foot | The "many" symbol goes on the side of whatever is "many" | Ask: the quantity of what? The symbol goes next to that entity |
| Forgetting the minimum | People only think about "one or many" | For each end, ask whether it can be zero |

## // Guided practice

1. For each pair of entities in your project that are linked, write the sentence with a verb.
2. Read each sentence in both directions and write down the maximum (one or many) and the minimum (zero or one).
3. Classify each relationship as 1:1, 1:N or N:N.
4. For each N:N, propose the associative entity and list the attributes that belong to the link.

## // Practice on your own

> **CHALLENGE**
> In the library from Module 03, "a reader borrows books, and a book can be borrowed by several readers over time". What type of relationship is this? Which associative entity would you create and what attributes would it have?

## // Applying it to the week's project

1. In `docs/arquitetura.md`, create the section "Relationships" with a table in the format of this section.
2. Record the associative entity that solves your project's N:N.
3. Commit: `git commit -m "Document relationships and cardinalities"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> In the 1:N relationship between Subject and Group, which of the two tables will store the reference to the other?

Answer: the table on the "many" side, that is, Group. Each group stores the identifier of its subject, and this works because each group has exactly one. The opposite would not work: a subject would have to store the list of all its groups, bringing back the problem of a list inside a field.

## // Module summary

- [ ] I can describe a relationship with a verb and read the cardinality in both directions.
- [ ] I can tell 1:1, 1:N and N:N apart.
- [ ] I know what minimum cardinality is (required or optional).
- [ ] I can read the four symbols of crow's foot notation.
- [ ] I can solve an N:N with an associative entity.
- [ ] I have already listed my project's relationships.

---

**Next module:** `05-o-diagrama-der.en.md`, the entities and links are defined. Time to bring everything together in one drawing.

`Study Material // Coffee & Code`
