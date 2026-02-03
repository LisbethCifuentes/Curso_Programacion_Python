# 🚀 INICIO RÁPIDO - PETS + REDIS PROJECT

## ⚡ Instrucciones en 5 Pasos

### 1️⃣ LEVANTAR LOS SERVICIOS

```bash
docker-compose up --build
```

Esto iniciará automáticamente:
- ✅ Redis (puerto 6379)
- ✅ MongoDB (puerto 27017)
- ✅ Django API (puerto 8000)
- ✅ 3 Workers/Consumidores

**Espera a ver estos mensajes:**
```
pets-redis        | Ready to accept connections
pets-mongodb      | Waiting for connections
pets-django-api   | Starting development server at http://0.0.0.0:8000/
pets-consumer-1   | [Consumer-1] 👂 Waiting for tasks...
pets-consumer-2   | [Consumer-2] 👂 Waiting for tasks...
pets-consumer-3   | [Consumer-3] 👂 Waiting for tasks...
```

---

### 2️⃣ MIGRAR LA BASE DE DATOS (en otra terminal)

```bash
docker exec -it pets-django-api python manage.py migrate
```

---

### 3️⃣ CREAR SUPERUSUARIO

```bash
docker exec -it pets-django-api python manage.py createsuperuser
```

Usa estas credenciales:
- **Username**: `admin`
- **Email**: (presiona Enter)
- **Password**: `admin123`
- **Confirmar password**: `admin123`

---

### 4️⃣ OBTENER TOKEN JWT

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Copia el `access` token de la respuesta.**

---

### 5️⃣ CREAR UNA MASCOTA (y ver la magia)

Reemplaza `TU_TOKEN_AQUI` con el token que copiaste:

```bash
curl -X POST http://localhost:8000/api/pets/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d '{
    "name": "Max",
    "species": "Dog",
    "age": 5,
    "owner": "Juan Pérez",
    "vaccinated": true
  }'
```

---

## 🎉 ¡Listo! ¿Qué Pasó?

1. ✅ La mascota se guardó en **MongoDB**
2. ✅ Se envió una tarea a la cola de **Redis**
3. ✅ Uno de los 3 **workers** la procesó automáticamente
4. ✅ Se generó un **archivo JSON enriquecido** con:
   - Información de Wikipedia sobre la especie
   - Datos curiosos (esperanza de vida, dieta, etc.)
   - Recomendaciones de salud personalizadas

---

## 👀 Ver los Resultados

### Ver logs de un worker procesando:
```bash
docker logs -f pets-consumer-1
```

Verás algo como:
```
[2025-01-24 14:30:22] [Consumer-1] [INFO] 📨 Received new task from queue
[2025-01-24 14:30:22] [Consumer-1] [INFO] Processing pet: Max (Dog) - ID: 67698abc
[2025-01-24 14:30:23] [Consumer-1] [INFO] Fetching Wikipedia data for Dog...
[2025-01-24 14:30:24] [Consumer-1] [SUCCESS] ✅ Enriched data saved to: 67698abc_Max_20250124_143024.json
```

### Ver archivo JSON generado:
```bash
docker exec -it pets-consumer-1 ls -lh /app/processed_data
docker exec -it pets-consumer-1 cat /app/processed_data/NOMBRE_ARCHIVO.json
```

### Ver estadísticas de Redis:
```bash
curl http://localhost:8000/api/redis/stats/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## 📝 Ejemplos Windows (PowerShell)

### Crear usuario:
```powershell
docker exec -it pets-django-api python manage.py createsuperuser
```

### Obtener token:
```powershell
curl.exe -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{\"username\": \"admin\", \"password\": \"admin123\"}'
```

### Crear mascota:
```powershell
curl.exe -X POST http://localhost:8000/api/pets/ -H "Content-Type: application/json" -H "Authorization: Bearer TU_TOKEN" -d '{\"name\": \"Luna\", \"species\": \"Cat\", \"age\": 3, \"owner\": \"María\", \"vaccinated\": true}'
```

---

## 🔥 Script de Prueba Automático

Ejecuta el script de prueba:

```bash
./test_quick.sh
```

Esto verificará:
- ✅ Redis funcionando
- ✅ Workers activos
- ✅ Tareas pendientes
- ✅ Archivos procesados
- ✅ API respondiendo

---

## 📚 Más Información

- **README.md** - Documentación completa
- **ARQUITECTURA.md** - Diagramas del sistema
- **COMANDOS.txt** - Todos los comandos disponibles

---

## 🛑 Detener Todo

```bash
docker-compose down
```

Para limpiar TODO (incluyendo datos):
```bash
docker-compose down -v
```

---

## ❓ Problemas Comunes

### "Port 8000 already in use"
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "Redis connection refused"
```bash
docker-compose restart redis
docker logs pets-redis
```

### Workers no procesan
```bash
docker-compose restart pets-consumer-1
docker logs --tail 50 pets-consumer-1
```

---

## 🎯 Próximos Pasos

1. Crea varias mascotas diferentes (perros, gatos, pájaros)
2. Observa cómo los 3 workers procesan las tareas en paralelo
3. Revisa los archivos JSON generados
4. Experimenta con los filtros de la API
5. Lee el README.md para funcionalidades avanzadas

---

**¡Disfruta del proyecto! 🐾**
