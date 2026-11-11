# Arquitetura do FixAqui

## 1. Visão do produto

O FixAqui é uma aplicação web acadêmica que aproxima pessoas que precisam de pequenos serviços de profissionais autônomos. O cliente pode explorar categorias, pesquisar profissionais e, na versão planejada, solicitar e acompanhar serviços. Profissionais poderão divulgar suas especialidades.

O repositório contém o protótipo de frontend estático e o modelo PostgreSQL da Semana 04. O frontend ainda não se comunica com o banco; cadastro, login e favoritos são demonstrações locais, não serviços reais.

## 2. Arquitetura atual

```text
Navegador
├── HTML: dashboard.html, login.html, perfil.html
├── CSS: css/styles.css
└── JavaScript: js/script.js
    └── dados mockados em memória

Supabase
└── PostgreSQL: modelo relacional da Semana 04
    └── sem conexão com o frontend ou backend nesta etapa
```

As páginas são arquivos HTML estáticos. O CSS compartilhado fornece layout e componentes visuais. O JavaScript compartilha um único arquivo, carregado com `defer`, e inicializa o comportamento dos elementos presentes na página. Não há framework, servidor de aplicação, API, processo de build ou pacote de dependências configurado no repositório.

## 3. Páginas e navegação

| Página | Responsabilidade | Navegação principal |
|---|---|---|
| `dashboard.html` | Página inicial para explorar serviços; apresenta categorias, busca e profissionais em destaque. | Acesso ao cadastro e ao login. |
| `perfil.html` | Formulário demonstrativo de criação de conta e resumo local do cadastro. | Retorno ao login ou exploração do dashboard. |
| `login.html` | Formulário demonstrativo de login. | Acesso ao cadastro ou exploração do dashboard. |

As páginas usam `css/styles.css` e carregam `js/script.js`. Os links entre páginas são navegação HTML convencional. O link “Sair” do dashboard direciona ao formulário de login, mas não encerra uma sessão autenticada, pois não existe autenticação nesta versão.

## 4. Comportamentos implementados no protótipo

* A busca filtra os profissionais mockados por nome, categoria e descrição, sem diferenciar maiúsculas/minúsculas ou acentos.
* Os cards de categoria preenchem a busca e levam a pessoa usuária até os resultados.
* Os favoritos podem ser adicionados e removidos durante a visita à página; ficam apenas em memória e não persistem após recarregar.
* O formulário de cadastro valida nome, formato do e-mail, tamanho mínimo da senha e confirmação. Após a validação, exibe um resumo local e permite voltar à edição.
* O formulário de login valida formato do e-mail e tamanho mínimo da senha e, se válido, direciona ao dashboard. Não verifica credenciais.

Os comportamentos acima são prototipados no navegador e não armazenam contas, senhas, favoritos ou solicitações no Supabase. Dados apresentados como avaliações e profissionais também são fictícios.

## 5. Organização do repositório

```text
/
├── dashboard.html
├── login.html
├── perfil.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── docs/
│   ├── arquitetura.md
│   ├── der.svg
│   ├── dicionario-de-dados.md
│   ├── design-system.md
│   ├── historias-de-usuarios.md
│   └── requisitos.md
└── sql/
    ├── 01_criacao.sql
    ├── 02_dados.sql
    └── 03_consultas.sql
```

## 6. Interface e apresentação

O design system está implementado em `css/styles.css` com variáveis CSS para cores, tipografia, espaçamento, bordas, sombras e largura do conteúdo. As telas compartilham cabeçalho, navegação, botões, campos e rodapé. O layout usa regras responsivas e HTML semântico; formulários têm rótulos e áreas de feedback para validação.

As decisões e tokens visuais estão descritos em [design-system.md](./design-system.md).

## 7. Modelo de dados

O modelo da Semana 04 está no PostgreSQL do Supabase e tem cinco tabelas:

* `usuarios`: clientes e profissionais, diferenciados pelo campo `tipo`.
* `categorias`: tipos de serviço oferecidos.
* `profissionais_categorias`: tabela associativa que resolve a relação N:N entre profissionais e categorias.
* `solicitacoes`: pedido de um cliente a um profissional para uma categoria, com descrição, status e data.
* `avaliacoes`: nota e comentário de uma solicitação; cada solicitação pode ter no máximo uma avaliação.

O DER está em [der.svg](./der.svg), e as colunas, tipos e restrições estão no [dicionário de dados](./dicionario-de-dados.md). Os campos calculáveis, como quantidade de avaliações, não são armazenados como colunas.

O banco e o mock do frontend são fontes de dados separadas nesta entrega. A existência de dados no banco não altera o conteúdo exibido pelo dashboard.

## 8. Supabase, segurança e configuração

* **Projeto Supabase:** FixAqui após criar ou identificar o projeto — substitua esta indicação pelo nome exato mostrado no painel.
* **Banco:** PostgreSQL com as cinco tabelas descritas acima.
* **RLS:** habilitado nas cinco tabelas pelo script de criação; não há políticas configuradas, de acordo com o escopo desta semana.
* **Credenciais:** nenhuma credencial deve ser colocada no frontend ou versionada. O `.gitignore` ignora `.env` e arquivos `.env.*`.
* **Estado remoto:** confirme no painel do Supabase que o projeto está ativo e que as tabelas contêm os dados esperados.

Como o frontend não acessa o banco, habilitar RLS sem políticas não afeta o protótipo. Em uma futura integração, o acesso deverá ser projetado com autenticação e políticas apropriadas antes de expor operações pela API.

## 9. Execução e validação do banco

Em um banco de testes vazio, execute os scripts pelo SQL Editor do Supabase, nesta ordem:

1. `sql/01_criacao.sql` — cria as tabelas, chaves, restrições e habilita RLS.
2. `sql/02_dados.sql` — insere os registros de exemplo e sincroniza as sequências de identidade.
3. `sql/03_consultas.sql` — apresenta consultas com `JOIN`, `GROUP BY` e `LEFT JOIN`, além das contagens.

As contagens esperadas após a carga são 8 usuários, 6 categorias, 10 associações, 6 solicitações e 4 avaliações. Os scripts de criação e carga são destinados a banco vazio: não os execute novamente em um projeto com dados a preservar. Confirme os resultados no Table Editor do Supabase.

## 10. Funcionalidades planejadas

Os requisitos e histórias de usuário também descrevem funcionalidades que não estão implementadas no protótipo atual, incluindo perfil detalhado do profissional, solicitação e acompanhamento de serviços, cadastro de especialidades pelo profissional e envio de avaliações. Essas capacidades dependem de evolução da interface e, para persistência e operação real, de autenticação e acesso ao backend.

Uma evolução possível é conectar o frontend a serviços do Supabase com políticas de acesso adequadas, sem expor credenciais privilegiadas no navegador. Recursos como chat, localização, notificações, pagamentos e aplicativo mobile permanecem ideias futuras, não componentes existentes.
