import json
from pathlib import Path

# Comprehensive translations for notebook 03
nb03_translations = {
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
    "- Implement custom RAG baseline in": "- Implementar línea base de RAG personalizado en",
    "- Run same query set on custom RAG": "- Ejecutar el mismo conjunto de consultas en RAG personalizado",
    "- Compare metrics in": "- Comparar métricas en",
}

# Comprehensive translations for notebook 04
nb04_translations = {
    "# Custom RAG Baseline Implementation": "# Implementación de Línea Base RAG Personalizada",
    "This notebook implements a custom RAG system for comparison with GFS.": "Este cuaderno implementa un sistema RAG personalizado para comparación con GFS.",
    "**Objectives**:": "**Objetivos**:",
    "1. Set up vector database (ChromaDB)": "1. Configurar base de datos vectorial (ChromaDB)",
    "2. Index documents with embeddings": "2. Indexar documentos con embeddings",
    "3. Implement retrieval + generation pipeline": "3. Implementar pipeline de recuperación + generación",
    "4. Run same test queries as GFS experiments": "4. Ejecutar las mismas consultas de prueba que los experimentos GFS",
    "5. Measure performance metrics": "5. Medir métricas de rendimiento",
    "## 1. Initialize Custom RAG": "## 1. Inicializar RAG Personalizado",
    "## 2. Create Collection and Index Documents": "## 2. Crear Colección e Indexar Documentos",
    "## 3. Run Test Queries": "## 3. Ejecutar Consultas de Prueba",
    "## 4. Analyze Performance": "## 4. Analizar Rendimiento",
    "## 5. Save Results": "## 5. Guardar Resultados",
    "## Summary": "## Resumen",
    "**Custom RAG Metrics Collected**:": "**Métricas de RAG Personalizado Recopiladas**:",
    "- Query latency": "- Latencia de consulta",
    "- Retrieval quality": "- Calidad de recuperación",
    "- Token usage": "- Uso de tokens",
    "- Implementation complexity": "- Complejidad de implementación",
    "**Next Steps**:": "**Próximos Pasos**:",
    "- Compare with GFS results in": "- Comparar con resultados GFS en",
    "- Analyze trade-offs": "- Analizar compromisos",
    "- Make recommendations": "- Hacer recomendaciones",
}

# Comprehensive translations for notebook 05
nb05_translations = {
    "# RAG Comparison Analysis": "# Análisis Comparativo de RAG",
    "This notebook compares GFS and custom RAG implementations.": "Este cuaderno compara las implementaciones de GFS y RAG personalizado.",
    "**Objectives**:": "**Objetivos**:",
    "1. Load results from both experiments": "1. Cargar resultados de ambos experimentos",
    "2. Compare latency metrics": "2. Comparar métricas de latencia",
    "3. Compare cost estimates": "3. Comparar estimaciones de costos",
    "4. Evaluate quality differences": "4. Evaluar diferencias de calidad",
    "5. Assess implementation complexity": "5. Evaluar complejidad de implementación",
    "6. Provide recommendations": "6. Proporcionar recomendaciones",
    "## 1. Load Experimental Results": "## 1. Cargar Resultados Experimentales",
    "## 2. Latency Comparison": "## 2. Comparación de Latencia",
    "## 3. Cost Comparison": "## 3. Comparación de Costos",
    "## 4. Quality Assessment": "## 4. Evaluación de Calidad",
    "## 5. Complexity Analysis": "## 5. Análisis de Complejidad",
    "## 6. Recommendations": "## 6. Recomendaciones",
    "## Summary": "## Resumen",
    "**Key Findings**:": "**Hallazgos Clave**:",
    "**Recommendations**:": "**Recomendaciones**:",
}

def translate_notebook(notebook_path, translations):
    """Translate markdown cells in a notebook"""
    path = Path(notebook_path)
    if not path.exists():
        print(f"❌ {notebook_path} not found")
        return False
    
    print(f"📝 Processing {notebook_path}...")
    
    with open(path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Translate markdown cells
    translated_count = 0
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            translated_source = []
            
            for line in source:
                translated_line = line
                # Apply all translations
                for eng, esp in translations.items():
                    translated_line = translated_line.replace(eng, esp)
                translated_source.append(translated_line)
            
            cell['source'] = translated_source
            translated_count += 1
    
    # Save translated notebook
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Translated {translated_count} markdown cells in {notebook_path}")
    return True

# Translate all notebooks
print("=" * 60)
print("Translating notebooks to Formal Chilean Spanish")
print("=" * 60)

translate_notebook("notebooks/03_gfs_experiments.ipynb", nb03_translations)
translate_notebook("notebooks/04_custom_rag_baseline.ipynb", nb04_translations)
translate_notebook("notebooks/05_comparison_analysis.ipynb", nb05_translations)

print("\n✨ All notebooks translated successfully!")
