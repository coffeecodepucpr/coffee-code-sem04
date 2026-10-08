# Exemplos executáveis, Semana 04

🇧🇷 Português · 🇺🇸 [English](../../docs-eng/example/README.md)

Esta pasta reúne tudo que pode ser executado nesta semana. É referência, e não gabarito obrigatório: o seu projeto precisa aplicar os mesmos conceitos, não ser igual a este.

## `sql/`: a trilha principal

Scripts do Buscador de Grupos de Estudo, testados em um PostgreSQL 16. Rode na ordem, no SQL Editor do Supabase:

| Arquivo | O que faz |
|---|---|
| `01-schema.sql` | Cria as cinco tabelas, as restrições e liga o RLS |
| `02-seed.sql` | Insere os dados de exemplo (6 matérias, 8 usuários, 6 grupos, 16 participações, 7 encontros) |
| `03-consultas.sql` | Sete consultas, de `select` simples a `join` com `group by` |
| `04-indices.sql` | Trilha veterano: índices das chaves estrangeiras |
| `05-laboratorio-indices.sql` | Trilha veterano: laboratório com 300 mil linhas para medir o efeito de um índice (roda em um schema separado, `lab`) |

## `sqlalchemy/`: trilha veterano, testado

O modelo em SQLAlchemy 2.0 e o histórico de migrations com Alembic, testados contra um PostgreSQL 16 (SQLAlchemy 2.0.54, Alembic 1.20, psycopg 3).

```
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://usuario:senha@host:5432/banco_de_testes"
alembic upgrade head      # cria as tabelas pela migration inicial
python consultas.py       # roda as consultas (precisa do seed carregado)
```

## `prisma/`: trilha veterano, NÃO testado pelo autor

> **ATENÇÃO**
> O ambiente em que este material foi produzido não conseguiu baixar o motor do Prisma, então estes arquivos **nunca foram executados nem validados**. Eles seguem a documentação oficial do Prisma 7, consultada em 4 de outubro de 2026. Confira na sua máquina.

O Prisma ORM 8 ainda é *release candidate* nessa data, e `npm install prisma` já instala a ferramenta do Prisma 8, que tem um fluxo próprio (sem `generate` nem `migrate dev`). Um projeto Prisma 7 em PostgreSQL pode ser importado para o Prisma 8 com `npx prisma@latest orm init --from-prisma7-schema prisma/schema.prisma`. Por isso o `package.json` fixa a versão 7, para manter os exemplos estáveis.

```
npm install
cp .env.example .env      # preencha o DATABASE_URL de um banco de testes
npx prisma generate
npx tsx src/consultas.ts
```

## Regras de segurança

- Use sempre um **banco de testes separado** do banco do seu entregável.
- A senha vai no `.env`, que nunca entra no Git. Os arquivos `.env.example` não têm senha.
- Nunca rode `prisma migrate dev` no banco do entregável: ele pode propor resetar o banco.
