# Módulo 05, O Diagrama DER

🇧🇷 Português · 🇺🇸 [English](./05-o-diagrama-der.en.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

Nos Módulos 03 e 04 você descobriu as entidades, os atributos e os relacionamentos do projeto, e anotou tudo em tabelas de texto. Este módulo junta tudo em um único desenho, o DER, que é o documento central da modelagem e o ponto de partida para criar o banco.

## // O problema: texto não mostra a estrutura

Uma lista de entidades e relacionamentos descreve o modelo, mas não deixa ver o conjunto. Em um desenho, bastam alguns segundos para perceber que o Grupo está no centro do sistema, que a Participação liga duas pontas, e que a Matéria depende de nada. É por isso que quem trabalha com banco de dados desenha diagramas antes de criar as tabelas.

## // O que é um DER

> **DER: EM PALAVRAS SIMPLES**
> O Diagrama Entidade-Relacionamento é um desenho que mostra as entidades (as futuras tabelas), os seus atributos (as futuras colunas) e os relacionamentos entre elas, com a cardinalidade em cada ponta.

Em livros de modelagem, o DER aparece em três níveis de detalhe: **conceitual** (só entidades e relacionamentos), **lógico** (com atributos, chaves e cardinalidades) e **físico** (com os tipos de dados e detalhes do banco escolhido). O DER desta semana é o nível **lógico**: ele já mostra as colunas e as chaves, mas os tipos de dados só entram no Módulo 08.

## // Os elementos de um DER

| Elemento | Como aparece no desenho |
|---|---|
| Entidade | Uma caixa com o nome no topo |
| Atributo | Uma linha dentro da caixa |
| Chave primária | Marcada com PK ao lado do atributo |
| Chave estrangeira | Marcada com FK ao lado do atributo |
| Relacionamento | Uma linha entre as caixas, com os símbolos de cardinalidade nas pontas |

A **chave estrangeira** (FK) é a coluna que guarda o identificador de outra tabela, e é ela que concretiza o relacionamento. Como você viu no Módulo 04, ela fica na tabela do lado "muitos". O Módulo 08 explica as chaves em detalhe.

## // O DER do Buscador de Grupos de Estudo

<div align="center">
<img src="./assets/der-buscador-grupos.svg" alt="DER do projeto com cinco tabelas: usuarios, participacoes, grupos, materias e encontros" width="640">
</div>

Para conferir se o desenho está certo, leia cada linha de relacionamento como uma frase, nos dois sentidos:

- Uma matéria tem zero ou muitos grupos; cada grupo pertence a exatamente uma matéria.
- Um grupo tem zero ou muitos encontros; cada encontro pertence a exatamente um grupo.
- Um usuário tem zero ou muitas participações; cada participação pertence a exatamente um usuário.
- Um grupo tem zero ou muitas participações; cada participação pertence a exatamente um grupo.

Os dois últimos formam, juntos, o N:N entre usuários e grupos.

## // Como desenhar um DER, passo a passo

1. Desenhe uma caixa para cada entidade, com o nome no topo.
2. Escreva os atributos dentro de cada caixa e marque a chave primária (PK).
3. Para cada N:N, acrescente a entidade associativa entre as duas caixas.
4. Desenhe as linhas dos relacionamentos 1:N e coloque, em cada ponta, o símbolo da cardinalidade.
5. Nas tabelas do lado "muitos", acrescente a chave estrangeira (FK) e marque.
6. Releia cada linha como uma frase, nos dois sentidos.

## // Ferramentas para desenhar

O primeiro DER pode ser feito em papel, e isso é recomendado: ajustar uma caixa de lugar é rápido, e o desenho obriga você a pensar. Para a versão final, qualquer ferramenta de diagramas que aceite caixas e linhas serve (o diagrams.net é uma opção gratuita). Depois que as tabelas existirem no Supabase, o painel pode mostrar um visualizador do esquema, que desenha o DER a partir das tabelas reais. Isso é útil para conferir se o banco criado ficou igual ao desenho (os nomes dos menus podem mudar com o tempo).

## // Bom exemplo × mau exemplo

**Mau exemplo**: N:N desenhado direto entre usuário e grupo, e a matéria como texto dentro do grupo:

| Entidade | Atributos |
|---|---|
| usuarios | usuario_id PK, nome_usuario, email, lista de grupos |
| grupos | grupo_id PK, nome_grupo, materia (texto), codigo_materia |

**Bom exemplo**: associativa no meio, e a matéria em tabela própria:

| Entidade | Atributos |
|---|---|
| usuarios | usuario_id PK, nome_usuario, email, criado_em |
| participacoes | usuario_id PK/FK, grupo_id PK/FK, entrou_em |
| grupos | grupo_id PK, nome_grupo, materia_id FK, max_participantes, criado_em |
| materias | materia_id PK, nome, codigo |

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Esquecer de marcar as chaves | O desenho parece completo sem elas | Marque PK e FK em todas as tabelas antes de dar o DER por terminado |
| Colocar a FK na tabela errada | Confusão sobre qual lado é o "muitos" | A FK fica no lado N do relacionamento 1:N |
| Linhas se cruzando sem necessidade | As caixas foram desenhadas sem planejar | Reposicione as caixas até as linhas ficarem limpas |
| Incluir colunas calculadas | O mock tinha o campo `participantes` | Não inclua atributos derivados no DER |

## // Prática guiada

1. Desenhe o DER do seu projeto em papel, seguindo os seis passos desta seção.
2. Marque PK e FK em cada tabela.
3. Coloque os símbolos de cardinalidade nas duas pontas de cada relacionamento.
4. Leia cada relacionamento como uma frase, nos dois sentidos, e corrija qualquer erro.
5. Passe o desenho a limpo, em papel ou em uma ferramenta de diagramas.

## // Pratique sozinho

> **DESAFIO**
> Desenhe o DER da biblioteca dos módulos anteriores: leitores, livros e a entidade associativa de empréstimos. Inclua os atributos, as chaves e a cardinalidade em cada ponta.

## // Aplicando no projeto da semana

1. Exporte o DER do seu projeto como imagem e salve em `docs/der.png` (ou `.svg`).
2. No `docs/arquitetura.md`, inclua a imagem e as quatro frases de leitura dos relacionamentos.
3. Commit: `git commit -m "Adiciona o DER do projeto"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Quantas tabelas o DER do projeto vai gerar, e por que a Participação é uma delas, mesmo sem ser uma "coisa" do mundo real como um usuário ou um grupo?

Resposta: cinco tabelas (usuarios, materias, grupos, participacoes e encontros). A Participação é uma tabela porque o relacionamento entre usuários e grupos é N:N, e um banco relacional só representa N:N com uma tabela de ligação no meio. Além disso, ela guarda um atributo próprio da ligação, o `entrou_em`.

## // Resumo do módulo

- [ ] Sei o que é um DER e o que significa o nível lógico.
- [ ] Sei os cinco elementos de um DER (entidade, atributo, PK, FK e relacionamento).
- [ ] Sei desenhar um DER em seis passos.
- [ ] Sei ler um DER como frases, nos dois sentidos.
- [ ] Já tenho o DER do meu projeto salvo no repositório.

---

**Próximo módulo:** `06-normalizacao-anomalias-e-1fn.md`, o DER está desenhado. Antes de criar tabelas, vale testar se o desenho evita repetição.

`Material de Estudo // Coffee & Code`
