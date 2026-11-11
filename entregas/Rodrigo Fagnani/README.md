# FixAqui

O FixAqui é uma plataforma que conecta clientes a profissionais que realizam pequenos serviços.

## Objetivo

Facilitar a busca por profissionais e permitir que clientes solicitem serviços de forma simples.

## Funcionalidades planejadas

* Cadastro e login
* Busca por serviços
* Categorias de serviços
* Perfis de profissionais
* Avaliações
* Solicitação de serviços
* Acompanhamento de solicitações
* Histórico de serviços

## Protótipo

[Figma - FixAqui](https://www.figma.com/proto/8NBkV8NkIjlPJSXg4am1bf/Untitled?node-id=0-1&t=aBlZ6abbcyV5SmwH-1)

## Documentação

A documentação do projeto está disponível na pasta [`/docs`](./docs).

### Documentos

* [Requisitos](./docs/requisitos.md)
* [Histórias de Usuário](./docs/historias-de-usuario.md)
* [Design System](./docs/design-system.md)
* [Arquitetura](./docs/arquitetura.md)
* [Dicionário de dados](./docs/dicionario-de-dados.md)
* [Diagrama Entidade-Relacionamento](./docs/der.svg)

## Banco de dados (Semana 04)

Os scripts PostgreSQL estão na pasta [`/sql`](./sql) e devem ser executados em um banco de testes vazio, nesta ordem:

1. [`sql/01_criacao.sql`](./sql/01_criacao.sql) — cria as cinco tabelas e habilita RLS.
2. [`sql/02_dados.sql`](./sql/02_dados.sql) — insere os dados iniciais.
3. [`sql/03_consultas.sql`](./sql/03_consultas.sql) — consultas de exemplo e conferência das contagens.

O front-end continua usando dados mockados; não configure credenciais do banco nele.
