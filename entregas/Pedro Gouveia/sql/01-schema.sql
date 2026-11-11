create table estudantes(
  id bigint generated always as identity primary key,
  nome text not null unique,
  email text not null unique,
  senha text not null
);

create table materias(
  id bigint generated always as identity primary key,
  nome text not null 
);

create table grupos(
  id bigint generated always as identity primary key,
  nome text not null,
  max_membros integer not null default 15 check(max_membros>0),
  id_materia bigint not null references materias(id)
);

create table grupo_horarios(
  id_grupo bigint not null references grupos(id),
  horario time not null
);

create table participacoes(
  id_grupo bigint not null references grupos(id),
  id_estudante bigint not null references estudantes(id),
  data_entrada date not null default current_date,
  primary key (id_grupo, id_estudante)
);

alter table estudantes enable row level security;
alter table materias enable row level security;
alter table grupos enable row level security;
alter table grupo_horarios enable row level security;
alter table participacoes enable row level security;