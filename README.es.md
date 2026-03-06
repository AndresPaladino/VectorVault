# VectorVault

> [English](./README.md)

Subí imágenes y buscalas por significado. VectorVault usa embeddings para encontrar imágenes visualmente similares a una búsqueda de texto.

## Estado

En desarrollo, por ahora solo existe el schema de base de datos y las migraciones.

---

## Base de datos

Postgres con la extensión [pgvector](https://github.com/pgvector/pgvector). El schema tiene 3 tablas:

### `assets`
Representa una imagen subida al sistema.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | PK |
| `storage_path` | String | Ruta en disco donde está guardada la imagen |
| `original_filename` | String | Nombre original del archivo |
| `bytes` | BigInteger | Peso del archivo en bytes |
| `created_at` | Timestamp | Fecha de subida |

### `embedding_models`
Registra los modelos usados para generar embeddings. Permite asociar cada vector al modelo que lo generó.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | PK |
| `provider` | String | Ej: `"openclip"` |
| `name` | String | Ej: `"ViT-B-32"` |
| `pretrained` | String | Nombre del checkpoint, ej: `"laion2b_s34b_b79k"` |
| `dim` | Integer | Dimensión del vector generado |
| `created_at` | Timestamp | Fecha de registro |

> La combinación `(provider, name, pretrained)` es única.

### `embeddings`
Relaciona un asset con su vector, generado por un modelo específico.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | PK |
| `asset_id` | UUID | FK → `assets.id` (CASCADE) |
| `model_id` | UUID | FK → `embedding_models.id` (RESTRICT) |
| `vector` | Vector(512) | Embedding generado |
| `created_at` | Timestamp | Fecha de generación |

> La combinación `(asset_id, model_id)` es única — un embedding por modelo por asset.  
> Hay un índice HNSW sobre `vector` con distancia coseno para búsqueda eficiente.

---

## Levantar la base de datos

```bash
docker compose up -d
```

Correr las migraciones:

```bash
cd backend
alembic upgrade head
```

---

## Variables de entorno

Copiá `.env.example` y completá los valores:

```bash
cp .env.example .env
```
