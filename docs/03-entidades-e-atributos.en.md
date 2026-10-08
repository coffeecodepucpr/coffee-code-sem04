# Module 03, Entities and Attributes

🇧🇷 [Português](./03-entidades-e-atributos.md) · 🇺🇸 English

`WEEK 04 // Data Modeling`

---

## // Before you start

With the environment ready, the part that gives the week its name begins: modeling. Modeling means deciding, before writing any SQL, which things the system needs to store and which information exists about each of them. This module teaches you how to find those things from what the project already says.

## // The problem: where to start?

There is a common temptation: opening the SQL Editor and creating tables by intuition. The risk is finding out three modules later that one table should have been two, and redoing everything. Modeling first costs a few minutes of paper and avoids that rework.

## // Entity and attribute

> **ENTITY: IN PLAIN WORDS**
> It is a "thing" the system needs to store information about, and that will later become a table. Examples: User, Group, Subject.

> **ATTRIBUTE: IN PLAIN WORDS**
> It is a piece of information about an entity, and that will later become a column. Examples: a user's name, the time of a meeting.

Each concrete example of an entity (the user Ana Martins, the group "Modelagem e SQL") is called an **instance**, and it will be a row in the table.

## // How to find the entities: read what the project says

A simple technique is to take the project's user stories and underline the nouns. Consider these two:

- "As a student, I want to search for groups by my subject, so I can find people studying the same content."
- "As a student, I want to see when and where the group meets, so I know whether I can join."

The nouns that show up: **student**, **group**, **subject**, **meeting** (the "when and where"). Each of them is a candidate entity. "Student" will be the User entity, and the other three keep their names.

## // Entity or attribute? Three questions to decide

Not every noun becomes an entity. Some are just information about something else. To decide, ask:

1. Is there more than one piece of information about it? (A subject has a name *and* a code.)
2. Does this value repeat across several instances of another entity? (The same subject shows up in several groups.)
3. Does it make sense on its own? (A subject can exist even with no group created yet.)

If the answers are "yes", it is an entity. If not, it is an attribute. That is why **Subject** becomes an entity, while a meeting's **day of the week** is just an attribute.

## // The project's attributes

<div align="center">
<img src="./assets/entidades-atributos.svg" alt="Four entities of the project, User, Subject, Group and Meeting, with their attributes" width="640">
</div>

| Entity | Attributes | Identifier candidates |
|---|---|---|
| User | name, email, sign-up date | email |
| Subject | name, code | name, code |
| Group | group name, participant limit, creation date | (no natural one) |
| Meeting | day of the week, start time, location | (no natural one) |

An **identifier** is the attribute (or set of attributes) that distinguishes one instance from the others. When no attribute works well, as with Group, the model will create an artificial identifier. Module 08 shows how.

## // Three kinds of attribute that need care

**Derived attribute**: can be calculated from other data. In Week 03's `gruposMock` there was `participantes: 5`, but that number can be calculated by counting each group's memberships. Derived attributes, as a rule, do **not** become columns.

**Multivalued attribute**: holds more than one value at the same time. In `usuarioMock`, the property `materias: [1, 2, 3]` is an example. An attribute like this does not fit in a column: it signals that there is a relationship between two entities, which the next module covers.

**Composite attribute**: can be split into parts. An address, for example, has street, number and city. When the parts are queried separately, each one becomes a column.

## // Good example × bad example

**Bad example**: the subject as a text attribute inside Group:

| Entity | Attributes |
|---|---|
| Group | group name, subject, subject code, participant limit |

The subject's name and code repeat in every group of that subject, and a subject with no group does not even exist in the model.

**Good example**: Subject as its own entity:

| Entity | Attributes |
|---|---|
| Subject | name, code |
| Group | group name, participant limit |

Each subject is recorded once. The link between Group and Subject will be drawn in the next module.

## // Common mistakes

| Mistake | Why it happens | How to fix it |
|---|---|---|
| Turning everything into an entity | Underlining nouns catches too many words | Apply the three questions: only what has its own information, repeats or exists on its own becomes an entity |
| Storing a value that can be calculated | The mock already had that field | Identify derived attributes and calculate them with a query |
| Putting a list inside an attribute | The JavaScript array allowed it | Treat it as a relationship between two entities |
| Mixing two concepts in one entity | It seems simpler at first | If a part repeats or can exist on its own, it deserves its own entity |

## // Guided practice

1. Take two or three user stories from your project (the ones from Week 01 will do).
2. Underline the nouns in each one.
3. For each noun, apply the three questions and decide: entity, attribute or neither.
4. For each entity, list the attributes and propose an identifier.
5. Mark any derived or multivalued attribute that shows up.

## // Practice on your own

> **CHALLENGE**
> Consider this fictional system: "A library lends books to readers. Each book has a title, an author and a year. Each loan has a pick-up date and an expected return date." What are the entities and the attributes? Is there any attribute you would classify as derived?

## // Applying it to the week's project

1. In `docs/arquitetura.md`, create the section "Entities and attributes" with a table in the same format as this section.
2. Record, in one line, the decision about `participantes` (derived) and about `materias` (multivalued).
3. Commit: `git commit -m "Document the project's entities and attributes"`.

## // Checkpoint

> **BEFORE MOVING ON, THINK ABOUT THIS**
> Should a meeting's `dia_semana` (day of the week) be an entity, with a table just for the days of the week? Apply the three questions.

Answer: it should not. The day of the week has a single piece of information (the day's name itself), it needs no additional data, and a value like "Monday" gains nothing by existing on its own. It is a simple attribute of Meeting. It would be different if each day had its own information, such as the university's opening hours.

## // Module summary

- [ ] I can tell entity, attribute and instance apart.
- [ ] I can extract candidate entities from user stories.
- [ ] I can apply the three questions to decide between entity and attribute.
- [ ] I can recognize derived and multivalued attributes.
- [ ] I have already listed my project's entities and attributes.

---

**Next module:** `04-relacionamentos-e-cardinalidade.en.md`, the entities exist. Now, how they connect to each other.

`Study Material // Coffee & Code`
