# 📋 TaskFlow API

Una API REST moderna para gestión de tareas con autenticación, filtros avanzados y documentación automática.

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.4-green?logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=django&logoColor=white)](https://django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)

## 🚀 **Características**

### ✨ **Funcionalidades principales:**
- 🔐 **Autenticación** con tokens DRF
- 📝 **CRUD completo** de tareas y etiquetas
- 🔍 **Filtros avanzados** (estado, etiquetas, búsqueda)
- 📊 **Ordenamiento** por fecha, título y etiquetas
- 👥 **Multi-usuario** con permisos de propietario
- 📖 **Documentación automática** con Swagger UI/ReDoc
- 🧪 **Suite de testing** completa con pytest
- 🏷️ **Sistema de etiquetas** many-to-many

### 🛡️ **Seguridad:**
- ✅ Validación de títulos únicos por usuario
- ✅ Permisos `IsOwner` - solo acceso a propias tareas
- ✅ Variables de entorno para configuración sensible
- ✅ Autenticación requerida en todos los endpoints protegidos
- ✅ Validación de contraseñas en registro

## 📋 **Instalación**

### **Prerrequisitos:**
- Python 3.13+
- PostgreSQL 12+
- Git

### **1. Clonar el repositorio:**
```bash
git clone https://github.com/mgguajardo/taskflow-api.git
cd taskflow-api
```

### **2. Crear entorno virtual:**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### **3. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### **4. Configurar PostgreSQL:**
```sql
-- Crear base de datos en PostgreSQL
CREATE DATABASE taskflow_db;
CREATE USER taskflow_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE taskflow_db TO taskflow_user;
```

### **5. Configurar variables de entorno:**
```bash
# Crear archivo .env en la raíz del proyecto
SECRET_KEY=tu_secret_key_super_segura_aqui
DEBUG=True
DB_NAME=taskflow_db
DB_USER=taskflow_user
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### **6. Aplicar migraciones:**
```bash
python manage.py migrate
```

### **7. Crear superusuario (opcional):**
```bash
python manage.py createsuperuser
```

### **8. Ejecutar servidor:**
```bash
python manage.py runserver
```

## 📖 **Documentación API**

### **🔗 URLs principales:**
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **Schema JSON**: http://127.0.0.1:8000/api/schema/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### **🛡️ Authentication**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Registro de nuevo usuario |
| POST | `/api/auth/login/` | Login y obtención de token |

### **📝 Tasks**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks/` | Listar tareas del usuario (con filtros) |
| POST | `/api/tasks/` | Crear nueva tarea |
| GET | `/api/tasks/{id}/` | Obtener tarea específica |
| PUT | `/api/tasks/{id}/` | Actualizar tarea completa |
| PATCH | `/api/tasks/{id}/` | Actualización parcial |
| DELETE | `/api/tasks/{id}/` | Eliminar tarea |

### **🏷️ Tags**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tags/` | Listar todas las etiquetas |
| POST | `/api/tags/` | Crear nueva etiqueta |
| GET | `/api/tags/{id}/` | Obtener etiqueta específica |
| PUT | `/api/tags/{id}/` | Actualizar etiqueta completa |
| PATCH | `/api/tags/{id}/` | Actualización parcial |
| DELETE | `/api/tags/{id}/` | Eliminar etiqueta |

## 🔍 **Filtros y Búsqueda Avanzada**

### **Parámetros de query disponibles en `/api/tasks/`:**
```bash
# Filtrar por estado completado
GET /api/tasks/?completed=true
GET /api/tasks/?completed=false

# Filtrar por etiqueta específica
GET /api/tasks/?tags=1
GET /api/tasks/?tags=2

# Búsqueda en título, descripción y nombre de etiqueta
GET /api/tasks/?search=reunion
GET /api/tasks/?search=importante

# Ordenamiento
GET /api/tasks/?ordering=-created_at    # Más recientes primero
GET /api/tasks/?ordering=title          # Alfabético por título
GET /api/tasks/?ordering=tags__name     # Por nombre de etiqueta

# Combinación de filtros
GET /api/tasks/?completed=false&tags=1&search=reunion&ordering=-created_at
```

## 🧪 **Testing**

### **Ejecutar suite completa de tests:**
```bash
pytest
```

### **Ejecutar tests específicos:**
```bash
# Tests de filtrado avanzado
pytest tasks/test_filter.py -v

# Tests con cobertura
pytest --cov=tasks

# Tests verbosos
pytest tasks/test_filter.py::test_filter_tasks_by_completed -v
```

### **📊 Suite de tests incluye:**
- ✅ **Seguridad**: Usuarios no acceden a tareas de otros
- ✅ **Filtrado por etiquetas**: Multiple tags y combinaciones
- ✅ **Filtrado por estado**: Completadas vs pendientes
- ✅ **Validaciones**: Títulos únicos por usuario
- ✅ **Permisos**: Solo propietarios pueden modificar
- ✅ **Autenticación**: Endpoints protegidos correctamente

## 🌟 **Ejemplos de uso**

### **1. Registro y autenticación:**
```bash
# Registro de nuevo usuario
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "gabriel",
    "password": "password123",
    "password2": "password123",
    "email": "gabriel@example.com"
  }'

# Login para obtener token
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "gabriel",
    "password": "password123"
  }'

# Respuesta: {"token": "abc123..."}
```

### **2. Crear etiqueta:**
```bash
curl -X POST http://127.0.0.1:8000/api/tags/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123..." \
  -d '{
    "name": "trabajo"
  }'
```

### **3. Crear tarea con etiquetas:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123..." \
  -d '{
    "title": "Reunión importante",
    "description": "Reunión con cliente sobre proyecto TaskFlow",
    "completed": false,
    "tags": [1, 2]
  }'
```

### **4. Listar tareas con filtros:**
```bash
# Todas las tareas del usuario
curl -H "Authorization: Token abc123..." \
  "http://127.0.0.1:8000/api/tasks/"

# Solo tareas completadas
curl -H "Authorization: Token abc123..." \
  "http://127.0.0.1:8000/api/tasks/?completed=true"

# Buscar tareas con "reunion"
curl -H "Authorization: Token abc123..." \
  "http://127.0.0.1:8000/api/tasks/?search=reunion"

# Tareas con etiqueta específica
curl -H "Authorization: Token abc123..." \
  "http://127.0.0.1:8000/api/tasks/?tags=1"
```

## 🛠️ **Tecnologías utilizadas**

- **Backend**: Django 5.2.4 + Django REST Framework 3.15
- **Base de datos**: PostgreSQL 12+
- **Autenticación**: Token Authentication (DRF)
- **Documentación**: drf-spectacular (OpenAPI 3.0/Swagger)
- **Testing**: pytest + pytest-django
- **Filtros**: django-filter + DRF filters
- **Validación**: Django Validators + DRF Serializers
- **Variables de entorno**: python-decouple

## 📂 **Estructura del proyecto**

```
taskflow_api/
├── config/                    # Configuración principal
│   ├── __init__.py
│   ├── settings.py           # Settings con PostgreSQL
│   ├── urls.py               # URLs principales
│   └── wsgi.py
├── tasks/                    # App principal de tareas
│   ├── __init__.py
│   ├── models.py             # Task y Tag models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # ViewSets con documentación
│   ├── urls.py               # URLs de tasks y tags
│   ├── permissions.py        # IsOwner permission
│   └── test_filter.py        # Tests de filtrado
├── accounts/                 # App de autenticación
│   ├── __init__.py
│   ├── views.py              # UserRegisterView
│   ├── serializers.py        # User serializers
│   └── urls.py               # URLs de auth
├── manage.py                 # Django management
├── requirements.txt          # Dependencias del proyecto
├── .env.example             # Template de variables de entorno
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

## 🔧 **Modelos de datos**

### **Task Model:**
```python
- title (CharField): Título único por usuario
- description (TextField): Descripción opcional
- completed (BooleanField): Estado de completado
- created_at (DateTimeField): Fecha de creación
- user (ForeignKey): Usuario propietario
- tags (ManyToManyField): Etiquetas asociadas
```

### **Tag Model:**
```python
- name (CharField): Nombre único de la etiqueta
```

## 🚀 **Próximos pasos**

- [ ] **Dockerización** completa del proyecto
- [ ] **CI/CD** con GitHub Actions
- [ ] **Deploy** en Railway/Render/DigitalOcean
- [ ] **Cache** con Redis para optimización
- [ ] **Logging** estructurado con loguru
- [ ] **Rate limiting** para protección API
- [ ] **Notificaciones** por email
- [ ] **API versioning** v2

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 👨‍💻 **Autor**

**Gabriel Guajardo**
- GitHub: [@mgguajardo](https://github.com/mgguajardo)
- LinkedIn: [Tu perfil LinkedIn]
- Email: tu.email@example.com

---

⭐ **¡Dale una estrella si te gustó el proyecto!**

## 📈 **Stats del proyecto**

- **Endpoints**: 14 endpoints completamente documentados
- **Tests**: 6+ tests automatizados
- **Cobertura**: 90%+ de código testeado
- **Documentación**: OpenAPI 3.0 completa
- **Seguridad**: Autenticación y permisos implementados
