# Módulo 08, Tipos de Dados e Chaves

🇧🇷 Português · 🇺🇸 [English](./08-tipos-de-dados-e-chaves.en.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

O DER está desenhado e verificado até a 3FN. Falta decidir os detalhes que o banco exige para criar cada tabela: o **tipo** de cada coluna e as **chaves** que ligam e protegem os dados. É a passagem do nível lógico para o nível físico do modelo, e fecha o desenho antes de qualquer SQL.

## // O problema: o banco precisa saber o que cada coluna guarda

Um array do JavaScript aceita qualquer coisa em qualquer posição. Um banco relacional é o contrário: cada coluna tem um **tipo** declarado, e o banco recusa o que não combina. Isso é uma vantagem, porque erros que passariam despercebidos no array (um texto onde devia haver um número) são barrados na entrada.

## // Os tipos mais usados no PostgreSQL

| Tipo | Guarda | Usado no projeto |
|---|---|---|
| `text` | Texto de qualquer tamanho | `nome_usuario`, `nome_grupo`, `local` |
| `integer` | Número inteiro comum | `max_participantes` |
| `smallint` | Número inteiro pequeno | `dia_semana` |
| `bigint` | Número inteiro grande | os identificadores (`usuario_id`, `grupo_id`) |
| `boolean` | Verdadeiro ou falso | (não usado nesta semana) |
| `date` | Uma data, sem hora | `entrou_em` |
| `time` | Uma hora do dia, sem data | `hora_inicio` |
| `timestamptz` | Um instante exato no tempo (guardado em UTC) | `criado_em` |
| `numeric` | Número decimal exato (valores monetários, por exemplo) | (não usado nesta semana) |

Duas dicas que evitam dor de cabeça. No PostgreSQL, `text` não é mais lento que `varchar(n)`, então use `text` e, se precisar limitar o tamanho, faça isso com uma restrição `check`. E, para representar um momento real no tempo, geralmente prefira `timestamptz` a `timestamp`: o PostgreSQL interpreta o fuso horário informado, converte o instante para UTC internamente e o mostra de acordo com o fuso configurado na sessão. Repare que ele guarda o **instante**, e não o fuso original que foi digitado.

## // Chave primária

> **CHAVE PRIMÁRIA: EM PALAVRAS SIMPLES**
> É a coluna (ou o conjunto de colunas) cujo valor identifica cada linha de forma única. Nunca é vazia e nunca se repete.

Existem duas formas de escolher a chave primária:

- **Chave natural:** um dado que já existe e é único no mundo real, como o e-mail. O risco é que dados reais mudam: se uma pessoa trocar de e-mail, todas as tabelas que o referenciam precisariam ser atualizadas.
- **Chave artificial (substituta):** um número gerado pelo próprio banco, sem significado no mundo real. Ela nunca precisa mudar, e é a escolha mais segura.

O projeto usa chaves artificiais, geradas assim:

```sql
usuario_id  bigint generated always as identity primary key
```

`generated always as identity` pede ao banco que numere sozinho cada nova linha (1, 2, 3, ...). É o formato padrão do SQL, e substitui o antigo `serial` que ainda aparece em tutoriais.

> **O IDENTITY PODE PULAR NÚMEROS**
> O contador do `identity` não volta atrás. Se um `insert` falhar, o número que seria usado é descartado, e a próxima linha recebe o seguinte. Por isso uma tabela pode ter ids 1, 2, 5, 6. Isso é normal e não indica nenhum problema: o id serve para identificar, não para contar.

A tabela `participacoes` usa uma **chave primária composta**, formada por duas colunas. O par `(usuario_id, grupo_id)` identifica cada linha, e isso impede, ao mesmo tempo, que a mesma pessoa entre duas vezes no mesmo grupo.

## // Chave estrangeira

> **CHAVE ESTRANGEIRA: EM PALAVRAS SIMPLES**
> É a coluna que guarda o identificador de uma linha de outra tabela, e que o banco obriga a apontar para uma linha que existe de verdade.

<div align="center">
<img src="./assets/pk-fk-ligacao.svg" alt="A coluna materia_id da tabela grupos apontando para a chave primária da tabela materias" width="640">
</div>

Na declaração, a chave estrangeira usa a palavra `references`:

```sql
materia_id  bigint not null references materias (materia_id)
```

Com isso, o banco passa a conferir a ligação em toda operação. Tentar inserir um grupo com uma matéria que não existe resulta em um erro:

```
ERROR:  insert or update on table "grupos" violates foreign key constraint "grupos_materia_id_fkey"
DETAIL:  Key (materia_id)=(999) is not present in table "materias".
```

O banco também protege o caminho contrário. Apagar uma matéria que ainda tem grupos é recusado:

```
ERROR:  update or delete on table "materias" violates foreign key constraint "grupos_materia_id_fkey" on table "grupos"
DETAIL:  Key (materia_id)=(1) is still referenced from table "grupos".
```

### > O que acontece ao apagar: `on delete`

Para cada chave estrangeira, você decide o que fazer quando a linha apontada for apagada:

| Opção | Efeito | Onde o projeto usa |
|---|---|---|
| (padrão) | Recusa apagar enquanto existirem linhas apontando | `grupos` apontando para `materias` |
| `on delete cascade` | Apaga também as linhas que apontam | `participacoes` e `encontros` apontando para `grupos` |
| `on delete set null` | Deixa as linhas, mas esvazia a coluna que apontava | (não usado nesta semana) |

A escolha segue o significado dos dados: sem o grupo, as suas participações e encontros não fazem sentido e podem sumir junto. Já uma matéria com grupos não deve ser apagada por descuido, e o banco impede.

## // Outras restrições

Além das chaves, cada coluna pode ter regras que o banco aplica sempre:

| Restrição | O que garante | Exemplo no projeto |
|---|---|---|
| `not null` | A coluna nunca fica vazia | `nome_usuario` |
| `unique` | Nenhum valor se repete na coluna | `email` |
| `default` | Valor usado quando nada é informado | `criado_em` recebe `now()` |
| `check` | Uma condição que todo valor precisa cumprir | `max_participantes > 0` |

Quando uma regra é violada, o banco recusa a operação e diz qual foi:

```
ERROR:  duplicate key value violates unique constraint "usuarios_email_key"
DETAIL:  Key (email)=(ana.martins@exemplo.com) already exists.

ERROR:  new row for relation "grupos" violates check constraint "grupos_max_participantes_check"

ERROR:  null value in column "nome_usuario" of relation "usuarios" violates not-null constraint
```

Essas mensagens são a proteção funcionando: elas evitam, no banco, os problemas que o array do `script.js` deixava passar.

## // Convenção de nomes do projeto

- Tabelas no **plural** (`usuarios`), colunas no **singular** (`nome_usuario`).
- Tudo em minúsculas, com palavras separadas por `_`, **sem acentos**, para nunca precisar de aspas nos comandos.
- A chave primária de cada tabela se chama `<tabela no singular>_id`, e a chave estrangeira que aponta para ela usa o mesmo nome (`materia_id` em `materias` e em `grupos`).

## // O dicionário de dados do projeto

O dicionário de dados reúne, em um só lugar, o tipo e as restrições de cada coluna. É o documento que une o DER ao SQL do próximo módulo:

| Tabela | Coluna | Tipo | Restrições |
|---|---|---|---|
| usuarios | `usuario_id` | bigint | chave primária, identity |
| usuarios | `nome_usuario` | text | not null |
| usuarios | `email` | text | not null, unique |
| usuarios | `criado_em` | timestamptz | not null, default now() |
| materias | `materia_id` | bigint | chave primária, identity |
| materias | `nome` | text | not null, unique |
| materias | `codigo` | text | not null, unique |
| grupos | `grupo_id` | bigint | chave primária, identity |
| grupos | `nome_grupo` | text | not null |
| grupos | `materia_id` | bigint | not null, referencia materias |
| grupos | `max_participantes` | integer | not null, default 10, check maior que 0 |
| grupos | `criado_em` | timestamptz | not null, default now() |
| participacoes | `usuario_id` | bigint | chave primária composta, referencia usuarios, cascade |
| participacoes | `grupo_id` | bigint | chave primária composta, referencia grupos, cascade |
| participacoes | `entrou_em` | date | not null, default current_date |
| encontros | `encontro_id` | bigint | chave primária, identity |
| encontros | `grupo_id` | bigint | not null, referencia grupos, cascade |
| encontros | `dia_semana` | smallint | not null, check entre 1 e 7 (1 = segunda) |
| encontros | `hora_inicio` | time | not null |
| encontros | `local` | text | not null |

## // Bom exemplo × mau exemplo

**Mau exemplo**: uma data guardada como texto:

```
data (texto):  '10/09/2026'   '15/08/2026'   '9/09/2026'
ordenadas:     10/09/2026     15/08/2026     9/09/2026
```

Ordenado como texto, "10/09" vem antes de "15/08" e de "9/09", porque o banco compara caractere por caractere. Além disso, nada impede de guardar "31/02/2026".

**Bom exemplo**: o tipo `date`:

```
data (date):   2026-08-15   2026-09-09   2026-09-10
```

O banco entende a data, ordena na ordem do calendário e recusa datas que não existem.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Usar `text` para tudo | É o tipo que aceita qualquer coisa | Escolha o tipo que representa o dado: `date` para datas, `integer` para quantidades |
| Usar o e-mail como chave primária | Parece natural, já que é único | Use um id artificial e deixe o e-mail como `unique` |
| Estranhar os pulos nos ids | O `identity` descarta números de operações que falharam | Lembre que o id serve para identificar, não para contar |
| Esquecer o `not null` em chaves estrangeiras obrigatórias | O banco aceita a coluna vazia | Se o relacionamento é obrigatório (mínimo 1), coloque `not null` |
| Esquecer o `on delete` | O padrão recusa apagar | Decida, para cada chave estrangeira, se o correto é recusar ou apagar em cascata |

## // Prática guiada

1. Pegue o DER do seu projeto e, para cada coluna, escolha o tipo.
2. Marque a chave primária de cada tabela e decida se ela é artificial ou natural.
3. Para cada chave estrangeira, decida o `on delete` e justifique em uma frase.
4. Liste as restrições `not null`, `unique` e `check` que o seu projeto precisa.
5. Monte o dicionário de dados no mesmo formato da tabela desta seção.

## // Pratique sozinho

> **DESAFIO**
> Na biblioteca dos módulos anteriores, o empréstimo guarda uma data de retirada e uma data prevista de devolução. Qual `check` você criaria para garantir que a devolução nunca seja anterior à retirada? Escreva a condição em uma linha.

## // Aplicando no projeto da semana

1. Salve o dicionário de dados do seu projeto no `docs/arquitetura.md`, na seção "Dicionário de dados".
2. Confira se cada relacionamento do DER tem a sua chave estrangeira no dicionário.
3. Commit: `git commit -m "Adiciona o dicionário de dados do projeto"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Por que usar o `email` como chave primária da tabela `usuarios` seria um risco, mesmo ele sendo único?

Resposta: porque a chave primária é copiada para as chaves estrangeiras de outras tabelas (como em `participacoes`), e um e-mail pode mudar. Se uma pessoa trocar de e-mail, o valor precisaria ser alterado em todas as tabelas que a referenciam, e qualquer falha deixaria dados órfãos. Um id artificial nunca muda, e o e-mail fica protegido pela restrição `unique`.

## // Resumo do módulo

- [ ] Sei escolher o tipo adequado para cada coluna.
- [ ] Sei a diferença entre chave natural e chave artificial, e o que é `identity`.
- [ ] Sei o que é uma chave primária composta e quando usá-la.
- [ ] Sei declarar uma chave estrangeira e escolher o `on delete`.
- [ ] Sei usar `not null`, `unique`, `default` e `check`.
- [ ] Tenho o dicionário de dados do meu projeto.

---

**Próximo módulo:** `09-sql-criando-as-tabelas.md`, o desenho está completo, com tipos e chaves. Hora de transformá-lo em tabelas de verdade.

`Material de Estudo // Coffee & Code`
