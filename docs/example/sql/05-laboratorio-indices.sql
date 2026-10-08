-- Trilha veterano: laboratório de índices.
-- Roda em um schema separado (lab), para não misturar com as tabelas do projeto.
-- Os números de tempo mudam de computador para computador; o que importa é a proporção.

create schema lab;

-- 300 mil linhas parecidas com a tabela participacoes, sem nenhum índice
create table lab.participacoes_teste as
select u as usuario_id,
       1 + ((u * 7 + k * 131) % 5000) as grupo_id,
       date '2026-01-01' + (k % 200)  as entrou_em
from generate_series(1, 50000) u, generate_series(1, 6) k;

analyze lab.participacoes_teste;

-- 1. Sem índice
explain analyze select * from lab.participacoes_teste where grupo_id = 123;

-- 2. Com índice
create index idx_lab_grupo_id on lab.participacoes_teste (grupo_id);
analyze lab.participacoes_teste;
explain analyze select * from lab.participacoes_teste where grupo_id = 123;

-- 3. Tamanho da tabela e do índice
select relname, pg_size_pretty(pg_relation_size(oid)) as tamanho
from pg_class
where relname in ('participacoes_teste', 'idx_lab_grupo_id');

-- Limpeza: apaga o laboratório inteiro
-- drop schema lab cascade;
