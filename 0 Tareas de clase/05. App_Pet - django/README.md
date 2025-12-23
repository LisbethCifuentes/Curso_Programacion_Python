# 🐾 Pet App - Django + MongoDB + JWT

Aplicación web para gestionar mascotas con Django, MongoDB y autenticación JWT.

## 📋 Requisitos del Proyecto

✅ API CRUD completo de mascotas  
✅ Vista renderizada (HTML) sin autenticación  
✅ Endpoints protegidos en `/api/` usando JWT  
✅ Ejecutar todo con `docker-compose up --build`  

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 4.2.7
- **Base de Datos:** MongoDB 7.0
- **ORM:** MongoEngine 0.27.0
- **API:** Django REST Framework 3.14.0
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Contenedores:** Docker + Docker Compose

---

## 📁 Estructura del Proyecto

```
05.App_Pet-django/
├── pets_project/                # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs principales
│   ├── asgi.py
│   └── wsgi.py
├── pets/                        # Aplicación de mascotas
│   ├── __init__.py
│   ├── models.py               # Modelo Pet (MongoEngine)
│   ├── views.py                # Vistas y API endpoints
│   ├── urls.py                 # URLs de la app
│   └── admin.py
├── templates/                   # Templates HTML
│   └── pets/
│       └── pets_list.html      # Vista pública de mascotas
├── Dockerfile                   # Imagen Docker de Django
├── docker-compose.yml           # Orquestación de contenedores
├── requirements.txt             # Dependencias Python
├── manage.py                    # Script de gestión Django
└── LEEME.md                     # Este archivo
```

---

## 🚀 Instalación y Ejecución

### Prerequisitos

- Docker Desktop instalado
- Git (opcional)

### Paso 1: Clonar o descargar el proyecto

```bash
cd 05.App_Pet-django
```

### Paso 2: Levantar los contenedores

```bash
docker-compose up --build
```

Esto hará:
- Construir la imagen de Django
- Descargar MongoDB 7.0
- Iniciar ambos servicios
- Django estará disponible en `http://localhost:8000`
- MongoDB en `localhost:27017`

### Paso 3: Migrar la base de datos (en otra terminal)

```bash
docker exec -it pets-django-api python manage.py migrate
```

### Paso 4: Crear un superusuario

```bash
docker exec -it pets-django-api python manage.py createsuperuser
```

Ejemplo:
- Username: `admin`
- Email: (presiona Enter)
- Password: `admin123`

---

## 🌐 Endpoints Disponibles

### 📄 Vista Pública (Sin autenticación)

| URL | Método | Descripción |
|-----|--------|-------------|
| `/` | GET | Vista HTML de todas las mascotas |

**Ejemplo:** `http://localhost:8000/`

---

### 🔑 Autenticación JWT

| URL | Método | Descripción |
|-----|--------|-------------|
| `/api/token/` | POST | Obtener access y refresh token |
| `/api/token/refresh/` | POST | Renovar access token |

**Ejemplo de solicitud:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 🔒 API de Mascotas (Requiere JWT)

| URL | Método | Descripción |
|-----|--------|-------------|
| `/api/pets/` | GET | Listar todas las mascotas |
| `/api/pets/` | POST | Crear nueva mascota |
| `/api/pets/<id>/` | GET | Obtener mascota específica |
| `/api/pets/<id>/` | PUT | Actualizar mascota |
| `/api/pets/<id>/` | DELETE | Eliminar mascota |

#### Filtros disponibles:
- Por especie: `/api/pets/?species=Dog`
- Por vacunación: `/api/pets/?vaccinated=true`
- Combinados: `/api/pets/?species=Cat&vaccinated=false`

---

## 📝 Ejemplos de Uso

### 1. Crear una mascota

```bash
curl -X POST http://localhost:8000/api/pets/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN" \
  -d '{
    "name": "Max",
    "species": "Dog",
    "age": 3,
    "owner": "Juan Pérez",
    "vaccinated": true
  }'
```

### 2. Listar todas las mascotas

```bash
curl http://localhost:8000/api/pets/ \
  -H "Authorization: Bearer TU_TOKEN"
```

### 3. Filtrar perros vacunados

```bash
curl "http://localhost:8000/api/pets/?species=Dog&vaccinated=true" \
  -H "Authorization: Bearer TU_TOKEN"
```

### 4. Actualizar una mascota

```bash
curl -X PUT http://localhost:8000/api/pets/ID_MASCOTA/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN" \
  -d '{"age": 4, "vaccinated": true}'
```

### 5. Eliminar una mascota

```bash
curl -X DELETE http://localhost:8000/api/pets/ID_MASCOTA/ \
  -H "Authorization: Bearer TU_TOKEN"
```

---

## 🧪 Pruebas Manuales

### ✅ Verificar que la vista HTML funciona (sin auth):
```
http://localhost:8000/
```
**Resultado esperado:** Página HTML con lista de mascotas

---

### ❌ Verificar que la API requiere autenticación:
```bash
curl http://localhost:8000/api/pets/
```
**Resultado esperado:** 
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### ✅ Verificar que la API funciona con token:
```bash
# 1. Obtener token
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' \
  | grep -o '"access":"[^"]*' | cut -d'"' -f4)

# 2. Usar token
curl http://localhost:8000/api/pets/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🗄️ Modelo de Datos

### Pet (Mascota)

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `name` | String | Sí | Nombre de la mascota |
| `species` | String | Sí | Especie (Dog, Cat, Bird, etc.) |
| `age` | Integer | Sí | Edad en años |
| `owner` | String | Sí | Nombre del dueño |
| `vaccinated` | Boolean | No | Estado de vacunación (default: false) |

**Ejemplo JSON:**
```json
{
  "id": "67698abc123def456789",
  "name": "Max",
  "species": "Dog",
  "age": 3,
  "owner": "Juan Pérez",
  "vaccinated": true
}
```

---

## 🛠️ Comandos Útiles

### Docker

```bash
# Levantar contenedores
docker-compose up -d

# Ver logs en tiempo real
docker logs -f pets-django-api
docker logs -f pets-mongodb

# Detener contenedores
docker-compose down

# Eliminar todo (incluyendo datos)
docker-compose down -v

# Reconstruir imágenes
docker-compose up --build
```

### Django

```bash
# Crear superusuario
docker exec -it pets-django-api python manage.py createsuperuser

# Acceder al shell de Django
docker exec -it pets-django-api python manage.py shell

# Migrar base de datos
docker exec -it pets-django-api python manage.py migrate

# Ver logs del servidor
docker logs pets-django-api --tail 50 -f
```

### MongoDB

```bash
# Acceder al shell de MongoDB
docker exec -it pets-mongodb mongosh pets_database

# Comandos dentro de mongosh:
show collections           # Mostrar colecciones
db.pet.find()             # Ver todas las mascotas
db.pet.find().pretty()    # Ver con formato
db.pet.countDocuments()   # Contar documentos
```

---

## 🔐 Seguridad

- Los tokens JWT expiran después de **1 hora**
- Los refresh tokens expiran después de **1 día**
- Las contraseñas se almacenan hasheadas (bcrypt)
- CORS está habilitado para desarrollo (desactivar en producción)
- La SECRET_KEY debe cambiarse en producción

---

## 🚨 Solución de Problemas

### Puerto 8000 ya en uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### MongoDB no se conecta
```bash
# Verificar estado
docker-compose ps

# Reiniciar solo MongoDB
docker-compose restart mongo
```

### Token expirado
```bash
# Obtener nuevo token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Ver errores detallados
```bash
docker logs pets-django-api --tail 100
```

---

## 📦 Variables de Entorno

Definidas en `docker-compose.yml`:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `MONGO_HOST` | `mongo` | Host de MongoDB |
| `MONGO_DB` | `pets_database` | Nombre de la base de datos |
| `MONGO_INITDB_DATABASE` | `pets_database` | DB inicial de MongoDB |

---

## 🎯 Características Implementadas

✅ CRUD completo (Create, Read, Update, Delete)  
✅ Autenticación JWT con tokens de acceso y refresco  
✅ Vista HTML renderizada sin autenticación  
✅ API REST protegida con JWT  
✅ Filtros de búsqueda por especie y vacunación  
✅ Validación de campos requeridos  
✅ Interfaz web de Django REST Framework  
✅ Dockerizado completamente  
✅ MongoDB como base de datos NoSQL  
✅ Healthcheck para MongoDB  

---

## 📚 Dependencias

```txt
Django==4.2.7
mongoengine==0.27.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
PyJWT==2.8.0
pymongo==4.6.0
django-cors-headers==4.3.1
```

---

## 👨‍💻 Autor

Proyecto desarrollado como tarea de Desarrollo Web

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 🔗 Enlaces Útiles

- [Documentación de Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [MongoEngine](http://mongoengine.org/)
- [JWT Simple](https://django-rest-framework-simplejwt.readthedocs.io/)
- [MongoDB](https://www.mongodb.com/docs/)
- [Docker](https://docs.docker.com/)

---

## ✨ Próximas Mejoras

- [ ] Agregar paginación a la lista de mascotas
- [ ] Implementar búsqueda por nombre
- [ ] Agregar imágenes de mascotas
- [ ] Sistema de roles (admin, user)
- [ ] Tests unitarios y de integración
- [ ] Documentación automática con Swagger/OpenAPI
- [ ] Deploy en producción (Heroku, AWS, etc.)