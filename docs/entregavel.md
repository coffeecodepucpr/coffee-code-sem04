# Entregável, Semana 04

🇧🇷 Português · 🇺🇸 [English](./entregavel.en.md)

`SEM 04 // Modelagem de Dados`

Use este arquivo como checklist final antes de considerar a Semana 04 concluída. Ele reúne o que é **obrigatório**; os desafios extras em `desafios.md` e os Módulos 13 a 15 da trilha veterano são opcionais.

## // O que você deve ter em mãos agora

Se você seguiu os módulos em ordem, o seu repositório agora deve ter, além de tudo o que veio das semanas anteriores: o DER do projeto, o dicionário de dados, os scripts SQL versionados e um banco PostgreSQL ativo no Supabase, com as tabelas criadas e dados dentro.

## // Checklist do entregável

### > Banco ativo no Supabase

- [ ] O projeto Supabase está **ativo** (não pausado) no dia da entrega.
- [ ] As cinco tabelas do projeto existem (ou as equivalentes, se o seu domínio for outro).
- [ ] O RLS está ligado em todas as tabelas.
- [ ] As tabelas contêm dados iniciais, e as contagens batem com o seu script de dados.

### > Modelagem

- [ ] O DER está no repositório (por exemplo, em `docs/der.png`), com entidades, chaves e cardinalidade nas pontas.
- [ ] Todo N:N está resolvido com uma tabela associativa.
- [ ] O modelo respeita a 1FN, a 2FN e a 3FN, e nenhum dado calculável (como a contagem de participantes) virou coluna.
- [ ] O dicionário de dados descreve o tipo e as restrições de cada coluna.

### > SQL

- [ ] A pasta `sql/` tem o script de criação das tabelas e o script de dados, na ordem de execução.
- [ ] Toda chave estrangeira tem `references`, e cada uma tem o `on delete` decidido.
- [ ] Existe pelo menos uma consulta com `join`, uma com `group by` e uma com `left join`.

### > Segurança e organização

- [ ] A senha do banco **não** está em nenhum arquivo versionado, e o `.env` está no `.gitignore`.
- [ ] O `docs/arquitetura.md` descreve o modelo, a ordem de execução dos scripts e o nome do projeto no Supabase.

## // O que NÃO é esperado nesta semana

- Não é esperado ligar a página web ao banco: o front-end continua com dados mock.
- Não é esperado login de verdade nem políticas de acesso por usuário (as regras de RLS, além de ligá-lo).
- Não são esperados índices, migrations nem ORM: isso é da trilha veterano.
- Não é esperado que o banco tenha muitos dados: algumas dezenas de linhas bastam.

> **UM MODELO CORRETO VALE MAIS QUE UM BANCO GRANDE**
> Um DER que resolve bem o N:N e um modelo sem repetição, com poucas linhas, valem mais nesta avaliação do que um banco cheio de dados em uma tabela única mal desenhada. O que está sendo avaliado esta semana é a qualidade do desenho.

## // Como revisar antes de entregar

> **O TESTE MAIS IMPORTANTE DESTA SEMANA**
> Entre no painel do Supabase e confirme, com os próprios olhos, que o projeto está ativo e que as tabelas aparecem com dados no Table Editor. Depois, em um banco de testes vazio, rode os seus scripts do zero, na ordem, e confira se todos passam sem erro.

Se os dois testes passarem, o seu banco é reproduzível e a sua entrega está no caminho certo. Se algum falhar, a mensagem de erro quase sempre aponta a tabela ou a linha exata: volte ao módulo correspondente.

## // Onde tirar dúvidas

Os encontros semanais do Coffee & Code existem para isso. "A minha chave estrangeira dá erro ao inserir, já conferi a ordem e o tipo" é muito mais rápido de resolver do que "o meu banco não funciona".

Se quiser se aprofundar além do que foi pedido, veja `desafios.md` e a trilha veterano, nos Módulos 13 a 15.

## // O que vem na Semana 05

A Semana 04 termina com um banco bem desenhado, ativo e com dados, mas ainda isolado: a página web da Semana 03 segue usando dados mock. É essa ponte, ligar a interface ao banco, que as próximas semanas do clube começam a construir.

Bom trabalho até aqui.

`Material de Estudo // Coffee & Code`
