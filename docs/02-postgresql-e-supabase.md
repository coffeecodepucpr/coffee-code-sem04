# Módulo 02, PostgreSQL e Supabase

🇧🇷 Português · 🇺🇸 [English](./02-postgresql-e-supabase.en.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

No Módulo 01 você viu a diferença entre SGBD, SQL e plataforma. Agora você vai tocar nelas: criar o seu projeto no Supabase, conhecer o painel e rodar a primeira consulta. Desenhar o banco vem nos próximos módulos, mas é melhor já ter o ambiente funcionando, para que nada seja novidade quando chegar a hora de criar as tabelas.

## // O que o Supabase entrega

> **SUPABASE: EM PALAVRAS SIMPLES**
> É uma plataforma que hospeda um banco PostgreSQL pronto na nuvem e oferece, ao redor dele, um painel visual e uma API gerada automaticamente a partir das suas tabelas.

<div align="center">
<img src="./assets/supabase-visao-geral.svg" alt="Um projeto Supabase: o painel e a API acessando o mesmo banco PostgreSQL" width="640">
</div>

Cada projeto do Supabase tem o seu próprio PostgreSQL. O painel é onde você olha e edita os dados com cliques; a API é o que, mais adiante, permite que uma aplicação converse com o banco. Esta semana você usa só o painel e o SQL.

## // Criando o seu projeto

> **SOBRE OS NOMES DOS BOTÕES**
> Plataformas mudam a interface com frequência. Os nomes abaixo estavam corretos na data da consulta deste material (4 de outubro de 2026). Se algo estiver em outro lugar, o caminho continua o mesmo: criar conta, criar projeto, definir senha do banco, esperar a criação.

1. Acesse `supabase.com` e crie uma conta gratuita.
2. No painel, clique em **New project** e escolha a organização (uma é criada junto com a conta).
3. Preencha o nome do projeto (por exemplo, `buscador-de-grupos`).
4. Defina a **senha do banco de dados** e guarde-a em um lugar seguro. Se esquecer, é possível redefinir nas configurações do banco do projeto.
5. Escolha a região mais próxima de você e o plano **Free**.
6. Clique para criar e aguarde. A criação costuma levar um ou dois minutos.

## // Conhecendo o painel

No menu lateral do projeto, duas áreas são as mais usadas nesta semana:

| Área | Para que serve |
|---|---|
| Table Editor | Ver, criar e editar tabelas e linhas de forma visual, como em uma planilha |
| SQL Editor | Escrever e executar comandos SQL, e salvar as consultas que você quiser reaproveitar |

A regra deste guia é: **desenhar no papel, criar com SQL, conferir no Table Editor.** O Table Editor é ótimo para olhar e corrigir dados, mas um script SQL pode ser versionado no Git, repetido e revisado, e uma sequência de cliques não.

## // A primeira consulta

Abra o **SQL Editor**, crie uma nova consulta e rode:

```sql
select version();
select now();
```

A primeira devolve a versão do PostgreSQL que o seu projeto usa; a segunda, a data e a hora do servidor. Se as duas responderam, o seu banco está vivo.

## // Uma tabela de teste, para sentir a ferramenta

```sql
create table teste (
  id    integer,
  texto text
);

insert into teste (id, texto) values (1, 'olá, banco');

select * from teste;

drop table teste;
```

O que cada comando fez: criou uma tabela, guardou uma linha, leu a tabela inteira e, por fim, apagou a tabela. Os Módulos 09 e 10 explicam cada um desses comandos em detalhe. Por ora, o importante é ver que o fluxo funciona de ponta a ponta, e apagar a tabela de teste no final, para não deixar lixo no banco.

## // O plano gratuito e a pausa por inatividade

> **ATENÇÃO: PROJETOS FREE SÃO PAUSADOS**
> No plano gratuito, um projeto que fica uma semana sem atividade é pausado. Os dados são mantidos, mas o banco fica fora do ar até alguém reativá-lo pelo painel. Os limites do plano gratuito incluem 500 MB de espaço de banco por projeto. Esses números foram consultados em 4 de outubro de 2026, e vale confirmar na página de preços do Supabase antes de depender deles.

Na prática, isso significa um cuidado simples: **antes de entregar o trabalho, entre no painel e confira que o projeto está ativo.** Se estiver pausado, o painel avisa e oferece a opção de restaurar.

## // Dois cuidados de segurança desde o primeiro dia

> **CUIDADO COM A SENHA E COM O RLS**
> A senha do banco nunca vai para o repositório. Quanto à API que o Supabase gera automaticamente (a Data API), o acesso a uma tabela depende de **duas camadas**: as permissões (*grants*) concedidas aos papéis da API, como `anon` e `authenticated`, e o *Row Level Security* (RLS), que decide quais linhas esses papéis enxergam. Nos projetos criados desde 30 de maio de 2026, as tabelas novas do schema `public` não recebem essas permissões automaticamente, e o Supabase informou que o mesmo comportamento passa a valer para os projetos mais antigos a partir de 30 de outubro de 2026 (informações consultadas em 7 de outubro de 2026). Mesmo assim, por segurança, habilite o RLS em toda tabela que possa ser exposta: uma tabela com permissões e sem RLS fica aberta aos papéis da API. Com o RLS ligado e nenhuma policy criada, as requisições comuns da API não enxergam nenhuma linha, e esta semana isso é exatamente o que queremos. As regras de acesso de verdade, com permissões e policies, ficam para quando houver autenticação.

## // Bom exemplo × mau exemplo

**Mau exemplo**: a senha do banco escrita dentro de um arquivo que vai para o Git:

```
DATABASE_URL=postgresql://postgres:minha-senha@db.exemplo.supabase.co:5432/postgres
```

Em um arquivo versionado, qualquer pessoa que veja o repositório vê a senha, e ela fica para sempre no histórico.

**Bom exemplo**: a senha em um arquivo `.env` que o Git ignora:

```
# arquivo .gitignore
.env
```

Assim o `.env` existe no seu computador, mas nunca entra em um commit.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Esquecer a senha do banco | Ela só é exibida na criação do projeto | Redefina nas configurações do banco do projeto e guarde em um gerenciador de senhas |
| Projeto "sumiu" depois de alguns dias | Projetos Free são pausados após uma semana sem uso | Entre no painel e restaure o projeto |
| Criar tabelas e esquecer o RLS | O banco aceita a tabela sem ele | Rode `alter table ... enable row level security` logo após cada `create table` |
| Rodar um comando e não saber em qual projeto | Contas podem ter mais de um projeto | Confira o nome do projeto no topo do painel antes de executar |

## // Prática guiada

1. Crie a sua conta e o projeto, seguindo os passos desta seção.
2. No SQL Editor, rode `select version();` e anote a versão do PostgreSQL.
3. Rode o bloco da tabela `teste` inteiro, comando por comando.
4. Abra o Table Editor entre o `insert` e o `drop table` e confira que a tabela e a linha aparecem lá.
5. Confirme, no final, que a tabela `teste` foi apagada.

## // Pratique sozinho

> **DESAFIO**
> Rode `select current_database(), current_user;` e descubra o nome do banco e o papel com que o SQL Editor está conectado. Depois, pesquise o que é um "papel" (role) no PostgreSQL e escreva uma frase explicando.

## // Aplicando no projeto da semana

1. No seu `docs/arquitetura.md`, registre o nome do projeto no Supabase e a região escolhida. **Não registre a senha.**
2. Adicione `.env` ao seu `.gitignore`, se ainda não estiver lá.
3. Commit: `git commit -m "Documenta o projeto Supabase e protege o .env"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> O seu projeto Supabase gratuito ficou dez dias sem ninguém acessar. Ao voltar, o banco não responde. O que provavelmente aconteceu, e o que você precisa fazer?

Resposta: o projeto foi pausado por inatividade, que é o comportamento do plano gratuito depois de uma semana sem uso. Os dados continuam guardados; basta entrar no painel e restaurar o projeto. Por isso vale conferir que ele está ativo antes de qualquer entrega.

## // Resumo do módulo

- [ ] Tenho um projeto Supabase criado, com a senha guardada em local seguro.
- [ ] Sei onde ficam o Table Editor e o SQL Editor.
- [ ] Rodei a primeira consulta e a tabela de teste com sucesso.
- [ ] Sei que projetos Free são pausados após uma semana sem uso, e que preciso conferir isso antes de entregar.
- [ ] Sei por que a senha não vai para o repositório e o que o RLS faz.

---

**Próximo módulo:** `03-entidades-e-atributos.md`, o ambiente está pronto. Hora de descobrir quais tabelas o projeto realmente precisa.

`Material de Estudo // Coffee & Code`
