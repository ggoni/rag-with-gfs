import json
from pathlib import Path

# Traducciones completas para TODOS los textos en inglés
translations = {
    # Notebook 03
    "This notebook conducts systematic experiments with Google Generative File Search.": "Este cuaderno realiza experimentos sistemáticos con Google Generative File Search.",
    "Create a diverse query set covering different patterns:": "Crear un conjunto diverso de consultas que cubra diferentes patrones:",
    "- Factual lookups": "- Búsquedas factuales",
    "- Analytical questions": "- Preguntas analíticas",
    "- Multi-document reasoning": "- Razonamiento multi-documento",
    "- Edge cases (out-of-domain)": "- Casos extremos (fuera de dominio)",
    
    # Notebook 04
    "# Custom RAG Baseline Implementation": "# Implementación de Línea Base RAG Personalizada",
    "This notebook implements a custom RAG system for comparison with GFS.": "Este cuaderno implementa un sistema RAG personalizado para comparación con GFS.",
    "1. Set up vector database (ChromaDB)": "1. Configurar base de datos vectorial (ChromaDB)",
    "2. Index documents with embeddings": "2. Indexar documentos con embeddings",
    "3. Implement retrieval + generation pipeline": "3. Implementar pipeline de recuperación + generación",
    "4. Run same test queries as GFS experiments": "4. Ejecutar las mismas consultas de prueba que los experimentos GFS",
    "5. Measure performance metrics": "5. Medir métricas de rendimiento",
    "## 1. Initialize Custom RAG": "## 1. Inicializar RAG Personalizado",
    "## 2. Create Collection and Index Documents": "## 2. Crear Colección e Indexar Documentos",
    "## 3. Run Test Queries": "## 3. Ejecutar Consultas de Prueba",
    "**Custom RAG Metrics Collected**:": "**Métricas de RAG Personalizado Recopiladas**:",
    "- Query latency": "- Latencia de consulta",
    "- Retrieval quality": "- Calidad de recuperación",
    "- Token usage": "- Uso de tokens",
    "- Implementation complexity": "- Complejidad de implementación",
    "- Compare with GFS results in": "- Comparar con resultados GFS en",
    "- Analyze trade-offs": "- Analizar compromisos",
    "- Make recommendations": "- Hacer recomendaciones",
    
    # Notebook 05
    "# RAG Comparison Analysis": "# Análisis Comparativo de RAG: GFS vs Custom RAG",
    "This notebook provides a comprehensive comparison between Google Generative File Search and a custom RAG implementation.": "Este cuaderno proporciona una comparación exhaustiva entre Google Generative File Search y una implementación RAG personalizada.",
    "**Comparison Dimensions**:": "**Dimensiones de Comparación**:",
    "1. **Latency**: End-to-end response time": "1. **Latencia**: Tiempo de respuesta de extremo a extremo",
    "2. **Cost**: API usage and pricing": "2. **Costo**: Uso de API y precios",
    "3. **Quality**: Answer relevance and grounding": "3. **Calidad**: Relevancia de respuestas y fundamentación",
    "4. **Complexity**: Implementation and maintenance effort": "4. **Complejidad**: Esfuerzo de implementación y mantenimiento",
    "5. **Scalability**: Performance with dataset size": "5. **Escalabilidad**: Rendimiento con tamaño de conjunto de datos",
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
    "**Key Findings**:": "**Hallazgos Clave**:",
    "**Recommendations**:": "**Recomendaciones**:",
    
    # Common terms
    "**Objectives**:": "**Objetivos**:",
    "**Next Steps**:": "**Próximos Pasos**:",
    "## Summary": "## Resumen",
    "## 4. Analyze Performance": "## 4. Analizar Rendimiento",
    "## 5. Save Results": "## 5. Guardar Resultados",
}

def translate_notebook(notebook_path):
    """Translate ALL markdown content in a notebook"""
    path = Path(notebook_path)
    if not path.exists():
        print(f"❌ {notebook_path} not found")
        return False
    
    print(f"\n📝 Processing {notebook_path}...")
    
    with open(path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Translate markdown cells
    translated_count = 0
    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            translated_source = []
            
            for line in source:
                translated_line = line
                # Apply all translations
                for eng, esp in translations.items():
                    if eng in translated_line:
                        translated_line = translated_line.replace(eng, esp)
                        print(f"  ✓ Cell {i}: '{eng[:50]}...' → '{esp[:50]}...'")
                translated_source.append(translated_line)
            
            cell['source'] = translated_source
            translated_count += 1
    
    # Save translated notebook
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Translated {translated_count} markdown cells in {notebook_path}")
    return True

# Translate all notebooks
print("=" * 70)
print("TRADUCIENDO TODOS LOS CUADERNOS A ESPAÑOL FORMAL CHILENO")
print("=" * 70)

notebooks = [
    "notebooks/03_gfs_experiments.ipynb",
    "notebooks/04_custom_rag_baseline.ipynb",
    "notebooks/05_comparison_analysis.ipynb"
]

for nb in notebooks:
    translate_notebook(nb)

print("\n" + "=" * 70)
print("✨ TODOS LOS CUADERNOS HAN SIDO TRADUCIDOS EXITOSAMENTE")
print("=" * 70)
