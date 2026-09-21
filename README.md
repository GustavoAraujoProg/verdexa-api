# Verdexa API

API desenvolvida em Python para o projeto Verdexa.

A ideia do Verdexa é futuramente identificar doenças em plantas através de imagens e retornar informações como sintomas, causas, prevenção e tratamento recomendado.

Nesta primeira etapa estamos desenvolvendo somente a API e a estrutura do banco de dados.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- MySQL / MariaDB
- XAMPP

## Como rodar o projeto

Clone o projeto e entre na pasta:

```bash
git clone URL_DO_REPOSITORIO
cd verdexa-api

Crie o ambiente virtual:

python -m venv venv

Ative o ambiente:

venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Abra o XAMPP e inicie o MySQL.

No phpMyAdmin crie um banco chamado:

verdexa

Não precisa criar as tabelas manualmente, o projeto cria automaticamente ao iniciar.

Depois rode:

uvicorn main:app --reload

A API ficará disponível em:

http://127.0.0.1:8000

Documentação da API:

http://127.0.0.1:8000/docs
O que já está funcionando
Cadastro de plantas
Listagem de plantas
Alteração de plantas
Exclusão de plantas
Cadastro de doenças
Listagem de doenças
Alteração de doenças
Exclusão de doenças
Consulta das doenças relacionadas a uma planta

O restante da API será desenvolvido nas próximas etapas do projeto.

Antes de subir
Confere se seu .gitignore está assim:

venv/
__pycache__/
*.pyc
.env
.vscode/

Isso é importante principalmente para não mandar o venv para o GitHub. agora podemos subir.

Cria um repositório novo no GitHub chamado:

verdexa-api


git init

Depois:

git add .

Depois:

git commit -m "Estrutura inicial da API Verdexa"

Depois:

git branch -M main

O GitHub vai te dar uma URL parecida com:

https://github.com/SEU-USUARIO/verdexa-api.git

Aí:

git remote add origin https://github.com/SEU-USUARIO/verdexa-api.git

E por último:

git push -u origin main


git clone LINK_DO_REPOSITORIO

cada um cria o próprio venv, instala o requirements.txt, cria o banco verdexa no XAMPP e roda a API.


## O que já foi feito
Até o momento deixei pronta a estrutura inicial da API, incluindo:

- Conexão com o banco de dados
- Criação automática das tabelas
- CRUD de plantas
- CRUD de doenças
- Consulta das doenças relacionadas a uma planta
- Estrutura inicial do FastAPI
- Documentação automática pelo `/docs`

## O que falta fazer
As próximas partes podem ser divididas da seguinte forma:

### Parte 2 - Usuários e Análises

Criar as rotas e schemas relacionados a:

- usuários
- análises

Sugestão de endpoints:

```text
POST /usuarios
GET /usuarios
GET /usuarios/{id}
PUT /usuarios/{id}
DELETE /usuarios/{id}

POST /analises
GET /analises
GET /analises/{id}
GET /usuarios/{id}/analises



## Parte 3 - Resultados e Histórico de Cuidados

Criar as rotas e schemas relacionados a:

resultados_analise
historico_cuidados

Sugestão de endpoints:

POST /resultados
GET /resultados/{id}
GET /analises/{id}/resultado

POST /historico
GET /historico
GET /analises/{id}/historico

O resultado da análise deve relacionar uma análise com uma doença e armazenar também a precisão da identificação.

O histórico de cuidados será utilizado para registrar observações e a situação da planta ao longo do tempo.