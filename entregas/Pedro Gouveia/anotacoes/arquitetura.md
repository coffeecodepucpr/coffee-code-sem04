Nome do projeto: grupos-coffee-code



Região: São Paulo



Ordem de execução dos scripts: 01, 02 e 03, ordem numeral crescente, efetivamente



Dicionário:



|TABELA|COLUNA|TIPO|RESTRIÇÕES|
|-|-|-|-|
|estudantes|id|bigint|PK, identity|
|estudantes|nome|text|not null, unique|
|estudantes|email|text|not null, unique|
|estudantes|senha|text|not null, unique|
|materias|id|bigint|PK, identity|
|materias|nome|text|not null, unique|
|grupos|id|bigint|PK, identity|
|grupos|nome|text|not null, unique|
|grupos|vagas\_abertas|smallint|not null|
|grupos|id\_materia|bigint|not null, refernces materias|
|grupo\_horarios|id\_grupo|bigint|not null, references grupos|
|grupo\_horarios|horario|timestamptz|not null|
|participacoes|id\_estudante|bigint|PK composta, references estudantes, cascade|
|participacoes|id\_grupo|bigint|PK composta, references grupos, cascade|
|participacoes|data\_entrada|timestamptz|default now()|



