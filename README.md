# RAG con Google Generative File Search (GFS)

Exploración y evaluación de las capacidades de Google Generative File Search como solución RAG gestionada.

## Descripción del Proyecto

Este proyecto compara Google GFS (RAG gestionado) con implementaciones RAG personalizadas para comprender:
- Características de rendimiento (latencia, relevancia, costo)
- Calidad de recuperación versus pipelines personalizados
- Idoneidad según casos de uso

## Configuración

**Requisitos**: Python 3.12, uv

```bash
# Instalar dependencias
uv sync

# Configurar clave API
echo "GOOGLE_API_KEY=su_clave_aqui" > .env
```

## Estructura del Proyecto

- `data/`: Corpus de documentos (excluido de git)
- `notebooks/`: Notebooks exploratorios de Jupyter
- `src/`: Módulos reutilizables
- `models/`: Stores de GFS y artefactos RAG personalizados
- `reports/`: Resultados de análisis

## Desarrollo

```bash
# Ejecutar notebook EDA
jupyter notebook notebooks/01_data_exploration.ipynb

# Ejecutar pruebas
pytest

# Formatear código
ruff format .
```
