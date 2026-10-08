# Módulo 15, ORMs: Prisma e SQLAlchemy

🇧🇷 Português · 🇺🇸 [English](../docs-eng/15-orms-prisma-and-sqlalchemy.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

> **TRILHA VETERANO**
> Este módulo faz parte da trilha veterano: ele vem depois do conteúdo essencial e não é necessário para o entregável da semana. Quem segue a trilha principal pode pular para o `entregavel.md`.

Até aqui você conversou com o banco escrevendo SQL no painel do Supabase. Uma aplicação de verdade conversa com ele a partir do código, em Python, TypeScript ou outra linguagem. Este módulo apresenta a ferramenta que faz essa ponte, o ORM, e mostra o mesmo modelo do projeto em duas delas: SQLAlchemy e Prisma.

## // O problema: o abismo entre objetos e tabelas

No código, os dados são objetos: um `Grupo` com propriedades e métodos. No banco, são linhas em tabelas. Traduzir de um para o outro à mão, escrevendo SQL em texto dentro do código, é trabalhoso e fácil de errar, e cada nome de coluna digitado errado só dá erro quando o código roda.

## // O que é um ORM

> **ORM: EM PALAVRAS SIMPLES**
> *Object-Relational Mapping* (mapeamento objeto-relacional) é uma biblioteca que representa as tabelas do banco como classes do seu código, as linhas como objetos, e traduz as operações em objetos para comandos SQL.

<div align="center">
<img src="./assets/orm-camadas.svg" alt="As camadas entre o código e o banco: o ORM traduz objetos em SQL, que o PostgreSQL executa" width="640">
</div>

Os ganhos são reais: o editor completa nomes de colunas, erros de digitação aparecem antes, e as relações entre tabelas viram propriedades navegáveis (`ana.participacoes`). Mas o ORM **não substitui** o SQL. Ele escreve SQL por você, e entender SQL, como você fez nos Módulos 09 a 11, é o que permite conferir se ele escreveu direito, e resolver o que ele não resolve sozinho.

## // As duas ferramentas

| | SQLAlchemy | Prisma |
|---|---|---|
| Linguagem | Python | TypeScript e JavaScript |
| Onde o modelo é descrito | Classes Python (`models.py`) | Arquivo próprio (`schema.prisma`) |
| Migrations | Alembic | Prisma Migrate |
| Versão usada neste guia | SQLAlchemy 2.0 (testado com a 2.0.54) | Prisma 7 |

> **ATENÇÃO À VERSÃO DO PRISMA**
> Na data da consulta deste material (7 de outubro de 2026), a página oficial de status do Prisma informa que o **Prisma ORM 8 ainda é release candidate**, com lançamento previsto para outubro de 2026, e que `npm install prisma` já instala a ferramenta de linha de comando do Prisma 8. O fluxo normal do Prisma 8 usa um formato próprio de schema (o *contract*) e não tem os comandos `generate` e `migrate dev` usados neste guia. Projetos Prisma 7 em PostgreSQL podem, porém, ser importados para o Prisma 8 por um comando de migração (`npx prisma@latest orm init --from-prisma7-schema prisma/schema.prisma`), que permite rodar as duas versões lado a lado. Esse comando renomeia a ferramenta do Prisma 7 para `prisma7` e a configuração para `prisma7.config.ts`. O Prisma 7 continua recebendo correções por 18 meses depois do lançamento do 8. Por isso este guia usa o **Prisma 7, com a versão fixada** (`npm install --save-dev prisma@7`), para manter os exemplos estáveis. Confira a página de status do Prisma antes de começar, porque isso pode ter mudado.

## // SQLAlchemy 2.0

### > O modelo

Cada tabela vira uma classe, e cada coluna vira um atributo anotado com o seu tipo. Veja a tabela `grupos`, a mesma do Módulo 09, em Python:

```python
class Grupo(Base):
    __tablename__ = "grupos"

    grupo_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome_grupo: Mapped[str] = mapped_column(Text)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.materia_id"))
    max_participantes: Mapped[int] = mapped_column(Integer, server_default=text("10"))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    materia: Mapped["Materia"] = relationship(back_populates="grupos")
    participacoes: Mapped[list["Participacao"]] = relationship(back_populates="grupo")
```

Compare com o `create table` do Módulo 09: cada linha tem a sua correspondente. `Mapped[str]` sem `None` equivale a `not null`; `ForeignKey(...)` equivale a `references`; e `relationship(...)` é novidade, porque ela não cria nenhuma coluna: apenas diz ao SQLAlchemy como navegar entre as tabelas.

O modelo completo, com as cinco tabelas, está em `example/sqlalchemy/models.py`.

### > Consultando

O SQLAlchemy 2.0 monta consultas com a função `select`, e o resultado se lê quase como o SQL:

```python
consulta = (
    select(Grupo.nome_grupo, Grupo.max_participantes,
           func.count(Participacao.usuario_id).label("participantes"))
    .join(Participacao, Participacao.grupo_id == Grupo.grupo_id, isouter=True)
    .group_by(Grupo.grupo_id)
    .order_by(Grupo.nome_grupo)
)
```

Esta é a consulta de vagas do Módulo 11, com `join` à esquerda, `count` e `group by`. Executada contra o banco do seed, ela devolveu:

```
Cálculo passo a passo      3/6
Estruturas na prática      2/5
Modelagem e SQL            6/8
Processos e memória        1/4
Redes na unha              2/6
Requisitos e histórias     2/5
```

Os mesmos números da consulta em SQL puro. Para ver o SQL que o ORM escreveu, a consulta `select(Grupo).where(Grupo.max_participantes >= 6).order_by(Grupo.nome_grupo)` vira:

```
SELECT grupos.grupo_id, grupos.nome_grupo, grupos.materia_id, grupos.max_participantes, grupos.criado_em
FROM grupos
WHERE grupos.max_participantes >= %(max_participantes_1)s ORDER BY grupos.nome_grupo
```

O `%(max_participantes_1)s` é um **parâmetro**: o valor (6) viaja separado do texto do SQL, e isso protege contra uma falha de segurança famosa, a injeção de SQL.

### > Navegando pelos relacionamentos

Os grupos de uma pessoa, que no Módulo 11 exigiam um `join` encadeado por três tabelas, viram uma navegação por propriedades:

```python
ana = session.scalars(select(Usuario).where(Usuario.email == "ana.martins@exemplo.com")).one()
for p in ana.participacoes:
    print(f"{p.grupo.nome_grupo} ({p.grupo.materia.nome}), desde {p.entrou_em}")
```

```
Cálculo passo a passo (Cálculo I), desde 2026-09-01
Estruturas na prática (Estrutura de Dados), desde 2026-09-03
Modelagem e SQL (Banco de Dados), desde 2026-09-05
```

### > Inserindo, e desfazendo

```python
novo = Grupo(nome_grupo="Cálculo II na prática", materia=materia, max_participantes=5)
session.add(novo)
session.flush()          # envia o insert, e o banco devolve o id gerado
session.rollback()       # desfaz tudo, o banco fica como estava
```

O arquivo `example/sqlalchemy/consultas.py` reúne os três exemplos e pode ser executado com a variável `DATABASE_URL` apontando para o banco de testes (no formato `postgresql+psycopg://usuario:senha@host:5432/banco`).

## // Prisma 7

> **AVISO: ESTE TRECHO NÃO FOI EXECUTADO PELO AUTOR**
> O ambiente em que este material foi produzido não conseguiu baixar o motor do Prisma, então nada desta seção foi executado, nem o `schema.prisma` validado. O conteúdo segue a documentação oficial do Prisma 7, consultada em 4 de outubro de 2026. Execute na sua máquina e, em caso de divergência, a documentação oficial é a referência.

### > Instalação e configuração

```
npm install --save-dev prisma@7 dotenv typescript tsx
npm install @prisma/client@7 @prisma/adapter-pg pg
```

No Prisma 7, o banco é configurado em um arquivo `prisma.config.ts` na raiz do projeto, e não mais dentro do `schema.prisma`:

```ts
import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: { url: process.env["DATABASE_URL"] },
});
```

Duas diferenças em relação a tutoriais mais antigos: a URL do banco **saiu** do `schema.prisma`, e o Prisma 7 exige um *driver adapter* na hora de criar o cliente (no caso do PostgreSQL, o `@prisma/adapter-pg`).

### > O modelo

O Prisma descreve as tabelas em um arquivo com sintaxe própria. Veja `Grupo`, a mesma tabela dos exemplos anteriores:

```
model Grupo {
  id               BigInt         @id @default(autoincrement()) @map("grupo_id")
  nome             String         @map("nome_grupo")
  materiaId        BigInt         @map("materia_id")
  maxParticipantes Int            @default(10) @map("max_participantes")
  criadoEm         DateTime       @default(now()) @map("criado_em") @db.Timestamptz(6)
  materia          Materia        @relation(fields: [materiaId], references: [id])
  participacoes    Participacao[]
  encontros        Encontro[]

  @@index([materiaId])
  @@map("grupos")
}
```

O `@map` e o `@@map` ligam os nomes do código (`maxParticipantes`) aos nomes das colunas do banco (`max_participantes`), e é isso que permite manter as convenções de nome do Módulo 08. O modelo completo está em `example/prisma/prisma/schema.prisma`.

Um detalhe a conferir na sua máquina: o Prisma costuma criar identificadores automáticos com `@default(autoincrement())`, que pode gerar uma coluna do tipo `serial`, e não o `generated always as identity` do script SQL deste guia. O efeito prático para o projeto é o mesmo, mas a estrutura gerada não é idêntica, e você pode comparar com `\d grupos` no `psql`.

### > Gerando o cliente e consultando

```
npx prisma generate
```

E, no código, o cliente é criado passando o adapter:

```ts
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "./generated/prisma/client";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL! });
const prisma = new PrismaClient({ adapter });
```

A consulta de vagas, e os grupos de uma pessoa:

```ts
const grupos = await prisma.grupo.findMany({
  include: { materia: true, _count: { select: { participacoes: true } } },
  orderBy: { nome: "asc" },
});

const ana = await prisma.usuario.findUnique({
  where: { email: "ana.martins@exemplo.com" },
  include: { participacoes: { include: { grupo: { include: { materia: true } } } } },
});
```

O `include` é o equivalente do `join`: pede ao Prisma que traga, junto com o objeto, os registros relacionados. O arquivo `example/prisma/src/consultas.ts` reúne os exemplos.

## // Os dois lado a lado

| Quero... | SQL (Módulo 11) | SQLAlchemy | Prisma |
|---|---|---|---|
| Os grupos com a matéria | `join materias` | `.join(Materia)` ou `grupo.materia` | `include: { materia: true }` |
| Contar participantes | `count(...)` com `group by` | `func.count(...)` | `_count: { select: { participacoes: true } }` |
| Filtrar | `where` | `.where(...)` | `where: { ... }` |
| Ordenar | `order by` | `.order_by(...)` | `orderBy: { ... }` |
| Os grupos de uma pessoa | `join` encadeado | `ana.participacoes` | `include` aninhado |

## // Quando usar um ORM, e quando escrever SQL

Um ORM brilha no dia a dia de uma aplicação: operações simples de ler, criar e alterar, com segurança de tipos e relacionamentos navegáveis. Mas há casos em que o SQL direto é melhor: relatórios com agregações complicadas, consultas que precisam de um desempenho muito específico, ou recursos particulares do PostgreSQL que o ORM não expõe. Os dois principais ORMs deste módulo permitem executar SQL puro quando necessário, e o seu conhecimento dos Módulos 09 a 13 vale nos dois mundos.

## // Bom exemplo × mau exemplo

**Mau exemplo**: montar o SQL juntando texto com a entrada da pessoa:

```python
email = input("E-mail: ")
session.execute(text(f"select * from usuarios where email = '{email}'"))
```

Se alguém digitar `' or '1'='1`, a condição passa a ser sempre verdadeira e a consulta devolve **todos** os usuários. É a injeção de SQL.

**Bom exemplo**: deixar o ORM (ou o parâmetro) cuidar do valor:

```python
session.scalars(select(Usuario).where(Usuario.email == email))
```

O valor viaja como parâmetro, separado do texto do SQL, e nunca é interpretado como comando.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Esquecer o `relationship` e tentar navegar `ana.participacoes` | A chave estrangeira sozinha não cria a propriedade | Declare o `relationship` nos dois lados da ligação |
| Achar que o ORM dispensa saber SQL | Ele esconde o SQL, mas não o elimina | Olhe o SQL gerado e confira com `explain analyze` quando algo estiver lento |
| `npm install prisma` e os comandos `generate` e `migrate dev` sumirem | Hoje isso instala a ferramenta do Prisma 8 | Instale `prisma@7` e fixe a versão no `package.json` |
| Montar SQL com texto concatenado | É o caminho mais curto | Use parâmetros ou os métodos do ORM |
| Executar o ORM contra o banco do entregável com `migrate dev` | O Prisma pode propor resetar o banco | Use um banco de testes separado |

## // Prática guiada

1. Em `example/sqlalchemy/`, aponte a variável `DATABASE_URL` para o seu banco de testes e rode `consultas.py`.
2. Compare os números do resultado com a consulta de vagas do Módulo 11.
3. Escreva, na própria `consultas.py`, uma consulta ORM que traga os encontros de um grupo (dica: use o relacionamento `grupo.encontros`).
4. Se for usar o Prisma, configure o `.env`, rode `npx prisma generate` e execute o `src/consultas.ts`.

## // Pratique sozinho

> **DESAFIO**
> Escolha uma das consultas do Módulo 11 que você ainda não reescreveu em ORM (por exemplo, "as matérias com o total de participações") e reescreva-a em SQLAlchemy ou em Prisma. Depois, confira o resultado contra o do SQL puro.

## // Aplicando no projeto da semana

1. Registre no `docs/arquitetura.md` qual ORM você escolheu e por quê, em duas ou três frases.
2. Adicione ao repositório o modelo (`models.py` ou `schema.prisma`) e um arquivo `.env.example` sem senha.
3. Commit: `git commit -m "Adiciona o modelo ORM do projeto"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você lê em um fórum que "com ORM nem precisa aprender SQL". Que dois argumentos deste módulo mostram o problema dessa ideia?

Resposta: primeiro, o ORM apenas escreve o SQL por você, e para saber se ele escreveu uma consulta eficiente (ou diagnosticar uma lenta) é preciso ler o SQL gerado e o plano de execução, como no Módulo 13. Segundo, existem casos, como relatórios complexos ou recursos específicos do PostgreSQL, em que o caminho certo é escrever SQL direto. O ORM economiza trabalho no dia a dia, mas depende de quem o usa entender o que acontece por baixo.

## // Resumo do módulo

- [ ] Sei o que é um ORM e o problema que ele resolve.
- [ ] Sei descrever uma tabela como classe no SQLAlchemy e como model no Prisma.
- [ ] Sei fazer uma consulta com `join`, agregação e filtro em pelo menos um dos dois.
- [ ] Sei que o Prisma 8 ainda é release candidate e que este guia usa o Prisma 7 com a versão fixada.
- [ ] Sei por que o ORM não substitui o SQL.

---

**Próximo passo:** `entregavel.md`, a revisão final de tudo que a Semana 04 pediu.

`Material de Estudo // Coffee & Code`
