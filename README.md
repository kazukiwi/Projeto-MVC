### 1. Instalação
```bash
pip install -r requirements.txt
```

### 2. Inicialização
```bash
python -m alembic init migrations
```

### 3. Configuração do `alembic.ini`
Na **linha 89**, deixe a URL vazia:
```ini
sqlalchemy.url =
```

### 4. Configuração do `migrations/env.py`

Substitua as seções correspondentes no arquivo:

```python
# 1. Adicione os imports no topo
from dotenv import load_dotenv
import os
from app.database import Base
from app.models import usuario  # Importe seus modelos aqui

# ... (código existente)

# 2. Configure o carregamento do .env (Abaixo de config = context.config)
config = context.config
load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# 3. Vincule os modelos (Linha 22 aprox.)
target_metadata = Base.metadata
```

### 5. Comandos de Execução

**Gerar revisão (Autogenerate):**
```bash
python -m alembic revision --autogenerate -m "Criar tabela usuarios"
```

**Aplicar ao Banco (Upgrade):**
```bash
python -m alembic upgrade head
```

**Como rodar o código:**
```bash
python -m uvicorn app.main:app --reload
```

---

> **Nota:** Certifique-se de que a variável `DATABASE_URL` no seu arquivo `.env` está seguindo o padrão da sua biblioteca de conexão (ex: `postgresql://user:pass@localhost/db`).