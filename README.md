# 🛍️ API Mult-Lojas SaaS (Python + Flask)

Seja bem-vindo(a) à API do nosso SaaS de Lojas Virtuais! Esta API foi construída utilizando Python e Flask, permitindo a criação de múltiplas lojas com produtos isolados (arquitetura multi-tenant) e um painel mestre de estatísticas.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.14+**
- **Flask** (Framework Web)
- **SQLAlchemy** (ORM de Banco de Dados)
- **Flask-Migrate** (Gerenciamento de Migrações do Banco)
- **PyMySQL** (Driver MySQL)
- **Flask-JWT-Extended** (Autenticação via JWT Token)
- **Laragon / MySQL** (Hospedagem de Banco Local)

---

## 🚀 Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar o ambiente e rodar a API no seu computador:

### 1. Requisitos
- Tenha o Python instalado na máquina.
- Tenha o Laragon ativo com o MySQL rodando na porta `3306`.

### 2. Ativação do Ambiente e Instalação
Abra o terminal dentro da pasta `flask-api` e rode os comandos:

```bash
# Ativa o ambiente virtual Python (no Windows)
.\venv\Scripts\Activate

# Instala todas as dependências do projeto
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados
A API precisa de um arquivo `.env` para conectar ao banco. Verifique se ele existe e tem o formato:
```env
SECRET_KEY=sua_chave_flask
JWT_SECRET_KEY=sua_chave_jwt
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/loja_multi_db
```
Caso as tabelas ainda não existam, rode as migrações:
```bash
python run_migrations.py
```

### 4. Inicializar o Servidor
Com tudo configurado e o banco de dados rodando através do Laragon, suba a aplicação com:
```bash
python app.py
```
A API ficará online em `http://127.0.0.1:5000/`.

---

## 🗺️ Mapa de Rotas da API

Ao acessar a raiz da API (`GET /`) via navegador, você verá também um mapa estruturado em JSON detalhando as rotas disponíveis. Abaixo está o resumo da documentação:

### 🔐 Autenticação (`/api/auth`)
Rotas para obter acesso ao sistema.
- `POST /register`: Cadastra um usuário/dono de loja (Requer JSON `name`, `email`, `password`).
- `POST /login`: Retorna o seu token de acesso JWT (Requer JSON `email`, `password`).

### 🏪 Gerenciamento da Loja do Usuário (`/api/lojas`)
Rotas isoladas para criar a sua marca. **Requer Token JWT logado.**
- `POST /`: Cria a sua loja (Requer JSON `name`, e opcional `description`). Gera o "slug" (Nome de URL único).
- `GET /<slug>`: *(Acesso Público)* Retorna informações de uma vitrine e todos os seus produtos.

### 📦 Produtos da Loja Atual (`/api/admin/produtos`)
Painel de administração exclusivo da loja a qual o dono pertence. **Requer Token JWT logado.**
- `GET /`: Lista todos os produtos cadastrados da loja atual do usuário logado.
- `POST /`: Adiciona um novíssimo produto no seu estoque. 

### 📊 Painel Master do Sistema (`/api/master`)
Área de controle para os administradores gerais da plataforma inteira.
- `GET /lojas`: Retorna uma lista contendo **todas as lojas** ativas na plataforma e informações sobre seus donos.
- `GET /estatisticas`: Retorna métricas analíticas preciosas (Quantidade de lojas, evolução e adesão em 7 dias, ranqueamento top 5 lojas com mais estoque, etc).

---

Feito com ☕ e muito código.
