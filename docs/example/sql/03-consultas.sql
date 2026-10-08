-- Consultas da Semana 04 (rode depois do schema e do seed).

-- 1. Tudo de uma tabela
select * from materias;

-- 2. Filtrar e ordenar
select nome_grupo, max_participantes
from grupos
where max_participantes >= 6
order by nome_grupo;

-- 3. JOIN: cada grupo com o nome da matéria
select g.nome_grupo, m.nome as materia, m.codigo
from grupos g
join materias m on m.materia_id = g.materia_id
order by m.nome;

-- 4. Agregação: quantos participantes cada grupo tem (o campo que sumiu do mock)
select g.grupo_id, g.nome_grupo, count(p.usuario_id) as participantes
from grupos g
left join participacoes p on p.grupo_id = g.grupo_id
group by g.grupo_id, g.nome_grupo
order by participantes desc, g.nome_grupo;

-- 5. Vagas restantes por grupo
select g.nome_grupo,
       g.max_participantes,
       count(p.usuario_id) as participantes,
       g.max_participantes - count(p.usuario_id) as vagas
from grupos g
left join participacoes p on p.grupo_id = g.grupo_id
group by g.grupo_id, g.nome_grupo, g.max_participantes
order by vagas desc, g.nome_grupo;

-- 6. Os grupos de uma pessoa (o que o Perfil da Semana 03 mostrava)
select u.nome_usuario, g.nome_grupo, m.nome as materia, p.entrou_em
from usuarios u
join participacoes p on p.usuario_id = u.usuario_id
join grupos g        on g.grupo_id   = p.grupo_id
join materias m      on m.materia_id = g.materia_id
where u.email = 'ana.martins@exemplo.com'
order by p.entrou_em;

-- 7. Agenda de um grupo
select g.nome_grupo, e.dia_semana, e.hora_inicio, e.local
from grupos g
join encontros e on e.grupo_id = g.grupo_id
where g.nome_grupo = 'Modelagem e SQL'
order by e.dia_semana, e.hora_inicio;
