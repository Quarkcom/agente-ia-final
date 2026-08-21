# Agente Analista de KPI de TGM

## Descripción

Este proyecto desarrolla un agente de inteligencia artificial para analizar indicadores operativos de máquinas tragamonedas (TGM) a partir de archivos Excel.

El agente fue construido con Microsoft Foundry, Python y Code Interpreter, y permite:

- leer archivos Excel con datos operativos
- identificar automáticamente la tabla principal
- validar la calidad de los datos
- calcular KPI
- convertir valores monetarios de soles a USD
- detectar días sin juego
- detectar datos faltantes o inconsistentes
- generar gráficos
- generar archivos Excel procesados.

## Objetivo

Automatizar el análisis básico de KPI de máquinas tragamonedas mediante un agente de IA capaz de interpretar preguntas en lenguaje natural y ejecutar los cálculos con Python.

El proyecto busca reducir tareas manuales de revisión y facilitar la identificación de errores de calidad de datos antes de realizar análisis operativos.

## Tecnologías utilizadas

- Python 3.10
- Microsoft Azure
- Microsoft Foundry
- Azure AI Projects SDK
- Azure Identity
- OpenAI Responses API mediante Microsoft Foundry
- Code Interpreter
- pandas
- matplotlib
- openpyxl
- python-dotenv
- Visual Studio Code

## Modelo utilizado

El agente utiliza el deployment:
gpt-5-mini

configurado en Microsoft Foundry.

## Arquitectura general

El flujo del sistema es:


1 Usuario
  
2 agente_kpi_tgm_final.py
   
   2.1 solicita archivo Excel
   2.2 solicita tipo de cambio
   2.3 solicita RTP teórico
   2.4 recibe pregunta del usuario
   
3 Microsoft Foundry
   
4 Agente GPT-5-mini
   
5 Code Interpreter
   
   5.1 lee Excel
   5.2 valida datos
   5.3 ejecuta Python
   5.4 calcula KPI
   5.5 genera gráficos / Excel

Respuesta al usuario

## Estructura esperada del archivo de entrada

El agente busca automáticamente una tabla que contenga los siguientes encabezados:

- LOCAL
- MARCA
- MOD_COMER
- MAQUINA
- fecha_op
- COIN IN
- COIN OUT
- JP
- GAMES PLAYED

Las filas superiores que contengan títulos, resúmenes o metadatos son ignoradas.

## Definición de KPI

### NetWin Día
NETWIN DIA USD = (COIN IN - COIN OUT - JP) / tipo_cambio

### Apuesta Promedio
APUESTA PROMEDIO = COIN IN / GAMES PLAYED

La Apuesta Promedio se expresa en soles.

### Coin In acumulado
Suma progresiva de COIN IN desde el primer registro.

### Coin Out acumulado
Suma progresiva de COIN OUT desde el primer registro.

### JP acumulado
Suma progresiva de JP desde el primer registro.

### RTP acumulado
RTP ACUMULADO (%) = (COIN OUT acumulado + JP acumulado) / COIN IN acumulado * 100

## Definición de GPD
GPD significa **Games Played Día**.
GAMES PLAYED representa la variación de juegos correspondiente al período registrado.
Si cada registro corresponde a un día: GPD = GAMES PLAYED
Si un registro representa varios días consolidados:

GPD = GAMES PLAYED / cantidad de días

Esta división solo debe realizarse si la cantidad de días es conocida y confiable.
En la base utilizada para las pruebas, cada fila corresponde a un día, por lo que:

GPD = GAMES PLAYED

## Media móvil de GPD
Se utiliza una media móvil de:30 períodos diarios

La columna generada es:
GPD_MA30
Para presentación en Excel se muestra como valor entero.

## Tratamiento de días sin juego
Si:

COIN IN = 0
COIN OUT = 0
GAMES PLAYED = 0
el registro se considera un día sin juego.

En ese caso:

- GPD = 0
- APUESTA PROMEDIO = 0
- NETWIN = 0
- los acumulados no se reinician
- el RTP acumulado conserva el valor anterior
- el cero participa normalmente en la media móvil de GPD.

## Tratamiento de datos faltantes
El agente no debe inventar información.

Ejemplo:
Si GAMES PLAYED está vacío pero existe actividad en COIN IN o COIN OUT, el agente:

- no reemplaza el valor por cero;
- marca el registro para revisión;
- no calcula GPD;
- no calcula Apuesta Promedio;
- advierte que la media móvil GPD y los acumulados dependientes de Games Played quedan afectados.

Si fecha_op está vacía:

- no intenta inventar una fecha;
- marca el registro para revisión;
- advierte que el análisis temporal y los gráficos quedan afectados.

## Conversión monetaria
Los datos originales permanecen en soles.
Para presentación:

- Coin In = USD
- Coin Out = USD
- JP = USD
- NetWin = USD
- Apuesta Promedio = soles
- RTP = porcentaje
- Games Played / GPD = cantidad de juegos

La conversión se realiza con:

VALOR USD = VALOR SOLES / tipo_cambio
El tipo de cambio es solicitado al usuario al iniciar cada ejecución.

## Gráfico de RTP acumulado

El gráfico incluye:

- RTP acumulado diario
- RTP teórico
- área roja cuando RTP acumulado está sobre el teórico
- área verde cuando RTP acumulado está bajo el teórico
- GPD diario
- media móvil GPD de 30 períodos
- etiquetas del eje X aproximadamente cada 7 días;
- fechas en formato dd/mm/yyyy.

### Eje RTP

El RTP teórico se utiliza como centro del eje.
Límite inferior = RTP teórico - 6 puntos porcentuales
Límite superior = RTP teórico + 6 puntos porcentuales

### Eje GPD
Se realiza un zoom deliberado:

GPD_ESCALA_MAX =
GPD_MAX_REAL * 0.50

El valor máximo real se informa en la leyenda:
GPD MAX = valor máximo observado

También se informa:
Días analizados = cantidad de registros diarios

### Estilo GPD
- línea sólida
- color RGB (0,176,80)
- grosor aproximado 0.75 pt.

### Media móvil

- color negro
- línea segmentada
- 30 períodos diarios.

## Archivo Excel de salida
Cuando se genera un archivo procesado, el formato de salida es:
.xlsx

No se utiliza CSV salvo solicitud explícita.
Reglas de formato:

- fechas: dd/mm/yyyy
- sin hora
- monetarios: 2 decimales
- RTP: 2 decimales
- Apuesta Promedio: 2 decimales
- Games Played: entero
- GPD: entero
- GPD_MA30: entero
- no se mantiene una columna redundante : fecha_op_raw.

## Instalación

### 1. Crear entorno Python
Se recomienda Python 3.10.

### 2. Instalar dependencias
bash
pip install azure-ai-projects==2.4.0 azure-identity python-dotenv pandas matplotlib openpyxl

## Variables de entorno
Crear un archivo .env en la carpeta del proyecto:

env
PROJECT_ENDPOINT=https://<recurso>.services.ai.azure.com/api/projects/<proyecto>
MODEL_DEPLOYMENT_NAME=gpt-5-mini

No incluir credenciales ni contraseñas en el repositorio.

## Autenticación Azure

Antes de ejecutar el proyecto:

bash
az login

Verificar la suscripción:

bash
az account show

## Ejecución
Desde la carpeta del proyecto:

bash
python agente_kpi_tgm_final.py

El programa solicitará:

1. ruta del archivo Excel
2. tipo de cambio
3. RTP teórico
4. pregunta para el agente.

## Ejemplos de preguntas

1 Calcula el RTP acumulado final.
2 Genera el gráfico de RTP acumulado.
3 Calcula la cantidad de filas, el Coin In acumulado en USD,
el Coin Out acumulado en USD, el JP acumulado en USD,
el RTP acumulado final y la apuesta promedio del último día.

Valida la calidad de los datos y dame observaciones.

## Pruebas realizadas
Se realizaron tres pruebas funcionales.

### Prueba 1 — Cálculos normales
Validó:

- acumulados
- conversión a USD
- RTP acumulado
- apuesta promedio.

Resultado:
**APROBADA**

### Prueba 2 — Día sin juego
Se evaluó el registro del 08/08/2025.

El agente detectó correctamente:

- ausencia de juego
- GPD igual a cero
- apuesta promedio igual a cero
- mantenimiento de acumulados
- mantenimiento del RTP acumulado.

Resultado:
**APROBADA**

### Prueba 3 — Errores de calidad

Se creó un archivo de prueba con:

- GAMES PLAYED vacío en un día con actividad monetaria;
- fecha_op vacía en otro registro.

El agente:

- detectó ambos errores;
- no inventó valores;
- no normalizó automáticamente el Games Played faltante;
- identificó qué KPI y análisis quedaban afectados.

Resultado:

**APROBADA**
La documentación completa de las pruebas se encuentra en:
docs/pruebas.md

## Archivos principales

agente-ia-final/

    agente_kpi_tgm_final.py
      .env
    .env.example
    .gitignore
    requirements.txt
    README.md

    docs/
       pruebas.md

## Limitaciones actuales

- El análisis depende de que los encabezados esperados existan en el archivo.
- Los datos faltantes que no puedan interpretarse de forma segura requieren revisión humana.
- La calidad del gráfico generado puede depender de las fuentes disponibles en el entorno de Code Interpreter.
- La escala del eje GPD utiliza un zoom deliberado para mejorar la lectura visual.
- El agente no modifica automáticamente datos inconsistentes cuando no existe evidencia suficiente.

## Conclusión

El proyecto demuestra que un agente de IA puede combinar lenguaje natural con Python y Code Interpreter para automatizar tareas de análisis operativo de máquinas tragamonedas.

El agente no solo calcula KPI, sino que también valida la calidad de la información, distingue entre días sin juego y errores reales de datos, genera visualizaciones y produce archivos procesados para análisis posterior.

## Repositorio del proyecto

Repositorio GitHub:
https://github.com/Quarkcom/agente-ia-final

ACTUALIZACION
El agente ya descarga correctamente los archivos generados y que GPD_MA30 usa ventana estricta de 30 períodos


## Video de demostración

Video de presentación y demostración del proyecto:
https://we.tl/t-oGWUVVz7Q0gsAPqp

