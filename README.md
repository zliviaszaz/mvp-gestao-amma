# MVP de Gestão – AMMA

Aplicação web responsiva para apoiar o cadastro de participantes, o registro de atividades, as inscrições e o controle de frequência.

## Escopo inicial
- Cadastro, consulta e atualização de participantes.
- Cadastro e consulta de atividades.
- Inscrição de participantes em atividades.
- Registro e consulta de frequência por inscrição e data.
- API REST com validação no servidor.

> Este repositório contém uma implementação inicial do MVP para desenvolvimento e testes. Não representa uma implantação oficial ou uma validação pela AMMA. Use apenas dados fictícios durante os testes.

## Tecnologias
- Frontend: Angular 22 + TypeScript.
- Backend: Python 3.12 + FastAPI.
- Persistência: PostgreSQL (compatível com Supabase).
- Testes: Pytest.

## Estrutura
```text
mvp-gestao-amma/
├── backend/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── tests/
│   │   └── test_health.py
│   ├── .env.example
│   └── requirements.txt
└── frontend/
    ├── package.json
    ├── angular.json
    ├── tsconfig.json
    └── src/
        ├── index.html
        ├── main.ts
        └── app/
            ├── app.component.ts
            ├── app.component.html
            ├── app.component.css
            └── app.config.ts
```

## 1. Configurar o backend
Requisitos: Python 3.12 e PostgreSQL.

No terminal, entre na pasta `backend` e execute:

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e informe a URL de conexão PostgreSQL. Exemplo:
```env
DATABASE_URL=postgresql+psycopg://usuario:senha@host:5432/postgres
```

Inicie a API:
```bash
uvicorn app.main:app --reload
```

A documentação interativa ficará em `http://127.0.0.1:8000/docs`.

## 2. Configurar o frontend
Requisitos: Node.js compatível com Angular 22 e npm.

No terminal, entre na pasta `frontend` e execute:
```bash
npm install
npm start
```

A aplicação ficará disponível em `http://localhost:4200`.

O frontend espera a API em `http://127.0.0.1:8000`. Para outro endereço, ajuste `API_URL` em `frontend/src/app/app.component.ts`.

## 3. Executar os testes
Na pasta `backend`, com o ambiente virtual ativo:
```bash
pytest
```

## Segurança e próximos passos
- Não coloque senhas, tokens ou chaves do Supabase no frontend ou no GitHub.
- Configure CORS para os domínios autorizados antes de publicar.
- A autenticação de colaboradores deverá ser integrada antes de utilizar dados reais.
- Configure migrações de banco (por exemplo, Alembic), backups e política de acesso antes de produção.
- O exemplo de CORS e a configuração local devem ser ajustados para o ambiente real.

## Modelo de dados
- `participantes`: dados básicos do participante.
- `atividades`: atividades oferecidas.
- `inscricoes`: vínculo entre participante e atividade, sem inscrição ativa duplicada.
- `frequencias`: presença por inscrição e data, sem duplicidade para a mesma data.
