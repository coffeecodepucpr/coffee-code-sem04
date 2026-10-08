# Módulo 14, Migrations

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

> **TRILHA VETERANO**
> Este módulo faz parte da trilha veterano: ele vem depois do conteúdo essencial e não é necessário para o entregável da semana. Quem segue a trilha principal pode pular para o `entregavel.md`.

No Módulo 09 você criou o banco rodando um script. Isso funciona uma vez. Mas projetos mudam: amanhã alguém vai querer uma coluna `descricao` nos grupos, e o banco já tem dados que não podem ser apagados. Este módulo ensina a mudar a estrutura do banco de forma controlada, versionada e reversível.

## // O problema: como mudar um banco que já tem dados?

O `drop table` seguido de um novo `create table` funcionava enquanto o banco estava vazio. Com dados de verdade, é impensável: apagar a tabela apaga tudo que as pessoas cadastraram. O `alter table` do Módulo 09 resolve o comando em si, mas deixa três perguntas em aberto:

- Como saber, daqui a um mês, **quais mudanças** já foram aplicadas a este banco?
- Como aplicar **exatamente as mesmas mudanças**, na mesma ordem, em outro banco (um de testes, por exemplo)?
- Como **desfazer** uma mudança que deu errado?

## // O que é uma migration

> **MIGRATION: EM PALAVRAS SIMPLES**
> É um arquivo, guardado no repositório, que descreve uma mudança no esquema do banco: como aplicá-la (`upgrade`) e como desfazê-la (`downgrade`). Cada migration tem um número de versão, e juntas formam o histórico de como o banco chegou ao estado atual.

<div align="center">
<img src="./assets/migrations-fluxo.svg" alt="O fluxo de uma migration: mudar o modelo, gerar o arquivo, versionar no Git, aplicar e ter o banco atualizado" width="640">
</div>

O próprio banco guarda em qual versão está, em uma tabela de controle (`alembic_version` no Alembic, `_prisma_migrations` no Prisma). Ao aplicar as migrations, a ferramenta consulta essa tabela e roda apenas as que ainda faltam.

## // Duas ferramentas, a mesma ideia

| | Alembic (Python) | Prisma Migrate (TypeScript) |
|---|---|---|
| Onde você descreve o modelo | `models.py` | `schema.prisma` |
| Gerar a migration | `alembic revision --autogenerate` | `prisma migrate dev` |
| Onde ficam os arquivos | `alembic/versions/` | `prisma/migrations/` |
| Aplicar | `alembic upgrade head` | `prisma migrate deploy` |
| Desfazer | `alembic downgrade -1` | Não existe comando equivalente (cria-se uma nova migration) |

As duas fazem o mesmo ciclo: você muda o modelo, a ferramenta compara o modelo com o banco e escreve a migration para você. O Módulo 15 explica os modelos; aqui o foco é o ciclo.

> **ANTES DE QUALQUER COISA: USE UM BANCO DE TESTES**
> Os exemplos deste módulo mudam a estrutura do banco. Faça-os em um **banco separado** do banco do seu entregável: um PostgreSQL local ou um segundo projeto do Supabase (confira, na página de preços, quantos projetos gratuitos a sua conta permite). Assim, um erro nunca atinge o banco que você vai entregar.

## // Alembic, na prática

Os comandos abaixo foram executados contra um PostgreSQL de teste. Os arquivos estão em `example/sqlalchemy/`.

### > 1. Configuração (uma vez)

```
pip install -r requirements.txt
alembic init alembic
```

O `alembic init` cria o arquivo `alembic.ini` e a pasta `alembic/`. Dois ajustes no `alembic/env.py` conectam o Alembic ao seu projeto: dizer qual é o modelo (`target_metadata = Base.metadata`, importado do `models.py`) e ler a URL do banco de uma variável de ambiente, em vez de escrevê-la no arquivo. O `env.py` do exemplo já está ajustado.

### > 2. A migration inicial

Com o banco vazio e o `models.py` pronto, o Alembic compara os dois e escreve a migration sozinho:

```
alembic revision --autogenerate -m "cria as tabelas iniciais"
```

```
Detected added table 'usuarios'
Detected added table 'grupos'
Detected added index 'idx_grupos_materia_id' on '('materia_id',)'
...
Generating alembic/versions/93fcab46a778_cria_as_tabelas_iniciais.py ... done
```

O arquivo gerado tem duas funções, `upgrade` (cria as tabelas) e `downgrade` (as apaga). Para aplicar:

```
alembic upgrade head
```

```
Running upgrade  -> 93fcab46a778, cria as tabelas iniciais
```

`head` significa "a versão mais recente". Depois disso, o banco tem as cinco tabelas do projeto, mais a tabela `alembic_version`, e o comando `alembic check` confirma que o modelo e o banco estão iguais (`No new upgrade operations detected`).

### > 3. Mudando o esquema: a coluna `descricao`

Agora a mudança de verdade. Em `models.py`, acrescente uma linha à classe `Grupo`:

```python
descricao: Mapped[str | None] = mapped_column(Text)
```

O `str | None` indica que a coluna aceita valor vazio, o que é obrigatório aqui: as linhas que já existem não têm descrição. Gere e aplique a segunda migration:

```
alembic revision --autogenerate -m "adiciona descricao em grupos"
alembic upgrade head
```

```
Detected added column 'grupos.descricao'
Running upgrade 93fcab46a778 -> 493b688f9baa, adiciona descricao em grupos
```

O corpo da migration gerada é pequeno e legível:

```python
def upgrade() -> None:
    op.add_column('grupos', sa.Column('descricao', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('grupos', 'descricao')
```

Conferindo os dados: o grupo "Cálculo passo a passo", que já existia, continua lá, agora com a coluna `descricao` vazia. Foi uma mudança de estrutura, sem perda de dados.

### > 4. O histórico e o `downgrade`

```
alembic history
```

```
93fcab46a778 -> 493b688f9baa (head), adiciona descricao em grupos
<base> -> 93fcab46a778, cria as tabelas iniciais
```

Para desfazer a última migration:

```
alembic downgrade -1
```

```
Running downgrade 493b688f9baa -> 93fcab46a778, adiciona descricao em grupos
```

A coluna `descricao` desaparece, e os grupos continuam. Mas guarde este aviso: o `downgrade` de uma coluna apaga **o conteúdo dessa coluna**. Se alguém já tivesse preenchido descrições, elas seriam perdidas. Desfazer uma migration é seguro para a estrutura, e não para os dados que ela guardava.

## // Prisma Migrate, em resumo

O ciclo do Prisma é o mesmo, com outros nomes. Você muda o `schema.prisma` (por exemplo, acrescentando `descricao String?` ao model `Grupo`) e roda:

```
npx prisma migrate dev --name adiciona_descricao
```

O comando compara o modelo com o banco, cria uma pasta nova em `prisma/migrations/` com o SQL da mudança, aplica no banco de desenvolvimento e regenera o cliente. Em um ambiente que não é de desenvolvimento, o comando de aplicar migrations já criadas é o `prisma migrate deploy`.

> **AVISO: ESTE TRECHO NÃO FOI EXECUTADO PELO AUTOR**
> O ambiente em que este material foi produzido não conseguiu baixar o motor do Prisma, então o `migrate dev` e o `generate` **não foram testados**. O que está aqui segue a documentação oficial do Prisma 7, consultada em 4 de outubro de 2026. Execute os passos na sua máquina e, se algo divergir, siga a documentação oficial.

> **O PERIGO DO `MIGRATE DEV` EM BANCO COM DADOS**
> Se o Prisma detectar que o banco tem estruturas que não vieram das migrations dele (como as tabelas criadas pelo script SQL do Módulo 09), o `migrate dev` pode propor **resetar o banco**, o que apaga todos os dados. Se aparecer essa pergunta, pare e responda que não. Por isso o banco de testes separado é indispensável.

## // Conectando ao Supabase: qual URL usar

Se o seu banco de testes for um projeto do Supabase, a documentação oficial (consultada em 4 de outubro de 2026) distingue três formas de conexão, e para migrations a escolha importa:

| Conexão | Porta | Quando usar |
|---|---|---|
| Direta | 5432 | Migrations, `pg_dump` e processos de longa duração. Por padrão, usa apenas IPv6 |
| Session pooler | 5432 | Quando a sua rede é só IPv4 e você precisa da mesma finalidade da conexão direta |
| Transaction pooler | 6543 | Aplicações serverless e de curta duração, e não migrations |

Em resumo: **para migrations, use a conexão direta, ou o Session pooler se a sua rede não tiver IPv6.** Não use o Transaction pooler para elas. O botão **Connect** do painel mostra as três strings. E a regra do Módulo 02 continua valendo: a string tem senha, então ela vai no `.env`, e nunca no repositório.

## // Bom exemplo × mau exemplo

**Mau exemplo**: mudar a estrutura direto no Table Editor, ou editar uma migration que já foi aplicada:

Alterar o banco por cliques deixa o histórico sem registro da mudança. E editar o arquivo de uma migration que já rodou em algum banco faz esse banco e o arquivo contarem histórias diferentes.

**Bom exemplo**: uma migration nova para cada mudança, sempre versionada:

```
alembic/versions/
├── 93fcab46a778_cria_as_tabelas_iniciais.py
└── 493b688f9baa_adiciona_descricao_em_grupos.py
```

Cada mudança é um arquivo novo, que entra no Git junto com a alteração do modelo, e a cadeia de versões conta a história completa do banco.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `alembic revision --autogenerate` gera uma migration vazia | O `target_metadata` não está apontando para o `Base.metadata` | Confira o import do `models.py` no `env.py` |
| Coluna nova obrigatória (`not null`) quebra a migration | As linhas que já existem não têm valor para ela | Crie a coluna aceitando vazio, preencha os dados e só depois torne obrigatória, ou defina um valor padrão |
| O banco está em uma versão que o histórico não conhece | Alguém mudou a estrutura sem passar pelas migrations | Use `alembic history` e `alembic current` para comparar, e refaça a mudança por migration |
| `migrate dev` propõe resetar o banco | O banco tem estruturas que não vieram das migrations do Prisma | Responda que não, e use um banco de testes separado |
| Editar uma migration antiga | Parece mais simples do que criar uma nova | Nunca edite uma migration já aplicada: crie uma nova |
| Conexão recusada ao usar a URL direta do Supabase | A conexão direta é só IPv6 por padrão | Use a string do Session pooler (porta 5432) |

## // Prática guiada

1. Crie um banco de testes (local ou um segundo projeto do Supabase) e guarde a URL no `.env`.
2. Em `example/sqlalchemy/`, rode `alembic upgrade head` e confira as cinco tabelas.
3. Acrescente `descricao` ao `Grupo`, gere a segunda migration e aplique.
4. Rode `alembic history` e `alembic current`, e anote as duas versões.
5. Rode `alembic downgrade -1` e confira que a coluna sumiu e os dados dos grupos continuam.

## // Pratique sozinho

> **DESAFIO**
> Crie uma terceira migration que acrescente a coluna `ativo boolean not null default true` à tabela `usuarios`. Aplique, confira que os usuários que já existiam receberam o valor `true`, e depois desfaça com `downgrade`.

## // Aplicando no projeto da semana

1. Adicione ao seu repositório a pasta de migrations (`alembic/` ou `prisma/migrations/`), com a migration inicial do seu projeto.
2. No `docs/arquitetura.md`, registre qual ferramenta você usou e o comando para aplicar as migrations do zero.
3. Commit: `git commit -m "Adiciona o histórico de migrations do projeto"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você aplicou a migration 0002 (que cria uma coluna) no banco de testes e funcionou. Antes de aplicar no banco do entregável, percebe que errou o tipo da coluna. Qual é o caminho correto: editar o arquivo da migration 0002 e rodar de novo?

Resposta: não. O arquivo da 0002 já foi aplicado em um banco, e editá-lo faz o histórico e o banco divergirem. O caminho correto é, no banco de testes, fazer o `downgrade` para antes da 0002, corrigir o modelo e gerar a migration de novo. Se a migration já estivesse em uso em outros bancos, o caminho seria criar uma 0003 que corrige a coluna.

## // Resumo do módulo

- [ ] Sei explicar o que é uma migration, e o que `upgrade` e `downgrade` fazem.
- [ ] Sei o ciclo: mudar o modelo, gerar a migration, versionar, aplicar.
- [ ] Sei usar `alembic revision --autogenerate`, `upgrade`, `downgrade`, `history` e `current`.
- [ ] Sei por que o `downgrade` de uma coluna apaga o conteúdo dela.
- [ ] Sei qual conexão do Supabase usar para migrations.
- [ ] Sei que devo usar um banco de testes separado do banco do entregável.

---

**Próximo módulo:** `15-orms-prisma-e-sqlalchemy.md`, o histórico do banco está sob controle. Falta ver como usar o banco a partir de código.

`Material de Estudo // Coffee & Code`
