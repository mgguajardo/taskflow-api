#!/bin/bash
set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 TaskFlow API - Docker Entrypoint${NC}"
echo -e "${BLUE}=================================${NC}"

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Esperar a que PostgreSQL esté disponible
log "⏳ Waiting for PostgreSQL..."
while ! python manage.py check --database default >/dev/null 2>&1; do
    warning "PostgreSQL is unavailable - sleeping"
    sleep 2
done
log "✅ PostgreSQL is available!"

# Ejecutar migraciones
log "🔄 Running database migrations..."
python manage.py migrate --no-input

# Crear superusuario si no existe
log "👤 Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@taskflow.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('ℹ️  Superuser already exists')
"

# Recopilar archivos estáticos
log "📁 Collecting static files..."
python manage.py collectstatic --no-input --clear

# Verificar configuración
log "🔍 Checking Django configuration..."
python manage.py check

log "🚀 Starting TaskFlow API server..."
echo -e "${GREEN}=================================${NC}"
echo -e "${GREEN}🎯 API Documentation: http://localhost:8000/api/docs/${NC}"
echo -e "${GREEN}📊 Admin Panel: http://localhost:8000/admin/${NC}"
echo -e "${GREEN}🔑 Superuser: admin / admin123${NC}"
echo -e "${GREEN}=================================${NC}"

# Ejecutar comando
exec "$@"