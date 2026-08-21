# Pruebas del Agente Analista KPI TGM

## Objetivo

Documentar las tres pruebas funcionales realizadas sobre el agente "agente_kpi_tgm_final.py", desarrollado con Microsoft Foundry, "gpt-5-mini" y Code Interpreter.

Las pruebas buscan validar:

1. cálculos KPI normales
2. tratamiento de días sin juego
3. detección de errores de calidad de datos sin inventar ni imputar información.

# Prueba 1 — Cálculos normales y conversiones

## Objetivo

Verificar que el agente:

- detecte correctamente la tabla de datos
- procese todos los registros
- calcule los acumulados
- convierta correctamente los valores monetarios a USD
- calcule RTP acumulado
- calcule la apuesta promedio del último día
- ejecute los cálculos con Python mediante Code Interpreter.

## Archivo usado
BDTGM.xlsx

## Parámetros de entrada
- Tipo de cambio: 3.40 S/ por USD
- RTP teórico: 94.15%

## Pregunta enviada al agente
Calcula la cantidad de filas, el Coin In acumulado en USD, el Coin Out acumulado en USD, el JP acumulado en USD, el RTP acumulado final y la apuesta promedio del último día.

## Resultado esperado

- Filas procesadas: 414
- Coin In acumulado: US$ 558,571.69
- Coin Out acumulado: US$ 512,594.01
- JP acumulado: US$ 26,287.59
- RTP acumulado final: 96.47%
- Apuesta promedio último día: S/ 2.39

## Resultado obtenido

El agente devolvió:

- Filas procesadas: 414
- Coin In acumulado: US$ 558,571.69
- Coin Out acumulado: US$ 512,594.01
- JP acumulado: US$ 26,287.59
- RTP acumulado final: 96.47%
- Apuesta promedio último día: S/ 2.39

También indicó que:

- no había fechas inválidas
- no había valores negativos
- existían dos días sin juego
- todos los cálculos numéricos fueron realizados con Python.

## Conclusión

**PRUEBA 1 APROBADA.**

Los resultados coincidieron con los valores previamente validados localmente.

Esto fue lo que arrojo el TERMINAL

PS C:\Users\Usuario\Documents\DSRP\TRABAJO FINAL\PYTHON> & C:\Users\Usuario\AppData\Local\Programs\Python\Python310\python.exe "c:/Users/Usuario/Documents/DSRP/TRABAJO FINAL/PYTHON/agente_kpi_tgm_final.py"
=== AGENTE ANALISTA KPI TGM - FOUNDY + CODE INTERPRETER ===
Ruta del archivo Excel: "C:\Users\Usuario\Documents\DSRP\TRABAJO FINAL\PYTHON\BDTGM.xlsx"
Tipo de cambio (S/ por USD): 3.4
RTP teórico (%) [déjalo vacío si no aplica]: 94.15

Ejemplos de preguntas:
- ¿Cuál fue la máquina con mayor NetWin?
- Calcula el RTP acumulado final.
- Genera el gráfico de RTP acumulado.
- Genera el gráfico de Coin In diario.
- Valida la calidad de los datos y dame observaciones.

Escribe tu pregunta: Calcula la cantidad de filas, el Coin In acumulado en USD, el Coin Out acumulado en USD, el JP acumulado en USD, el RTP acumulado final y la apuesta promedio del último día.

Archivo cargado correctamente: assistant-1TR1br1TsQr9NzUGrDqyUU
Agente creado: agente-kpi-tgm-final - versión 1

=== RESPUESTA DEL AGENTE ===
Análisis realizado. Resumen de la validación (anomalías detectadas) — leído y procesado el archivo usando Python:

- Detección de encabezado: fila localizada correctamente con los encabezados requeridos (LOCAL, MARCA, MOD_COMER, MAQUINA, fecha_op, COIN IN, COIN OUT, JP, GAMES PLAYED). Se ignoraron filas superiores de metadatos y se usaron únicamente los registros debajo del encabezado.
- Orden: los registros se ordenaron cronológicamente por fecha_op antes de los cálculos.
- Fechas inválidas o vacías: 0 (ninguna).
- Valores negativos en contadores (COIN IN, COIN OUT, JP, GAMES PLAYED): 0 (ninguno).
- Valores vacíos en columnas obligatorias (COIN IN, COIN OUT, JP, GAMES PLAYED): 0 (ninguno).
- Días sin juego (COIN IN = 0, COIN OUT = 0, GAMES PLAYED = 0): 2 registros. Fechas de días sin juego identificadas: 08/08/2025 y 23/11/2025.
  - Estos días se trataron como días sin juego según las reglas; los acumulados no se reinician en esos días y el RTP acumulado conserva su valor anterior en esos puntos.
- No se detectaron casos de GAMES PLAYED en blanco que requirieran normalización (todos los registros tienen GAMES PLAYED).

Validación: correcta (salvo las 2 filas identificadas como días sin juego, que se reportan como anomalía detectada y se interpretaron conforme a las reglas).

Cálculos solicitados (todos calculados en Python; tipo de cambio usado = 3.4 soles/USD; RTP teórico provisto = 94.15%):

- Cantidad de filas procesadas: 414
- COIN IN acumulado (USD) = 558,571.69 USD
  - (Se calculó sumando COIN IN en soles y luego dividiendo el acumulado entre 3.4; resultado final mostrado con 2 decimales.)
- COIN OUT acumulado (USD) = 512,594.01 USD
  - (Suma acumulada en soles ÷ 3.4; mostrado con 2 decimales.)
- JP acumulado (USD) = 26,287.59 USD
  - (Suma acumulada en soles ÷ 3.4; mostrado con 2 decimales.)
- RTP acumulado final = 96.47 %
  - (Cálculo: (COIN OUT acumulado + JP acumulado) / COIN IN acumulado * 100; mostrado con 2 decimales.)
- Apuesta promedio del último día (último registro, fecha 15/08/2026) = 2.39 soles
  - (Cálculo: COIN IN del último día / GAMES PLAYED del último día, mostrado en soles con 2 decimales.)
  - Último registro procesado: fecha_op = 15/08/2026, COIN IN = 1,273.84 soles, COIN OUT = 1,774.10 soles, JP = 0.00 soles, GAMES PLAYED = 533.

Notas adicionales:
- Todos los cálculos numéricos fueron ejecutados en Python (Code Interpreter). Los resultados visibles fueron redondeados únicamente al final a 2 decimales según las reglas.
- Se respetaron las reglas de tratamiento de días sin juego: no se reiniciaron acumulados y se reportaron los registros como anomalías.
- Si desea que genere el archivo Excel procesado (.xlsx) con las columnas adicionales (acumulados, NETWIN, GPD, GPD_MA30, RTP acumulado diario, etc.) o los gráficos (RTP acumulado, COIN IN, NETWIN) los puedo producir y adjuntar. Indique qué archivos o gráficos desea.

No se generaron archivos descargables.

# Prueba 2 — Día sin juego

## Objetivo

Validar el comportamiento del agente ante un día sin actividad.

Se espera que un día sin juego:

- tenga GPD = 0
- tenga apuesta promedio igual a 0
- no reinicie acumulados
- conserve el RTP acumulado del día anterior
- no sea tratado como error de calidad.

## Archivo usado
BDTGM.xlsx

## Parámetros de entrada
- Tipo de cambio: 3.40 S/ por USD
- RTP teórico: 94.15%

## Fecha evaluada
08/08/2025

## Pregunta enviada al agente

Revisa el día 08/08/2025. Indica si hubo juego, muestra COIN IN, COIN OUT, GAMES PLAYED, GPD y apuesta promedio de ese día, y explica qué ocurre con los acumulados y el RTP acumulado.

## Resultado esperado

Para el día 08/08/2025:

- Coin In = 0
- Coin Out = 0
- JP = 0
- Games Played = 0
- GPD = 0
- Apuesta Promedio = 0
- NetWin = 0

Los acumulados deben conservar el valor del día anterior.

El RTP acumulado no debe cambiar.

## Resultado obtenido

El agente identificó correctamente el día como día sin juego y devolvió:

- Coin In: US$ 0.00
- Coin Out: US$ 0.00
- JP: US$ 0.00
- Games Played: 0
- GPD: 0
- Apuesta Promedio: S/ 0.00
- NetWin: US$ 0.00

También confirmó que:

- los acumulados se mantuvieron;
- el RTP acumulado permaneció en `93.20%`;
- el RTP estaba `0.95 puntos porcentuales` por debajo del RTP teórico;
- no se inventaron datos.

## Conclusión

**PRUEBA 2 APROBADA.**

El agente trató correctamente un día sin juego y conservó los acumulados y el RTP acumulado.

Esto fue lo que se tuvo en el TERMINAL DE VS CODE

PS C:\Users\Usuario\Documents\DSRP\TRABAJO FINAL\PYTHON> & C:\Users\Usuario\AppData\Local\Programs\Python\Python310\python.exe "c:/Users/Usuario/Documents/DSRP/TRABAJO FINAL/PYTHON/agente_kpi_tgm_final.py"
=== AGENTE ANALISTA KPI TGM - FOUNDY + CODE INTERPRETER ===
Ruta del archivo Excel: "C:\Users\Usuario\Documents\DSRP\TRABAJO FINAL\PYTHON\BDTGM.xlsx"
Tipo de cambio (S/ por USD): 3.4
RTP teórico (%) [déjalo vacío si no aplica]: 94.15

Ejemplos de preguntas:
- ¿Cuál fue la máquina con mayor NetWin?
- Calcula el RTP acumulado final.
- Genera el gráfico de RTP acumulado.
- Genera el gráfico de Coin In diario.
- Valida la calidad de los datos y dame observaciones.

Escribe tu pregunta: Revisa el día 08/08/2025. Indica si hubo juego, muestra COIN IN, COIN OUT, GAMES PLAYED, GPD y apuesta promedio de ese día, y explica qué ocurre con los acumulados y el RTP acumulado.

Archivo cargado correctamente: assistant-YRriuUw3VxTaMU6i8NzPgP
Agente creado: agente-kpi-tgm-final - versión 1

=== RESPUESTA DEL AGENTE ===
Validación previa (resumen)
- Encabezado real detectado correctamente y datos usados desde esa fila hacia abajo.
- Columnas obligatorias presentes: LOCAL, MARCA, MOD_COMER, MAQUINA, fecha_op, COIN IN, COIN OUT, JP, GAMES PLAYED.
- Fechas convertidas y ordenadas cronológicamente.
- Valores negativos: ninguno detectado en COIN IN, COIN OUT, JP ni GAMES PLAYED.
- Filas con GAMES_PLAYED vacías que requieren revisión: ninguna con actividad incompatible.
- Normalizaciones aplicadas por regla (GAMES_PLAYED vacío + COIN IN = COIN OUT = JP = 0): ninguna en este archivo.
- Resultado de la validación: correcta (no se detectaron inconsistencias relevantes).

Nota: todos los cálculos numéricos fueron ejecutados con Python (Code Interpreter) siguiendo las reglas indicadas (conversión a USD = VALOR_SOLES / tipo_cambio; acumulados calculados en soles y convertidos luego a USD; RTP acumulado calculado con acumulados, etc.).

Parámetros usados
- Tipo de cambio usado: 3.4 (S/ por USD).
- RTP teórico indicado: 94.15%.

Revisión del día 08/08/2025
- ¿Hubo juego ese día? No. Ese registro cumple la condición de día sin juego: COIN IN = 0, COIN OUT = 0 y GAMES PLAYED = 0.
Valores del día (mostrados con el formato solicitado)
- COIN IN (USD): 0.00
- COIN OUT (USD): 0.00
- JP (USD): 0.00
- GAMES PLAYED: 0
- GPD (Games Played Día): 0
- APUESTA PROMEDIO (soles): 0.00
- NETWIN día (USD): 0.00

Explicación sobre acumulados y RTP acumulado
- Los acumulados no se reinician en días sin juego. En 08/08/2025 los acumulados conservan su valor previo.
  - COIN IN acumulado (Soles): 143,030.32 -> COIN IN acumulado (USD): 42,067.74
  - COIN OUT acumulado (Soles): 133,303.88 -> COIN OUT acumulado (USD): 39,207.02
  - JP acumulado (Soles): 0.00 -> JP acumulado (USD): 0.00
  - NETWIN acumulado (USD): 2,860.72
  (Los acumulados en USD se calcularon dividiendo primero el acumulado en soles entre el tipo de cambio 3.4 y redondeando la cifra final a 2 decimales.)
- RTP acumulado en 08/08/2025: 93.20%
  - Cálculo aplicado: RTP_acum = (COIN_OUT_acum + JP_acum) / COIN_IN_acum * 100 (conservando el valor del día anterior si es día sin juego).
  - Comparación con RTP teórico (94.15%): el RTP acumulado está 0.95 puntos porcentuales por debajo del teórico.

Observaciones finales y cumplimiento de reglas
- Día 08/08/2025 se considera día sin juego (GPD = 0). Según las reglas, los acumulados permanecen y el RTP acumulado conserva su valor (es decir, no se recalcula para forzar reinicios).
- No se realizó ninguna imputación de datos (no se “inventó” ningún GAMES PLAYED). Todas las operaciones monetarias y porcentuales fueron calculadas con Python.
- Validación: correcta (no se encontraron inconsistencias ni valores negativos; no hubo normalizaciones aplicadas en este caso).

Si desea, puedo:
- Generar y adjuntar el Excel procesado (.xlsx) que contiene las columnas calculadas (COIN_IN_ACUM, COIN_OUT_ACUM, JP_ACUM, NETWIN_USD, RTP_ACUM, GPD, APUESTA_PROMEDIO, GPD_MA30, etc.).
- Mostrar el gráfico de RTP acumulado y GPD diario según las especificaciones (frecuencia diaria, RTP teórico, áreas roja/verde, media móvil MA30, etiquetas cada ~7 días, etc.).

Indíqueme si desea que genere el archivo Excel procesado y/o los gráficos solicitados.

No se generaron archivos descargables.
PS C:\Users\Usuario\Documents\DSRP\TRABAJO FINAL\PYTHON>

# Prueba 3 — Detección de errores de calidad de datos

## Objetivo

Comprobar que el agente pueda distinguir entre:

- un día sin juego legítimo
- un dato realmente faltante o inconsistente.

La prueba también verifica que el agente no complete automáticamente datos faltantes cuando existe actividad.

## Archivo usado
BDTGM_PRUEBA_ERROR.xlsx

Este archivo es una copia de prueba creada a partir de la base original.

## Errores introducidos deliberadamente

### Error 1 — GAMES PLAYED vacío con actividad monetaria

Fecha:

09/12/2025

Se eliminó únicamente el valor de GAMES PLAYED, manteniendo actividad monetaria.

Valores reportados por el agente:

- Coin In = S/ 7,968.28
- Coin Out = S/ 7,693.86
- JP = 0
- Games Played = vacío

### Error 2 — fecha_op vacía

En la fila Excel 234 se eliminó únicamente fecha_op, manteniendo los demás valores.

Valores presentes:

- Coin In = S/ 9,420.88
- Coin Out = S/ 9,803.18
- JP = 0
- Games Played = 4,452

## Parámetros de entrada

- Tipo de cambio: 3.40 S/ por USD
- RTP teórico: 94.15%

## Pregunta enviada al agente

> Valida la calidad de los datos e identifica todos los valores faltantes o inconsistentes. Para cada caso, indica la fila o registro afectado, el campo con problema, por qué no debe corregirse automáticamente y qué cálculos o análisis quedan afectados.

## Resultado esperado

El agente debe detectar ambos errores.

### Para GAMES PLAYED vacío

Debe:

- identificar que existe actividad monetaria
- no reemplazar el dato por 
- no inventar Games Played
- marcar GPD como no calculable
- marcar Apuesta Promedio como no calculable
- advertir que quedan afectados Games Played acumulado y GPD_MA30.

### Para fecha_op vacía

Debe:

- identificar la fecha faltante
- no inventar una fecha
- advertir que el registro no puede ubicarse correctamente en la serie temporal
- indicar que afecta gráficos y análisis cronológicos.

## Resultado obtenido

El agente detectó correctamente:

### 1. Fecha vacía / inválida

- Fila Excel: 234
- Campo: fecha_op
- No intentó inferir ni inventar una fecha.
- Indicó que se afectan:
  - orden cronológico
  - eje X de gráficos
  - GPD diario
  - media móvil de 30 períodos
  - RTP acumulado por fecha
  - análisis temporales.

### 2. GAMES PLAYED vacío con actividad

- Fila Excel: 168
- Fecha: 09/12/2025
- Campo: GAMES PLAYED
- Detectó que no es un día sin juego.
- No reemplazó el valor por 0.
- No calculó Apuesta Promedio.
- Dejó GPD como indefinido.
- Indicó que quedan afectados:
  - Apuesta Promedio;
  - GPD;
  - Games Played acumulado;
  - GPD_MA30.

También detectó correctamente los dos días sin juego legítimos:

- 08/08/2025
- 23/11/2025

y los diferenció de los errores introducidos.

## Conclusión

**PRUEBA 3 APROBADA.**

El agente detectó correctamente ambos errores, evitó imputar datos sin evidencia y distinguió los errores reales de los días sin juego válidos.

# Resumen final

Las tres pruebas aprobadas
Esto es lo que arrojo el TERMINAL en VS CODE

PS C:\Users\Usuario\Documents\DSRP\TRABAJO FINAL\PYTHON> & C:\Users\Usuario\AppData\Local\Programs\Python\Python310\python.exe "c:/Users/Usuario/Documents/DSRP/TRABAJO FINAL/PYTHON/agente_kpi_tgm_final.py"
=== AGENTE ANALISTA KPI TGM - FOUNDY + CODE INTERPRETER ===
Ruta del archivo Excel: "C:\Users\Usuario\Documents\DSRP\TRABAJO FINAL\PYTHON\BDTGM_PRUEBA_ERROR.xlsx"
Tipo de cambio (S/ por USD): 3.4
RTP teórico (%) [déjalo vacío si no aplica]: 94.15

Ejemplos de preguntas:
- ¿Cuál fue la máquina con mayor NetWin?
- Calcula el RTP acumulado final.
- Genera el gráfico de RTP acumulado.
- Genera el gráfico de Coin In diario.
- Valida la calidad de los datos y dame observaciones.

Escribe tu pregunta: Valida la calidad de los datos e identifica todos los valores faltantes o inconsistentes. Para cada caso, indica la fila o registro afectado, el campo con problema, por qué no debe corregirse automáticamente y qué cálculos o análisis quedan afectados.

Archivo cargado correctamente: assistant-Sh6ZB1yy91gR7oVq3wGssw
Agente creado: agente-kpi-tgm-final - versión 1

=== RESPUESTA DEL AGENTE ===
Resumen ejecutivo (validación de calidad)
- Archivo: BDTGM_PRUEBA_ERROR.xlsx, hoja detectada: "1312".
- Fila usada como encabezado real: fila 3 (encabezados detectados: LOCAL, MARCA, MOD_COMER, MAQUINA,      fecha_op, COIN IN, COIN OUT, JP, GAMES PLAYED).
- Registros procesados (filas debajo del encabezado): 414 (calculado con Python).
- Tipo de cambio usado: 3.4 (proporcionado).
- RTP teórico: 94.15% (proporcionado).
- Resultado de la validación: No pasó completamente. Se detectaron anomalías que requieren revisión humana antes de cualquier corrección automática.

Anomalías detectadas (explicación y efectos)
1) Fecha vacía / inválida
- Registro afectado: fila Excel 234.
- Campo: fecha_op.
- Detalle (valores presentes): COIN IN = 9,420.88 soles; COIN OUT = 9,803.18 soles; JP = 0; GAMES PLAYED = 4,452.
- Por qué no debe corregirse automáticamente: falta la fecha; no es posible inferir de forma fiable el día al que corresponde este registro. Asignar una fecha arbitraria o desplazar el registro rompería la serie temporal diaria y alteraría todos los análisis basados en fecha.
- Cálculos / análisis afectados:
  - Orden cronológico y eje X de todos los gráficos (RTP acumulado, NETWIN diario, COIN IN diario).
  - Cálculo diario de GPD (no se puede ubicar ese GPD en la línea temporal).
  - Media móvil GPD 30d (GPD_MA30) y cualquier estadística agregada por fecha.
  - RTP acumulado por fecha si se espera una serie con fechas completas.
- Recomendación: el registro debe completarse con la fecha correcta en la fuente (sistema / reporte) antes de procesar para series diarias.

2) GAMES PLAYED vacío con actividad monetaria
- Registro afectado: fila Excel 168 (fecha en el archivo: 09/12/2025).
- Campo: GAMES PLAYED.
- Detalle (valores presentes): COIN IN = 7,968.28 soles; COIN OUT = 7,693.86 soles; JP = 0; GAMES PLAYED = vacío.
  - NETWIN_DIA_USD calculado (según la fórmula requerida): (COIN IN - COIN OUT - JP) / tipo_cambio = 80.71 USD (valor calculado y redondeado a 2 decimales).
  - APUESTA PROMEDIO: no puede calcularse porque GAMES PLAYED está vacío → resultado NaN (no se debe reemplazar automáticamente).
- Por qué no debe corregirse automáticamente: existen COIN IN y/o COIN OUT distintos de cero; el vacío en GAMES PLAYED no es compatible con un "día sin juego". Asumir 0 o inferir un número de juegos sería inventar datos.
- Cálculos / análisis afectados:
  - APUESTA PROMEDIO para ese día (COIN IN / GAMES PLAYED) → no puede calcularse.
  - GPD (Games Played Día) para ese día → falta el dato, por lo tanto GPD queda indefinido.
  - GAMES PLAYED ACUMULADO: si se propaga la ausencia (tratamiento riguroso), el acumulado de GAMES PLAYED queda indefinido (NaN) desde ese registro en adelante; esto invalida cualquier métrica acumulada que dependa de GAMES PLAYED.
  - Media móvil GPD 30 días (GPD_MA30): la presencia de un GAMES PLAYED vacío que no corresponde a un día sin juego interrumpe el cálculo correcto de la MA30 porque no es un 0 válido que podamos normalizar.
- Recomendación: solicitar el valor correcto de GAMES PLAYED para la fila 168 o confirmar que efectivamente hubo error en el conteo.

3) Días sin juego (normalización válida)
- Registros afectados:
  - fila Excel 45 — fecha 08/08/2025 — COIN IN = 0.00, COIN OUT = 0.00, JP = 0.00, GAMES PLAYED = 0.
  - fila Excel 152 — fecha 23/11/2025 — COIN IN = 0.00, COIN OUT = 0.00, JP = 0.00, GAMES PLAYED = 0.
- Tratamiento aplicado: son días sin juego legítimos. Según las reglas, se interpretan/normalizan como GAMES PLAYED = 0 (en estos registros ya figura 0) y APUESTA_PROMEDIO = 0, sin reiniciar acumulados.
- Verificación (hecho con Python): los acumulados monetarios (COIN IN ACUM, COIN OUT ACUM, JP ACUM) no se reinician en esos días; el acumulado conserva el valor anterior (comportamiento correcto).
- Impacto en cálculos:
  - No hay impacto negativo en RTP acumulado; el RTP acumulado conserva el valor anterior y sigue siendo calculable.
  - En la media móvil GPD 30d, estos días se deben usar como GPD = 0 (no NaN) para que la MA30 no se interrumpa (esto está conforme a las reglas).

Comprobaciones adicionales (resultados calculados con Python)
- Registros procesados: 414.
- Cantidad de fechas inválidas / vacías detectadas: 1 (fila 234).
- Cantidad de GAMES PLAYED vacíos: 1 (fila 168 — con actividad monetaria).
- Cantidad de días sin juego (COIN IN=0, COIN OUT=0, GAMES PLAYED=0): 2 (filas 45 y 152).
- Valores negativos detectados en COIN IN / COIN OUT / JP / GAMES PLAYED: 0 (ninguno).
- Valores calculados de ejemplo (redondeados solo para presentación):
  - Fila 168 (09/12/2025): NETWIN_DIA_USD = 80.71 USD; APUESTA_PROMEDIO = no calculable (GAMES PLAYED vacío).
  - Fila 234 (fecha vacía): NETWIN_DIA_USD = -112.44 USD; GAMES PLAYED = 4,452 (pero sin fecha asociada).
  - Fila 45 (08/08/2025): APUESTA_PROMEDIO = 0.00 (día sin juego).
  - Fila 152 (23/11/2025): APUESTA_PROMEDIO = 0.00 (día sin juego).

Impacto general en los KPIs solicitados
- RTP acumulado (serie diaria): puede calcularse con las filas que tienen fecha. Sin embargo:
  - La fila sin fecha (234) no tiene fecha para ubicarla cronológicamente; debe corregirse antes de graficar con fecha_op en eje X.
  - La falta de GAMES PLAYED en la fila 168 no afecta directamente al cálculo del RTP (que usa COIN IN / COIN OUT / JP), pero sí afecta a las métricas dependientes de juegos (GPD diario, GAMES PLAYED ACUM, APUESTA PROMEDIO, GPD_MA30).
- GPD diario: la fila 168 queda sin GPD y por tanto rompe la serie de GPD si se deja como NaN. No se debe convertir automáticamente en 0 porque existe actividad monetaria.
- GPD_MA30: la media móvil de 30 días se verá afectada por el NaN en GAMES PLAYED (fila 168). Si se utiliza el comportamiento correcto (no reemplazar por 0), la MA30 dará NaN para ventanas que incluyan ese día; por eso se requiere la corrección del dato.
- NETWIN diario y COIN IN diario: pueden calcularse para todas las filas con fecha válida. El registro sin fecha no puede ubicarse en la serie temporal hasta que se le asigne fecha.

Acciones recomendadas (prioritarias)
1) Completar la fecha del registro en la fila Excel 234 (fecha_op). Sin la fecha correcta no se puede integrar ese registro en las series diarias ni representarlo en eje X.
2) Proveer el valor de GAMES PLAYED para la fila Excel 168 (09/12/2025) o confirmar la razón por la que falta (error de captura, reporte parcial, etc.). Es imprescindible para:
   - APUESTA PROMEDIO de ese día,
   - GPD diario,
   - GAMES PLAYED ACUM y GPD_MA30 (todos los cálculos acumulados y de media móvil que dependen de GAMES PLAYED).
3) Tras las correcciones anteriores, re-ejecutar el procesamiento (orden cronológico por fecha_op y cálculo de acumulados) y regenerar:
   - Tabla procesada (.xlsx) con formatos requeridos (fechas dd/mm/yyyy, formatos monetarios/porcentuales con 2 decimales, juegos/GPD enteros).
   - Gráficos: RTP acumulado (con las reglas visuales establecidas), GPD MA30, y series de NETWIN y COIN IN diarias.

Notas técnicas sobre el procesamiento realizado
- La detección del encabezado y la selección de registros se realizó automáticamente buscando la fila que contiene los encabezados requeridos.
- Ordené los registros cronológicamente por fecha_op (las filas con fecha vacía quedaron sin fecha y se detectaron explícitamente).
- Todos los cálculos numéricos y detecciones descritas aquí fueron realizados con Python (Code Interpreter).
- No se han modificado los datos originales; solo se detectaron y marcaron anomalías. No se imputó ni inventó ningún valor.

# Conclusión general

Las tres pruebas funcionales fueron superadas.

El agente demostró capacidad para:

- leer correctamente la estructura del Excel;
- validar datos;
- calcular KPI;
- convertir valores monetarios;
- mantener acumulados;
- tratar días sin juego;
- detectar datos faltantes;
- evitar inventar o imputar información;
- distinguir errores reales de registros válidos;
- usar Python mediante Code Interpreter para ejecutar los cálculos numéricos.
