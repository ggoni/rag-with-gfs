import json
from pathlib import Path

# TODAS las traducciones faltantes para notebook 04
nb04_complete_translations = {
    # Cell 0
    "This notebook implements a traditional RAG system for comparison with GFS.": "Este cuaderno implementa un sistema RAG tradicional para comparación con GFS.",
    "**Components**:": "**Componentes**:",
    "- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)": "- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)",
    "- **Vector DB**: ChromaDB": "- **Base de Datos Vectorial**: ChromaDB",
    "- **LLM**: Gemini (same as GFS)": "- **LLM**: Gemini (igual que GFS)",
    "1. Index documents with custom chunking": "1. Indexar documentos con fragmentación personalizada",
    "2. Run same test queries as GFS experiments": "2. Ejecutar las mismas consultas de prueba que los experimentos GFS",
    "3. Measure performance metrics": "3. Medir métricas de rendimiento",
    "4. Compare with GFS results": "4. Comparar con resultados GFS",
    
    # Cell 16
    "**Custom RAG Baseline Completed**:": "**Línea Base RAG Personalizada Completada**:",
    "- Indexed documents with ChromaDB": "- Documentos indexados con ChromaDB",
    "- Ran same test queries as GFS": "- Ejecutadas las mismas consultas de prueba que GFS",
    "- Measured latency (retrieval + generation)": "- Medida la latencia (recuperación + generación)",
    "- Saved results for comparison": "- Resultados guardados para comparación",
    "- Compare GFS vs Custom RAG in": "- Comparar GFS vs RAG Personalizado en",
    "- Analizar compromisos (latency, cost, quality)": "- Analizar compromisos (latencia, costo, calidad)",
}

def translate_notebook_04():
    """Translate ALL remaining English text in notebook 04"""
    notebook_path = "notebooks/04_custom_rag_baseline.ipynb"
    path = Path(notebook_path)
    
    if not path.exists():
        print(f"❌ {notebook_path} not found")
        return False
    
    print(f"\n📝 Traduciendo {notebook_path}...")
    print("=" * 70)
    
    with open(path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Translate markdown cells
    changes_made = 0
    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            translated_source = []
            
            for line in source:
                original_line = line
                translated_line = line
                
                # Apply all translations
                for eng, esp in nb04_complete_translations.items():
                    if eng in translated_line:
                        translated_line = translated_line.replace(eng, esp)
                        if original_line != translated_line:
                            print(f"  ✓ Cell {i}: '{eng[:60]}...'")
                            print(f"           → '{esp[:60]}...'")
                            changes_made += 1
                
                translated_source.append(translated_line)
            
            cell['source'] = translated_source
    
    # Save translated notebook
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print("=" * 70)
    print(f"✅ {changes_made} traducciones aplicadas en {notebook_path}")
    return True

# Execute translation
print("\n" + "=" * 70)
print("TRADUCIENDO NOTEBOOK 04 - TODAS LAS FRASES RESTANTES")
print("=" * 70)

translate_notebook_04()

print("\n" + "=" * 70)
print("✨ NOTEBOOK 04 COMPLETAMENTE TRADUCIDO")
print("=" * 70)
