# Módulo 09, SQL: Criando as Tabelas

🇧🇷 Português · 🇺🇸 [English](./09-sql-criando-as-tabelas.en.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

Você tem o DER e o dicionário de dados. Este módulo transforma os dois em tabelas reais, no seu projeto do Supabase, usando a linguagem SQL. É o momento em que o desenho vira banco.

## // O problema: como "dizer" ao banco o que criar

O banco não lê o seu desenho. Ele aceita comandos escritos em SQL, e é através deles que você descreve cada tabela, cada coluna e cada regra. A boa notícia é que o dicionário de dados do Módulo 08 já contém tudo que o comando precisa.

## // O que é SQL

> **SQL: EM PALAVRAS SIMPLES**
> É a linguagem usada para conversar com um banco relacional. Ela é declarativa: você descreve **o que** quer, e o banco decide **como** fazer.

Os comandos de SQL se dividem em famílias, de acordo com o que fazem:

| Família | Para que serve | Comandos | Onde aparece |
|---|---|---|---|
| DDL | Definir a estrutura do banco | `create`, `alter`, `drop` | Este módulo |
| DML | Alterar os dados | `insert`, `update`, `delete` | Módulo 10 |
| DQL | Consultar os dados | `select` | Módulos 10 e 11 |

## // Anatomia de um `create table`

Veja a tabela `materias`, a mais simples do projeto:

```sql
create table materias (
  materia_id  bigint generated always as identity primary key,
  nome        text not null unique,
  codigo      text not null unique
);
```

O comando lê quase como uma frase:

1. `create table materias`: crie uma tabela chamada `materias`.
2. Entre parênteses, uma coluna por linha, separadas por vírgula: o **nome**, o **tipo** e as **restrições**.
3. `primary key`, `not null` e `unique` são as restrições do dicionário de dados.
4. O comando termina com ponto e vírgula.

Em uma tabela com chave estrangeira, a coluna ganha o `references`:

<div align="center">
<img src="./assets/der-para-ddl.svg" alt="O DER de materias e grupos ao lado do comando create table da tabela grupos, com cada parte numerada" width="640">
</div>

## // A ordem importa: a tabela apontada vem primeiro

Uma chave estrangeira precisa apontar para uma tabela que **já existe**. Se você tentar criar `grupos` antes de `materias`, o banco recusa:

```
ERROR:  relation "materias" does not exist
```

A regra é criar primeiro as tabelas que ninguém referencia, e depois as que dependem delas. No projeto, a ordem é esta:

1. `materias` (não depende de ninguém)
2. `usuarios` (não depende de ninguém)
3. `grupos` (depende de `materias`)
4. `participacoes` (depende de `usuarios` e `grupos`)
5. `encontros` (depende de `grupos`)

## // O script completo do projeto

Este é o script que cria o banco inteiro. Ele também está no arquivo `example/sql/01-schema.sql`:

```sql
create table usuarios (
  usuario_id    bigint generated always as identity primary key,
  nome_usuario  text not null,
  email         text not null unique,
  criado_em     timestamptz not null default now()
);

create table materias (
  materia_id  bigint generated always as identity primary key,
  nome        text not null unique,
  codigo      text not null unique
);

create table grupos (
  grupo_id           bigint generated always as identity primary key,
  nome_grupo         text not null,
  materia_id         bigint not null references materias (materia_id),
  max_participantes  integer not null default 10 check (max_participantes > 0),
  criado_em          timestamptz not null default now()
);

create table participacoes (
  usuario_id  bigint not null references usuarios (usuario_id) on delete cascade,
  grupo_id    bigint not null references grupos (grupo_id) on delete cascade,
  entrou_em   date not null default current_date,
  primary key (usuario_id, grupo_id)
);

create table encontros (
  encontro_id  bigint generated always as identity primary key,
  grupo_id     bigint not null references grupos (grupo_id) on delete cascade,
  dia_semana   smallint not null check (dia_semana between 1 and 7),
  hora_inicio  time not null,
  local        text not null
);

alter table usuarios       enable row level security;
alter table materias       enable row level security;
alter table grupos         enable row level security;
alter table participacoes  enable row level security;
alter table encontros      enable row level security;
```

As cinco linhas finais ligam o RLS que o Módulo 02 explicou. Ele é a camada que decide quais linhas a API do Supabase pode enxergar, e ligá-lo em toda tabela exposta é a prática de segurança recomendada.

## // Rodando o script no Supabase

1. Abra o **SQL Editor** do seu projeto e crie uma nova consulta.
2. Cole o script completo e execute.
3. Abra o **Table Editor** e confirme que as cinco tabelas aparecem na lista.
4. Clique em cada tabela e confira que as colunas e os tipos batem com o dicionário de dados.

## // Corrigindo um erro: `alter` e `drop`

Se você notar um problema depois de criar, existem dois caminhos. Para **acrescentar ou remover uma coluna**, use `alter table`:

```sql
alter table grupos add column descricao text;
alter table grupos drop column descricao;
```

Para **apagar uma tabela inteira**, use `drop table`:

```sql
drop table encontros;
```

> **CUIDADO COM O `DROP`**
> `drop table` apaga a tabela e todos os dados dela, sem confirmação e sem volta. Agora, com o banco vazio, recriar é inofensivo. Com dados de verdade, o caminho correto são as migrations, que o Módulo 14 apresenta na trilha veterano.

## // Bom exemplo × mau exemplo

**Mau exemplo**: criar as tabelas só com cliques no Table Editor:

Os cliques funcionam, mas não deixam rastro. Daqui a um mês, ninguém sabe exatamente o que foi feito, e recriar o banco em outro projeto exige repetir tudo de memória.

**Bom exemplo**: criar com um script SQL, salvo no repositório:

```
sql/
├── 01-schema.sql
└── 02-seed.sql
```

O script é a documentação exata do banco: pode ser lido, versionado no Git e executado de novo em qualquer projeto, com o mesmo resultado.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `relation "materias" does not exist` | A tabela apontada ainda não foi criada | Crie primeiro as tabelas que ninguém referencia |
| `syntax error at or near ...` | Uma vírgula, parêntese ou palavra faltando | Releia o comando: cada coluna termina com vírgula, menos a última |
| `relation "materias" already exists` | Rodar o mesmo `create table` duas vezes | Confira o Table Editor antes de repetir, ou apague a tabela com `drop table` se for recomeçar |
| Esquecer o ponto e vírgula entre comandos | Em um script com vários comandos, ele separa um do outro | Termine cada comando com `;` |
| Esquecer o `enable row level security` | O banco aceita a tabela sem ele | Rode o `alter table ... enable row level security` para cada tabela |

## // Prática guiada

1. Escreva, em um arquivo `sql/01-schema.sql` do seu repositório, o script completo do seu projeto, seguindo o dicionário de dados.
2. Confira a ordem de criação das tabelas.
3. Cole o script no SQL Editor do Supabase e execute.
4. Abra o Table Editor e confirme que todas as tabelas e colunas foram criadas.
5. Compare o Table Editor com o seu DER: as tabelas e as ligações batem?

## // Pratique sozinho

> **DESAFIO**
> Acrescente ao banco uma coluna `descricao text` na tabela `grupos`, usando `alter table`. Depois, remova a coluna. Confira no Table Editor, após cada comando, o que mudou.

## // Aplicando no projeto da semana

1. Salve o `01-schema.sql` no repositório, em uma pasta `sql/`.
2. Confirme, no Supabase, que as tabelas existem e que o RLS está ligado em todas.
3. Commit: `git commit -m "Adiciona o script de criação das tabelas"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Por que a tabela `participacoes` precisa vir depois de `usuarios` e de `grupos` no script, e a tabela `materias` pode vir em qualquer ponto antes de `grupos`?

Resposta: porque `participacoes` tem duas chaves estrangeiras, uma para `usuarios` e outra para `grupos`, e cada uma só pode apontar para uma tabela que já existe. A `materias` não aponta para ninguém, então só precisa existir antes de quem a referencia, que é a `grupos`.

## // Resumo do módulo

- [ ] Sei o que é SQL e as três famílias de comandos (DDL, DML e DQL).
- [ ] Sei escrever um `create table` com colunas, tipos e restrições.
- [ ] Sei por que a ordem de criação importa.
- [ ] Executei o script no SQL Editor e conferi as tabelas no Table Editor.
- [ ] Sei usar `alter table` e conheço o risco do `drop table`.

---

**Próximo módulo:** `10-sql-inserindo-e-consultando.md`, as tabelas existem, mas estão vazias. Hora de colocar dados e fazer as primeiras consultas.

`Material de Estudo // Coffee & Code`
