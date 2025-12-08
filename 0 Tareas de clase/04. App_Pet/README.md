📘 API de Mascotas – Proyecto Flask

# 🐾 Pets API – Flask + MongoDB + Autenticación + SSR

Esta es una API desarrollada como parte del curso de Desarrollo Web.  
Incluye autenticación, operaciones CRUD básicas, filtros, conexión con MongoDB, Server-Side Rendering (SSR), y pruebas con Postman.

---

## 📌 Objetivos cumplidos en la tarea

- ✔ Migración de datos “quemados” a **MongoDB**
- ✔ Crear **usuarios** y soportar autenticación
- ✔ Implementar **Login** y obtener **Token**
- ✔ Permitir creación de ítems (mascotas) con token válido
- ✔ Crear y documentar **endpoints REST**
- ✔ Implementar **SSR (Server Side Rendering)** con plantillas HTML
- ✔ Organizar el proyecto usando buenas prácticas
- ✔ Generar **colección Postman** completa para pruebas
- ✔ Documentar y entregar la API

---

# 🚀 Ejecutar el Proyecto

### 1️⃣ Instalar dependencias

```bash
pip install -r requirements.txt


## Ejemplos de uso (curl)

### 1. SignIn user (registro, rol por defecto: client)

```bash
curl -X POST http://127.0.0.1:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "password": "123456"
  }'

2. Create user (con rol, por ejemplo admin)

curl -X POST http://127.0.0.1:5000/auth/create \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123",
    "role": "admin"
  }'

3. Login user

curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "password": "123456"
  }'

La respuesta incluye un token:

{
  "message": "Login ok",
  "token": "AQUI_VA_EL_TOKEN"
}

4. Post Item (Pet) – requiere token

curl -X POST http://127.0.0.1:5000/pets/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer AQUI_VA_EL_TOKEN" \
  -d '{
    "name": "Max",
    "species": "dog",
    "age": 2,
    "owner": "Laura",
    "vaccinated": true
  }'

5. Get Items con filtros

# todas las mascotas
curl http://127.0.0.1:5000/pets/

# filtrar por especie
curl "http://127.0.0.1:5000/pets/?species=dog"

# filtrar por vacunación
curl "http://127.0.0.1:5000/pets/?vaccinated=true"

# combinación de filtros
curl "http://127.0.0.1:5000/pets/?species=dog&vaccinated=true"

6. Endpoint SSR (Server Side Rendering)

GET http://127.0.0.1:5000/pets/html

