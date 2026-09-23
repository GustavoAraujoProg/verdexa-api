Verdexa API

API desenvolvida em Python para o projeto Verdexa, voltado à identificação e ao acompanhamento de doenças em plantas por meio de imagens e inteligência artificial.

A API permite cadastrar usuários, consultar plantas e doenças, enviar fotos para um serviço de IA e acompanhar análises e cuidados. As informações das doenças incluem sintomas, causas, prevenção e tratamento recomendado.

Situação atual: a estrutura da API e a integração com um serviço externo de IA estão implementadas. O projeto ainda não inclui um modelo treinado. A identificação real de doenças depende de conectar um serviço compatível.

Tecnologias

Python 3.11 ou superior

FastAPI — criação das rotas e documentação interativa

SQLAlchemy — acesso ao banco de dados

MySQL / MariaDB — banco do projeto

XAMPP — ambiente local para MySQL/MariaDB

SQLite — alternativa para testes locais

Alembic — controle das alterações na estrutura do banco

Pydantic — validação dos dados

JWT e Argon2 — autenticação e proteção das senhas

Pillow — validação e processamento de imagens

HTTPX — comunicação com o serviço de IA

Pytest — testes automatizados

Como rodar o projeto

1. Obter o código

Clone o repositório e entre na pasta. Substitua a URL abaixo pela URL real:

git clone https://github.com/SEU-USUARIO/verdexa-api.git
cd verdexa-api

Se recebeu o projeto em ZIP, extraia o arquivo e abra no PyCharm a pasta que contém main.py.

2. Criar o ambiente virtual

python -m venv .venv

No PowerShell do Windows:

.\.venv\Scripts\Activate.ps1

No Prompt de Comando do Windows:

.venv\Scripts\activate.bat

No Linux ou macOS:

source .venv/bin/activate

3. Instalar as dependências

python -m pip install -r requirements.txt

4. Configurar o ambiente

Crie uma cópia de .env.example com o nome .env. No PowerShell:

Copy-Item .env.example .env

Gere a chave usada para assinar os tokens:

python -c "import secrets; print(secrets.token_urlsafe(48))"

Copie o valor gerado para JWT_SECRET no .env. Exemplo de configuração para MySQL:

JWT_SECRET=COLE_AQUI_O_SEGREDO_GERADO
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost:3306/verdexa
TOKEN_MINUTES=60
UPLOAD_DIR=uploads
MAX_UPLOAD_MB=10
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
IA_TIMEOUT_SECONDS=60
IA_MIN_CONFIDENCE=0.7

Substitua USUARIO e SENHA pelas credenciais locais. Caracteres especiais nas credenciais precisam de codificação de URL. A chave JWT deve ter pelo menos 32 caracteres. Não publique o .env no GitHub.

Para testar sem XAMPP, use:

DATABASE_URL=sqlite:///./verdexa.db

5. Preparar o banco

Para MySQL/MariaDB, abra o XAMPP, inicie o MySQL e crie no phpMyAdmin um banco chamado verdexa.

Banco novo e vazio:

python -m alembic upgrade head

Esse comando cria as tabelas e aplica as alterações previstas nas migrações. Nesta versão, as tabelas não são criadas automaticamente ao iniciar o servidor.

Banco existente com a estrutura original do projeto:

Faça backup e pare a API antiga. Se o banco tiver exatamente as seis tabelas originais, sem outras alterações e ainda sem controle do Alembic, execute:

python -m alembic stamp 0001
python -m alembic upgrade head

stamp 0001 apenas registra que a estrutura original já existe; não cria nem verifica as tabelas. Não use esse comando em banco vazio ou para contornar falhas.

Se o banco já estiver versionado por esta entrega, execute apenas upgrade head.

6. Iniciar a API

python -m uvicorn main:app --reload

Endereços locais:

API: http://127.0.0.1:8000

Documentação e testes interativos: http://127.0.0.1:8000/docs

Use --reload durante o desenvolvimento.

Como testar pelo /docs

Abra /docs e execute POST /auth/cadastro com nome, e-mail e senha.

Clique em Authorize.

Informe seu e-mail no campo username e sua senha no campo password.

Deixe os campos de client ID e client secret vazios.

Execute as rotas protegidas com a sessão autenticada.

O cadastro cria uma conta comum. Para permitir que sua conta altere o catálogo, execute no terminal:

python manage.py promover-admin seu@email.com

A conta deve estar cadastrada antes da promoção. Esse comando é administrativo e não está disponível como rota pública.

Funcionalidades implementadas

Usuários e autenticação

Cadastro de usuários com e-mail único

Armazenamento de senhas com hash Argon2

Login com token JWT e expiração configurável

Consulta e atualização do próprio perfil

Verificação de permissões de administrador

Plantas e doenças

Cadastro, listagem, consulta, atualização e exclusão

Consulta das doenças relacionadas a uma espécie

Leituras públicas e alterações restritas a administradores

Bloqueio de exclusões que conflitem com registros vinculados

Análises e imagens

Recebimento e validação de imagens JPEG, PNG e WEBP

Limite de tamanho configurável, com padrão de 10 MiB

Normalização da imagem para JPEG e remoção de metadados

Armazenamento com nome aleatório e acesso autenticado

Integração com um serviço externo de IA

Registro do status, conclusão, versão do modelo e hipóteses

Histórico restrito ao usuário proprietário

Histórico de cuidados

Registro de observações vinculadas a uma análise

Acompanhamento de situações como melhorando e em_tratamento

Consulta restrita ao proprietário da análise

Endpoints

Autenticação e usuários

Método

Rota

Função

POST

/auth/cadastro

Cadastrar usuário

POST

/auth/login

Autenticar e obter token

GET

/usuarios/me

Consultar o próprio perfil

PATCH

/usuarios/me

Atualizar nome e e-mail do próprio perfil

Exemplo de cadastro em JSON:

{
  "nome": "Antonio",
  "email": "antonio@example.com",
  "senha": "uma-senha-de-exemplo"
}

O login recebe formulário com username (e-mail) e password, não um JSON. A senha de cadastro deve ter entre 8 e 128 caracteres.

As requisições protegidas devem enviar o token no cabeçalho:

Authorization: Bearer SEU_TOKEN

Não há listagem pública de usuários nem rota para consultar o perfil de outras pessoas.

Plantas

Método

Rota

Função

POST

/plantas/

Cadastrar planta — administrador

GET

/plantas/

Listar plantas

GET

/plantas/{planta_id}

Consultar planta

PUT

/plantas/{planta_id}

Atualizar planta — administrador

DELETE

/plantas/{planta_id}

Excluir planta — administrador

GET

/plantas/{planta_id}/doencas

Consultar doenças da planta

Doenças

Método

Rota

Função

POST

/doencas/

Cadastrar doença — administrador

GET

/doencas/

Listar doenças

GET

/doencas/{doenca_id}

Consultar doença

PUT

/doencas/{doenca_id}

Atualizar doença — administrador

DELETE

/doencas/{doenca_id}

Excluir doença — administrador

Análises e resultados

Método

Rota

Função

POST

/analises

Enviar foto para análise

GET

/analises

Listar análises do usuário

GET

/analises/{analise_id}

Consultar análise e resultados

GET

/analises/{analise_id}/imagem

Consultar foto privada

O envio usa multipart/form-data, com o campo obrigatório imagem e o campo opcional planta_id.

Os resultados são gerados pela integração com a IA e retornados junto da análise. Não existe rota pública para o usuário cadastrar um diagnóstico manualmente.

Cuidados

Método

Rota

Função

POST

/analises/{analise_id}/cuidados

Registrar cuidado

GET

/analises/{analise_id}/cuidados

Consultar cuidados

Exemplo de registro:

{
  "observacao": "As folhas novas apresentam melhora.",
  "status_planta": "melhorando"
}

Novos registros aceitam os status em_tratamento, melhorando, estavel, piorando e recuperada.

Paginação

As listagens de plantas, doenças, análises e cuidados aceitam offset e limit:

GET /analises?offset=0&limit=20

O padrão é 20 registros e o máximo é 100 por solicitação. A consulta de doenças por planta mantém o formato original sem paginação.

Como funciona a análise por IA

O usuário faz login e envia a foto com seu token.

A API verifica a configuração da IA, valida a foto e salva o arquivo.

Um registro é criado em analises com status processando.

A API envia a foto ao serviço de IA configurado.

A resposta é validada e vinculada às doenças existentes no catálogo.

A análise passa para concluida, e a resposta é devolvida ao aplicativo.

Nesta versão o processamento é síncrono: a requisição aguarda o serviço de IA. Em caso de falha na integração, a análise fica com status erro, sem resultados parciais.

As conclusões possíveis são:

Conclusão

Significado

suspeita_doenca

O modelo retornou hipóteses de doenças

saudavel

O modelo classificou a imagem como saudável

inconclusivo

Não foi possível obter uma conclusão suficiente

planta_nao_suportada

A espécie está fora do escopo do modelo

A confiança do modelo não representa uma garantia de acerto. O limite inicial de 0,7 deve ser ajustado com base na avaliação do modelo.

Conectar o serviço de IA

Adicione ao .env:

IA_URL=https://seu-servico/predict
IA_API_KEY=sua-chave-se-necessaria

O endereço deve apontar para um serviço compatível com o contrato de services/ia_service.py. A chave é opcional quando o serviço não exige autenticação. O modelo treinado e esse serviço precisam ser fornecidos pela equipe.

A API envia um POST com imagem em JPEG e, quando informado, planta_id. Se houver chave, envia Authorization: Bearer ....

Exemplo ilustrativo de resposta esperada do serviço:

{
  "versao_modelo": "modelo-folhas-v1",
  "conclusao": "suspeita_doenca",
  "resultados": [
    {"doenca_id": 1, "confianca": 0.92}
  ]
}

Os IDs devem corresponder às doenças cadastradas. Para as demais conclusões, envie resultados: []. Se a maior confiança estiver abaixo do limite configurado, a API converte a conclusão para inconclusivo e remove as hipóteses.

Sem IA_URL, POST /analises retorna 503 antes de salvar a foto. As demais funcionalidades continuam disponíveis.

Estrutura do banco

Tabela

Responsabilidade

usuarios

Contas, hashes de senha e permissão administrativa

plantas

Catálogo de espécies

doencas

Doenças associadas a uma espécie

analises

Foto, usuário, espécie opcional, status e conclusão

resultados_analise

Hipóteses de doenças e confiança

historico_cuidados

Observações e evolução relacionadas à análise

Uma análise pode ter várias hipóteses e vários registros de cuidados. A foto fica em arquivo; o banco guarda sua referência. A resposta da API expõe uma rota privada para acessá-la.

O modelo atual mantém uma espécie por registro de doença. Ainda não há tabela de exemplares individuais, como “meu tomateiro da varanda”.

Migrações com Alembic

A pasta migrations guarda as instruções de evolução do banco:

env.py: configura a execução das migrações.

versions/0001_original.py: representa a estrutura original.

versions/0002_analises_auth.py: adiciona campos, índices e validações.

O banco registra a revisão aplicada em alembic_version. O comando python -m alembic upgrade head aplica as revisões pendentes.

Análises antigas recebem status=legado. Não são tratadas como diagnósticos novos. As imagens antigas não são baixadas nem movidas automaticamente.

Compatibilidade da confiança antiga

O nome físico da coluna precisao_ia foi preservado. Na API, o campo se chama confianca_modelo e usa valores de 0 a 1, com duas casas decimais.

A migração bloqueia valores antigos nulos ou fora de 0–1. Se confirmar que todos os valores antigos usam percentuais de 0 a 100, faça backup e converta uma única vez:

UPDATE resultados_analise SET precisao_ia = precisao_ia / 100;

Não aplique essa conversão em dados que já usam 0–1 ou misturam escalas. Valores nulos exigem revisão, sem inventar uma pontuação. Em MySQL, uma falha de migração pode deixar alterações parciais: restaure o backup antes de repetir uma migração que começou a alterar tabelas.

Organização dos arquivos

Arquivo ou pasta

Função

main.py

Inicialização e registro das rotas

config.py

Leitura das variáveis de ambiente

database.py

Conexão e sessões do banco

models.py

Mapeamento das tabelas

schemas.py

Validação de entradas e formato das respostas

security.py

Hash de senha, token e permissões

routes/

Operações de catálogo, usuários, análises e cuidados

services/imagens.py

Validação e armazenamento de fotos

services/ia_service.py

Comunicação com o serviço de IA

migrations/

Alterações versionadas no banco

manage.py

Promoção administrativa pelo terminal

tests/

Testes automatizados

.env.example

Modelo de configuração local

requirements.txt

Dependências da aplicação

requirements-dev.txt

Dependências para desenvolvimento e testes

Respostas de erro

Código HTTP

Situação

401

Token ausente, inválido ou expirado; login incorreto

403

Conta sem permissão administrativa

404

Registro não encontrado ou análise de outro usuário

409

E-mail duplicado ou conflito com registros vinculados

413

Imagem acima do limite de tamanho

415

Formato de imagem não aceito

422

Dados ou imagem inválidos

502

Falha na análise pelo serviço de IA

503

Serviço de IA não configurado

Testes automatizados

python -m pip install -r requirements-dev.txt
python -m pytest -q

A entrega foi validada com 10 testes aprovados em Python 3.12 e SQLite, cobrindo autenticação, permissões, isolamento entre usuários, imagens inválidas, falhas da IA, confiança baixa e migrações com dados existentes.

Os testes usam respostas controladas da IA e não comprovam a qualidade de um modelo real. A configuração MySQL/MariaDB foi mantida, mas não foi testada contra um servidor MySQL no ambiente da entrega.

Antes de enviar ao GitHub

Mantenha no .gitignore:

.venv/
venv/
__pycache__/
*.pyc
.env
.idea/
.vscode/
.pytest_cache/
uploads/
*.db

Versione .env.example sem segredos e mantenha a pasta migrations no repositório. Não envie fotos de usuários, bancos locais, credenciais ou o ambiente virtual.

Para um projeto extraído do ZIP, ainda sem repositório Git:

git init
git add .
git commit -m "Implementa autenticação, análises e cuidados na API Verdexa"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/verdexa-api.git
git push -u origin main

Crie antes um repositório vazio no GitHub e substitua a URL pelo endereço real. Se você clonou um repositório existente, não repita git init nem git remote add origin; use o fluxo normal de commit e push da equipe.

Cada integrante deve criar seu próprio ambiente virtual, configurar o .env, preparar o banco e executar as migrações.

Próximas etapas

Treinar ou escolher o modelo de identificação de doenças.

Conectar um serviço compatível ao adaptador de IA.

Validar a qualidade das previsões com imagens reais.

Integrar o aplicativo às rotas da API.

Validar as migrações no MySQL/MariaDB usado pela equipe.

Implementar recuperação de senha e renovação de sessão, se necessárias.

Criar fila persistente para análises demoradas e recuperação de tarefas interrompidas.

Cadastrar exemplares individuais para reunir análises da mesma planta ao longo do tempo.

Antes de hospedar publicamente, configure HTTPS, limites de requisição e frequência, backup do banco e das fotos e as origens reais em CORS_ORIGINS. A pasta de imagens não deve ser exposta como conteúdo estático público.