# AssisPrexTest API

API REST para gestión de productos construida con FastAPI, SQLAlchemy y PostgreSQL.

## Estructura del proyecto

```
AssisPrexTest/
├── app/
│   ├── main.py                  # Punto de entrada, lifespan, registro de rutas
│   ├── core/
│   │   ├── config.py            # Configuración con pydantic-settings
│   │   └── database.py          # Engine, session, Base y get_db
│   ├── modules/
│   │   ├── products/
│   │   │   ├── model.py         # Modelo SQLAlchemy (Product)
│   │   │   ├── schema.py        # Schemas Pydantic (CRUD + response)
│   │   │   ├── service.py       # Lógica de negocio
│   │   │   └── router.py        # Endpoints REST
│   │   └── events/
│   │       ├── model.py         # Modelo SQLAlchemy (Event)
│   │       ├── schema.py        # Schema Pydantic (EventResponse)
│   │       ├── service.py       # Registro y consulta de eventos
│   │       └── router.py        # Endpoints REST (solo lectura)
│   └── api/v1/
│       └── api.py               # Router principal v1
├── docker-compose.yml
├── Dockerfile
├── start.sh                     # Entrypoint del contenedor
├── wait_for_db.py               # Espera a que PostgreSQL esté listo
├── .env                         # Variables de entorno
└── requirements.txt
```

## Requisitos

- [Docker](https://docs.docker.com/get-docker/) y Docker Compose
- O alternativamente: Python 3.12+ y PostgreSQL

## Endpoints

### Productos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/products/` | Listar productos |
| `GET` | `/api/v1/products/{id}` | Obtener producto |
| `POST` | `/api/v1/products/` | Crear producto |
| `PUT` | `/api/v1/products/{id}` | Actualizar producto |
| `DELETE` | `/api/v1/products/{id}` | Eliminar producto |

### Eventos (solo lectura)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/events/` | Listar todos los eventos |
| `GET` | `/api/v1/events/{id}` | Obtener un evento |
| `GET` | `/api/v1/products/{id}/events/` | Eventos de un producto |

### Sistema

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/health` | Health check |

**Documentación interactiva:**  
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Modelo Product

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `int` | Identificador único (autoincremental) |
| `name` | `string` | Nombre del producto (requerido, máx 200) |
| `description` | `string \| null` | Descripción del producto |
| `price` | `float` | Precio (requerido, > 0) |
| `stock` | `int` | Cantidad en inventario (default 0) |
| `state` | `string` | Estado del producto (default "active") |
| `create_at` | `datetime` | Fecha de creación (automática) |

## Modelo Event

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `int` | Identificador único (autoincremental) |
| `product_id` | `int` | ID del producto relacionado |
| `action` | `string` | Acción: `CREATE`, `UPDATE`, `DELETE`, `STATUS_CHANGED` |
| `description` | `string \| null` | Descripción del evento |
| `create_at` | `datetime` | Fecha de creación (automática) |

> Los eventos se registran automáticamente al crear, actualizar o eliminar productos. Cuando se modifica el campo `state`, se genera un evento adicional `STATUS_CHANGED`.

## Instalación y ejecución

### Opción 1: Docker Compose (recomendado)

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd AssisPrexTest

# 2. (Opcional) Editar variables de entorno
# El archivo .env ya contiene valores por defecto funcionales.
# Si necesitas cambiarlos, edita el archivo .env antes de continuar.
nano .env

# 3. Construir y levantar los servicios
docker compose up --build -d

# 4. Verificar que todo esté funcionando
curl http://localhost:8000/health
# Respuesta esperada: {"status":"healthy"}

# 5. Probar la API
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "stock": 10}'

curl http://localhost:8000/api/v1/products/

# 6. Detener los servicios
docker compose down
```

### Opción 2: Desarrollo local (sin Docker)

```bash
# 1. Clonar y crear entorno virtual
git clone <repo-url>
cd AssisPrexTest
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar PostgreSQL
# Asegúrate de tener PostgreSQL corriendo y edita .env:
#   DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_db
# O usa SQLite por defecto (sin cambios en .env)

# 4. Ejecutar la aplicación
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# La API estará disponible en http://localhost:8000
```

## Variables de entorno (.env)

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `POSTGRES_USER` | `assisprex_user` | Usuario de PostgreSQL |
| `POSTGRES_PASSWORD` | `assisprex_pass` | Contraseña de PostgreSQL |
| `POSTGRES_DB` | `assisprex_db` | Nombre de la base de datos |
| `DATABASE_URL` | `sqlite:///./app.db` | URL de conexión a la BD |
| `SECRET_KEY` | `dev-secret-key...` | Clave secreta de la app |
| `API_V1_STR` | `/api/v1` | Prefijo de la API |
| `PROJECT_NAME` | `AssisPrexTest API` | Nombre del proyecto |
| `APP_PORT` | `8000` | Puerto de la aplicación |

> **Nota:** Al usar Docker Compose, `DATABASE_URL` se configura automáticamente para apuntar a PostgreSQL. El valor en `.env` solo se usa en desarrollo local.
