# 🚍 Sistema de Gestão de Passe de Transporte
API backend completa para gestão de passe de transporte digital,
desenvolvida com foco em **arquitetura limpa, princípios SOLID e boas
práticas de mercado**, garantindo escalabilidade, desacoplamento e alta
testabilidade.

------------------------------------------------------------------------

## 📌 Visão Geral

Este projeto de estudo implementa parte de um sistema de passe de transporte
digital, incluindo:

-   ✅ Controle de saldo
-   💳 Recarga de créditos
-   🚌 Débito (uso do transporte)
-   📊 Histórico detalhado de transações
-   🔐 Autenticação com JWT (Access + Refresh Token)
-   🌐 Login com Google OAuth2
-   🗂 Upload e armazenamento de arquivos com MinIO
-   🤖 Chatbot conversacional com gerenciamento de estado persistente

O sistema foi projetado como uma API RESTful assíncrona, preparada para
escalar e evoluir com facilidade.

------------------------------------------------------------------------

# 🧱 Arquitetura

O projeto atualmente segue uma arquitetura em camadas fortemente
inspirada em **Clean Architecture**, promovendo baixo acoplamento, alta coesão e facilidade
de manutenção.

## 🔄 Fluxo de Dependência

    API (Routers / Controllers)
    ↓
    Application Layer (Use Cases)
    ↓
    Domain (Models, Enums, Regras de Negócio)
    ↓
    Interfaces (Contracts / Ports)
    ↓
    Infrastructure (Repositories - MongoDB / MinIO)
    ↓
    External Systems (MongoDB / MinIO)



------------------------------------------------------------------------

## 🎯 Separação de Responsabilidades

  ```mermaid
  graph TD
  A[Router] --> B[UseCase]
  B --> C[Domain]
  B --> D[Interface]
  D --> E[Repository]
  E --> F[(MongoDB)]
  ```

 
  Camada              |  Responsabilidade |
  | :-----------------| :---------------  |
  | **Router (Controller)** | Exposição da API HTTP, validação de entrada e resposta |
  |**Use Case  (Application Layer)** | Orquestração das regras de negócio |
  |**Domain** | Entidades, modelos, enums e regras centrais do sistema |
  |**Interface (Contracts)** | Abstrações que definem contratos entre camadas |
  | **Repository (Infrastructure)** | Implementação concreta de acesso a dados |
  |**External Systems**| Sistemas externos como MongoDB e MinIO |
  

## 🏗 Princípios Aplicados

-   **Single Responsibility Principle (SRP)** --- Cada camada possui
    responsabilidade única.
-   **Dependency Inversion Principle (DIP)** --- As regras de negócio
    não dependem de implementações concretas.
-   **Separation of Concerns** --- Separação clara entre regras de
    negócio e infraestrutura.
-   **Testabilidade** --- Use cases podem ser testados isoladamente com
    mocks das interfaces.

  
------------------------------------------------------------------------

# ⚙️ Tecnologias Utilizadas

## 🚀 Backend

-   **Python 3.11+**
-   **FastAPI**
-   **Pydantic v2**
-   **Motor (MongoDB Async Driver)**
-   **JWT (JSON Web Token)**
-   **OAuth2 (Google Login)**
-   **MinIO**
-   **pydantic-settings**
-   **Docker**

------------------------------------------------------------------------

## 🗄 Banco de Dados

-   **MongoDB**
-   Operações assíncronas
-   Atualizações atômicas com `$inc`
-   Controle de concorrência com query condicional (`$gte`)

Exemplo:

``` json
{
  "balance": { "$gte": amount }
}
```

Isso evita inconsistências financeiras.

------------------------------------------------------------------------

## 🔐 Sistema de Autenticação

-   Access Token
-   Refresh Token
-   Middleware seguro
-   Dependency Injection com `get_current_user`
-   Login com Google OAuth2
-   Integração segura com JWT interno

------------------------------------------------------------------------

## 💳 Módulo Passe de Transporte

Funcionalidades:

-   Consultar saldo
-   Realizar recarga
-   Debitar saldo
-   Registrar transações automaticamente

### Conceitos Aplicados

✔️ **Atomicidade** -- Débito só ocorre se houver saldo suficiente.\
✔️ **Rastreabilidade Financeira** -- Cada operação gera uma transação
com tipo, valor, saldo antes/depois e timestamp.

------------------------------------------------------------------------

## 📊 Histórico de Transações

-   Listagem paginada
-   Ordenação por data decrescente
-   Separação entre Repository (consulta) e UseCase

------------------------------------------------------------------------

## 🤖 Chatbot com Gerenciamento de Estado

Estados:

-   IDLE
-   WAITING_RECHARGE_AMOUNT
-   CONFIRM_RECHARGE

Fluxo exemplo:

Usuário: Quero recarregar\
*Bot:* Qual valor?\
Usuário: 20\
*Bot:* Confirmar recarga de R\$20?\
Usuário: sim\
*Bot:* Recarga realizada com sucesso

----------------------------------------------------------------------

## 🛡 Tratamento de Erros

Uso de `AppException` com:

-   Status HTTP adequado
-   Código estruturado
-   Mensagens padronizadas

------------------------------------------------------------------------

## 🐳 Executando o Projeto com Docker
**📦 Pré-requisitos**

Docker e Docker Compose

1️⃣ Clonar o repositório
``` bash
git clone https://github.com/RafaelViniciusBrambillaAlves/desafio-backend-pref-rio
cd seu-repo
```
2️⃣ Criar arquivo .env
Crie um arquivo .env na raiz do projeto:
``` bash
DATABASE_URL=mongodb://mongo:27017
DB_NAME=app_db

JWT_SECRET_KEY=sua_chave_super_secreta
JWT_ALGORITHM=HS256
JWT_REFRESH_TOKEN_EXPIRES_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7

GOOGLE_CLIENT_ID=seu_google_client_id
GOOGLE_CLIENT_SECRET=seu_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123
MINIO_BUCKET=storage-photos
MINIO_SECURE=false
```
3️⃣ Subir os containers
```bash
docker-compose up --build
```

4️⃣ Acessos
```
http://localhost:8000 
```
```
http://localhost:8000/docs 
```
```
http://localhost:8000/redoc
```
``` 
http://localhost:9001
```

5️⃣ Parar containers
```
docker-compose down
```
------------------------------------------------------------------------

## 🎯 Competências Demonstradas

-   Backend moderno com FastAPI
-   Clean Architecture
-   SOLID aplicado
-   Segurança com JWT
-   Integração OAuth2
-   MongoDB assíncrono
-   Operações financeiras seguras
-   API REST profissional

------------------------------------------------------------------------

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, estudar e adaptar.

------------------------------------------------------------------------

👨‍💻 Desenvolvido para fins de estudo e evolução técnica.


