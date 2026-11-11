BEGIN;

-- Contagens esperadas: 8 usuarios, 6 categorias, 10 associacoes,
-- 6 solicitacoes e 4 avaliacoes.
INSERT INTO usuarios (id, nome, email, telefone, tipo) VALUES
    (1, 'Joao Silva', 'joao.silva@example.com', '(41) 99999-0001', 'profissional'),
    (2, 'Ana Costa', 'ana.costa@example.com', '(41) 99999-0002', 'profissional'),
    (3, 'Paula Mendes', 'paula.mendes@example.com', '(41) 99999-0003', 'profissional'),
    (4, 'Lucas Almeida', 'lucas.almeida@example.com', '(41) 99999-0004', 'profissional'),
    (5, 'Fernanda Rocha', 'fernanda.rocha@example.com', '(41) 99999-0005', 'profissional'),
    (6, 'Marina Oliveira', 'marina.oliveira@example.com', '(41) 99999-0006', 'cliente'),
    (7, 'Rafael Santos', 'rafael.santos@example.com', '(41) 99999-0007', 'cliente'),
    (8, 'Camila Ferreira', 'camila.ferreira@example.com', '(41) 99999-0008', 'cliente');

INSERT INTO categorias (id, nome, descricao) VALUES
    (1, 'Reparos', 'Montagem de moveis e pequenos consertos.'),
    (2, 'Eletrica', 'Instalacoes e manutencao eletrica.'),
    (3, 'Hidraulica', 'Reparos em torneiras, canos e encanamentos.'),
    (4, 'Limpeza', 'Limpeza residencial e organizacao.'),
    (5, 'Informatica', 'Computadores, redes e suporte tecnico.'),
    (6, 'Pintura', 'Pintura de ambientes e acabamento.');

INSERT INTO profissionais_categorias (profissional_id, categoria_id) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 3),
    (3, 4),
    (4, 1),
    (4, 5),
    (5, 1),
    (5, 6),
    (3, 1);

INSERT INTO solicitacoes (
    id, cliente_id, profissional_id, categoria_id, descricao, status
) VALUES
    (1, 6, 1, 2, 'Instalar uma luminaria na sala.', 'concluida'),
    (2, 7, 2, 3, 'Consertar uma torneira com vazamento.', 'concluida'),
    (3, 8, 3, 4, 'Fazer limpeza detalhada do apartamento.', 'concluida'),
    (4, 6, 4, 5, 'Verificar computador que nao inicia.', 'concluida'),
    (5, 7, 5, 6, 'Pintar uma parede do quarto.', 'em_andamento'),
    (6, 8, 1, 2, 'Revisar tomadas da cozinha.', 'solicitada');

INSERT INTO avaliacoes (id, solicitacao_id, nota, comentario) VALUES
    (1, 1, 5, 'Servico pontual e bem executado.'),
    (2, 2, 4, 'Problema resolvido com rapidez.'),
    (3, 3, 5, 'Apartamento ficou muito limpo.'),
    (4, 4, 5, 'Computador voltou a funcionar.');

SELECT setval(pg_get_serial_sequence('usuarios', 'id'), (SELECT MAX(id) FROM usuarios));
SELECT setval(pg_get_serial_sequence('categorias', 'id'), (SELECT MAX(id) FROM categorias));
SELECT setval(pg_get_serial_sequence('solicitacoes', 'id'), (SELECT MAX(id) FROM solicitacoes));
SELECT setval(pg_get_serial_sequence('avaliacoes', 'id'), (SELECT MAX(id) FROM avaliacoes));

COMMIT;
