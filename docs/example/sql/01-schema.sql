-- Buscador de Grupos de Estudo: esquema da Semana 04
-- Rode este script inteiro no SQL Editor do Supabase (ou em qualquer PostgreSQL).

create table usuarios (
  usuario_id    bigint generated always as identity primary key,
  nome_usuario  text not null,
  email         text not null unique,
  criado_em     timestamptz not null default now()
);

create table materias (
  materia_id  bigint generated always as identity primary key,
  nome        text not null unique,
  codigo      text not null unique
);

create table grupos (
  grupo_id           bigint generated always as identity primary key,
  nome_grupo         text not null,
  materia_id         bigint not null references materias (materia_id),
  max_participantes  integer not null default 10 check (max_participantes > 0),
  criado_em          timestamptz not null default now()
);

-- tabela associativa: resolve a relação N:N entre usuarios e grupos
create table participacoes (
  usuario_id  bigint not null references usuarios (usuario_id) on delete cascade,
  grupo_id    bigint not null references grupos (grupo_id) on delete cascade,
  entrou_em   date not null default current_date,
  primary key (usuario_id, grupo_id)
);

create table encontros (
  encontro_id  bigint generated always as identity primary key,
  grupo_id     bigint not null references grupos (grupo_id) on delete cascade,
  dia_semana   smallint not null check (dia_semana between 1 and 7),  -- 1 = segunda, 7 = domingo
  hora_inicio  time not null,
  local        text not null
);

-- Segurança: o acesso pela API do Supabase depende de permissões (grants) e de RLS.
-- Por segurança, ligue o RLS em toda tabela de um schema exposto pela API, como o public.
-- Sem nenhuma policy criada, as requisições comuns da API não enxergam nenhuma linha.
-- O SQL Editor continua mostrando tudo, porque roda com um papel administrativo.
alter table usuarios       enable row level security;
alter table materias       enable row level security;
alter table grupos         enable row level security;
alter table participacoes  enable row level security;
alter table encontros      enable row level security;
