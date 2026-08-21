# Demo Final – Agente Analista KPI TGM

## 1.- Objetivo de la demostración

Realizar una ejecución final del agente con una consulta distinta a las tres pruebas funcionales previamente documentadas.

La finalidad de esta demostración es comprobar que el agente:

- carga correctamente el archivo Excel
- valida la calidad de los datos antes del análisis
- interpreta una pregunta abierta en lenguaje natural
- ejecuta cálculos con Python mediante Code Interpreter
- relaciona varias columnas y KPI
- entrega una respuesta coherente
- finaliza la ejecución sin errores

## 2.- Parámetros usados

### 2.1.- Archivo de entrada :
BDTGM.xlsx

### 2.2.- Tipo de cambio :
3.40 S/ por USD

### 2.3.- RTP teórico :
94.15%

## 3.- Pregunta realizada al agente

Analiza el periodo completo y dime cuál fue el día con mayor Coin In, indicando la fecha, Coin In en USD, Games Played, GPD, NetWin en USD y Apuesta Promedio.

## 4.- Validación previa realizada por el agente

El agente confirmó:

- encabezado detectado correctamente
- columnas obligatorias presentes
- fechas válidas
- ausencia de valores negativos
- ausencia de valores vacíos en columnas obligatorias
- existencia de 2 días sin juego:
    a) 08/08/2025
    b) 23/11/2025
- no fue necesario aplicar normalizaciones adicionales
- la validación general de los datos fue correcta.

También indicó que todos los cálculos numéricos fueron ejecutados mediante Python en Code Interpreter.

Aqui la respuesta en el TERMINAL de VS Code

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

Escribe tu pregunta: Analiza el periodo completo y dime cuál fue el día con mayor Coin In, indicando la fecha, Coin In en USD, Games Played, GPD, NetWin en USD y Apuesta Promedio.

Archivo cargado correctamente: assistant-9NEkq6tvgETtiQ3zNo53Vn
Agente creado: agente-kpi-tgm-final - versión 1

=== RESPUESTA DEL AGENTE ===
Validación de datos (resumen)

- Encabezado detectado correctamente y datos usados a partir de la fila del encabezado.
- Columnas obligatorias presentes: LOCAL, MARCA, MOD_COMER, MAQUINA, fecha_op, COIN IN, COIN OUT, JP, GAMES PLAYED.
- Fechas: no se detectaron fechas vacías o inválidas.
- Valores negativos en contadores: no se detectaron valores negativos en COIN IN, COIN OUT, JP ni GAMES PLAYED.
- Valores vacíos: no hay valores vacíos en las columnas obligatorias (GAMES PLAYED no está vacío en ningún registro).
- Días sin juego (COIN IN = 0, COIN OUT = 0, GAMES PLAYED = 0): 2 registros
  - 08/08/2025
  - 23/11/2025
  Estos días fueron identificados como "días sin juego" según la regla definida. No fue necesario normalizar GAMES PLAYED porque no había celdas vacías en esa columna.
- Normalizaciones aplicadas: ninguna (no hubo GAMES PLAYED vacío que cumpliera las condiciones para interpretarse como 0).
- Conclusión de validación: los datos pasan la validación (sin inconsistencias de estructura ni valores negativos). Se detectaron 2 días sin juego, reportados arriba.

Notas sobre procedimiento
- Todos los cálculos numéricos fueron realizados mediante Python en Code Interpreter.
- Tipo de cambio aplicado: 3.4 soles / USD (convertido a float en los cálculos).
- RTP teórico recibido: 94.15% (no se solicitó el gráfico en esta tarea específica).

## 5.- Resultado obtenido

El agente identificó como día con mayor Coin In:

### 5.1.- Fecha
31/03/2026

### 5.2.- Coin In
- Coin In en soles: S/ 47,514.60
- Coin In en USD: US$ 13,974.88

### 5.3.- Games Played
7,235

### 5.4.- GPD
7,235

Como cada fila representa un día:

```text
GPD = GAMES PLAYED
```

### 5.5.- NetWin
US$ 3,865.14

Fórmula aplicada:

```text
NETWIN DIA USD =
(COIN IN - COIN OUT - JP) / tipo_cambio
```

### 5.6.- Apuesta Promedio
S/ 6.57

Fórmula aplicada:

```text
APUESTA PROMEDIO =
COIN IN / GAMES PLAYED
```

## 6.- Resumen de resultados

Resultado solicitado — Día con mayor COIN IN
- Fecha (fecha_op): 31/03/2026
- COIN IN (USD): 13,974.88 USD
  - (COIN IN en soles = 47,514.60; conversión USD = COIN_IN_soles / 3.4)
- GAMES PLAYED: 7,235
- GPD: 7,235
  - (cada fila representa un día; por tanto GPD = GAMES PLAYED)
- NETWIN (USD): 3,865.14 USD
  - (NETWIN día USD = (COIN IN - COIN OUT - JP) / tipo_cambio)
- APUESTA PROMEDIO (soles): 6.57 soles
  - (APUESTA PROMEDIO = COIN IN / GAMES PLAYED; mostrado en soles)

## 7.- Verificación de ejecución

La ejecución terminó correctamente.

No se presentaron errores de tipo:

- Traceback
- Exception
- PermissionError
- errores de conexión
- errores de lectura del Excel
- errores de Code Interpreter

La terminal regresó normalmente al prompt de PowerShell al finalizar.

## 8.- Conclusión de la demostración

**DEMO FINAL APROBADA.**

El agente pudo responder correctamente una consulta abierta diferente a las tres pruebas documentadas.

La demostración confirmó que el sistema puede:

- interpretar consultas en lenguaje natural
- validar datos antes de calcular
- buscar máximos dentro del periodo
- convertir valores monetarios
- calcular KPI
- relacionar Games Played con GPD
- entregar resultados claros
- completar el flujo Python → Microsoft Foundry → Code Interpreter → respuesta sin errores.

Esta ejecución puede utilizarse como evidencia adicional del funcionamiento integral del proyecto.
