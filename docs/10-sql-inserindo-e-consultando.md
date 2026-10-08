# Módulo 10, SQL: Inserindo e Consultando

🇧🇷 Português · 🇺🇸 [English](../docs-eng/10-sql-inserting-and-querying.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

No Módulo 09 você criou as cinco tabelas, mas elas estão vazias. Este módulo ensina a colocar dados nelas (`insert`), a ler o que foi guardado (`select`) e a corrigir ou apagar linhas (`update` e `delete`). É o equivalente em SQL de tudo que você fazia com arrays na Semana 03.

## // O problema: tabelas vazias não respondem nada

O `gruposMock` da Semana 03 tinha seis grupos prontos. Para que o banco tenha o mesmo conteúdo, cada objeto do array precisa virar linhas em tabelas. E, depois, é preciso ter uma forma de perguntar ao banco "quais são os grupos com mais de seis vagas?", que é o que o `.filter()` fazia no JavaScript.

## // `insert`: gravando linhas

```sql
insert into materias (nome, codigo)
values ('Cálculo I', 'MAT101');
```

A lista entre parênteses depois do nome da tabela diz **quais colunas** você vai preencher, e `values` traz os valores, na mesma ordem. As colunas que ficam de fora (como `materia_id`, gerada pelo `identity`) recebem o valor padrão.

Para gravar várias linhas de uma vez, separe os conjuntos de valores por vírgula:

```sql
insert into materias (nome, codigo) values
  ('Estrutura de Dados', 'INF201'),
  ('Banco de Dados',     'INF301');
```

Como você viu no Módulo 09, a ordem importa: as tabelas apontadas por chaves estrangeiras recebem dados primeiro. No projeto, `materias` e `usuarios` antes de `grupos`, e `grupos` e `usuarios` antes de `participacoes`.

## // Do `gruposMock` para as tabelas

Cada objeto do array se desdobra em linhas de mais de uma tabela:

| No `gruposMock` (Semana 03) | No banco |
|---|---|
| `materia: "Cálculo I"` | Uma linha em `materias`, e o `materia_id` dela em `grupos` |
| O nome do grupo | A coluna `nome_grupo` em `grupos` |
| `participantes: 5` | **Some**: vira cinco linhas em `participacoes` |
| `horario: "encontros às terças"` | Uma linha em `encontros` (dia da semana, hora e local) |

O arquivo `example/sql/02-seed.sql` já faz essa conversão para os seis grupos do exemplo. Nele, os ids das matérias estão escritos direto (1, 2, 3...), porque o banco acabou de ser criado e a ordem é conhecida. Em um banco com dados de verdade, o mais seguro é buscar o id com uma subconsulta, em vez de escrevê-lo à mão:

```sql
insert into grupos (nome_grupo, materia_id, max_participantes)
values (
  'Cálculo II na prática',
  (select materia_id from materias where nome = 'Cálculo I'),
  5
);
```

## // `returning`: devolvendo o que foi gravado

O PostgreSQL permite pedir de volta os valores da linha recém-criada, incluindo o id que o banco gerou:

```sql
insert into grupos (nome_grupo, materia_id) values ('Teste', 1)
returning grupo_id, nome_grupo;
```

Isso evita ter que fazer uma segunda consulta só para descobrir o id da linha nova.

## // `select`: lendo os dados

```sql
select * from materias;
```

```
 materia_id |          nome          | codigo
------------+------------------------+--------
          1 | Cálculo I              | MAT101
          2 | Estrutura de Dados     | INF201
          3 | Banco de Dados         | INF301
          4 | Engenharia de Software | INF305
          5 | Redes de Computadores  | INF310
          6 | Sistemas Operacionais  | INF315
```

O `*` significa "todas as colunas". Para escolher só as que interessam, liste-as:

```sql
select nome_grupo, max_participantes from grupos;
```

### > Filtrando com `where`

```sql
select nome_grupo, max_participantes
from grupos
where max_participantes >= 6
order by nome_grupo;
```

```
       nome_grupo       | max_participantes
------------------------+-------------------
 Cálculo passo a passo  |                 6
 Modelagem e SQL        |                 8
 Redes na unha          |                 6
```

Os operadores mais usados no `where`:

| Operador | Uso | Exemplo |
|---|---|---|
| `=`, `<>`, `<`, `>`, `<=`, `>=` | Comparar valores | `max_participantes >= 6` |
| `and`, `or`, `not` | Combinar condições | `materia_id = 1 and max_participantes > 4` |
| `in (...)` | Um de vários valores | `materia_id in (1, 3)` |
| `ilike` | Texto parecido, sem diferenciar maiúsculas | `nome_grupo ilike '%sql%'` |
| `is null` | A coluna está vazia | `descricao is null` |

No `ilike`, o símbolo `%` significa "qualquer sequência de caracteres". Por isso `'%sql%'` encontra o grupo "Modelagem e SQL". É o equivalente, no banco, do `.includes()` que a busca do Dashboard usava na Semana 03.

### > Ordenando e limitando

```sql
select nome_grupo, max_participantes
from grupos
order by max_participantes desc, nome_grupo
limit 3;
```

`order by` ordena (`desc` inverte a ordem), e `limit` devolve só as primeiras linhas.

## // `update` e `delete`: corrigindo e apagando

```sql
update grupos
set max_participantes = 12
where nome_grupo = 'Modelagem e SQL';
```

```sql
delete from participacoes
where usuario_id = 1 and grupo_id = 2;
```

O segundo comando é, em SQL, o "Sair do grupo" do Perfil da Semana 03: remove a linha que liga a pessoa ao grupo, e mais nada.

> **O PERIGO DO `WHERE` ESQUECIDO**
> `update` e `delete` sem `where` afetam **todas** as linhas da tabela. `delete from participacoes;` apaga as participações de todas as pessoas, sem pedir confirmação. O hábito que evita o susto: escreva primeiro um `select` com o mesmo `where`, confira quais linhas apareceram, e só então troque o `select` por `update` ou `delete`.

Duas ajudas do PostgreSQL para ensaiar sem risco: o `returning` também funciona em `update` e `delete`, mostrando as linhas afetadas, e é possível envolver o comando em `begin;` e terminar com `rollback;` para desfazer tudo.

## // O que o `.filter()`, `.find()` e companhia viram em SQL

| JavaScript (Semana 03) | SQL |
|---|---|
| `lista.filter(...)` | `select ... where ...` |
| `lista.find(...)` | `select ... where ... limit 1` |
| `lista.push(item)` | `insert into ...` |
| `lista.filter(g => g.id !== id)` (remover) | `delete from ... where ...` |
| Alterar uma propriedade de um objeto | `update ... set ... where ...` |
| `lista.sort(...)` | `order by ...` |

## // Bom exemplo × mau exemplo

**Mau exemplo**: um `update` sem `where`:

```sql
update grupos set max_participantes = 12;
```

Todos os seis grupos passam a ter limite de 12 participantes.

**Bom exemplo**: o mesmo `update`, restrito à linha certa:

```sql
update grupos set max_participantes = 12
where nome_grupo = 'Modelagem e SQL';
```

Só um grupo muda, e o comando informa `UPDATE 1`, confirmando que uma única linha foi afetada.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `violates foreign key constraint` ao inserir | A linha apontada ainda não existe | Insira primeiro na tabela apontada |
| `duplicate key value violates unique constraint "participacoes_pkey"` | A pessoa já participa daquele grupo | Confira o que já existe antes de inserir |
| Esquecer o `where` em um `update` ou `delete` | O comando funciona mesmo assim | Teste com `select` antes, e use `begin` e `rollback` para ensaiar |
| Comparar texto com aspas duplas (`"Cálculo I"`) | Em JavaScript as duas aspas valem | Em SQL, texto usa aspas simples: `'Cálculo I'` |
| Esquecer o `%` no `ilike` | O padrão exige correspondência exata sem ele | Use `'%termo%'` para procurar um pedaço do texto |

## // Prática guiada

1. Rode o `01-schema.sql` e depois o `02-seed.sql` (que está em `example/sql/`) no SQL Editor.
2. Rode `select * from materias;` e confira as seis matérias.
3. Escreva um `select` que traga só os grupos com limite de 6 participantes ou mais, em ordem alfabética.
4. Escreva um `select` com `ilike` que encontre os grupos cujo nome contém "prática".
5. Ensaie um `delete` seguro: dentro de `begin;`, apague uma participação, confira com `select`, e termine com `rollback;`.

## // Pratique sozinho

> **DESAFIO**
> Escreva um `insert` que crie uma nova matéria, "Cálculo II" (código MAT102), e depois um segundo `insert` que crie um grupo dessa matéria, buscando o `materia_id` com uma subconsulta, sem escrever o número à mão.

## // Aplicando no projeto da semana

1. Salve o seu script de dados em `sql/02-seed.sql`, convertendo os dados do seu `gruposMock` em `insert`.
2. Rode no Supabase e confira cada tabela no Table Editor.
3. Commit: `git commit -m "Adiciona o script de dados iniciais"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você roda `delete from participacoes;` sem `where`. O que acontece, e que hábito teria evitado o problema?

Resposta: todas as linhas da tabela `participacoes` são apagadas, ou seja, todas as pessoas "saem" de todos os grupos de uma vez, sem confirmação. O hábito que evita isso é escrever primeiro um `select` com o mesmo `where` e conferir as linhas que aparecem. Ensaiar dentro de `begin;` e terminar com `rollback;` também desfaz o estrago.

## // Resumo do módulo

- [ ] Sei gravar linhas com `insert`, incluindo várias de uma vez e com `returning`.
- [ ] Sei converter um objeto do `gruposMock` em linhas de várias tabelas.
- [ ] Sei ler dados com `select`, `where`, `order by` e `limit`.
- [ ] Sei usar `update` e `delete`, e por que o `where` é indispensável.
- [ ] Sei o que cada método de array da Semana 03 vira em SQL.

---

**Próximo módulo:** `11-sql-join-e-agregacoes.md`, os dados estão no banco e as consultas simples funcionam. Falta cruzar tabelas e contar resultados.

`Material de Estudo // Coffee & Code`
