# MVP de Gestão – AMMA

MVP acadêmico de aplicação web para gestão de participantes, atividades, inscrições e frequência.

> **Estado do projeto:** versão de desenvolvimento. Use exclusivamente dados fictícios. A aplicação não está homologada pela AMMA e não deve receber dados pessoais reais. A autenticação incluída é uma base demonstrativa e requer revisão de segurança antes de qualquer uso real.

## Funcionalidades implementadas
- Login de colaborador por usuário e senha.
- Cadastro, listagem, busca e atualização de participantes.
- Cadastro e listagem de atividades.
- Inscrição de participante em atividade, com prevenção de duplicidade.
- Registro e consulta de frequência por inscrição e data, com prevenção de duplicidade.
- Validação dos dados no backend e testes automatizados da API.

## Tecnologias
- Angular 22 + TypeScript 6
- Python 3.12 + FastAPI
- SQLAlchemy + PostgreSQL (ou SQLite local para desenvolvimento)
- Pytest

## Estrutura
```text
backend/
  app/
    auth.py
    database.py
    main.py
    models.py
    schemas.py
  tests/
    conftest.py
    test_api.py
  .env.example
  requirements.txt
frontend/
  src/app/
    app.component.ts
    app.component.html
    app.component.css
    app.config.ts
  src/main.ts
  index.html
  package.json
  angular.json
  tsconfig.json
  tsconfig.app.json
```

## Executar backend
Requer Python 3.12.

```bash
cd backend
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e configure uma chave longa e aleatória para `JWT_SECRET`. Para uso local, o banco padrão é SQLite e o usuário inicial demonstrativo é criado automaticamente.

```bash
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`
Documentação: `http://127.0.0.1:8000/docs`

**Acesso local demonstrativo:** usuário `admin`; senha `MudeEstaSenha123!`. Altere `ADMIN_USERNAME` e `ADMIN_PASSWORD` nas variáveis de ambiente antes de qualquer publicação. Nunca reutilize essa senha.

## Executar frontend
Requer Node.js compatível com a versão instalada do Angular CLI.

```bash
cd frontend
npm install
npm start
```

Frontend: `http://localhost:4200`

O frontend utiliza a API em `http://127.0.0.1:8000/api`. Altere `API_URL` no componente caso necessário.

## Testes
Na pasta `backend`, com o ambiente virtual ativado:
```bash
pytest -q
```

Os testes usam banco SQLite isolado e verificam login, proteção de rotas, cadastro/consulta de participantes e atividades, inscrição, prevenção de inscrição duplicada e registro de frequência.

## Segurança: limitações conhecidas
- Senhas são armazenadas como hash Argon2.
- A API usa token JWT com expiração; rotas de dados exigem autenticação.
- Para produção, implementar revogação/rotação de refresh tokens, limitação de tentativas de login, HTTPS, CORS restrito ao domínio definitivo, gestão segura de segredos, política de backup, migrações de banco e revisão independente.
- O login inicial é apenas para demonstração; não representa cadastro de usuários nem gestão completa de colaboradores.
- Não publique `.env`, senhas, chaves ou dados pessoais. O `.gitignore` exclui esses arquivos.

## Modelo de dados
- Participante: identificação, nome, data de nascimento opcional, telefone opcional e status.
- Atividade: nome, descrição opcional, data de início e status.
- Inscrição: vínculo entre participante e atividade, data e status.
- Frequência: vínculo com inscrição, data de registro e presença.

A restrição única impede duas inscrições do mesmo participante na mesma atividade e dois registros de frequência para a mesma inscrição na mesma data.
