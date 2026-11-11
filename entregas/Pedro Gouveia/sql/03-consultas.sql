-- Mosrta o ID do grupo, o nome do grupo e a matéria dele.
select g.id as id, g.nome as grupo, m.nome as materia
from grupos g join materias m on g.id_materia = m.id
group by g.id, m.nome order by g.id; 

-- Mostra o ID do grupo, o nome do grupo e seu número de participantes.
-- O resultado difere do valor de participantes em gruposMock porque ainda não criei usuários para entrar nos grupos.
select g.id as id, g.nome as grupo, count(p.id_estudante) as participantes
from grupos g left join participacoes p on p.id_grupo = g.id
group by g.id, g.nome 
order by participantes desc, g.nome;

-- Similar ao anterior, porém agora com uma coluna para demonstrar vagas abertas.
select g.id as id, g.nome as grupo, g.max_membros as limite_membros, count(p.id_estudante) as participantes, g.max_membros-count(p.id_estudante) as vagas
from grupos g left join participacoes p on p.id_grupo = g.id
group by g.id, g.nome 
order by vagas desc, g.nome;

-- Select para perfis 
select e.nome as nome, g.nome as nome_grupo, m.nome as materia, p.data_entrada as entrou_em
from estudantes e
join participacoes p on p.id_estudante = e.id
join grupos g        on p.id_grupo = g.id
join materias m      on g.id_materia = m.id
where e.email = 'gorfo@email.com' -- Qualquer email que estivesse incluído na tabela de estudantes poderia ser posto aqui, não funcionaria atualmente por a tebela estudante estar vazia.
order by p.data_entrada, g.nome;
