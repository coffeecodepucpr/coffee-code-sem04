# Submissions — Week 04

🇧🇷 [Português](README.md) · 🇺🇸 English

This is where the submissions from people who did Week 04 live. The list with each person's project is in the [main README](../README.en.md#class-submissions).

## How to submit

1. **Fork** this repository (the *Fork* button, in the top right corner).
2. In your fork, create the folder `entregas/First Last/` — with your first and last name.
3. Put your files inside it, following the structure below.
4. Commit and push to your fork.
5. Open a **Pull Request** to this repository and fill in the template that shows up.

After the merge, your submission goes into the main README's table.

> **Prefer to keep the project in your own repository?** That works too. Send the link on Discord or [open an issue](../../../issues/new) here with the link to the week's folder, and it goes into the table the same way. Just take good care of the `README.md`, as explained below, because it is what shows up first.

## Expected structure

```text
entregas/First Last/
├── README.md
├── login.html
├── dashboard.html
├── perfil.html
├── script.js
├── css/
│   └── styles.css
├── sql/               ← new
│   ├── 01-schema.sql
│   ├── 02-seed.sql
│   └── 03-consultas.sql
└── docs/              ← the documents from previous weeks, updated
    ├── der.png        ← new
    └── arquitetura.md ← with the model and the data dictionary
```

- The documentation folder is `docs/` (not `doc/`).
- File names in lowercase, separated by hyphens and **with an extension**: `historias-de-usuario.md`, not `historia de usuario`.
- **Never** send the database password or a `.env` file. If you need to show the connection, use a `.env.example` without the password.
- Only change files inside your own folder.

## What your README needs to have

The `README.md` in your folder is your project's cover. Whoever opens it needs to understand, without you explaining:

- **the project name** as the title (`# Shelf Hub`, not `# Assignment`);
- **one sentence** saying what it is;
- **the problem** it solves and **who** will use it;
- **the link to the Figma prototype**;
- **how to open the screens**, if there are any (which `.html` to open first);
- **how to recreate the database**: in which order to run the scripts in the `sql/` folder.

## Already submitted in another week?

No problem repeating the same project. Just remember that each week is a complete folder: send its updated version here too.
