import csv
import os

# Comparative table data synthesized from all 26 student group reports
# Models compared: Gemini, ChatGPT, Claude, Copilot, FACILE/ReadEasy.ai

data = [
    {
        "Categoría": "Análisis (Parte II)",
        "Característica / Criterio de Evaluación": "Precisión en Vocabulario Complejo/Jergas",
        "Gemini": "Bueno en vocabulario dependiente de contexto y detección de jerga técnica (Teams 6, 23). Más estricto que ChatGPT al marcar abreviaturas como PhD (Team 8). Sin embargo, puede perder adverbios terminados en '-ly' (Team 25) y clasifica incorrectamente algunas palabras (Team 28). Análisis más amplio pero menos preciso en los detalles específicos.",
        "ChatGPT": "Bueno en gramática abstracta y vocabulario (Teams 6, 27). Interpretación correcta de la regla de sinónimos (Team 10). Genera falsos positivos ocasionalmente (Team 25) y puede ser 'confidentemente incorrecto' (Team 1). Más preciso en las coincidencias exactas con las reglas E2R (Team 28).",
        "Claude": "Altamente estructurado y cita metodología (Team 2). Muy exhaustivo en la detección, encontrando elementos que otros modelos omiten como punto y coma (Team 10). Sin embargo, interpretó incorrectamente la regla de sinónimos (Team 10) y mantuvo adverbios '-ly' en Tarea 3 (Team 1).",
        "Copilot": "Estructuración automática en tablas con ejemplos concretos (Team 4). Menos preciso en detección gramatical con 3 errores versus 0 de ChatGPT (Team 4). Más simple pero no cumple con estándares E2R estrictos (Team 15).",
        "FACILE / ReadEasy.ai": "FACILE: Fiable y confiable dentro de sus límites, pero proporciona menos información que las herramientas de IA generales (Teams 1, 11). ReadEasy.ai: Excelente como auditor con métricas objetivas y niveles de lectura (Team 21), pero sugirió reemplazar nombres propios esenciales (Team 21). No identifica vocabulario complejo de forma exhaustiva."
    },
    {
        "Categoría": "Análisis (Parte II)",
        "Característica / Criterio de Evaluación": "Comprensión de Contexto (Nombres Propios/Entidades)",
        "Gemini": "Dificultades con nombres propios relacionados entre sí (Team 23). No distingue marcas comerciales de palabras extranjeras (Team 6). Marcó números de teléfono como 'números grandes' (Team 17). Mejor en vocabulario contextual general pero falla en entidades específicas.",
        "ChatGPT": "Mejor comprensión de nombres propios y su contexto (Team 23). Reconoce correctamente que 'PhD' es una palabra autónoma (Team 8). Sin embargo, confundió negación gramatical con sentimiento negativo emocional (Team 23). Más preciso en contexto de entidades que Gemini.",
        "Claude": "Excelente consistencia estructurada y cita metodología (Team 2). Sin evidencia específica de problemas significativos con nombres propios. Riguroso pero puede carecer de juicio contextual fino - demasiado prescriptivo en aplicar reglas (Team 2).",
        "Copilot": "Datos insuficientes para evaluar esta característica de forma concluyente. Solo 2 grupos lo utilizaron (Teams 4, 15).",
        "FACILE / ReadEasy.ai": "ReadEasy.ai carece de contexto y sugirió reemplazar nombres propios esenciales (Team 21). FACILE no tiene capacidad de comprensión contextual profunda - funciona por reglas fijas."
    },
    {
        "Categoría": "Análisis (Parte II)",
        "Característica / Criterio de Evaluación": "Identificación de Negaciones (vs. Sentimiento)",
        "Gemini": "Mejor precisión en la definición de negación gramatical real (Team 23). Identifica consistentemente oraciones negativas y voz pasiva (Teams 20, 27). Más estricto en la clasificación.",
        "ChatGPT": "Confundió negación gramatical con emoción/sentimiento negativo en al menos un caso documentado (Team 23 - 'alucinación de sentimiento'). Detecta gerundios y negativos de forma consistente (Team 20), pero puede generar falsos positivos en esta categoría.",
        "Claude": "Sin problemas reportados específicamente en negación vs sentimiento. Exhaustivo en detección general (Team 10).",
        "Copilot": "Sin datos suficientes en esta categoría específica.",
        "FACILE / ReadEasy.ai": "RevisiónFACILE identificó incorrectamente la voz pasiva (Team 9). Limitaciones en la capacidad de análisis gramatical profundo."
    },
    {
        "Categoría": "Adaptación (Parte III)",
        "Característica / Criterio de Evaluación": "Cumplimiento de Estructura (Una oración por línea)",
        "Gemini": "Estricto en 'una oración por línea' (Team 23), pero puede generar salida fragmentada (Team 23). Falló la regla de nueva línea en algunos casos (Team 4). Tendencia a condensar/resumir demasiado en vez de adaptar (Team 8). Reestructura párrafos proactivamente (Team 17).",
        "ChatGPT": "Estructura más clara con una idea por línea y vocabulario más simple (Team 11). Mejor flujo y transiciones entre oraciones (Team 23). Retuvo oraciones compuestas en algunos casos (Team 23). Sigue bien las reglas estructurales estrictas (Team 4). Más efectivo para reescritura controlada (Team 12).",
        "Claude": "Necesita prompts de seguimiento para producir propuestas completas (Team 1). Riguroso pero rígido/prescriptivo - puede hacer el texto demasiado 'elemental' (Team 2). Sin problemas documentados específicos de estructura por línea.",
        "Copilot": "Produce prosa periodística/explicativa en lugar de formato E2R (Team 15). No cumple con el formato de una oración por línea. Más adecuado para lenguaje claro general que para E2R formal.",
        "FACILE / ReadEasy.ai": "FACILE: Conservador, más cercano al original, simplificación mínima (Team 7). Falló en simplificar estructura (Team 20). Cortó oraciones de forma incoherente (Team 30). ReadEasy.ai: Funciona como auditor, no como creador - no reorganiza estructura automáticamente (Team 17)."
    },
    {
        "Categoría": "Adaptación (Parte III)",
        "Característica / Criterio de Evaluación": "Tono y Nivel de Simplificación",
        "Gemini": "Tendencia a simplificación agresiva (Team 3) - puede eliminar demasiada información causando pérdida de precisión (Team 20). Palabras más simples/seguras (Team 13) pero tono 'académico' o 'demasiado educado' (Teams 21, 14). Pierde contexto por exceso de simplicidad (Team 30). Buen editor pero a veces demasiado radical.",
        "ChatGPT": "Equilibra mejor simplificación y preservación del contenido (Teams 8, 25). Vocabulario más simple y estructura clara (Team 11). Efectivo como soporte de escritura (Teams 5, 6). Prioriza accesibilidad y se asemeja a ejemplos oficiales E2R (Team 15). Mejor en transiciones y no depende de títulos para coherencia (Team 13).",
        "Claude": "Comprende bien los principios pero es demasiado rígido/prescriptivo (Team 2). Puede hacer el texto 'elemental' - falta juicio contextual para matices (Team 2). Sin datos de múltiples grupos para comparación exhaustiva en Tarea 3.",
        "Copilot": "Tono periodístico/explicativo, no E2R (Team 15). Adecuado para lenguaje claro general pero subestima la carga cognitiva del lector objetivo (Team 15). No calibrado para el nivel de simplificación que requiere E2R.",
        "FACILE / ReadEasy.ai": "FACILE: Preserva más el contenido/significado original pero no simplifica lo suficiente (Teams 7, 20). ReadEasy.ai: No genera texto simplificado, solo audita el existente (Teams 17, 21). Ambos son más conservadores que los LLMs generales."
    },
    {
        "Categoría": "Limitaciones Técnicas",
        "Característica / Criterio de Evaluación": "Capacidad de Acceso/Lectura de Enlaces Web",
        "Gemini": "Procesamiento de URLs relativamente eficiente en algunos casos (Team 5), pero generó contenido incorrecto del artículo o saltó la confirmación (Team 5). Incapaz de leer artículos en algunos casos (Team 4). Problemas de acceso por robots.txt (Team 23). Alucinaciones cuando se proporciona solo un enlace (Team 8).",
        "ChatGPT": "Contenido incorrecto del artículo cuando se usa URL (Team 5). Se recomienda copiar/pegar el texto en lugar de proporcionar URLs (Team 5). Alucinaciones cuando se proporciona solo un enlace (Team 8). Limitado al análisis de texto únicamente.",
        "Claude": "Sin datos específicos sobre lectura de URLs. Principalmente utilizado con texto proporcionado directamente o materiales de clase (Team 2). Enfoque RAG con notas de clase resultó efectivo.",
        "Copilot": "Sin datos suficientes. Tiene integración con navegador web en su versión de Microsoft Edge pero no fue evaluado específicamente en esta capacidad.",
        "FACILE / ReadEasy.ai": "ReadEasy.ai tiene plugins para Word y Chrome (Team 17). Problemas de instalación y bugs (Team 3). Límites de cuentas gratuitas (Teams 3, 5). ReadEasy.ai no funcional en algunos casos (Team 4). FACILE tiempos de espera largos (Team 9)."
    },
    {
        "Categoría": "Limitaciones Técnicas",
        "Característica / Criterio de Evaluación": "Tratamiento de Acrónimos y Siglas",
        "Gemini": "Más estricto - marcó 'PhD' como abreviatura que necesita explicación (Team 8). Mantuvo acrónimos y siglas en la adaptación de Tarea 3 (Team 16). No siempre explica las siglas al adaptarlas. Tendencia a mantener paréntesis en algunos casos.",
        "ChatGPT": "Argumentó que 'PhD' es una palabra autónoma reconocida (Team 8). Explicó abreviaturas al adaptarlas cuando se le instruyó (Teams 6, 12). Introdujo abreviaturas no conformes ocasionalmente en Tarea 3 (Team 28). Mejor capacidad de seguir instrucciones específicas sobre acrónimos.",
        "Claude": "Sin problemas específicos reportados con acrónimos. Tiende a ser exhaustivo en la detección (Team 10). Estructurado en el manejo de abreviaturas.",
        "Copilot": "Sin datos suficientes en este criterio específico.",
        "FACILE / ReadEasy.ai": "FACILE: Funcionalidades limitadas, en desarrollo (Teams 9, 11). ReadEasy.ai: Se enfoca en el lenguaje pero no en reglas de presentación/formato de acrónimos (Team 5). No tiene capacidad específica para gestión de siglas."
    },
    {
        "Categoría": "Limitaciones Técnicas",
        "Característica / Criterio de Evaluación": "Detección de Elementos de Diseño (Listas, Layout)",
        "Gemini": "Más consistente con reglas de layout como nueva oración en nueva línea (Team 27). Reestructura párrafos proactivamente (Team 17). Sin capacidad de 'ver' el diseño de una página web - solo analiza texto (Team 14). Ceguera de layout reportada (Team 23). Formateo requiere trabajo adicional manual (Team 4).",
        "ChatGPT": "Excelente en simplificación de vocabulario pero no evalúa diseño visual (Team 27). Ceguera de layout reportada (Team 23). No puede analizar capturas de pantalla ni elementos visuales (Team 14). Detecta listas con comas para convertir a viñetas cuando se instruye (Teams 4, 12).",
        "Claude": "Dificultad con organización de páginas - confusión entre oraciones y párrafos (Team 12). Sin capacidad visual documentada.",
        "Copilot": "Genera tablas automáticamente sin necesidad de prompt específico (Team 4). Sin datos adicionales sobre detección de layout.",
        "FACILE / ReadEasy.ai": "ReadEasy.ai: Tiene integración con Word y niveles de lectura visual (Team 17). Se enfoca en lenguaje pero no en reglas de layout (Team 5). Problemas con alineación y colores (Team 5). FACILE: Retroalimentación visual estructurada con highlights de colores (Team 7). Limitaciones de UI reportadas (Team 20)."
    },
    {
        "Categoría": "Fiabilidad/Alucinaciones",
        "Característica / Criterio de Evaluación": "Presencia de Alucinaciones (Gramática/Adverbios)",
        "Gemini": "Alucina respuestas en lugar de decir 'no sé' (Team 9). Deterioro progresivo con muchos prompts en la misma conversación - comienza a añadir información no solicitada (Team 16). Demasiado 'educado' en sus alucinaciones (Team 21). Necesitó múltiples chats para retomar el análisis correcto (Team 16). Clasificación fija que necesita dobles verificaciones (Team 13).",
        "ChatGPT": "Alucinación de sentimiento - confundió negación con emoción negativa (Team 23). 'Confidentemente incorrecto' en ocasiones (Team 1). Falló en detectar algunos caracteres especiales (Team 7). Análisis a nivel superficial que omite reglas sutiles (Team 21). Contenido incorrecto del artículo cuando se proporcionó solo URL (Team 5).",
        "Claude": "Sin alucinaciones significativas reportadas. Interpretó incorrectamente la regla de sinónimos pero de forma consistente, no aleatoria (Team 10). Alta fiabilidad general pero rígido en sus aplicaciones.",
        "Copilot": "Sin alucinaciones reportadas en los pocos grupos que lo utilizaron. Datos insuficientes para evaluación completa.",
        "FACILE / ReadEasy.ai": "RevisiónFACILE: Detecciones inexactas con highlights amarillos que necesitan verificación manual (Team 7). Identificó incorrectamente voz pasiva (Team 9). Perdió varias infracciones en revisión (Team 30). ReadEasy.ai: Sin alucinaciones pero sugirió cambios innecesarios en nombres propios (Team 21)."
    },
    {
        "Categoría": "Fiabilidad/Alucinaciones",
        "Característica / Criterio de Evaluación": "Detección de Voz Pasiva",
        "Gemini": "Efectivo en la detección de voz pasiva y caracteres especiales (Team 27). Bueno con gerundios y negativos (Teams 20, 27). Mantuvo voz pasiva limitada en Tarea 3 (Team 11). Detección consistente en general.",
        "ChatGPT": "Detección consistente de voz pasiva (Teams 20, 27). Conteos más bajos que Claude pero con menos falsos positivos (Team 10). Buena capacidad de conversión a voz activa durante la adaptación. Dificultad con voz pasiva en escritura académica compleja (Team 6).",
        "Claude": "Exhaustivo en detección - encontró más instancias incluyendo puntuación compleja como punto y coma (Team 10). Sin problemas específicos con voz pasiva. Alto recall pero con posibles falsos positivos por exceso de sensibilidad.",
        "Copilot": "Menos preciso en detección gramatical general (Team 4). Sin datos específicos para voz pasiva.",
        "FACILE / ReadEasy.ai": "RevisiónFACILE: Incorrectamente identificó voz pasiva en al menos un caso (Team 9). FACILE: Perdió varias infracciones gramaticales (Team 30). Capacidad limitada de análisis gramatical profundo."
    },
    {
        "Categoría": "Consistencia",
        "Característica / Criterio de Evaluación": "Subjetividad en el Marcado de Complejidad",
        "Gemini": "Más estricto y rígido en la clasificación (Teams 1, 8, 23). Criterio fijo que a veces necesita doble toma o verificaciones adicionales (Team 13). Marcó números de teléfono como 'números grandes' - aplicación demasiado literal (Team 17). Puede variar entre ejecuciones - necesitó dos corridas para consistencia (Team 25). Mejor comprensión de principios pero aplicación inconsistente (Team 5).",
        "ChatGPT": "Más flexible y abierto en interpretación (Team 13). Evaluó todos los elementos correctamente en algunos casos (Team 4), pero generó falsos positivos en otros (Team 25). Clasificación más objetiva de elementos como números de teléfono (Team 17). Interpretación correcta de reglas contra-intuitivas como sinónimos (Team 10). Mayor variabilidad entre sesiones.",
        "Claude": "Alta consistencia estructurada (Team 2). Exhaustivo pero rígido - aplica reglas de forma sistemática sin flexibilidad contextual (Team 2). Interpretación incorrecta pero consistente de la regla de sinónimos (Team 10). Menor variabilidad entre ejecuciones que Gemini o ChatGPT.",
        "Copilot": "Resultados más simples pero no conformes con E2R formal (Team 15). Consistente en su enfoque pero calibrado para lenguaje claro general, no E2R específico. Pocos datos para evaluación completa.",
        "FACILE / ReadEasy.ai": "FACILE: Fiable y consistente dentro de sus límites funcionales (Team 1), pero esos límites son estrechos (Teams 9, 11). En desarrollo - funcionalidades faltantes. ReadEasy.ai: Métricas objetivas y niveles de lectura proporcionan consistencia medible (Team 21). Sin subjetividad por ser basado en reglas, pero carece de comprensión contextual."
    }
]

# Write to CSV
output_path = "/home/javi/practices/data/llm_comparison/llm_comparative_table.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

fieldnames = ["Categoría", "Característica / Criterio de Evaluación", "Gemini", "ChatGPT", "Claude", "Copilot", "FACILE / ReadEasy.ai"]

with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Generated {len(data)} rows to {output_path}")
print(f"Columns: {fieldnames}")
