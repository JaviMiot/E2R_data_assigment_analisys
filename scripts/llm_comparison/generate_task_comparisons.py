import csv
import os

# ============================================================
# TASK 2: DETECCIÓN DE PATRONES E2R - Comparación de LLMs
# ============================================================

task2_data = [
    {
        "Categoría": "Ortografía",
        "Criterio": "Detección de caracteres especiales (\\, &, <, §, #)",
        "Gemini": "Bueno. Identifica correctamente la mayoría de caracteres especiales (Teams 20, 27). Más estricto que ChatGPT en marcar estos elementos. Sin embargo, falló con caracteres especiales y números grandes en conjunto (Team 20).",
        "ChatGPT": "Bueno. Detecta caracteres especiales de forma consistente (Teams 20, 27). Falló en detectar algunos caracteres especiales puntuales (Team 7). Requiere texto copiado, no URLs.",
        "Claude": "Muy bueno. Exhaustivo en la detección, encontrando elementos que otros modelos omiten, incluyendo punto y coma (Team 10). Alta precisión sin falsos positivos significativos.",
        "Copilot": "Adecuado. Estructuración automática en tablas pero menos preciso en detección gramatical general, con 3 errores vs 0 de ChatGPT (Team 4).",
        "FACILE / RevisiónFACILE": "Limitado. Proporciona retroalimentación visual con highlights de colores (Team 7), pero detecciones inexactas que necesitan verificación (Team 7). Menos información que herramientas IA generales (Team 11).",
        "ReadEasy.ai": "Limitado. Se enfoca más en lenguaje que en elementos de ortografía específicos (Team 5). Funciona como auditor con métricas objetivas (Team 21) pero no desglosa caracteres individuales."
    },
    {
        "Categoría": "Ortografía",
        "Criterio": "Detección de paréntesis, corchetes y abreviaturas",
        "Gemini": "Estricto. Marcó 'PhD' como abreviatura que necesita explicación (Team 8). Detecta paréntesis consistentemente. Tendencia a mantener paréntesis en algunos resultados propios de Tarea 3 (Team 16).",
        "ChatGPT": "Flexible. Argumentó que 'PhD' es una palabra autónoma reconocida, no una abreviatura (Team 8). Detecta abreviaturas cuando se instruye específicamente. 'Confidentemente incorrecto' ocasionalmente (Team 1).",
        "Claude": "Exhaustivo. Detecta abreviaturas de forma sistemática y estructurada (Team 10). Tiende a ser más completo que ChatGPT en conteos (Team 10).",
        "Copilot": "Sin datos específicos suficientes para este criterio.",
        "FACILE / RevisiónFACILE": "Funcionalidades limitadas, herramienta en desarrollo (Teams 9, 11). No tiene capacidad específica para gestión de abreviaturas de forma detallada.",
        "ReadEasy.ai": "No tiene capacidad específica para gestión de siglas o abreviaturas (Team 5). Se enfoca en nivel de lectura general."
    },
    {
        "Categoría": "Ortografía",
        "Criterio": "Manejo de porcentajes y números grandes",
        "Gemini": "Problemático. Marcó números de teléfono como 'números grandes' - aplicación demasiado literal de la regla (Team 17). Falló en detectar cifras grandes y porcentajes consistentemente junto con caracteres especiales (Team 20).",
        "ChatGPT": "Mejor contexto. Clasificación más objetiva de elementos numéricos como números de teléfono (Team 17). Sin embargo, también falló en detectar números grandes en combinación con otros elementos (Team 20). Conteos más bajos que Claude (Team 10).",
        "Claude": "Exhaustivo. Mayor conteo de instancias detectadas que ChatGPT (Team 10). Recomienda definir umbrales claros para 'números grandes' (Team 10).",
        "Copilot": "Sin datos específicos para este criterio.",
        "FACILE / RevisiónFACILE": "Sin capacidad específica documentada para detección de números grandes.",
        "ReadEasy.ai": "Proporciona métricas objetivas de nivel de lectura pero no desglosa números grandes específicamente (Team 21)."
    },
    {
        "Categoría": "Gramática",
        "Criterio": "Detección de voz pasiva",
        "Gemini": "Bueno. Efectivo en la detección de voz pasiva (Teams 20, 27). Consistente en la identificación general. Detección fiable cuando se le pregunta específicamente.",
        "ChatGPT": "Bueno. Detección consistente (Teams 20, 27). Conteos más bajos que Claude pero con menos falsos positivos (Team 10). Dificultad con voz pasiva en escritura académica compleja (Team 6).",
        "Claude": "Muy bueno. Exhaustivo - encontró más instancias, incluyendo puntuación compleja asociada (Team 10). Alto recall pero posibles falsos positivos por exceso de sensibilidad.",
        "Copilot": "Menos preciso en detección gramatical general (Team 4). Sin datos específicos para voz pasiva detallada.",
        "FACILE / RevisiónFACILE": "Problemático. Identificó incorrectamente voz pasiva en al menos un caso documentado (Team 9). Perdió varias infracciones gramaticales (Team 30).",
        "ReadEasy.ai": "Sin capacidad específica documentada para detección de voz pasiva."
    },
    {
        "Categoría": "Gramática",
        "Criterio": "Detección de oraciones negativas (vs. sentimiento)",
        "Gemini": "Bueno. Mejor precisión en distinguir negación gramatical real del sentimiento (Team 23). Identifica consistentemente oraciones negativas (Teams 20, 27). Más estricto en clasificación.",
        "ChatGPT": "Problemático. Confundió negación gramatical con emoción/sentimiento negativo ('alucinación de sentimiento', Team 23). Detecta negativos de forma consistente en otros casos (Team 20), pero genera falsos positivos.",
        "Claude": "Sin problemas reportados específicamente en negación vs sentimiento. Exhaustivo en detección general (Team 10).",
        "Copilot": "Sin datos suficientes en esta categoría.",
        "FACILE / RevisiónFACILE": "Capacidad limitada de análisis gramatical profundo. Sin datos específicos.",
        "ReadEasy.ai": "Sin capacidad para este tipo de análisis gramatical."
    },
    {
        "Categoría": "Gramática",
        "Criterio": "Detección de gerundios",
        "Gemini": "Bueno. Detecta gerundios y formas en '-ing' de forma consistente (Teams 20, 27). Buen rendimiento en análisis gramatical general.",
        "ChatGPT": "Bueno. Detecta gerundios de forma consistente (Team 20). Luchó con gramática en algunos casos específicos, generando alucinaciones (Team 3).",
        "Claude": "Bueno. Detección exhaustiva de todas las formas gramaticales (Team 10). Sin problemas específicos reportados con gerundios.",
        "Copilot": "Less preciso en gramática general (Team 4). Sin datos específicos para gerundios.",
        "FACILE / RevisiónFACILE": "Capacidad limitada. Perdió varias infracciones gramaticales en revisión (Team 30).",
        "ReadEasy.ai": "Sin capacidad documentada para detección de gerundios."
    },
    {
        "Categoría": "Vocabulario",
        "Criterio": "Identificación de jerga/vocabulario complejo",
        "Gemini": "Bueno. Mejor en vocabulario dependiente de contexto y jerga técnica (Teams 6, 23). Más estricto al marcar elementos. Sin embargo, puede perder adverbios '-ly' (Team 25) y clasifica incorrectamente algunas palabras (Team 28). Análisis amplio pero menos preciso en detalles.",
        "ChatGPT": "Bueno. Preciso en gramática abstracta y vocabulario (Teams 6, 27). Interpretación correcta de regla de sinónimos (Team 10). Genera falsos positivos ocasionalmente (Team 25). Más preciso en coincidencias exactas con reglas E2R (Team 28).",
        "Claude": "Muy bueno. Altamente estructurado, cita metodología (Team 2). Muy exhaustivo encontrando elementos que otros omiten (Team 10). Interpretó incorrectamente regla de sinónimos (Team 10) pero consistentemente.",
        "Copilot": "Adecuado. Ejemplos concretos pero menos preciso en detección (Team 4). No cumple estándares E2R estrictos (Team 15).",
        "FACILE / RevisiónFACILE": "Limitado. Fiable dentro de sus límites pero proporciona menos información que IA general (Teams 1, 11). En desarrollo.",
        "ReadEasy.ai": "Excelente como auditor con métricas objetivas (Team 21), pero no identifica vocabulario complejo de forma exhaustiva."
    },
    {
        "Categoría": "Vocabulario",
        "Criterio": "Manejo de nombres propios y entidades",
        "Gemini": "Problemático. Dificultades con nombres propios relacionados (Team 23). No distingue marcas comerciales de palabras extranjeras (Team 6). Marcó números de teléfono como 'números grandes' (Team 17).",
        "ChatGPT": "Bueno. Mejor comprensión de nombres propios y contexto (Team 23). Reconoce 'PhD' como palabra autónoma (Team 8). Sin embargo, confundió negación con sentimiento en contexto de entidades (Team 23).",
        "Claude": "Adecuado. Sin evidencia específica de problemas con nombres propios. Riguroso pero puede carecer de juicio contextual fino (Team 2).",
        "Copilot": "Datos insuficientes. Solo 2 grupos lo utilizaron (Teams 4, 15).",
        "FACILE / RevisiónFACILE": "No tiene capacidad de comprensión contextual profunda - funciona por reglas fijas.",
        "ReadEasy.ai": "Problemático. Carece de contexto y sugirió reemplazar nombres propios esenciales (Team 21)."
    },
    {
        "Categoría": "Vocabulario",
        "Criterio": "Detección de adverbios en '-ly'/'-mente' y superlativos",
        "Gemini": "Irregular. Perdió adverbios '-ly' en algunos casos (Team 25). Mejor análisis de directrices E2R en general (Team 11) pero inconsistente en este aspecto específico.",
        "ChatGPT": "Bueno. Detección adecuada cuando se incluye en el prompt. Falsos positivos reportados (Team 25) pero generalmente más preciso que Gemini en este criterio.",
        "Claude": "Bueno en detección pero mantuvo adverbios '-ly' en sus propias adaptaciones de Tarea 3 (Team 1). Detección exhaustiva como auditor.",
        "Copilot": "Sin datos específicos para este criterio.",
        "FACILE / RevisiónFACILE": "Sin capacidad específica documentada.",
        "ReadEasy.ai": "Sin capacidad específica documentada."
    },
    {
        "Categoría": "Composición",
        "Criterio": "Detección de listas con comas (vs. viñetas)",
        "Gemini": "Bueno. Más consistente con reglas de layout como nueva oración en nueva línea (Team 27). Ceguera de layout reportada - solo analiza texto, no diseño visual (Teams 14, 23).",
        "ChatGPT": "Bueno. Detecta listas con comas para viñetas cuando se instruye (Teams 4, 12). Ceguera de layout (Team 23). No evalúa diseño visual (Teams 14, 27).",
        "Claude": "Adecuado. Dificultad con organización de páginas - confusión entre oraciones y párrafos (Team 12). Sin capacidad visual documentada.",
        "Copilot": "Genera tablas automáticamente sin prompt específico (Team 4). Sin datos adicionales sobre composición.",
        "FACILE / RevisiónFACILE": "Retroalimentación visual con highlights de colores (Team 7). Limitaciones de UI (Team 20).",
        "ReadEasy.ai": "Plugins para Word y Chrome con integración visual (Team 17). Se enfoca en lenguaje pero no en reglas de layout (Team 5). Problemas de alineación/colores (Team 5)."
    },
    {
        "Categoría": "Fiabilidad",
        "Criterio": "Nivel de alucinaciones / falsos positivos",
        "Gemini": "Problemático. Alucina respuestas en lugar de decir 'no sé' (Team 9). Deterioro progresivo con muchos prompts (Team 16). Necesitó múltiples chats para retomar análisis correcto (Team 16). Clasificación fija que necesita dobles verificaciones (Team 13).",
        "ChatGPT": "Moderado. 'Alucinación de sentimiento' documentada (Team 23). 'Confidentemente incorrecto' (Team 1). Falló en detectar caracteres especiales (Team 7). Nivel superficial que omite reglas sutiles (Team 21). Contenido incorrecto cuando se usa solo URL (Team 5).",
        "Claude": "Bajo. Sin alucinaciones significativas reportadas. Interpretación incorrecta pero consistente de regla de sinónimos (Team 10). Alta fiabilidad general aunque rígido.",
        "Copilot": "Sin alucinaciones reportadas. Datos insuficientes (solo 2 grupos).",
        "FACILE / RevisiónFACILE": "Moderado. Detecciones inexactas con highlights amarillos (Team 7). Identificó incorrectamente voz pasiva (Team 9). Perdió infracciones (Team 30).",
        "ReadEasy.ai": "Bajo. Sin alucinaciones pero sugirió cambios innecesarios en nombres propios (Team 21)."
    },
    {
        "Categoría": "Fiabilidad",
        "Criterio": "Consistencia entre ejecuciones",
        "Gemini": "Baja-Media. Necesitó dos corridas para consistencia (Team 25). Deterioro progresivo en la misma conversación (Team 16). Mejor comprensión de principios pero aplicación inconsistente (Team 5). Criterio más estricto y rígido (Teams 1, 8, 23).",
        "ChatGPT": "Media. Mayor variabilidad entre sesiones. Evaluó correctamente en algunos casos (Team 4), falsos positivos en otros (Team 25). Más flexible en interpretación (Team 13).",
        "Claude": "Alta. Consistencia estructurada (Team 2). Aplica reglas de forma sistemática sin flexibilidad contextual (Team 2). Menor variabilidad entre ejecuciones que Gemini o ChatGPT.",
        "Copilot": "Consistente pero calibrado para lenguaje claro general, no E2R específico (Team 15). Pocos datos.",
        "FACILE / RevisiónFACILE": "Media. Fiable dentro de sus límites funcionales (Team 1) pero esos límites son estrechos (Teams 9, 11).",
        "ReadEasy.ai": "Alta. Métricas objetivas basadas en reglas proporcionan consistencia medible (Team 21). Sin subjetividad."
    },
    {
        "Categoría": "Usabilidad",
        "Criterio": "Formato de salida (tabla, lista, texto libre)",
        "Gemini": "Variable. Puede requerir prompt específico para tablas. Proporciona sugerencias de corrección además de la detección (Team 17). Necesitó más pasos y combinación de categorías (Team 8).",
        "ChatGPT": "Bueno. Diseño limpio pero necesita prompt para generar tablas (Team 4). Explicaciones detalladas y conversacionales (Team 2). Más info y open-ended (Team 13).",
        "Claude": "Muy bueno. Salida altamente estructurada y fácil de parsear (Team 1). Tablas y outputs organizados por categorías. Cita metodología (Team 2).",
        "Copilot": "Bueno. Genera tablas automáticamente con ejemplos concretos sin necesidad de prompt específico (Team 4).",
        "FACILE / RevisiónFACILE": "Bueno. Retroalimentación visual estructurada con highlights de colores (amarillo/verde/rojo) (Team 7). Indica incertidumbre en sus detecciones.",
        "ReadEasy.ai": "Bueno. Plugins integrados con Word/Chrome. Niveles de lectura visuales (Team 17). Métricas objetivas claras (Team 21)."
    },
    {
        "Categoría": "Usabilidad",
        "Criterio": "Necesidad de prompts de seguimiento",
        "Gemini": "Alta. Requiere chunking de requisitos E2R y reset de chat tras deterioro (Team 16). Mejor con prompts progresivos que con todo a la vez (Team 16). Necesitó nueva conversación tras múltiples prompts.",
        "ChatGPT": "Media. Funciona bien con un prompt comprehensivo (Teams 10, 21). Puede requerir refinamiento para estructura específica. Necesita prompt explícito para formato tabla.",
        "Claude": "Baja-Media. Funciona bien con prompt único y contexto RAG (notas de clase, Team 2). Necesita seguimiento para propuestas completas en Tarea 3 (Team 1).",
        "Copilot": "Baja. Genera resultados estructurados desde el primer prompt (Team 4). Sin datos de interacción extendida.",
        "FACILE / RevisiónFACILE": "Baja. No requiere prompts - herramienta automática. Pero tiempos de espera largos (Team 9) y funcionalidades limitadas.",
        "ReadEasy.ai": "Baja. No requiere prompts - herramienta automática con plugins. Pero problemas de instalación (Team 3) y límites de cuentas gratuitas (Teams 3, 5)."
    }
]

# ============================================================
# TASK 3: ADAPTACIÓN DE TEXTOS A E2R - Comparación de LLMs
# ============================================================

task3_data = [
    {
        "Categoría": "Estructura",
        "Criterio": "Cumplimiento de 'una oración por línea'",
        "Gemini": "Estricto pero inconsistente. Cumple estrictamente en algunos casos (Team 23) pero genera salida fragmentada. Falló la regla de nueva línea en otros casos (Team 4). Reestructura párrafos proactivamente (Team 17) pero a veces condensa en vez de adaptar (Team 8).",
        "ChatGPT": "Bueno. Estructura más clara con una idea por línea (Team 11). Mejor flujo y transiciones (Team 23). Retuvo oraciones compuestas en algunos casos (Team 23). Más efectivo para reescritura controlada con formato de 3 columnas (Team 12). Sigue bien reglas estrictas (Team 4).",
        "Claude": "Riguroso pero rígido. Puede hacer el texto demasiado 'elemental' (Team 2). Necesita prompts de seguimiento para propuestas completas (Team 1). Sin problemas documentados específicos de estructura por línea.",
        "Copilot": "No cumple. Produce prosa periodística/explicativa en lugar de formato E2R (Team 15). No aplica la regla de una oración por línea. Más adecuado para lenguaje claro general.",
        "FACILE / RevisiónFACILE": "Problemático. Conservador, simplificación mínima (Team 7). Falló en simplificar estructura (Team 20). Cortó oraciones de forma incoherente (Team 30).",
        "ReadEasy.ai": "No aplica. Funciona como auditor, no como creador - no reorganiza estructura automáticamente (Team 17). Evalúa pero no adapta."
    },
    {
        "Categoría": "Estructura",
        "Criterio": "Uso de viñetas en lugar de listas con comas",
        "Gemini": "Bueno. Genera viñetas y estructura con bullets (Team 20). Estructura clara y legible. Reestructura listas de forma proactiva.",
        "ChatGPT": "Muy bueno. Convierte listas con comas a viñetas efectivamente cuando se instruye (Teams 4, 5, 12, 25). Más viñetas y mejor estructura general (Team 25).",
        "Claude": "Sin datos específicos suficientes en Tarea 3 para este criterio.",
        "Copilot": "Sin datos suficientes.",
        "FACILE / RevisiónFACILE": "No genera viñetas. Herramienta de auditoría, no de creación.",
        "ReadEasy.ai": "No genera viñetas. Solo audita el texto existente."
    },
    {
        "Categoría": "Estructura",
        "Criterio": "Organización del texto (encabezados, secciones)",
        "Gemini": "Bueno. Editor proactivo que reestructura párrafos (Team 17). Simplificación agresiva puede eliminar secciones completas (Team 3). Condensó/resumió demasiado en algunos casos (Team 8).",
        "ChatGPT": "Muy bueno. No depende de títulos para coherencia (Team 13). Mejor en transiciones entre secciones. Propuso encabezados cuando se le pidió (Team 16). Preserva más detalle que Gemini (Team 8).",
        "Claude": "Riguroso. Estructura jerárquica basada en principios pero rígida (Team 2). Comprende organización pero la aplica de forma prescriptiva.",
        "Copilot": "No organiza para E2R. Produce prosa continua (Team 15).",
        "FACILE / RevisiónFACILE": "No reorganiza. Sugerencias de corte de oraciones incoherentes (Team 30).",
        "ReadEasy.ai": "No reorganiza. Evalúa nivel de lectura de secciones existentes."
    },
    {
        "Categoría": "Gramática",
        "Criterio": "Conversión a voz activa",
        "Gemini": "Adecuado. Voz pasiva limitada en resultados (Team 11). Dificultad con voz pasiva en escritura académica compleja. Menos efectivo que ChatGPT en este aspecto.",
        "ChatGPT": "Bueno. Buena capacidad de conversión a voz activa. Dificultad con voz pasiva en escritura académica compleja (Team 6). Estructura más clara en resultado final.",
        "Claude": "Muy bueno. Riguroso en aplicar voz activa pero puede resultar en texto demasiado 'elemental' (Team 2). Aplica la regla de forma sistemática.",
        "Copilot": "Sin datos suficientes para Tarea 3.",
        "FACILE / RevisiónFACILE": "No aplica conversión. Solo identifica (con errores, Team 9).",
        "ReadEasy.ai": "No aplica conversión. Solo audita."
    },
    {
        "Categoría": "Gramática",
        "Criterio": "Eliminación de gerundios y negaciones",
        "Gemini": "Adecuado. Mantuvo algunos adverbios como 'very' en adaptación (Team 16). Limitado en eliminación completa de formas no E2R.",
        "ChatGPT": "Bueno. Simplificación efectiva de estructuras gramaticales complejas (Teams 7, 11). Vocabulario más simple y estructura limpia. Eliminación más consistente.",
        "Claude": "Riguroso. Aplica reglas sistemáticamente. Puede sobre-simplificar resultando en texto 'elemental' (Team 2).",
        "Copilot": "Sin datos suficientes.",
        "FACILE / RevisiónFACILE": "No aplica eliminación de gerundios. Simplificación mínima (Team 7).",
        "ReadEasy.ai": "No aplica eliminación. Solo audita."
    },
    {
        "Categoría": "Vocabulario",
        "Criterio": "Simplificación de vocabulario complejo",
        "Gemini": "Bueno. Palabras más simples/seguras (Team 13). Vocabulario más simple en lenguaje general (Team 14). Sin embargo, mantuvo palabras grandes ocasionalmente (Team 16). Buen editor general pero a veces demasiado radical en la simplificación.",
        "ChatGPT": "Muy bueno. Excelente simplificación de vocabulario (Team 27). Vocabulario más simple y estructura clara (Team 11). Explica palabras difíciles en negrita cuando se instruye (Teams 4, 5). Prioriza accesibilidad (Team 15).",
        "Claude": "Bueno. Comprende principios de simplificación. Riguroso pero puede hacer texto demasiado simple/'elemental' (Team 2). Falta juicio para matices contextuales.",
        "Copilot": "Inadecuado para E2R. Lenguaje claro general pero no simplifica al nivel necesario (Team 15). Subestima carga cognitiva.",
        "FACILE / RevisiónFACILE": "Preserva más el contenido original pero no simplifica suficiente (Teams 7, 20). Más conservador que LLMs generales.",
        "ReadEasy.ai": "No simplifica activamente. Audita nivel de lectura del texto existente (Teams 17, 21)."
    },
    {
        "Categoría": "Vocabulario",
        "Criterio": "Tratamiento de acrónimos y siglas",
        "Gemini": "Problemático. Mantuvo acrónimos, siglas y paréntesis en la adaptación (Team 16). No siempre expande las siglas. Necesita instrucción explícita.",
        "ChatGPT": "Bueno. Explicó abreviaturas cuando se instruyó (Teams 6, 12). Introdujo abreviaturas no conformes ocasionalmente (Team 28). Mejor en seguir instrucciones específicas sobre acrónimos.",
        "Claude": "Sin problemas específicos reportados. Tiende a ser estructurado en el manejo de abreviaturas.",
        "Copilot": "Sin datos suficientes.",
        "FACILE / RevisiónFACILE": "Sin capacidad específica para gestión de siglas en adaptación.",
        "ReadEasy.ai": "Sin capacidad específica para gestión de siglas."
    },
    {
        "Categoría": "Vocabulario",
        "Criterio": "Manejo de números grandes y porcentajes",
        "Gemini": "Problemático. Mantuvo números grandes en forma numérica (Team 11). Mantuvo porcentajes exactos (Team 13). Perdió contexto numérico por exceso de simplicidad (Team 30). No convierte a expresiones simples automáticamente.",
        "ChatGPT": "Problemático. Deletreó números en vez de simplificar (Team 6). Mejor en transiciones con números (Team 13). Inicialmente mantuvo demasiados números (Team 7). Requiere instrucción específica para redondeo.",
        "Claude": "Sin datos suficientes en Tarea 3 para este criterio específico.",
        "Copilot": "Sin datos suficientes.",
        "FACILE / RevisiónFACILE": "Sin capacidad de adaptación numérica.",
        "ReadEasy.ai": "Sin capacidad de adaptación numérica."
    },
    {
        "Categoría": "Fidelidad",
        "Criterio": "Preservación del contenido original",
        "Gemini": "Problemático. Tendencia a simplificación agresiva eliminando información (Teams 3, 20). Omitió partes del texto (Team 3). Perdió precisión (Team 20). Pérdida de contexto por exceso de simplicidad (Team 30).",
        "ChatGPT": "Bueno. Equilibra mejor simplificación y preservación (Teams 8, 25). Preserva más información relevante que Gemini (Team 8). Omitió texto original o introdujo abreviaturas no conformes ocasionalmente (Team 28).",
        "Claude": "Riguroso. Comprende principios de preservación pero es demasiado prescriptivo (Team 2). Puede hacer el texto 'elemental' perdiendo matices.",
        "Copilot": "Inadecuado para E2R. Prosa explicativa que reformula excesivamente (Team 15).",
        "FACILE / RevisiónFACILE": "Bueno en preservación. Preserva más contenido/significado original (Teams 7, 20). Más completo que Gemini pero no simplifica suficiente.",
        "ReadEasy.ai": "N/A. No genera adaptaciones, solo audita."
    },
    {
        "Categoría": "Fidelidad",
        "Criterio": "Nivel de resumen vs. adaptación",
        "Gemini": "Tiende a resumir. Condensó/resumió demasiado en vez de adaptar (Team 8). Eliminó secciones completas (Team 3). Omitió componentes informativos en oraciones largas (Team 28). Necesita instrucción explícita de 'no resumir'.",
        "ChatGPT": "Adapta fielmente. Procesó texto completo de una vez (Team 19). Adaptación más fiel que resumen. Más consistente en cambios mecánicos (Team 3). Mejor para reescritura controlada con formato de tabla (Team 12).",
        "Claude": "Adapta pero con exceso. Riguroso en seguir todas las reglas pero puede sobre-simplificar. Requiere seguimiento para propuestas completas (Team 1).",
        "Copilot": "Reformula. No adapta, produce prosa periodística diferente al formato E2R (Team 15).",
        "FACILE / RevisiónFACILE": "Sugerencias pobres. Cortó oraciones de forma incoherente (Team 30). Simplificación mínima sin verdadera adaptación (Team 7).",
        "ReadEasy.ai": "N/A. No genera adaptaciones."
    },
    {
        "Categoría": "Fidelidad",
        "Criterio": "Presencia de alucinaciones / información inventada",
        "Gemini": "Moderado. Alucinaciones y tono 'demasiado educado' (Team 21). Añade info no solicitada tras deterioro conversacional (Team 16). Sugirió imágenes irrelevantes (Team 14).",
        "ChatGPT": "Bajo-Moderado. Contenido incorrecto cuando se proporcionó solo URL (Team 5). En general, fiel al contenido original en la adaptación. Introdujo abreviaturas no conformes (Team 28).",
        "Claude": "Bajo. Sin alucinaciones reportadas en adaptación. Alta fiabilidad pero rígido.",
        "Copilot": "Sin datos suficientes.",
        "FACILE / RevisiónFACILE": "Bajo. No genera contenido nuevo, por lo tanto no alucina. Pero sus sugerencias son pobres (Team 30).",
        "ReadEasy.ai": "Bajo. Sin alucinaciones - métricas basadas en reglas. Pero sugirió cambios innecesarios en nombres propios (Team 21)."
    },
    {
        "Categoría": "Tono",
        "Criterio": "Nivel de simplificación alcanzado",
        "Gemini": "Variable. Tono 'académico' o 'demasiado educado' (Teams 14, 21). Simplificación agresiva que puede ser excesiva (Team 3) o insuficiente por tono académico. Palabras seguras/simples (Team 13) pero inconsistente.",
        "ChatGPT": "Adecuado. Se asemeja a ejemplos oficiales E2R (Team 15). Vocabulario más simple y estructura clara (Team 11). Nivel de simplificación generalmente apropiado para el público objetivo. Efectivo como soporte de escritura (Teams 5, 6).",
        "Claude": "Rígido. Puede hacer texto demasiado 'elemental' - falta juicio contextual (Team 2). Nivel de simplificación excesivo en algunos casos.",
        "Copilot": "Insuficiente. Tono periodístico/explicativo, no E2R (Team 15). No alcanza el nivel de simplificación necesario. Subestima carga cognitiva (Team 15).",
        "FACILE / RevisiónFACILE": "Insuficiente. Simplificación mínima/conservadora (Team 7). No alcanza el nivel de simplificación E2R necesario.",
        "ReadEasy.ai": "N/A. No genera texto simplificado, solo audita nivel de lectura existente."
    },
    {
        "Categoría": "Tono",
        "Criterio": "Naturalidad del texto resultante",
        "Gemini": "Variable. Salida fragmentada en algunos casos (Team 23). Tono 'demasiado educado' que suena artificial (Team 21). Reestructuración proactiva puede sonar mecánica. Mejor como editor pero resultado a veces poco natural.",
        "ChatGPT": "Bueno. Mejor flujo y transiciones entre oraciones (Team 23). Texto más natural y coherente. No depende de títulos para coherencia (Team 13). Más parecido a ejemplos oficiales E2R (Team 15). Efectivo pero necesita revisión humana.",
        "Claude": "Mecánico. Texto resultante suena 'elemental' y prescriptivo (Team 2). Aplicación rígida de reglas produce resultado funcional pero poco natural.",
        "Copilot": "Natural pero inadecuado. Prosa fluida y legible pero no sigue formato E2R (Team 15). Suena como artículo periodístico.",
        "FACILE / RevisiónFACILE": "N/A. Las sugerencias de corte de oraciones son incoherentes (Team 30), no produce texto continuo adaptado.",
        "ReadEasy.ai": "N/A. No genera texto."
    },
    {
        "Categoría": "Usabilidad",
        "Criterio": "Formato de salida (tabla 3 columnas, texto continuo)",
        "Gemini": "Variable. Control por párrafo permite verificación cuidadosa (Team 19). Sin formato de tabla automático. Requiere instrucción para formato específico.",
        "ChatGPT": "Muy bueno. Efectivo con formato de 3 columnas (Original | Propuesta | Comentarios, Teams 12, 25). Procesó texto completo de una vez (Team 19). Mejor para reescritura controlada con restricciones de salida (Team 12).",
        "Claude": "Bueno. Salida estructurada basada en formato solicitado. Sugirió '[IMAGE: Picture of...]' para complementos visuales (Team 2).",
        "Copilot": "Texto continuo tipo artículo, sin formato E2R (Team 15).",
        "FACILE / RevisiónFACILE": "No genera formato de tabla. Herramienta de auditoría visual (highlights).",
        "ReadEasy.ai": "Plugins integrados con Word/Chrome. No genera tabla comparativa pero proporciona métricas visuales de nivel de lectura (Team 17)."
    },
    {
        "Categoría": "Usabilidad",
        "Criterio": "Capacidad de seguir instrucciones iterativas",
        "Gemini": "Problemático. Deterioro progresivo con muchos prompts (Team 16). Necesitó nueva conversación tras múltiples iteraciones. Mejor en modo párrafo-por-párrafo que texto completo (Team 19). Responde a correcciones pero con calidad decreciente.",
        "ChatGPT": "Bueno. Respondió a clarificaciones y refinamientos (Team 16: encabezados; Team 7: números). Pidió aclaraciones antes de proceder (Team 16). Procesó texto completo y aceptó correcciones. Iteración efectiva.",
        "Claude": "Adecuado. Necesita prompts de seguimiento para propuestas completas (Team 1). Responde a contexto RAG (notas de clase). Sin deterioro reportado en iteraciones.",
        "Copilot": "Sin datos de interacción iterativa.",
        "FACILE / RevisiónFACILE": "N/A. No interactiva. Tiempos de espera largos (Team 9).",
        "ReadEasy.ai": "N/A. No interactiva. Problemas de instalación (Team 3), límites de cuentas (Teams 3, 5)."
    }
]

# Write Task 2 CSV
output_dir = "/home/javi/practices/data/llm_comparison"
os.makedirs(output_dir, exist_ok=True)

fieldnames_t2 = ["Categoría", "Criterio", "Gemini", "ChatGPT", "Claude", "Copilot", "FACILE / RevisiónFACILE", "ReadEasy.ai"]

with open(f"{output_dir}/task2_llm_comparison.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_t2)
    writer.writeheader()
    writer.writerows(task2_data)

print(f"Task 2: Generated {len(task2_data)} rows")

# Write Task 3 CSV
fieldnames_t3 = ["Categoría", "Criterio", "Gemini", "ChatGPT", "Claude", "Copilot", "FACILE / RevisiónFACILE", "ReadEasy.ai"]

with open(f"{output_dir}/task3_llm_comparison.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_t3)
    writer.writeheader()
    writer.writerows(task3_data)

print(f"Task 3: Generated {len(task3_data)} rows")
print("Done!")
