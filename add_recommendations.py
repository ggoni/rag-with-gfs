import json
from pathlib import Path

# Contenido de recomendaciones en español formal chileno
recommendations_markdown = """## Cuándo Usar GFS:

1. **Prototipado Rápido**: Necesidad de validar rápidamente el concepto RAG
2. **Casos de Uso Simples**: Preguntas y respuestas estándar sobre documentos sin lógica personalizada
3. **Recursos Limitados**: Sin infraestructura ML o equipo especializado
4. **Escala Pequeña-Mediana**: < 20 GB de documentos
5. **Requisitos de Citación**: Fundamentación integrada necesaria

## Cuándo Usar RAG Personalizado:

1. **Fragmentación Personalizada**: Lógica de división de texto específica del dominio
2. **Búsqueda Híbrida**: Combinación de búsqueda semántica + por palabras clave
3. **Filtrado Avanzado**: Consultas complejas de metadatos
4. **Optimización de Costos**: Alto volumen de consultas (sin costo de indexación)
5. **Control Total**: Necesidad de ajustar cada componente

## Enfoque Híbrido:

- **Prototipar con GFS**, migrar a RAG personalizado si es necesario
- Usar GFS para subconjuntos de documentos, RAG personalizado para datos estructurados
- Realizar pruebas A/B de ambos sistemas en producción
"""

def add_recommendations_cell():
    """Add rendered recommendations markdown cell to notebook 05"""
    notebook_path = "notebooks/05_comparison_analysis.ipynb"
    path = Path(notebook_path)
    
    if not path.exists():
        print(f"❌ {notebook_path} not found")
        return False
    
    print(f"\n📝 Agregando celda de recomendaciones a {notebook_path}...")
    
    with open(path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Find the cell with recommendations code (Cell 15)
    cells = notebook.get('cells', [])
    recommendations_code_index = None
    
    for i, cell in enumerate(cells):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            if 'Generate recommendations based on results' in source:
                recommendations_code_index = i
                print(f"  ✓ Encontrada celda de código de recomendaciones en índice {i}")
                break
    
    if recommendations_code_index is None:
        print("  ❌ No se encontró la celda de código de recomendaciones")
        return False
    
    # Check if markdown cell already exists after code cell
    next_index = recommendations_code_index + 1
    if next_index < len(cells) and cells[next_index].get('cell_type') == 'markdown':
        # Update existing markdown cell
        cells[next_index]['source'] = recommendations_markdown.split('\n')
        print(f"  ✓ Actualizada celda markdown existente en índice {next_index}")
    else:
        # Insert new markdown cell
        new_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": recommendations_markdown.split('\n')
        }
        cells.insert(next_index, new_cell)
        print(f"  ✓ Insertada nueva celda markdown en índice {next_index}")
    
    # Save updated notebook
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"✅ Celda de recomendaciones agregada exitosamente")
    return True

# Execute
print("=" * 70)
print("AGREGANDO RECOMENDACIONES RENDERIZADAS AL NOTEBOOK 05")
print("=" * 70)

add_recommendations_cell()

print("\n" + "=" * 70)
print("✨ RECOMENDACIONES AHORA VISIBLES EN EL NOTEBOOK")
print("=" * 70)
