# Módulo 01, Por que um Banco Relacional

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

No Módulo 00 você viu o problema: os dados do Buscador de Grupos de Estudo moram em arrays e somem quando a página recarrega. Este módulo explica, com calma, o que um banco de dados resolve que um array não resolve, e apresenta o vocabulário mínimo que o resto da semana vai usar.

## // O problema: o array pertence ao navegador

Quando o `script.js` roda, o array `gruposMock` é criado na memória do navegador, e só existe ali. Isso gera três limitações concretas:

- **Não persiste:** recarregar a página, fechar a aba ou desligar o computador apaga tudo.
- **Não é compartilhado:** se você abrir o Dashboard em dois computadores, cada um tem a sua própria cópia do array. Uma mudança feita em um não aparece no outro.
- **Não se protege:** nada impede que o array receba dois grupos com o mesmo id, ou um grupo apontando para uma matéria que não existe.

Um banco de dados resolve as três: os dados ficam guardados em um lugar central, que continua existindo mesmo com tudo desligado, e que pode impor regras sobre o que é aceito.

## // Banco de dados, SGBD e SQL: três nomes que se confundem

> **BANCO DE DADOS: EM PALAVRAS SIMPLES**
> É um conjunto organizado de dados guardados de forma permanente. No caso de um banco relacional, esses dados ficam em tabelas ligadas entre si.

Três nomes aparecem juntos o tempo todo, e é comum confundir um com o outro:

| Nome | O que é | Exemplo desta semana |
|---|---|---|
| SGBD | O programa que guarda os dados e responde aos pedidos | PostgreSQL |
| SQL | A linguagem usada para conversar com o SGBD | `SELECT * FROM grupos` |
| Plataforma | Um serviço que hospeda o SGBD e oferece ferramentas ao redor | Supabase |

Em uma frase: você usa a **linguagem SQL** para pedir coisas ao **PostgreSQL**, que está hospedado na **plataforma Supabase**.

## // O vocabulário mínimo de um banco relacional

Quase tudo que você já conhece de arrays e objetos tem um equivalente em um banco:

| No JavaScript (Semana 03) | No banco relacional |
|---|---|
| Um array de objetos (`gruposMock`) | Uma **tabela** (`grupos`) |
| Um objeto dentro do array | Uma **linha** (também chamada de registro) |
| Uma propriedade do objeto (`materia`) | Uma **coluna** (também chamada de campo) |
| A propriedade `id` | A **chave primária** |

A chave primária é a coluna cujo valor identifica cada linha de forma única. Em `gruposMock`, o `id` já cumpria esse papel, mesmo sem esse nome.

## // O que significa "relacional"

> **BANCO RELACIONAL: EM PALAVRAS SIMPLES**
> É um banco que guarda os dados em tabelas e permite ligar uma tabela à outra por meio de chaves, para que cada informação exista em um único lugar.

No `gruposMock`, o nome da matéria ("Cálculo I") está escrito dentro de cada grupo. Se houver três grupos de Cálculo I, o texto se repete três vezes. Em um banco relacional, a matéria existe em uma tabela só, e cada grupo apenas aponta para ela por meio de uma chave. É essa ligação entre tabelas que dá o nome "relacional", e é ela que a modelagem desta semana vai ensinar a desenhar.

## // Bom exemplo × mau exemplo

**Mau exemplo**: guardar uma lista dentro de um único campo:

| usuario_id | nome_usuario | grupos |
|---|---|---|
| 1 | Ana Martins | Cálculo I, Estrutura de Dados, Banco de Dados |

Para saber quem participa de "Banco de Dados", você teria que procurar um pedaço de texto dentro de cada campo. Para remover Ana de um grupo, teria que reescrever a lista inteira.

**Bom exemplo**: uma linha para cada ligação entre pessoa e grupo:

| usuario_id | grupo_id |
|---|---|
| 1 | 1 |
| 1 | 2 |
| 1 | 3 |

Agora cada fato ocupa uma linha. Descobrir quem participa de um grupo, ou remover uma participação, é uma operação simples e segura. Esse é o formato que o resto da semana vai construir.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Dizer que "o banco é o SQL" | SQL, PostgreSQL e Supabase aparecem sempre juntos | Lembre das três camadas: linguagem (SQL), programa (PostgreSQL) e plataforma (Supabase) |
| Tratar o banco como uma planilha enorme | Tabelas parecem planilhas | Em um banco, a ligação entre tabelas e as regras de validação são o ponto central |
| Guardar listas dentro de um campo de texto | É o jeito mais rápido de copiar o que o array já fazia | Use uma linha por item, em uma tabela própria |
| Achar que o banco deixa a página mais "completa" sozinho | Banco e página são coisas separadas | O banco só guarda dados; ligar a página a ele é um passo à parte, que vem depois |

## // Prática guiada

1. Abra o `script.js` do exemplo da Semana 03 e localize o array `gruposMock` e o objeto `usuarioMock`.
2. Em um papel ou editor de texto, escreva o `gruposMock` como uma tabela: uma coluna para cada propriedade, uma linha para cada grupo.
3. Marque qual coluna seria a chave primária.
4. Circule os valores que se repetem de uma linha para outra.

## // Pratique sozinho

> **DESAFIO**
> Olhe o objeto `usuarioMock` da Semana 03, que tem as propriedades `nome`, `email` e `materias` (um array de ids). Qual dessas propriedades não cabe em uma única coluna de uma tabela? Escreva uma ideia de como guardar essa informação usando linhas.

## // Aplicando no projeto da semana

1. Crie, no seu repositório, o arquivo `docs/arquitetura.md` (se ele ainda não existir).
2. Escreva uma seção "Dados que precisam persistir", listando, em tópicos, tudo que o seu projeto guarda hoje em arrays e que deveria sobreviver ao recarregamento da página.
3. Commit: `git commit -m "Lista os dados que precisam persistir"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Você abre o Dashboard no seu computador e, no mesmo momento, a mesma página em outro computador. Os dois mostram os mesmos grupos, mas, se você sair de um grupo no Perfil do primeiro, o segundo continua mostrando a participação. Por quê?

Resposta: porque cada navegador executa o seu próprio `script.js` e cria o seu próprio array `gruposMock` na memória. Não existe nenhum lugar central que os dois consultem. Para que uma mudança feita em um computador apareça no outro, os dados precisam morar em um lugar compartilhado e permanente, que é exatamente o papel do banco de dados.

## // Resumo do módulo

- [ ] Sei explicar três limitações de guardar dados em um array no navegador.
- [ ] Sei diferenciar SGBD, SQL e plataforma (PostgreSQL, SQL e Supabase).
- [ ] Sei relacionar array, objeto e propriedade com tabela, linha e coluna.
- [ ] Sei o que é uma chave primária.
- [ ] Sei explicar o que "relacional" significa e por que isso evita repetição.

---

**Próximo módulo:** `02-postgresql-e-supabase.md`, com o vocabulário pronto, hora de criar o seu banco e fazer a primeira consulta.

`Material de Estudo // Coffee & Code`
