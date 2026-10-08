# Módulo 12, Projeto Guiado: O Banco do Buscador de Grupos

🇧🇷 Português · 🇺🇸 [English](../docs-eng/12-guided-project.md)

`SEM 04 // Modelagem de Dados`

---

## // Para que serve este módulo

Nenhum conceito novo aparece aqui. Este módulo junta, em ordem, tudo que os Módulos 01 a 11 ensinaram, e termina com o entregável da semana: um banco relacional no Supabase, com as tabelas criadas e dados dentro.

## // Etapa 1, Confirmar o projeto Supabase (Módulo 02)

Entre no painel e confirme três coisas: o projeto está **ativo** (não pausado), a senha do banco está guardada em local seguro, e o arquivo `.env` está listado no `.gitignore` do repositório.

## // Etapa 2, Revisar o desenho (Módulos 03 a 08)

Antes de criar qualquer coisa, confira o DER e o dicionário de dados do seu projeto:

- [ ] Cada entidade virou uma tabela, e o N:N foi resolvido com uma tabela associativa.
- [ ] Toda tabela tem chave primária, e toda relação 1:N tem a chave estrangeira no lado "muitos".
- [ ] Nenhuma coluna guarda lista, e nenhum dado derivado (como a contagem de participantes) virou coluna.
- [ ] As tabelas respeitam a 2FN e a 3FN.
- [ ] Todas as colunas têm tipo definido, e as restrições (`not null`, `unique`, `check`) estão anotadas.

## // Etapa 3, Criar as tabelas (Módulo 09)

Rode o seu `sql/01-schema.sql` no SQL Editor e confira, no Table Editor, que as cinco tabelas existem e que o RLS está ligado em todas.

## // Etapa 4, Inserir os dados (Módulo 10)

Rode o seu `sql/02-seed.sql`. Depois, confira se todas as tabelas receberam as linhas esperadas com esta consulta, que reúne as contagens em um único resultado:

```sql
select 'materias' as tabela, count(*) as linhas from materias
union all select 'usuarios',      count(*) from usuarios
union all select 'grupos',        count(*) from grupos
union all select 'participacoes', count(*) from participacoes
union all select 'encontros',     count(*) from encontros;
```

Com os dados de exemplo deste guia, o resultado esperado é 6 matérias, 8 usuários, 6 grupos, 16 participações e 7 encontros. O `union all` é um comando novo, que apenas empilha os resultados de várias consultas, e aqui serve só para conferir tudo de uma vez.

## // Etapa 5, Consultar (Módulo 11)

Salve em `sql/03-consultas.sql` as consultas que o seu projeto precisaria: os grupos com as vagas restantes (o que o Dashboard mostrava) e os grupos de uma pessoa (o que o Perfil mostrava). Rode cada uma e confira se o resultado faz sentido.

## // Etapa 6, Documentar

No `docs/arquitetura.md`, reúna: o DER (imagem), o dicionário de dados, a ordem em que os scripts devem ser executados e o nome do projeto no Supabase. **Não inclua a senha nem a URL de conexão com senha.**

## // Etapa 7, Conferência final e commit

1. Rode `git status` e confirme que o `.env` **não** aparece na lista de arquivos novos.
2. Confirme que a pasta `sql/` tem os três scripts e que a pasta `docs/` tem o DER e a arquitetura.
3. Commit: `git commit -m "Finaliza o banco relacional do projeto"`.

## // Etapa extra para a trilha veterano

Se você seguiu os Módulos 13 a 15, o banco já pode receber mais três coisas: os índices do `04-indices.sql` (Módulo 13), o histórico de migrations (Módulo 14) e o modelo equivalente em Prisma ou SQLAlchemy (Módulo 15). Elas são opcionais e vêm **depois** do banco funcionando.

## // Checklist de fechamento

- [ ] O projeto Supabase está ativo, e a senha está fora do repositório.
- [ ] As cinco tabelas existem, com tipos e restrições conforme o dicionário de dados.
- [ ] O RLS está ligado em todas as tabelas.
- [ ] As tabelas contêm os dados iniciais, e as contagens batem com o esperado.
- [ ] As consultas com `join`, `group by` e `left join` funcionam.
- [ ] O DER e o dicionário de dados estão no repositório.
- [ ] Os scripts SQL estão versionados, na ordem de execução.

## // Erros comuns ao juntar tudo

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| `relation "..." does not exist` ao rodar o seed | O schema não foi criado antes, ou a tabela foi criada em outro projeto | Confira o nome do projeto no topo do painel e rode o schema primeiro |
| `duplicate key value violates unique constraint` ao rodar o seed de novo | As linhas já existem, e as restrições estão protegendo o banco | É o comportamento esperado. Para recomeçar do zero, apague as tabelas na ordem inversa e recrie |
| As tabelas aparecem, mas o Table Editor mostra 0 linhas | O seed falhou no meio, ou rodou em outra consulta | Rode as contagens da Etapa 4 e releia a mensagem de erro do SQL Editor |
| O projeto "sumiu" no dia da entrega | Pausa por inatividade do plano gratuito | Entre no painel e restaure o projeto antes de entregar |
| A senha foi parar em um commit | O `.env` não estava no `.gitignore` | Troque a senha do banco nas configurações do projeto, e adicione o `.env` ao `.gitignore` |

## // Aplicando no projeto da semana

Esta é a aplicação: não existe uma atividade separada. Ao final deste módulo, o seu banco deve passar pelo checklist do `entregavel.md`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você roda o seed duas vezes seguidas e a segunda execução termina em erro de chave duplicada. Isso significa que algo está quebrado?

Resposta: não, significa que as restrições estão funcionando. A coluna `nome` de `materias` e a coluna `email` de `usuarios` são `unique`, então o banco recusa os mesmos dados pela segunda vez e evita que o seu banco tenha linhas duplicadas. Para refazer do zero, apague as tabelas na ordem inversa da criação (encontros, participacoes, grupos, usuarios, materias) e rode o schema e o seed de novo.

## // Resumo do módulo

- [ ] Consigo repetir, de memória, a sequência: desenhar, normalizar, criar, popular, consultar e documentar.
- [ ] O meu banco está ativo no Supabase, com tabelas e dados.
- [ ] O checklist de fechamento está completo.

---

**Próximo módulo:** `13-indices-e-desempenho.md` para a trilha veterano, ou `entregavel.md` para a revisão final de quem segue a trilha principal.

`Material de Estudo // Coffee & Code`
