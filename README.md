# Secretary-IA

Assistente virtual capaz de realizar diversas tarefas. O projeto reúne um backend em **Python (FastAPI)**, um banco de dados **PostgreSQL** e uma interface de administração via **pgAdmin**, todos orquestrados com **Docker Compose**.

---

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Configuração do ambiente](#configuração-do-ambiente)
- [Subindo a aplicação](#subindo-a-aplicação)
- [Serviços disponíveis](#serviços-disponíveis)
- [Notas por sistema operacional](#notas-por-sistema-operacional)

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e Docker Compose instalados
- No Windows: Docker Desktop com backend **WSL2** habilitado

Não é necessário instalar Python nem PostgreSQL na máquina — tudo roda em containers.

---

## Estrutura do projeto

```
secretary-ia/
├── .env                      # variáveis de ambiente (credenciais e config)
├── .gitattributes            # normalização de fim de linha (Windows)
├── docker-compose.yml        # orquestração dos serviços
└── app/                      # contexto de build do backend
    ├── Dockerfile
    ├── requirements.txt
    ├── backend/              # pacote Python (a API)
    │   └── main.py
    └── frontend/             # arquivos estáticos (formulário)
        └── index.html
```

Três serviços compõem o ambiente:

- **db** — PostgreSQL 16, com locale configurado para pt-BR.
- **app** — backend FastAPI que expõe a API e serve o formulário estático.
- **pgadmin** — interface web para administrar o banco.

---

## Configuração do ambiente

### 1. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o conteúdo abaixo, **ajustando as senhas**:

```env
POSTGRES_USER=gustavo
POSTGRES_PASSWORD=troque_esta_senha
POSTGRES_DB=meu_banco

PGADMIN_EMAIL=gustavo@exemplo.com
PGADMIN_PASSWORD=troque_este_admin

# host = "db" (nome do serviço na rede Docker), NÃO localhost
DATABASE_URL=postgresql+psycopg://gustavo:troque_esta_senha@db:5432/meu_banco
```

> **Importante:** o `.env` contém credenciais e **não deve ser versionado**. Adicione-o ao `.gitignore`.

### 2. Dependências do backend

O arquivo `app/requirements.txt` define as dependências Python:

```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.35
psycopg[binary]==3.2.3
python-multipart==0.0.12
```

### 3. Normalização de fim de linha (Windows)

Para evitar problemas de `CRLF` vs `LF` ao versionar o projeto, o `.gitattributes` garante que os arquivos usem `LF` dentro dos containers Linux:

```gitattributes
* text=auto eol=lf
*.ps1 text eol=crlf
```

---

## Subindo a aplicação

Na raiz do projeto, execute:

```bash
docker compose up -d --build
```

O parâmetro `--build` reconstrói a imagem do backend, e `-d` roda em segundo plano. O `pgAdmin` e o `app` só sobem depois que o healthcheck do banco confirmar que o PostgreSQL está pronto para aceitar conexões.

Para acompanhar os logs:

```bash
docker compose logs -f
```

Para parar os serviços (mantendo os dados):

```bash
docker compose down
```

Para parar **e apagar os dados** do banco:

```bash
docker compose down -v
```

---

## Serviços disponíveis

Após subir o ambiente, os serviços ficam acessíveis em:

| Serviço | URL | Observação |
|---|---|---|
| Formulário | http://localhost:8000 | Interface estática servida pelo FastAPI |
| Health check | http://localhost:8000/health | Retorna a versão do PostgreSQL se a conexão estiver OK |
| pgAdmin | http://localhost:5050 | Administração do banco |
| PostgreSQL | localhost:5432 | Acesso via cliente externo (DBeaver, psql) |

### Conectando o pgAdmin ao banco

Ao cadastrar o servidor dentro do pgAdmin, use:

| Campo | Valor |
|---|---|
| Host name/address | `db` |
| Port | `5432` |
| Database | `meu_banco` |
| User | `gustavo` |
| Password | (o valor de `POSTGRES_PASSWORD`) |

> O host é `db` (nome do serviço), **não** `localhost`: de dentro da rede Docker, um container encontra o outro pelo nome do serviço. `localhost` só funciona a partir da sua própria máquina.

---

## Notas por sistema operacional

O `docker-compose.yml` é idêntico nos dois sistemas — o que muda é apenas o ambiente ao redor.

### Windows

- Os **dados do banco** ficam em um volume nomeado (`pgdata`), dentro do ext4 da VM do WSL2, com boa performance de I/O independentemente de onde o projeto está.
- Se o projeto estiver em uma pasta Windows (ex.: `C:\Users\...`), o **hot reload** do backend pode não disparar, pois os eventos de arquivo não atravessam de forma confiável a fronteira NTFS ↔ Linux. Para contornar, adicione a variável `WATCHFILES_FORCE_POLLING: "true"` ao serviço `app` no `docker-compose.yml`.

### macOS

- Em Apple Silicon (M1/M2/M3), todas as imagens (`postgres`, `python`, `pgadmin4`) possuem build **arm64 nativo**, rodando sem emulação.
- Os dados do banco também ficam em volume nomeado, protegidos da lentidão de bind mount.

---

## Próximos passos

- Persistir os dados do formulário no PostgreSQL (rota `/enviar`).
- Evoluir o frontend conforme a necessidade.