import csv

# Task 2 Data
task2_data = [
    {
        "Grupo": "Team 16 (Bystron)",
        "LLM": "Gemini Pro, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: ChatGPT buen punto de partida, Gemini exitoso con requisitos fragmentados. Desventajas: Gemini se degrada con muchos prompts.",
        "Prompt/Estrategia": "Requisitos por bloques (chunked). Prompt específico para cada categoría.",
        "Recomendaciones": "Dividir requisitos en bloques, reiniciar el chat periódicamente.",
        "Atributos": "Bueno: Identificación de problemas si se segmenta. Malo: Degradación de respuestas largas.",
        "Dificultades": "Claridad en instrucciones de la tarea."
    },
    {
        "Grupo": "Team 1 (Sanchez Gimeno)",
        "LLM": "Gemini, Claude, ChatGPT, FACILE",
        "Ventajas/Desventajas": "Ventajas: Claude estructurado (tablas), FACILE confiable. Desventajas: ChatGPT alucina violaciones incorrectas.",
        "Prompt/Estrategia": "Lista por categorías (Ortografía, Gramática, etc.).",
        "Recomendaciones": "Usar formatos estructurados como tablas.",
        "Atributos": "Bueno: Claude (facilidad de parsing), Gemini (estricto). Malo: ChatGPT (precisión).",
        "Dificultades": "Necesidad de verificación manual por errores de GPT."
    },
    {
        "Grupo": "Team 2 (Sankar)",
        "LLM": "Claude, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: Claude cita metodología y es riguroso. ChatGPT conversacional con explicaciones detalladas.",
        "Prompt/Estrategia": "RAG (proporcionar notas de clase) para Claude, ninguno para ChatGPT.",
        "Recomendaciones": "Claude para envío académico, ChatGPT para detalles de aprendizaje.",
        "Atributos": "Bueno: Claude (consistencia), ChatGPT (ejemplos prácticos).",
        "Dificultades": "Ninguna reportada."
    },
    {
        "Grupo": "Team 3 (Rajaonah)",
        "LLM": "Gemini, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: Gemini más preciso. Desventajas: ChatGPT alucina palabras.",
        "Prompt/Estrategia": "Evaluación punto por punto de requisitos E2R.",
        "Recomendaciones": "Preferir Gemini sobre ChatGPT para análisis.",
        "Atributos": "Bueno: Gemini (confiabilidad). Malo: ChatGPT (alucinaciones).",
        "Dificultades": "Dificultad de los LLM con criterios 'simples'."
    },
    {
        "Grupo": "Team 4 (Aller/Van Steijn)",
        "LLM": "Copilot, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: Copilot tablas automáticas y ejemplos concretos. Desventajas: Gemini no pudo leer el artículo.",
        "Prompt/Estrategia": "Basada en elementos específicos del checklist.",
        "Recomendaciones": "Preferir Copilot por su estructura tabular nativa.",
        "Atributos": "Bueno: ChatGPT (precisión), Copilot (formato). Malo: Copilot (errores gramaticales).",
        "Dificultades": "Diferentes enfoques requeridos para cada chatbot."
    },
    {
        "Grupo": "Team 5 (Osadici)",
        "LLM": "Gemini, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: Gemini eficiente con URLs. ChatGPT análisis exhaustivo.",
        "Prompt/Estrategia": "Punto por punto: presencia, conteo, ejemplos.",
        "Recomendaciones": "Pegar texto directamente en vez de usar URLs.",
        "Atributos": "Bueno: Gemini (comprensión de principios). Malo: ChatGPT (contenido incorrecto).",
        "Dificultades": "Problemas de acceso a URLs y respuestas inconsistentes."
    },
    {
        "Grupo": "Team 6 (Corrado)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: ChatGPT bueno en gramática abstracta. Gemini bueno en vocabulario contextual.",
        "Prompt/Estrategia": "Citar texto, explicar problema y categorizar.",
        "Recomendaciones": "Crear listas blancas para nombres propios y marcas.",
        "Atributos": "Bueno: ChatGPT (gramática), Gemini (vocabulario). Malo: Ambos marcan falsos positivos (apóstrofes).",
        "Dificultades": "Falsos positivos en elementos estándar del inglés."
    },
    {
        "Grupo": "Team 7 (Soleimani/Guillermet)",
        "LLM": "ChatGPT, RevisiónFACILE",
        "Ventajas/Desventajas": "Ventajas: ChatGPT explicaciones detalladas. RevisiónFACILE feedback visual.",
        "Prompt/Estrategia": "Prompt general refinado con criterios completos.",
        "Recomendaciones": "Combinar herramientas automáticas con análisis humano.",
        "Atributos": "Bueno: ChatGPT (fenómenos lingüísticos), RevisiónFACILE (formato). Malo: ChatGPT (caracteres especiales).",
        "Dificultades": "Evaluar la precisión de las herramientas."
    },
    {
        "Grupo": "Team 8 (Bollen)",
        "LLM": "Gemini, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: Gemini estricto con abreviaturas. ChatGPT flexible con palabras independientes.",
        "Prompt/Estrategia": "Subida de rúbrica excel + instrucciones de rol.",
        "Recomendaciones": "Clarificar si el objetivo es evaluar el LLM o la web.",
        "Atributos": "Bueno: Gemini (rigor), ChatGPT (consistencia).",
        "Dificultades": "Alucinaciones al usar solo links."
    },
    {
        "Grupo": "Team 9 (Lopez Llorente)",
        "LLM": "Gemini, RevisiónFacile",
        "Ventajas/Desventajas": "Ventajas: Gemini mejor lenguaje natural. RevisiónFacile fácil uso.",
        "Prompt/Estrategia": "Análisis web + comentarios de errores.",
        "Recomendaciones": "Clarificar número de revisiones por herramienta.",
        "Atributos": "Bueno: Gemini (lenguaje natural). Malo: RevisiónFacile (identificación incompleta).",
        "Dificultades": "Latencia en Facile."
    },
    {
        "Grupo": "Team 10 (Kusta)",
        "LLM": "Claude AI, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: Claude exhaustivo, detecta punto y coma. ChatGPT regla de sinónimos correcta.",
        "Prompt/Estrategia": "Prompt estandarizado con conteo de elementos.",
        "Recomendaciones": "Explicar explícitamente la regla de sinónimos.",
        "Atributos": "Bueno: Claude (detección), ChatGPT (interpretación de reglas).",
        "Dificultades": "Subjetividad del 'vocabulario difícil'."
    },
    {
        "Grupo": "Team 11 (Momcilovic/Varela)",
        "LLM": "ChatGPT, Gemini, RevisiónFACILE",
        "Ventajas/Desventajas": "Ventajas: ChatGPT cercano a manual. RevisiónFACILE reportes en PDF.",
        "Prompt/Estrategia": "Lista de puntos específicos para análisis.",
        "Recomendaciones": "Clarificar frecuencia de revisión.",
        "Atributos": "Bueno: Gemini (reglas), ChatGPT (español). Malo: RevisiónFACILE (incompleto).",
        "Dificultades": "Falta de información detallada en herramientas específicas."
    },
    {
        "Grupo": "Team 13 (Catalano)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: ChatGPT abierto e informativo. Gemini justificaciones correctas.",
        "Prompt/Estrategia": "Instrucciones detalladas con escala de valores (1-4).",
        "Recomendaciones": "Clarificar objetivo del ejercicio.",
        "Atributos": "Bueno: ChatGPT (flexibilidad), Gemini (justificación).",
        "Dificultades": "Hacer que el LLM entienda el ejercicio ('lucha')."
    },
    {
        "Grupo": "Team 17 (Maoro/Cirillo)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: ChatGPT objetivo (números). Gemini ofrece sugerencias de corrección.",
        "Prompt/Estrategia": "Chat en blanco, estructura específica, verificación.",
        "Recomendaciones": "Herramientas que analicen capturas de pantalla.",
        "Atributos": "Bueno: Gemini (correcciones), ChatGPT (categorización).",
        "Dificultades": "Copy-paste manual constante."
    },
    {
        "Grupo": "Team 19 (Ollero/Alonso Geesink)",
        "LLM": "Gemini 3 Pro, ChatGPT 5.0",
        "Ventajas/Desventajas": "Ventajas: Gemini análisis párrafo a párrafo efectivo. Ambos buenos con guía.",
        "Prompt/Estrategia": "Contexto (slides) + preguntas paso a paso.",
        "Recomendaciones": "Incluir ejemplos y restricciones en los prompts.",
        "Atributos": "Bueno: Ambos (confiabilidad con guía).",
        "Dificultades": "Ninguna reportada."
    },
    {
        "Grupo": "Team 21 (Zhang/Xinyi Tao)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: ChatGPT rápido para lo obvio. Gemini análisis profundo de flujo/lógica.",
        "Prompt/Estrategia": "Prompts específicos para 4 áreas clave.",
        "Recomendaciones": "Ninguna.",
        "Atributos": "Bueno: ChatGPT (obvios), Gemini (fluidez). Malo: Ambos (sinónimos).",
        "Dificultades": "Complejidad oculta en textos gramaticalmente correctos."
    }
]

# Task 3 Data
task3_data = [
    {
        "Grupo": "Team 16 (Bystron)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: ChatGPT apoyo útil. Desventajas: Gemini poco confiable (mantiene adverbios).",
        "Prompt/Estrategia": "Instrucciones -> Revisión -> Refinamiento manual.",
        "Recomendaciones": "Revisión humana siempre necesaria.",
        "Atributos": "Bueno: ChatGPT (adaptación). Malo: Gemini (abreviaturas/adverbios).",
        "Dificultades": "Formato Excel inadecuado para textos largos."
    },
    {
        "Grupo": "Team 1 (Sanchez Gimeno)",
        "LLM": "Gemini, Claude, ChatGPT, FACILE",
        "Ventajas/Desventajas": "Ventajas: ChatGPT adaptación drástica. Desventajas: FACILE modificaciones mínimas.",
        "Prompt/Estrategia": "Propuesta de nuevo documento E2R.",
        "Recomendaciones": "Claude requiere prompts adicionales para el texto completo.",
        "Atributos": "Bueno: ChatGPT (estructura). Malo: FACILE (límites de sentencia).",
        "Dificultades": "FACILE con límites de frases."
    },
    {
        "Grupo": "Team 3 (Rajaonah)",
        "LLM": "Gemini, ChatGPT, Read Easy.ai",
        "Ventajas/Desventajas": "Ventajas: Gemini explica cambios, Read Easy.ai es minucioso. ChatGPT arreglos mecánicos.",
        "Prompt/Estrategia": "Transformar según plantilla + reporte de cambios.",
        "Recomendaciones": "ChatGPT es el más fiel al estilo checklist.",
        "Atributos": "Bueno: Read Easy.ai (exhaustivo), Gemini (simplificación agresiva).",
        "Dificultades": "Instalación de Read Easy.ai."
    },
    {
        "Grupo": "Team 4 (Aller)",
        "LLM": "Gemini, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: ChatGPT sigue reglas estructurales. Gemini simplifica información pesada.",
        "Prompt/Estrategia": "Reglas IFLA 2010.",
        "Recomendaciones": "Intervención humana necesaria para negritas/formato visual.",
        "Atributos": "Bueno: ChatGPT (layout), Gemini (editor/simplificador).",
        "Dificultades": "ReadEasy.ai no funcionaba."
    },
    {
        "Grupo": "Team 5 (Osadici)",
        "LLM": "EasyRead.ai, ChatGPT",
        "Ventajas/Desventajas": "Ventajas: EasyRead integración con Word. ChatGPT ayuda a la redacción.",
        "Prompt/Estrategia": "Formateo específico (negritas, listas).",
        "Recomendaciones": "Permitir entrega en formato documento/web.",
        "Atributos": "Bueno: ChatGPT (eficiencia). Malo: EasyRead (prioriza lengua sobre layout).",
        "Dificultades": "Límites de cuenta en herramientas de pago."
    },
    {
        "Grupo": "Team 6 (Corrado)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: Ayuda a la escritura. Desventajas: ChatGPT deletrea números, Gemini demasiado preciso.",
        "Prompt/Estrategia": "800 palabras, voz activa, explicar abreviaturas.",
        "Recomendaciones": "Instrucciones específicas de redondeo numérico.",
        "Atributos": "Bueno: Redacción inicial. Malo: Manejo de números.",
        "Dificultades": "Voz pasiva en textos académicos complejos."
    },
    {
        "Grupo": "Team 7 (Soleimani/Guillermet)",
        "LLM": "ChatGPT, FACILE",
        "Ventajas/Desventajas": "Ventajas: ChatGPT adaptación profunda. FACILE conserva significado original.",
        "Prompt/Estrategia": "Escribir en E2R y explicar modificaciones.",
        "Recomendaciones": "Ninguna específica.",
        "Atributos": "Bueno: ChatGPT (simplificación), FACILE (precisión).",
        "Dificultades": "Adaptar textos largos manteniendo el sentido."
    },
    {
        "Grupo": "Team 12 (Cifrian)",
        "LLM": "ChatGPT",
        "Ventajas/Desventajas": "Ventajas: Muy efectivo para reescritura controlada mediante tablas.",
        "Prompt/Estrategia": "Reglas estrictas IFLA 2010. Tabla de 3 columnas.",
        "Recomendaciones": "Equilibrar simplificación y precisión.",
        "Atributos": "Bueno: ChatGPT (reescritura controlada).",
        "Dificultades": "Alta densidad de información."
    },
    {
        "Grupo": "Team 28 (Weerapperuma)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: ChatGPT adaptaciones sustanciales. Gemini segmentación sin omisiones.",
        "Prompt/Estrategia": "Conversión frase a frase en tabla.",
        "Recomendaciones": "Proporcionar ejemplos de informes profesionales.",
        "Atributos": "Bueno: ChatGPT (preservación), Gemini (segmentación).",
        "Dificultades": "Abreviaturas frecuentes en el origen."
    },
    {
        "Grupo": "Team 31 (Gismera)",
        "LLM": "ChatGPT, Gemini",
        "Ventajas/Desventajas": "Ventajas: ChatGPT buena aplicación. Gemini resultados equilibrados (brevedad).",
        "Prompt/Estrategia": "Adaptar sin resumir ni reescribir creativamente.",
        "Recomendaciones": "Ejemplos de mejores prácticas en Excel.",
        "Atributos": "Bueno: Gemini (claridad/brevedad).",
        "Dificultades": "Extensión y repetitividad del trabajo manual."
    }
]

def write_csv(filename, data):
    if not data: return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

write_csv('/home/javi/practices/data/task_2_analysis.csv', task2_data)
write_csv('/home/javi/practices/data/task_3_analysis.csv', task3_data)
print("CSVs generated successfully.")
