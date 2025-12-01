# @title Actividad RAG con Google Gemini File Search
# Descripción: Implementación de un asistente corporativo usando la herramienta nativa de búsqueda de archivos.

import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

def main():
    print("--- LIBRERÍAS INSTALADAS ---")

    # PASO 2: CONFIGURACIÓN Y API KEY
    # ------------------------------------------------------------------
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
    # ------------------------------------------------------------------

    client = genai.Client(api_key=GOOGLE_API_KEY)

    # PASO 3: CREAR DOCUMENTO SIMULADO (CONOCIMIENTO CORPORATIVO)
    # Creamos un archivo local que servirá como nuestra base de conocimiento privada.
    politica_texto = """
POLÍTICA DE TRABAJO HÍBRIDO - EMPRESA INNOVACIÓN 2025

1. DÍAS PRESENCIALES: Todos los empleados deben asistir a la oficina los días Martes y Jueves.
El horario núcleo de coincidencia es de 10:00 AM a 3:00 PM.

2. EQUIPAMIENTO: La empresa proveerá un bono único de $500 USD para equipamiento de oficina en casa
(silla, monitor, escritorio) para empleados con contrato indefinido.

3. REUNIONES VIRTUALES: Es obligatorio mantener la cámara encendida en reuniones con clientes externos.
Para reuniones internas, la cámara es opcional salvo que el organizador indique lo contrario.

4. CIBERSEGURIDAD: No está permitido trabajar desde redes Wi-Fi públicas (cafeterías, aeropuertos)
sin el uso de la VPN corporativa activada.
"""

    # Guardamos esto en un archivo real
    with open("politica_hibrida.txt", "w") as f:
        f.write(politica_texto)

    print("--- DOCUMENTO 'politica_hibrida.txt' CREADO LOCALMENTE ---")

    # PASO 4: SUBIDA E INDEXACIÓN (FILE SEARCH TOOL)
    # Aquí ocurre la magia del "Managed RAG". Subimos el archivo y Google lo indexa.

    # A. Crear un File Search Store
    print("Creando File Search Store...")
    store = client.file_search_stores.create(
        config={"display_name": "Politicas Corporativas"}
    )
    print(f"Store creado: {store.name}")

    # B. Subir el archivo al Store
    print("Subiendo archivo al Store...")
    client.file_search_stores.upload_to_file_search_store(
        file_search_store_name=store.name,
        file="politica_hibrida.txt"
    )
    print("Archivo enviado al store para indexación.")
    print("Esperando 10 segundos para que complete la indexación...")
    time.sleep(10)

    # PASO 5: CONFIGURACIÓN DEL MODELO CON LA HERRAMIENTA
    # Creamos la configuración para activar la herramienta de búsqueda de archivos
    tool_config = [
        types.Tool(
            file_search=types.FileSearch(
                file_search_store_names=[store.name]
            )
        )
    ]

    # Instanciamos el modelo (usamos Gemini 2.5 Flash como en la doc)
    model_id = "gemini-2.5-flash"

    # PASO 6: FUNCIÓN DE CONSULTA
    def preguntar_al_experto(pregunta):
        print(f"\nUsuario pregunta: {pregunta}")
        
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=pregunta,
                config=types.GenerateContentConfig(
                    tools=tool_config, # Aquí activamos el RAG
                    temperature=0.0    # Temperatura 0 para máxima precisión factual
                )
            )
            
            # Mostramos la respuesta
            print(f"Respuesta Gemini:\n{response.text}")

            # Verificamos si usó citas (Grounding)
            if hasattr(response.candidates[0], 'grounding_metadata') and response.candidates[0].grounding_metadata:
                print("[Fuente citada del documento]")
        except Exception as e:
            print(f"Error al generar respuesta: {e}")

    # PASO 7: PRUEBAS EN VIVO
    # Caso 1: Pregunta cuya respuesta está explícita
    preguntar_al_experto("¿Qué días debo ir obligado a la oficina?")

    # Caso 2: Pregunta sobre dinero (Bono)
    preguntar_al_experto("¿Cuánto dinero me dan para comprar una silla?")

    # Caso 3: Pregunta de seguridad (VPN)
    preguntar_al_experto("¿Puedo trabajar desde un Starbucks?")

    # Caso 4: Pregunta fuera de contexto (Alucinación check)
    preguntar_al_experto("¿Cuál es la política de mascotas en la oficina?")

    # Cleanup (Optional but good practice)
    # print("Limpiando recursos...")
    # client.file_search_stores.delete(name=store.name)

if __name__ == "__main__":
    main()