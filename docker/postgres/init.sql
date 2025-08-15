-- TaskFlow API - PostgreSQL Initialization Script
-- Este script se ejecuta automáticamente cuando PostgreSQL arranca por primera vez

-- Crear la base de datos si no existe
SELECT 'CREATE DATABASE taskflow_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'taskflow_db')\gexec

-- Crear el usuario si no existe
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'postgres') THEN

      CREATE ROLE postgres LOGIN PASSWORD '171216';
   END IF;
END
$do$;

-- Dar todos los permisos al usuario
GRANT ALL PRIVILEGES ON DATABASE taskflow_db TO postgres;
GRANT CREATE ON DATABASE taskflow_db TO postgres;

-- Mensaje de confirmacion
\echo 'Base de datos TaskFlow inicializada correctamente'