# Desafios, Semana 04

🇧🇷 Português · 🇺🇸 [English](./desafios.en.md)

Desafios opcionais, organizados pelos módulos da semana. Nenhum é obrigatório para a entrega básica; veja `entregavel.md` para o que é obrigatório. Use estes desafios se terminou os módulos principais e quer se aprofundar, ou se quer deixar o banco mais robusto.

---

## // Entidades, relacionamentos e DER (Módulos 03 a 05)

**Se você está começando**
- Acrescente ao DER uma entidade nova, `avaliacoes`, em que uma pessoa dá uma nota de 1 a 5 a um grupo do qual participa. Decida a cardinalidade, as chaves e se ela precisa de uma tabela associativa.

**Se você já tem experiência**
- Pesquise sobre o relacionamento recursivo (uma tabela que aponta para ela mesma) e proponha um caso no projeto, como grupos "filhos" de um grupo maior.
- Pesquise a diferença entre os níveis conceitual, lógico e físico de um DER e identifique em qual nível cada diagrama desta semana está.

---

## // Normalização (Módulos 06 e 07)

**Se você está começando**
- Pegue uma planilha sua de verdade (de gastos, de estudos, de uma coleção) e aplique a 1FN, a 2FN e a 3FN, escrevendo as tabelas resultantes.

**Se você já tem experiência**
- Pesquise a Forma Normal de Boyce-Codd (FNBC) e encontre um caso em que a 3FN não basta.
- Pesquise sobre desnormalização consciente e escreva um exemplo, no projeto, em que valeria duplicar um dado de propósito, justificando com uma medição.

---

## // Tipos, chaves e SQL (Módulos 08 a 11)

**Se você está começando**
- Escreva uma consulta que mostre, para cada pessoa, em quantos grupos ela participa, incluindo as pessoas que não participam de nenhum.
- Escreva uma consulta que liste os grupos que ainda têm vagas, ordenados do que tem mais vagas para o que tem menos.

**Se você já tem experiência**
- Pesquise sobre `window functions` (como `row_number()` e `rank()`) e use uma para numerar os grupos de cada matéria pela quantidade de participantes.
- Pesquise sobre `CTE` (a cláusula `with`) e reescreva a consulta de vagas restantes de forma mais legível.
- Pesquise sobre `unique` em mais de uma coluna e crie uma restrição que impeça dois encontros do mesmo grupo no mesmo dia e horário.

---

## // Índices, migrations e ORMs (Módulos 13 a 15)

**Se você está começando**
- Pegue duas consultas do Módulo 11 e rode `explain analyze` em cada uma, anotando o tipo de varredura que o banco escolheu.

**Se você já tem experiência**
- Pesquise sobre índices parciais (`create index ... where ...`) e crie um para uma consulta do projeto que só olha uma parte das linhas.
- Pesquise sobre `pg_stat_statements` e descubra como identificar, em um banco real, quais consultas mais consomem tempo.
- Reescreva todas as consultas do Módulo 11 em SQLAlchemy ou em Prisma e compare o SQL gerado com o SQL que você escreveu à mão.

---

## // Desafio geral (todos)

Escreva, em um arquivo `docs/decisoes.md`, as cinco principais decisões de modelagem do seu projeto, cada uma em duas frases: o que você decidiu e por quê. Exemplos: por que `materias` é uma tabela separada, por que `participantes` não é uma coluna, por que a chave de `participacoes` é composta. Se você conseguir justificar cada uma sem olhar o material, o seu modelo está em um bom nível.
