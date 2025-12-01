import json
from pathlib import Path

# Translation mappings for common terms
translations = {
    "# GFS Experiments: RAG Performance Analysis": "# Experimentos GFS: Análisis de Rendimiento RAG",
    "This notebook conducts systematic experiments with Google Generative File Search.": "Este cuaderno realiza experimentos sistemáticos con Google Generative File Search.",
    "**Objectives**:": "**Objetivos**:",
    "1. Define test query set": "1. Definir conjunto de consultas de prueba",
    "2. Measure response latency (P50, P95, P99)": "2. Medir latencia de respuesta (P50, P95, P99)",
    "3. Analyze retrieval quality": "3. Analizar calidad de recuperación",
    "4. Examine grounding/citations": "4. Examinar fundamentación/citas",
    "5. Calculate costs": "5. Calcular costos",
    "## 1. Load Store and Initialize Client": "## 1. Cargar Almacén e Inicializar Cliente",
    "## 2. Define Test Queries": "## 2. Definir Consultas de Prueba",
    "Create a diverse query set covering different patterns:": "Crear un conjunto diverso de consultas que cubra diferentes patrones:",
    "- Factual lookups": "- Búsquedas factuales",
    "- Analytical questions": "- Preguntas analíticas",
    "- Multi-document reasoning": "- Razonamiento multi-documento",
    "- Edge cases (out-of-domain)": "- Casos extremos (fuera de dominio)",
    "## 3. Run Experiments": "## 3. Ejecutar Experimentos",
    "## 4. Analyze Performance": "## 4. Analizar Rendimiento",
    "## 5. Cost Analysis": "## 5. Análisis de Costos",
    "## 6. Save Results": "## 6. Guardar Resultados",
    "## Summary": "## Resumen",
    "**GFS Performance Metrics Collected**:": "**Métricas de Rendimiento GFS Recopiladas**:",
    "- Query latency (P50, P95, P99)": "- Latencia de consulta (P50, P95, P99)",
    "- Citation/grounding rate": "- Tasa de citación/fundamentación",
    "- Token usage estimates": "- Estimaciones de uso de tokens",
    "- Cost projections": "- Proyecciones de costos",
    "**Next Steps**:": "**Próximos Pasos**:",
    "- Implement custom RAG baseline in `04_custom_rag_baseline.ipynb`": "- Implementar línea base de RAG personalizado en `04_custom_rag_baseline.ipynb`",
    "- Run same query set on custom RAG": "- Ejecutar el mismo conjunto de consultas en RAG personalizado",
    "- Compare metrics in `05_comparison_analysis.ipynb`": "- Comparar métricas en `05_comparison_analysis.ipynb`",
}

notebooks = [
    "notebooks/03_gfs_experiments.ipynb",
    "notebooks/04_custom_rag_baseline.ipynb",
    "notebooks/05_comparison_analysis.ipynb"
]

for notebook_path in notebooks:
    path = Path(notebook_path)
    if not path.exists():
        print(f"Skipping {notebook_path} - not found")
        continue
    
    print(f"Processing {notebook_path}...")
    
    with open(path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Translate markdown cells
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            translated_source = []
            
            for line in source:
                translated_line = line
                for eng, esp in translations.items():
                    translated_line = translated_line.replace(eng, esp)
                translated_source.append(translated_line)
            
            cell['source'] = translated_source
    
    # Save translated notebook
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✓ Translated {notebook_path}")

print("\nAll notebooks translated!")
