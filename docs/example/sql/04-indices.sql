-- Trilha veterano: índices (rode depois do schema e do seed).
-- O PostgreSQL cria índice automaticamente para PRIMARY KEY e UNIQUE,
-- mas NÃO para colunas de chave estrangeira.

create index idx_grupos_materia_id      on grupos (materia_id);
create index idx_participacoes_grupo_id on participacoes (grupo_id);
create index idx_encontros_grupo_id     on encontros (grupo_id);

-- Busca por nome de grupo sem diferenciar maiúsculas de minúsculas:
create index idx_grupos_nome_lower on grupos (lower(nome_grupo));

-- Para ver o efeito de um índice com muitas linhas, use o laboratório 05-laboratorio-indices.sql.
-- Comparar o plano de execução antes e depois:
-- explain analyze select * from participacoes where grupo_id = 3;
