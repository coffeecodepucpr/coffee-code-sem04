Versão: PostgreSQL 17.11 on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 15.2.0, 64-bit



Nome do Banco: postgres

Usuário atual: postgres



Papéis do Postgres:

&#x09;O Postgres usa o conceito de papéis para manejar permissões de acesso entre usuários ou grupos de usuários, especificamente o acesso de sistema.



//===================================================================================



Criar conta

"Como *estudante*, quero criar uma *conta* com meu *nome*, *e-mail* e *senha*, para poder participar das *matérias* da plataforma."



Buscar matérias

"Como estudante, quero buscar *matérias* pelo *nome*, para encontrar rapidamente um *grupo* do conteúdo que estou estudando."



Participar de uma matéria

"Como estudante, quero entrar em uma *matéria* que ainda tenha *vagas*, para estudar junto com outras *pessoas* no *horário* marcado."

Entidade - Estudante:

* Nome
* E-Mail (Identificador)

\- Senha

* Grupos (Multivalorado)

Entidade - Matérias:

* Nome (Identificador)
* Grupos (Multivalorado)
* Vagas disponíveis (Derivado)
* Horário de encontro (Multivalorado)

Entidade - Grupos:

* Nome (Identificador)
* Integrantes
* Número de integrantes (derivado)

\- Matéria

RELACIONAMENTOS:

* Cada Grupo tem exatamente uma matéria, cada matéria tem um ou vários grupos (Min:1, Max:N - 1:N)
* Um estudante pode estar em vários grupos, um grupo pode ter vários estudantes (Min:0, Max:N - N:N)

  * Poderia haver uma tabela estudante grupos que liga os dois



//===================================================================================



Usando da planilha no Módulo 6...

1 - Anomalia de Atualização:
Seria possível corrigir a anomalia usando uma tabela associativa entre usuários e matérias, e então uma tabela separada para matérias que inclui o código, permitindo alterar o código somente uma vez



2 - Anomalia de Exclusão:
Novamente, seria possível criar uma nova tabela que armazena os grupos e matérias, permitindo que não sejam perdidos caso a linha seja apagada

3 - Anomalia de Inserção:
Com uma tabela separada para matérias, mesmo uma matéria sem participantes seria registrada



//===================================================================================



Usando participacoes\_planilha do Módulo 7...



|usuario\_id|grupo\_id|nome\_usuário|nome\_grupo|materia|codigo\_materia|entrou\_em|
|-|-|-|-|-|-|-|
|1|10|Ana Martins|Cálculo passo a passo|Cálculo 1|MAT101|2026-09-01|
|1|11|Ana Martins|Estruturas na prática|Estrutura de Dados|INF201|2026-09-03|
|2|10|Bruno Lima|Cálculo passo a passo|Cálculo 1|MAT101|2026-09-02|
|3|11|Carla Souza|Estruturas na prática|Estrutura de Dados|INF201|2026-09-05|



* nome\_usuario -> usuario\_id
* nome\_grupo -> grupo\_id
* materia -> grupo\_id
* codigo\_materia -> materia
* entrou em -> usuario\_id, grupo\_id



2FN =>



Usuário

|usuario\_id|nome\_usuario|
|-|-|
|1|Ana Martins|
|2|Bruno Lima|
|3|Carla Souza|



Grupos

|grupo\_id|nome\_grupo|materia|codigo\_materia|
|-|-|-|-|
|10|Cálculo passo a passo|Cálculo 1|MAT101|
|11|Estruturas na prática|Estrutura de Dados|INF201|



Participações

|usuario\_id|grupo\_id|entrou\_em|
|-|-|-|
|1|10|2026-09-01|
|1|11|2026-09-03|
|2|10|2026-09-02|
|3|11|2026-09-05|





3FN - Grupos =>

Grupos

|grupo\_id|nome\_grupo|materia\_id|
|-|-|-|
|10|Cálculo passo a passo||
|11|Estruturas na prática||



Matérias

|materia\_id|nome\_materia|codigo\_materia|
|-|-|-|
|101|Cálculo 1|MAT101|
|102|Estrutura de Dados|INF201|



//===================================================================================



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



