-- Dados de exemplo: os mesmos grupos do gruposMock da Semana 03, agora em tabelas.

insert into materias (nome, codigo) values
  ('Cálculo I',              'MAT101'),
  ('Estrutura de Dados',     'INF201'),
  ('Banco de Dados',         'INF301'),
  ('Engenharia de Software', 'INF305'),
  ('Redes de Computadores',  'INF310'),
  ('Sistemas Operacionais',  'INF315');

insert into usuarios (nome_usuario, email) values
  ('Ana Martins',   'ana.martins@exemplo.com'),
  ('Bruno Lima',    'bruno.lima@exemplo.com'),
  ('Carla Souza',   'carla.souza@exemplo.com'),
  ('Diego Rocha',   'diego.rocha@exemplo.com'),
  ('Elisa Prado',   'elisa.prado@exemplo.com'),
  ('Felipe Nunes',  'felipe.nunes@exemplo.com'),
  ('Gabriela Dias', 'gabriela.dias@exemplo.com'),
  ('Henrique Melo', 'henrique.melo@exemplo.com');

-- materia_id vem da ordem de inserção acima (1 = Cálculo I, 2 = Estrutura de Dados, ...)
insert into grupos (nome_grupo, materia_id, max_participantes) values
  ('Cálculo passo a passo',   1, 6),
  ('Estruturas na prática',   2, 5),
  ('Modelagem e SQL',         3, 8),
  ('Requisitos e histórias',  4, 5),
  ('Redes na unha',           5, 6),
  ('Processos e memória',     6, 4);

insert into participacoes (usuario_id, grupo_id, entrou_em) values
  (1, 1, '2026-09-01'), (1, 2, '2026-09-03'), (1, 3, '2026-09-05'),
  (2, 1, '2026-09-02'), (2, 3, '2026-09-06'),
  (3, 2, '2026-09-05'), (3, 3, '2026-09-07'), (3, 4, '2026-09-08'),
  (4, 3, '2026-09-08'), (4, 5, '2026-09-09'),
  (5, 1, '2026-09-10'), (5, 6, '2026-09-10'),
  (6, 3, '2026-09-11'),
  (7, 4, '2026-09-12'), (7, 5, '2026-09-12'),
  (8, 3, '2026-09-13');

insert into encontros (grupo_id, dia_semana, hora_inicio, local) values
  (1, 2, '18:00', 'Biblioteca, sala 3'),
  (2, 4, '19:00', 'Laboratório 2'),
  (3, 6, '10:00', 'Online'),
  (3, 3, '19:30', 'Online'),
  (4, 1, '17:00', 'Biblioteca, sala 1'),
  (5, 3, '18:30', 'Laboratório 4'),
  (6, 5, '16:00', 'Online');
