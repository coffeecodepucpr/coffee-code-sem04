# Dicionário de dados

O banco usa PostgreSQL. Campos `IDENTITY` são gerados pelo banco; os identificadores explícitos no script de dados são apenas para tornar os exemplos reproduzíveis, e o próprio script sincroniza as sequências após a carga. Campos `TIMESTAMPTZ` guardam data e hora com fuso horário.

## `usuarios`

| Coluna | Tipo | Restrições e significado |
|---|---|---|
| `id` | `BIGINT` | Chave primária; identidade gerada. |
| `nome` | `TEXT` | Obrigatório; nome de exibição. |
| `email` | `TEXT` | Obrigatório e único. |
| `telefone` | `TEXT` | Opcional. |
| `tipo` | `TEXT` | Obrigatório; limitado a `cliente`, `profissional` ou `ambos`. |
| `criado_em` | `TIMESTAMPTZ` | Obrigatório; padrão `now()`. |

## `categorias`

| Coluna | Tipo | Restrições e significado |
|---|---|---|
| `id` | `BIGINT` | Chave primária; identidade gerada. |
| `nome` | `TEXT` | Obrigatório e único. |
| `descricao` | `TEXT` | Opcional. |
| `criado_em` | `TIMESTAMPTZ` | Obrigatório; padrão `now()`. |

## `profissionais_categorias`

| Coluna | Tipo | Restrições e significado |
|---|---|---|
| `profissional_id` | `BIGINT` | Parte da chave primária composta; FK para `usuarios.id`, exclusão `RESTRICT`. Deve identificar usuário do tipo profissional. |
| `categoria_id` | `BIGINT` | Parte da chave primária composta; FK para `categorias.id`, exclusão `RESTRICT`. |

A chave primária composta impede a associação duplicada do mesmo profissional à mesma categoria.

## `solicitacoes`

| Coluna | Tipo | Restrições e significado |
|---|---|---|
| `id` | `BIGINT` | Chave primária; identidade gerada. |
| `cliente_id` | `BIGINT` | Obrigatório; FK para `usuarios.id`, exclusão `RESTRICT`. Deve identificar cliente. |
| `profissional_id` | `BIGINT` | Obrigatório; FK para `usuarios.id`, exclusão `RESTRICT`. Deve identificar profissional. |
| `categoria_id` | `BIGINT` | Obrigatório; FK para `categorias.id`, exclusão `RESTRICT`. |
| `descricao` | `TEXT` | Obrigatório; descrição do serviço solicitado. |
| `status` | `TEXT` | Obrigatório; limitado a `solicitada`, `em_andamento`, `concluida` ou `cancelada`. |
| `criado_em` | `TIMESTAMPTZ` | Obrigatório; padrão `now()`. |

Uma restrição impede que o mesmo usuário seja cliente e profissional da mesma solicitação. A correspondência entre o tipo do usuário e seu papel nas FKs é uma regra de domínio; o script de criação não a valida entre tabelas.

## `avaliacoes`

| Coluna | Tipo | Restrições e significado |
|---|---|---|
| `id` | `BIGINT` | Chave primária; identidade gerada. |
| `solicitacao_id` | `BIGINT` | Obrigatório, único; FK para `solicitacoes.id`, exclusão `CASCADE`. Uma solicitação pode ter no máximo uma avaliação; apagar a solicitação apaga sua avaliação. |
| `nota` | `SMALLINT` | Obrigatório; inteiro entre 1 e 5. |
| `comentario` | `TEXT` | Opcional. |
| `criado_em` | `TIMESTAMPTZ` | Obrigatório; padrão `now()`. |

O cliente e o profissional avaliados são obtidos pela solicitação relacionada; seus identificadores não são duplicados nesta tabela.

## Segurança

RLS está habilitado nas cinco tabelas. Não há políticas configuradas nesta entrega, portanto o acesso pela API para papéis sujeitos a RLS permanece bloqueado até que políticas sejam definidas em uma etapa futura. As chaves estrangeiras usam `RESTRICT` para preservar usuários, categorias e histórico referenciado; a avaliação é removida em cascata somente quando sua solicitação é removida.
