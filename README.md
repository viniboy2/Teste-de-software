# Teste-de-software

## Estrutura do projeto

```text
Códigos/
|-- app/
|   |-- controllers/
|   |-- models/
|   |-- routes/
|   |-- static/
|   |   |-- css/
|   |   `-- js/
|   |-- templates/
|   `-- views/
`-- database/
```

## Tecnologias
- HTML5
- tailwindcss
- Python 3.12
- Flask
- PyMySQL
- MySQL 8.4
- Docker e Docker Compose

## Requisitos

- Docker
- Docker Compose

Para instalar o Docker Desktop siga o passo a passo abaixo:

1. Abra https://www.docker.com/products/docker-desktop no seu navegador.
2. Clique em **Download for Windows/Mac** (ou selecione o instalador Linux se estiver em WSL) e faça o download do instalador adequado à sua plataforma.
3. Execute o instalador e siga as instruções na tela; mantenha as opções padrão a menos que precise de uma configuração específica.
4. Ao finalizar, abra o Docker Desktop e aguarde ele inicializar completamente (ícone na bandeja indicando que o daemon está ativo).
5. Caso necessário, faça login com sua conta Docker ou crie uma gratuita para acessar recursos extras.
6. Verifique se o Docker e o Compose estão funcionando executando `docker version` e `docker compose version` no terminal.

## Como executar

1. Entre na pasta [`Códigos`](/home/roberto/Documents/GitHub/Teste-de-software/Códigos).
2. Execute:

```bash
docker compose up --build
```

3. Acesse a aplicação em `http://localhost:5000`.
4. O MySQL ficará disponível na porta `3306`.

## Containers

- `app`: container da aplicação Flask
- `db`: container do MySQL

## Banco de dados

O banco é criado a partir de [schema.sql](/home/roberto/Documents/GitHub/Teste-de-software/Códigos/database/schema.sql). Para acessar via MySQL Workbench siga:

1. Garanta que o container `db` esteja iniciado (`docker compose up -d` no diretório `Códigos`).
2. Abra o MySQL Workbench e clique em **New Connection**.
3. Configure a conexão com host `localhost`, porta `3306` e o usuário/senha definidos no `docker-compose.yml`.
4. Clique em **Test Connection** para validar e, depois, em **OK** para salvar.
5. Após conectar, você pode explorar o banco, criar tabelas e executar consultas a partir da interface gráfica.

## Configuração

As configurações da aplicação ficam em [config.py](/home/roberto/Documents/GitHub/Teste-de-software/Códigos/config.py) e são lidas de variáveis de ambiente:

- `SECRET_KEY`
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

No ambiente Docker, essas variáveis são definidas em [docker-compose.yml](/home/roberto/Documents/GitHub/Teste-de-software/Códigos/docker-compose.yml).

## Arquitetura

- `app/controllers`: controla o fluxo das requisições e integra as camadas da aplicação
- `app/models`: concentra regras de negócio e acesso aos dados
- `app/routes`: organiza e registra as rotas da aplicação
- `app/views`: centraliza a renderização das respostas
- `app/templates`: armazena os templates HTML
- `app/static`: guarda arquivos estáticos como CSS, JavaScript e imagens
- `database`: reúne scripts e artefatos relacionados ao banco de dados
