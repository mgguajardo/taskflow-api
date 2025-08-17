# 🚀 TaskFlow API
> **API REST lista para producción** con 95% de cobertura de tests, pipeline CI/CD empresarial, y estándares de seguridad modernos.

[![Pipeline CI/CD](https://github.com/mgguajardo/taskflow-api/actions/workflows/ci.yml/badge.svg)](https://github.com/mgguajardo/taskflow-api/actions)
[![Cobertura](https://img.shields.io/badge/Cobertura-95%25-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.4-green?logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=django&logoColor=white)](https://django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)](Dockerfile)
[![Estilo: Ruff](https://img.shields.io/badge/Estilo-Ruff-000000.svg)](https://github.com/astral-sh/ruff)

## 🎯 **Resumen Rápido**

Una **API de gestión de tareas nivel empresarial** construida con Django REST Framework, con filtrado avanzado, autenticación en tiempo real, y cobertura completa de tests. Ejemplo perfecto de **desarrollo backend Python moderno**.

```bash
📊 14+ endpoints REST  |  🧪 95% cobertura tests  |  🐳 Docker listo  |  🚀 Pipeline CI/CD
```

## 🌐 **Demo en Vivo y Documentación**

| Recurso | URL | Descripción |
|---------|-----|-------------|
| 📚 **Swagger UI** | `https://taskflow-api.railway.app/api/docs/` | Documentación interactiva |
| 📖 **ReDoc** | `https://taskflow-api.railway.app/api/redoc/` | Referencia hermosa de API |
| 🔗 **Schema OpenAPI** | `https://taskflow-api.railway.app/api/schema/` | Especificación de API |

## ⚡ **Características Clave**

### 🛡️ **Seguridad Empresarial**
- 🔐 **Autenticación con Tokens** estilo JWT con tokens DRF
- 👥 **Arquitectura multi-tenant** - usuarios solo acceden a sus datos
- ✅ **Sistema de permisos personalizado** (clase `IsOwner`)
- 🛡️ **Validación de entrada** con validadores Django
- 🔒 **Gestión de secretos** basada en variables de entorno

### 🎯 **Funciones API Avanzadas**
- 🔍 **Búsqueda inteligente** en título, descripción y etiquetas
- 🏷️ **Filtrado avanzado** por estado de completado y etiquetas
- 📊 **Ordenamiento flexible** por fecha, título o nombre de etiqueta
- 🔄 **Operaciones CRUD completas** con métodos HTTP apropiados
- 📝 **Validación integral** y manejo de errores

### 🧪 **Aseguramiento de Calidad**
- **95% cobertura de tests** con pytest
- **Pipeline CI/CD** con GitHub Actions
- **Formateo automático** con Ruff
- **Migraciones de base de datos** y validación de modelos
- **Contenedorización Docker** para deploys consistentes

## 🏗️ **Arquitectura y Diseño**

### **Filosofía de Diseño API**
- **Diseño RESTful** siguiendo estándares HTTP
- **Autenticación sin estado** con auth basado en tokens
- **URLs basadas en recursos** con anidamiento lógico
- **Respuestas de error consistentes** con códigos de estado apropiados
- **Especificación OpenAPI 3.0** para documentación

### **Schema de Base de Datos**
```
Usuarios (Django Auth)
    ↓
Tareas (relación 1:N)
    ↓
Etiquetas (relación M:N)
```

### **Modelo de Seguridad**
```
🔐 Autenticación → 👤 Contexto Usuario → 🛡️ Permiso IsOwner → ✅ Acceso Recurso
```

## 🚀 **Inicio Rápido**

### **Opción A: Docker (Recomendado)**
```bash
# Clonar y ejecutar con Docker
git clone https://github.com/mgguajardo/taskflow-api.git
cd taskflow-api
docker-compose up --build

# API disponible en: http://localhost:8000/api/
```

### **Opción B: Desarrollo Local**
```bash
# Configurar entorno virtual
python -m venv .venv && source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp .env.example .env  # Editar con configuración de tu BD

# Ejecutar migraciones y servidor
python manage.py migrate
python manage.py runserver
```

## 📋 **Referencia de API**

### **🔑 Endpoints de Autenticación**
```http
POST /api/auth/register/    # Registro de usuario
POST /api/auth/login/       # Login y generación de token
```

### **📝 Gestión de Tareas**
```http
GET    /api/tasks/          # Listar tareas (con filtros)
POST   /api/tasks/          # Crear tarea
GET    /api/tasks/{id}/     # Obtener tarea
PUT    /api/tasks/{id}/     # Actualizar tarea
DELETE /api/tasks/{id}/     # Eliminar tarea
```

### **🏷️ Gestión de Etiquetas**
```http
GET    /api/tags/           # Listar todas las etiquetas
POST   /api/tags/           # Crear etiqueta
GET    /api/tags/{id}/      # Obtener etiqueta
PUT    /api/tags/{id}/      # Actualizar etiqueta
DELETE /api/tags/{id}/      # Eliminar etiqueta
```

## 🔍 **Ejemplos de Filtrado Avanzado**

```bash
# Filtrar tareas completadas
GET /api/tasks/?completed=true

# Buscar en título, descripción y nombres de etiquetas
GET /api/tasks/?search=reunion

# Filtrar por etiquetas específicas
GET /api/tasks/?tags=1,2

# Filtrado complejo con ordenamiento
GET /api/tasks/?completed=false&tags=1&search=urgente&ordering=-created_at
```

## 🧪 **Testing y Calidad**

### **Ejecutar Suite de Tests**
```bash
# Suite completa con cobertura
pytest --cov=tasks --cov=accounts --cov-report=term-missing

# Categorías específicas de tests
pytest tasks/test_filter.py -v          # Tests de filtrado avanzado
pytest accounts/test_auth.py -v         # Tests de autenticación
```

### **Calidad de Código**
```bash
# Linting y formateo (usado en CI/CD)
ruff check . --fix
ruff format .
```

### **Highlights de Cobertura**
- ✅ **Flujo de autenticación** - registro, login, validación de token
- ✅ **Autorización** - usuarios solo pueden acceder a sus datos
- ✅ **Operaciones CRUD** - todos los endpoints probados apropiadamente
- ✅ **Filtrado avanzado** - combinaciones complejas de queries
- ✅ **Validación de datos** - restricciones de modelo y validación serializer
- ✅ **Casos edge** - respuestas vacías, inputs inválidos, permisos denegados

## 🛠️ **Stack Tecnológico Detallado**

### **Core Backend**
- **Django 5.2.4** - Framework web Python moderno
- **Django REST Framework 3.15** - Toolkit API poderoso
- **PostgreSQL 15** - Base de datos grado producción
- **drf-spectacular** - Generación schema OpenAPI 3.0

### **DevOps y Calidad**
- **GitHub Actions** - Pipeline CI/CD con testing automatizado
- **Docker y Docker Compose** - Desarrollo y deploy contenedorizado
- **pytest** - Framework testing Python con fixtures
- **Ruff** - Linter y formateador Python ultra-rápido
- **python-decouple** - Gestión variables de entorno

### **Documentación API**
- **Swagger UI** - Interfaz testing API interactiva
- **ReDoc** - Documentación API hermosa
- **OpenAPI 3.0** - Especificación API estándar industria

## 📈 **Rendimiento y Escalabilidad**

### **Optimización Base de Datos**
- **Claves foráneas indexadas** para queries eficientes
- **Queries select related** para prevenir problemas N+1
- **Serializers optimizados** con solo campos necesarios

### **Rendimiento API**
- **Autenticación basada en tokens** (sin estado)
- **Filtrado eficiente** con django-filter
- **Respuestas paginadas** para datasets grandes
- **Headers de cache HTTP** apropiados

## 🚀 **Listo para Deploy**

### **Características de Producción**
- ✅ **Configuración basada en entorno**
- ✅ **Contenedorización Docker**
- ✅ **Base de datos PostgreSQL** producción
- ✅ **Configuración serving archivos estáticos**
- ✅ **Headers CORS** para integración frontend
- ✅ **Middleware seguridad** habilitado

### **Opciones de Deploy**
- 🚢 **Railway** (deploy actual)
- 🌊 **DigitalOcean App Platform**
- ☁️ **AWS ECS/Elastic Beanstalk**
- 🎯 **Render** o **Heroku**

## 📊 **Métricas del Proyecto**

```
📁 Estructura Proyecto:    Arquitectura Django app limpia y escalable
🧪 Cobertura Tests:        95% (tasks, accounts, funcionalidad core)
📝 Documentación:          100% endpoints API documentados
🔍 Calidad Código:         Ruff-compliant, cero errores linting
🚀 Pipeline CI/CD:         Testing, linting y deploy automatizados
🐳 Contenedorización:      Docker-ready con builds multi-etapa
```

## 🎯 **Resultados de Aprendizaje Demostrados**

Este proyecto demuestra competencia en:

- ✅ **Desarrollo Python moderno** con type hints y mejores prácticas
- ✅ **Diseño API RESTful** siguiendo estándares HTTP
- ✅ **Modelado de base de datos** con Django ORM y PostgreSQL
- ✅ **Implementación autenticación y autorización**
- ✅ **Estrategias testing integral** con pytest
- ✅ **Setup pipeline CI/CD** con GitHub Actions
- ✅ **Contenedorización Docker** para desarrollo y producción
- ✅ **Documentación API** con OpenAPI/Swagger
- ✅ **Herramientas calidad código** y formateo automatizado

## 🔄 **Futuras Mejoras**

- [ ] **Cache Redis** para mejor rendimiento
- [ ] **Cola tareas Celery** para procesamiento background
- [ ] **Capacidades upload archivos** con integración S3
- [ ] **Notificaciones WebSocket** para actualizaciones tiempo real
- [ ] **Rate limiting API** con throttling DRF
- [ ] **Monitoreo y logging** con logs estructurados
- [ ] **Versionado API** para compatibilidad hacia atrás

## 👨‍💻 **Sobre el Desarrollador**

**Gabriel Guajardo** - Desarrollador Backend especializado en Python/Django

- 💼 **LinkedIn**: [Tu perfil LinkedIn]
- 📧 **Email**: [Tu email profesional]
- 🐙 **GitHub**: [@mgguajardo](https://github.com/mgguajardo)

---

⭐ **¡Dale una estrella si este repo te parece útil!**

🚀 **¿Listo para contratarme? Construyamos algo increíble juntos.**