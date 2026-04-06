# 🍕 API Pizzaria

API desenvolvida para gerenciamento de uma pizzaria, permitindo o controle de usuários, produtos (pizzas) e pedidos. O projeto segue uma arquitetura organizada em camadas (Service, Repository e Models), facilitando manutenção, escalabilidade e boas práticas de desenvolvimento.

---

## 🚀 Tecnologias Utilizadas

### 🔹 Backend

* **Python 3.5** — Linguagem principal do projeto
* **FastAPI** — Framework moderno para construção de APIs rápidas e performáticas
* **Pydantic v2** — Validação e tipagem de dados
* **SQLAlchemy** — ORM para manipulação do banco de dados

---

### 🔹 Banco de Dados

* **PostgreSQL** — Banco de dados relacional utilizado para persistência dos dados
* **psycopg2** — Driver para conexão com PostgreSQL

---

### 🔹 Segurança

* **JWT (JSON Web Token)** — Autenticação e autorização de usuários
* **bcrypt** — Hash de senhas para maior segurança

---

### 🔹 Configuração e Ambiente

* **python-dotenv** — Gerenciamento de variáveis de ambiente (.env)

---

## 📂 Estrutura do Projeto

O projeto segue uma divisão em camadas:

```bash
src/
│
├── model/          # Modelos do banco (SQLAlchemy)
├── schemas/        # Schemas (Pydantic)
├── repository/     # Acesso ao banco de dados (queries)
├── service/        # Regras de negócio
├── utils/          # Funções auxiliares
├── security/       # Autenticação e segurança (JWT)
```

---

## 🧠 Arquitetura

A API segue o padrão:

```text
Controller → Schema → Service → Repository → Database
```

### 🔹 Descrição das camadas

* **Schema (Pydantic)**
  Responsável por validar os dados de entrada e saída da API.

* **Service**
  Contém a lógica de negócio da aplicação.

* **Repository**
  Responsável pela comunicação direta com o banco de dados.

* **Model (SQLAlchemy)**
  Representa as tabelas do banco de dados.

---

## 🔑 Funcionalidades

* ✅ Cadastro de usuários
* ✅ Autenticação com JWT
* ✅ Criação e gerenciamento de pizzas
* ✅ Criação e controle de pedidos
* ✅ Atualização de dados (ex: nome da pizza)
* ✅ Controle de status de pedidos

---

## 🔒 Segurança

* Senhas são armazenadas com **hash (bcrypt)**
* Autenticação baseada em **JWT**
* Controle de acesso por usuário (admin ou comum)

---

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco
```

---

## ▶️ Como executar o projeto

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute o servidor:

```bash
uvicorn main:app --reload
```

3. Acesse a documentação automática:

```
http://localhost:8000/docs
```

---

## 📌 Boas Práticas Utilizadas

* Separação de responsabilidades (SRP)
* Tipagem estática com Pydantic
* Arquitetura em camadas
* Validação de dados na entrada
* Uso de variáveis de ambiente

---


## 👨‍💻 Autor
#### Desenvolvido por Camyla Genelice
Projeto desenvolvido para fins de estudo e prática de desenvolvimento backend com Python.

---
