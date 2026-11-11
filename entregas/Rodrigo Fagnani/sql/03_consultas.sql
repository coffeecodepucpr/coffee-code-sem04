-- JOIN: solicitacoes com cliente, profissional e categoria.
SELECT
    s.id AS solicitacao_id,
    cliente.nome AS cliente,
    profissional.nome AS profissional,
    categoria.nome AS categoria,
    s.status
FROM solicitacoes AS s
JOIN usuarios AS cliente ON cliente.id = s.cliente_id
JOIN usuarios AS profissional ON profissional.id = s.profissional_id
JOIN categorias AS categoria ON categoria.id = s.categoria_id
ORDER BY s.id;

-- GROUP BY: quantidade de solicitacoes por status.
SELECT status, COUNT(*) AS quantidade
FROM solicitacoes
GROUP BY status
ORDER BY status;

-- LEFT JOIN: inclui categorias mesmo que ainda nao tenham profissionais.
SELECT
    categoria.nome AS categoria,
    COUNT(pc.profissional_id) AS quantidade_profissionais
FROM categorias AS categoria
LEFT JOIN profissionais_categorias AS pc
    ON pc.categoria_id = categoria.id
GROUP BY categoria.id, categoria.nome
ORDER BY categoria.nome;

-- Conferencia das contagens do script de dados.
SELECT 'usuarios' AS tabela, COUNT(*) AS quantidade FROM usuarios
UNION ALL
SELECT 'categorias', COUNT(*) FROM categorias
UNION ALL
SELECT 'profissionais_categorias', COUNT(*) FROM profissionais_categorias
UNION ALL
SELECT 'solicitacoes', COUNT(*) FROM solicitacoes
UNION ALL
SELECT 'avaliacoes', COUNT(*) FROM avaliacoes
ORDER BY tabela;
