# Módulo 06, Normalização: Anomalias e 1FN

🇧🇷 Português · 🇺🇸 [English](./06-normalizacao-anomalias-e-1fn.en.md)

`SEM 04 // Modelagem de Dados`

---

## // Antes de começar

No Módulo 05 você terminou o DER. Antes de transformá-lo em tabelas, existe uma etapa de verificação: conferir se o desenho evita repetição e problemas de consistência. Essa verificação se chama **normalização**, e este é o primeiro de dois módulos sobre ela. Aqui você vê o que dá errado em uma tabela mal desenhada, e aplica o primeiro nível de correção, a 1FN.

## // O problema: a "planilha única"

Imagine que, em vez de cinco tabelas, alguém guardasse tudo em uma planilha só, uma linha por pessoa em cada grupo:

| usuario | grupo | materia | codigo_materia |
|---|---|---|---|
| Ana Martins | Cálculo passo a passo | Cálculo I | MAT101 |
| Bruno Lima | Cálculo passo a passo | Cálculo I | MAT101 |
| Ana Martins | Estruturas na prática | Estrutura de Dados | INF201 |
| Carla Souza | Estruturas na prática | Estrutura de Dados | INF201 |
| Diego Rocha | Processos e memória | Sistemas Operacionais | INF315 |

À primeira vista funciona. Mas tudo que se repete aqui é uma armadilha esperando para acontecer.

## // As três anomalias

> **ANOMALIA: EM PALAVRAS SIMPLES**
> É um problema que aparece ao alterar os dados de uma tabela mal desenhada, causado por informação repetida ou misturada. Existem três tipos clássicos.

<div align="center">
<img src="./assets/anomalias-tabela-unica.svg" alt="A planilha única com os dados repetidos destacados e as três anomalias: atualização, exclusão e inserção" width="640">
</div>

**Anomalia de atualização.** O código MAT101 aparece em duas linhas. Se a universidade mudar o código de Cálculo I, é preciso alterar as duas, e esquecer uma deixa a planilha dizendo duas coisas diferentes.

**Anomalia de exclusão.** Diego é a única pessoa no grupo "Processos e memória". Se ele sair do grupo e a linha for apagada, somem junto o grupo, a matéria e o código dela. Apagar uma participação destruiu informações que nada tinham a ver com ela.

**Anomalia de inserção.** Para cadastrar a matéria "Redes de Computadores", seria preciso que alguém já estivesse participando de um grupo dela, porque cada linha é uma participação. Uma matéria sem participante não tem onde ser guardada.

## // O que é normalização

> **NORMALIZAÇÃO: EM PALAVRAS SIMPLES**
> É um método para organizar as tabelas de forma que cada informação seja guardada em um único lugar, eliminando as anomalias. O método tem níveis, chamados de formas normais (1FN, 2FN, 3FN e outras).

Cada forma normal é uma regra. Uma tabela que respeita as regras de um nível está "nesse nível". Você já fez boa parte da normalização por intuição nos módulos anteriores, quando separou Matéria em uma entidade própria. Agora você vai aprender o método que explica o porquê.

## // A 1FN: valores atômicos

> **1FN: EM PALAVRAS SIMPLES**
> Uma tabela está na Primeira Forma Normal quando cada célula guarda um único valor (atômico), sem listas nem grupos repetidos, e quando cada linha pode ser identificada de forma única.

Para estar na 1FN, uma tabela precisa respeitar quatro condições:

1. Cada célula tem um **único valor**, nunca uma lista.
2. Não há **colunas repetidas** para o mesmo tipo de dado (como `grupo1`, `grupo2`, `grupo3`).
3. Cada linha tem uma **chave** que a identifica de forma única.
4. Todas as linhas têm a **mesma estrutura**.

## // Corrigindo uma tabela que viola a 1FN

Veja uma tabela em que cada usuário tem os seus grupos em uma única célula:

| usuario_id | nome_usuario | grupos |
|---|---|---|
| 1 | Ana Martins | Cálculo passo a passo, Estruturas na prática |
| 2 | Bruno Lima | Cálculo passo a passo |
| 3 | Carla Souza | Estruturas na prática |

A coluna `grupos` viola a 1FN: a célula de Ana guarda dois valores. A correção é dar a cada fato a sua própria linha, e usar como chave o par de colunas que identifica cada linha:

| usuario_id | grupo_id | nome_usuario | nome_grupo |
|---|---|---|---|
| 1 | 10 | Ana Martins | Cálculo passo a passo |
| 1 | 11 | Ana Martins | Estruturas na prática |
| 2 | 10 | Bruno Lima | Cálculo passo a passo |
| 3 | 11 | Carla Souza | Estruturas na prática |

Agora cada célula tem um único valor, e o par `(usuario_id, grupo_id)` é a chave. A tabela está na 1FN.

## // A 1FN não resolve tudo

Compare a tabela acima com a planilha do início do módulo. Mesmo na 1FN, o nome "Ana Martins" aparece em duas linhas, e o nome de cada grupo se repete. A 1FN só garante que os valores sejam atômicos, e as anomalias de atualização, exclusão e inserção continuam possíveis. O próximo módulo mostra as duas formas normais que eliminam a repetição que sobrou: a 2FN e a 3FN.

## // Bom exemplo × mau exemplo

**Mau exemplo**: colunas repetidas para simular uma lista:

| usuario_id | nome_usuario | grupo1 | grupo2 | grupo3 |
|---|---|---|---|---|
| 1 | Ana Martins | Cálculo passo a passo | Estruturas na prática | |

E se Ana entrar em um quarto grupo? É preciso alterar a estrutura da tabela inteira, e a maioria das células fica vazia.

**Bom exemplo**: uma linha por participação:

| usuario_id | grupo_id |
|---|---|
| 1 | 10 |
| 1 | 11 |

Entrar em um quarto grupo é só acrescentar uma linha, sem mudar a estrutura de nada.

## // Erros comuns

| Erro | Por que acontece | Como corrigir |
|---|---|---|
| Achar que 1FN é a normalização inteira | A 1FN corrige o problema mais visível, a lista na célula | Continue para a 2FN e a 3FN para eliminar a repetição |
| Separar valores com vírgula dentro de uma coluna | É o jeito mais rápido de copiar o array | Use uma linha por valor |
| Criar colunas numeradas (`grupo1`, `grupo2`) | Parece organizado | Troque por linhas em uma tabela de ligação |
| Esquecer a chave de cada linha | A planilha não pedia | Defina a coluna ou o par de colunas que identifica cada linha |

## // Prática guiada

1. Copie a planilha do início do módulo para um editor de texto.
2. Para cada uma das três anomalias, escreva um exemplo concreto usando os dados da planilha.
3. Pegue a tabela com a coluna `grupos` (lista em uma célula) e reescreva-a na 1FN.
4. Identifique qual é a chave da tabela depois da correção.

## // Pratique sozinho

> **DESAFIO**
> Uma tabela guarda `encontro_id`, `grupo_id` e uma coluna `dias` com valores como "terça, quinta". Ela está na 1FN? Reescreva-a para que esteja.

## // Aplicando no projeto da semana

1. Releia o DER que você desenhou no Módulo 05 e verifique: alguma coluna guarda uma lista, ou existem colunas numeradas?
2. Se existirem, corrija o DER e atualize o desenho em `docs/der.png`.
3. Registre no `docs/arquitetura.md` o resultado da verificação da 1FN.
4. Commit: `git commit -m "Verifica a 1FN no DER do projeto"`.

## // Checkpoint

> **ANTES DE SEGUIR, PENSE NISTO**
> Uma tabela `grupos` tem uma coluna `participantes` com valores como "Ana, Bruno, Carla". Qual regra da 1FN ela quebra, e que estrutura do DER você já conhece resolve esse problema?

Resposta: quebra a primeira regra, que exige um único valor por célula, porque a célula guarda uma lista de nomes. O problema se resolve com uma tabela de ligação (a Participação), que guarda uma linha para cada pessoa em cada grupo, exatamente como o DER do Módulo 05 já faz.

## // Resumo do módulo

- [ ] Sei explicar as três anomalias: atualização, exclusão e inserção.
- [ ] Sei o que é normalização e por que ela existe.
- [ ] Sei as quatro condições da 1FN.
- [ ] Sei corrigir uma tabela que guarda listas em uma célula.
- [ ] Sei que a 1FN sozinha não elimina toda a repetição.

---

**Próximo módulo:** `07-normalizacao-2fn-e-3fn.md`, a 1FN resolveu as listas, mas ainda sobra repetição. Os próximos dois níveis cuidam dela.

`Material de Estudo // Coffee & Code`
