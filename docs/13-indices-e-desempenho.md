# Módulo 13, Índices e Desempenho

🇧🇷 Português · 🇺🇸 [English](./13-indices-e-desempenho.en.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

> **TRILHA VETERANO**
> Este módulo faz parte da trilha veterano: ele vem depois do conteúdo essencial e não é necessário para o entregável da semana. Quem segue a trilha principal pode pular para o `entregavel.md`.

Com o banco funcionando e os dados dentro, aparece uma pergunta nova: ele continua rápido quando as tabelas crescem? Este módulo ensina a medir o tempo de uma consulta, a ler o plano de execução que o PostgreSQL escolhe e a criar índices que aceleram as buscas.

## // O problema: o que é rápido com 16 linhas pode ser lento com 300 mil

Com os dados de exemplo, qualquer consulta responde instantaneamente, porque a tabela `participacoes` tem 16 linhas. Mas imagine o Buscador de Grupos de Estudo funcionando de verdade, com milhares de pessoas e centenas de milhares de participações. A consulta que lista as pessoas de um grupo precisa encontrar as linhas certas no meio de todas as outras, e sem ajuda o banco só sabe uma coisa: olhar uma por uma.

## // O que é um índice

> **ÍNDICE: EM PALAVRAS SIMPLES**
> É uma estrutura auxiliar, guardada à parte, que o banco consulta para encontrar linhas sem precisar ler a tabela inteira. Funciona como o índice remissivo no fim de um livro: em vez de folhear todas as páginas atrás de um assunto, você vai direto às páginas indicadas.

<div align="center">
<img src="./assets/indice-vs-varredura.svg" alt="Comparação entre ler todas as linhas uma a uma e usar um índice para ir direto às linhas certas" width="640">
</div>

O tipo de índice mais comum no PostgreSQL é a **árvore B** (*B-tree*), que mantém os valores ordenados e permite achar um deles em poucos passos, mesmo em tabelas enormes.

## // Que índices o PostgreSQL já cria, e quais ele não cria

| Situação | Índice criado automaticamente? |
|---|---|
| Chave primária (`primary key`) | Sim |
| Restrição `unique` | Sim |
| Chave estrangeira (`references`) | **Não** |

O último item é o que mais surpreende: declarar uma chave estrangeira garante a integridade, mas **não acelera** as buscas pela coluna. Se o Dashboard filtra as participações por `grupo_id`, essa coluna precisa de um índice próprio.

## // Medindo antes de otimizar: `explain` e `explain analyze`

Para saber como o banco executa uma consulta, coloque `explain analyze` na frente dela:

```sql
explain analyze
select * from participacoes where grupo_id = 123;
```

O resultado é o **plano de execução**: a lista dos passos que o banco seguiu, com o tempo real de cada um. As partes que importam para quem está começando a ler um plano:

| Trecho do plano | O que significa |
|---|---|
| `Seq Scan` | Varredura sequencial: leu a tabela inteira |
| `Index Scan` ou `Bitmap Index Scan` | Usou um índice para ir direto às linhas |
| `Rows Removed by Filter` | Quantas linhas foram lidas e descartadas |
| `Execution Time` | Tempo total real, em milissegundos |

> **ATENÇÃO COM `EXPLAIN ANALYZE`**
> O `explain analyze` **executa** a consulta de verdade. Com um `select` isso é inofensivo, mas com `update` ou `delete` as alterações acontecem mesmo. Para ensaiar comandos que alteram dados, envolva-os em `begin;` e termine com `rollback;`.

## // O experimento: 300 mil linhas, com e sem índice

O arquivo `example/sql/05-laboratorio-indices.sql` monta um laboratório em um schema separado, chamado `lab`, para não misturar com as tabelas do seu projeto. Ele cria uma tabela parecida com `participacoes`, com 300 mil linhas e nenhum índice, e roda a mesma busca antes e depois de criar o índice.

**Sem índice**, o plano mostra uma varredura sequencial:

```
Parallel Seq Scan on participacoes_teste  (actual time=0.088..25.269 rows=30 loops=2)
  Filter: (grupo_id = 123)
  Rows Removed by Filter: 149970
Execution Time: 35.464 ms
```

O banco leu cerca de 300 mil linhas para devolver 60. Depois de criar o índice:

```sql
create index idx_lab_grupo_id on lab.participacoes_teste (grupo_id);
```

**Com índice**, o plano muda:

```
Bitmap Heap Scan on participacoes_teste  (actual time=0.035..0.126 rows=60 loops=1)
  ->  Bitmap Index Scan on idx_lab_grupo_id  (actual time=0.025..0.025 rows=60 loops=1)
Execution Time: 0.142 ms
```

Nesse teste, a mesma consulta caiu de cerca de 35 ms para cerca de 0,14 ms. Os números mudam de computador para computador, e o que importa é a proporção: o índice trocou a leitura de 300 mil linhas por uma ida direta às 60 certas.

Quando terminar o experimento, apague o laboratório:

```sql
drop schema lab cascade;
```

## // Os índices do projeto

O arquivo `example/sql/04-indices.sql` cria os índices que fazem sentido para o Buscador de Grupos de Estudo:

```sql
create index idx_grupos_materia_id      on grupos (materia_id);
create index idx_participacoes_grupo_id on participacoes (grupo_id);
create index idx_encontros_grupo_id     on encontros (grupo_id);
create index idx_grupos_nome_lower      on grupos (lower(nome_grupo));
```

Os três primeiros indexam chaves estrangeiras, que o PostgreSQL não indexa sozinho. A tabela `participacoes` já tem o índice da chave primária `(usuario_id, grupo_id)`, e ele serve para buscar por `usuario_id`, a primeira coluna do par, mas não ajuda a buscar só por `grupo_id`. Por isso o segundo índice existe.

O quarto é um **índice de expressão**: ele guarda o resultado de `lower(nome_grupo)`, e acelera buscas que ignoram maiúsculas e minúsculas. Em uma tabela de 5 mil grupos, a busca `where lower(nome_grupo) = 'grupo 123'` passou de uma varredura sequencial (cerca de 1,8 ms) para um `Index Scan` (cerca de 0,04 ms).

## // Quando o índice não ajuda

Índice não é remédio universal, e criá-los sem critério tem custo:

- **Quando quase todas as linhas atendem ao filtro.** Em um teste com `where max_participantes = 50`, em que todos os 5 mil grupos tinham esse valor, o banco ignorou o índice e fez uma varredura sequencial, porque ler tudo direto saía mais barato do que passar pelo índice.
- **Em tabelas pequenas.** Com poucas linhas, a varredura sequencial é tão rápida que o banco nem considera o índice.
- **Em buscas de "contém" com curinga no começo**, como `ilike '%sql%'`. O índice em árvore B não ajuda quando o começo do texto é desconhecido (existem outros tipos de índice para isso, que ficam fora do escopo desta semana).
- **O custo de escrita e de espaço.** Cada índice precisa ser atualizado a cada `insert`, `update` e `delete`, e ocupa espaço. No laboratório, a tabela de 300 mil linhas ocupou 13 MB, e o índice sobre `grupo_id` ocupou cerca de 2 MB.

A regra prática: **meça primeiro** com `explain analyze`, crie o índice para a consulta que realmente é lenta, e meça de novo.

## // Bom exemplo × mau exemplo

**Mau exemplo**: criar um índice em toda coluna "por garantia":

```sql
create index on participacoes (entrou_em);
create index on grupos (criado_em);
create index on usuarios (nome_usuario);
```

Cada índice desses deixa as gravações mais lentas e ocupa espaço, sem que nenhuma consulta conhecida precise deles.

**Bom exemplo**: medir, identificar a consulta lenta e criar o índice específico:

```sql
explain analyze select * from participacoes where grupo_id = 123;
-- Seq Scan, 35 ms: confirma o problema
create index idx_participacoes_grupo_id on participacoes (grupo_id);
explain analyze select * from participacoes where grupo_id = 123;
-- Bitmap Index Scan, 0,14 ms: confirma a melhoria
```

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Achar que a chave estrangeira cria índice | A chave primária e o `unique` criam, e a chave estrangeira parece da mesma família | Crie o índice das chaves estrangeiras usadas em filtros e `join` |
| O índice existe, mas o plano mostra `Seq Scan` | Tabela pequena, filtro pouco seletivo ou estatísticas desatualizadas | Rode `analyze` na tabela e teste com mais dados |
| Rodar `explain analyze` em um `delete` e perder dados | O comando é executado de verdade | Envolva em `begin;` e `rollback;` |
| Criar índice para uma busca com `ilike '%texto%'` | O curinga no começo impede o uso do índice em árvore B | Use outro tipo de índice, ou repense a busca |
| Comparar tempos de uma única execução | O primeiro resultado pode ser influenciado por cache | Execute algumas vezes e compare a ordem de grandeza |

## // Prática guiada

1. Rode o `05-laboratorio-indices.sql` no SQL Editor, passo a passo.
2. Compare os dois planos de execução e identifique, em cada um, o tipo de varredura e o `Execution Time`.
3. Anote o tamanho da tabela e do índice.
4. Apague o laboratório com `drop schema lab cascade;`.

## // Pratique sozinho

> **DESAFIO**
> No laboratório, antes de apagar o schema, crie um índice sobre `usuario_id` e compare o plano de `select * from lab.participacoes_teste where usuario_id = 777;` antes e depois. Depois, crie um índice sobre `entrou_em` e teste `where entrou_em = '2026-01-10'`: o banco usa o índice? Por quê?

## // Aplicando no projeto da semana

1. Rode o `04-indices.sql` no banco do projeto e confirme, no Table Editor ou com uma consulta a `pg_indexes`, que os índices foram criados.
2. Registre no `docs/arquitetura.md` quais índices existem e por que cada um foi criado.
3. Commit: `git commit -m "Adiciona os índices do projeto"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você roda `explain analyze` no banco do projeto, com as 16 participações do exemplo, e o plano mostra `Seq Scan` mesmo depois de criar o índice em `grupo_id`. O índice está errado?

Resposta: não necessariamente. Com uma tabela minúscula, ler tudo direto é mais barato do que passar pelo índice, e o banco escolhe a varredura sequencial por isso. O índice passa a fazer diferença quando a tabela cresce. Para ver o efeito, é preciso testar com muitas linhas, como no laboratório deste módulo.

## // Resumo do módulo

- [ ] Sei explicar o que é um índice e quando ele ajuda.
- [ ] Sei que o PostgreSQL cria índice para chave primária e `unique`, mas não para chave estrangeira.
- [ ] Sei usar `explain analyze` e ler os principais trechos do plano.
- [ ] Sei criar um índice simples e um índice de expressão.
- [ ] Sei os casos em que o índice não ajuda e o custo de ter índices demais.

---

**Próximo módulo:** `14-migrations.md`, o banco está rápido. Agora, como mudar a estrutura dele ao longo do tempo sem perder dados.

`Material de Estudo // Coffee & Code`
