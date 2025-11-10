# 🏨 Booking System API

Sistema profissional de reservas desenvolvido com FastAPI, incluindo autenticação JWT, lógica complexa de disponibilidade e API RESTful completa.

## 🚀 Funcionalidades

- ✅ **Autenticação JWT** - Sistema seguro de login/registro
- ✅ **Gestão de Espaços** - CRUD completo de espaços para reserva
- ✅ **Sistema de Reservas** - Lógica complexa de verificação de disponibilidade
- ✅ **Cálculo Automático de Preços** - Baseado na duração da reserva
- ✅ **API RESTful** - Endpoints bem documentados
- ✅ **Validações de Negócio** - Horários comerciais, conflitos, etc.
- ✅ **Documentação Interativa** - Swagger/OpenAPI automática

## 🛠 Tecnologias

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL/SQLite** - Banco de dados
- **JWT** - Autenticação stateless
- **Pydantic** - Validação de dados
- **Pytest** - Testes automatizados
- **Docker** - Containerização

## 📋 Pré-requisitos

- Python 3.8+
- Git
- (Opcional) Docker e Docker Compose

## ⚡ Instalação Rápida

### 1. Clonar o repositório
```bash
git clone https://github.com/DeveloperBruNao/booking-system.git
cd booking-system

2. Configurar ambiente virtual
bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

3. Instalar dependências
bash
pip install -r requirements.txt
4. Configurar variáveis de ambiente

bash
# Copiar arquivo de exemplo
copy .env.example .env  # Windows
# ou
cp .env.example .env    # Linux/Mac

# Editar .env com suas configurações
5. Executar a aplicação
bash
python run.py

# Ou
uvicorn app.main:app --reload

6. Acessar a documentação
Abra: http://localhost:8000/docs

🐳 Execução com Docker
Usando Docker Compose (Recomendado)
bash
docker-compose up --build
Apenas Docker
bash
docker build -t booking-system .
docker run -p 8000:8000 booking-system
📚 Como Usar a API
1. Registrar um usuário
bash
POST /auth/registrar
{
  "email": "usuario@exemplo.com",
  "nome_completo": "João Silva",
  "senha": "senha123"
}
2. Fazer login
bash
POST /auth/login
{
  "email": "usuario@exemplo.com",
  "senha": "senha123"
}

# Resposta: { "access_token": "seu_token", "token_type": "bearer" }
3. Criar um espaço (requer autenticação)
bash
POST /espacos/
Authorization: Bearer seu_token
{
  "nome": "Sala de Reuniões A",
  "descricao": "Sala para 10 pessoas com projetor",
  "capacidade": 10,
  "preco_por_hora": 75.50
}
4. Verificar disponibilidade
bash
POST /reservas/verificar-disponibilidade
{
  "space_id": 1,
  "start_time": "2024-01-15T10:00:00",
  "end_time": "2024-01-15T12:00:00"
}
5. Fazer uma reserva (requer autenticação)
bash
POST /reservas/
Authorization: Bearer seu_token
{
  "space_id": 1,
  "start_time": "2024-01-15T10:00:00",
  "end_time": "2024-01-15T12:00:00"
}
6. Ver minhas reservas
bash
GET /reservas/minhas
Authorization: Bearer seu_token
🧪 Executando Testes
bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=app tests/

# Executar testes específicos
pytest tests/test_booking.py -v
📊 Endpoints Principais
Autenticação
POST /auth/registrar - Registrar novo usuário

POST /auth/login - Fazer login

GET /auth/me - Obter dados do usuário logado

Espaços
GET /espacos/ - Listar espaços disponíveis

GET /espacos/{id} - Obter detalhes de um espaço

POST /espacos/ - Criar novo espaço

PUT /espacos/{id}/disponibilidade - Atualizar disponibilidade

Reservas
POST /reservas/ - Criar reserva

GET /reservas/minhas - Listar minhas reservas

GET /reservas/{id} - Obter detalhes da reserva

POST /reservas/{id}/cancelar - Cancelar reserva

POST /reservas/verificar-disponibilidade - Verificar disponibilidade

🔧 Configuração
Variáveis de Ambiente (.env)
env
SECRET_KEY=sua_chave_secreta_jwt
DATABASE_URL=sqlite:///./booking.db
# ou para PostgreSQL:
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/booking_db
Estrutura do Projeto
text
booking-system/
├── app/
│   ├── models/          # Modelos de banco
│   ├── schemas/         # Schemas Pydantic
│   ├── crud/            # Operações de banco
│   ├── auth/            # Autenticação
│   ├── utils/           # Utilitários
│   ├── main.py          # Aplicação FastAPI
│   └── database.py      # Configuração do banco
├── tests/               # Testes automatizados
├── requirements.txt     # Dependências
└── docker-compose.yml   # Docker
🤝 Contribuindo
Fork o projeto

Crie uma branch: git checkout -b feature/nova-funcionalidade

Commit suas mudanças: git commit -m 'feat: adiciona nova funcionalidade'

Push para a branch: git push origin feature/nova-funcionalidade

Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

👨‍💻 Desenvolvedor
Bruno - DeveloperBruNao

🆕 Próximas Funcionalidades
Notificações por email

Sistema de pagamentos

Dashboard administrativo

API para mobile

Cache com Redis

Filas com Celery