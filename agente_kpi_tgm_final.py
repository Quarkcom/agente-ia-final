mport os
from pathlib import Path
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    CodeInterpreterTool,
    AutoCodeInterpreterToolParam,
)

load_dotenv()


# =========================
# CONFIGURACIÓN BASE
# =========================
PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.environ["MODEL_DEPLOYMENT_NAME"]


# =========================
# INSTRUCCIONES DEL AGENTE
# =========================
AGENT_INSTRUCTIONS = """
Eres un Agente Analista de KPI de máquinas tragamonedas (TGM).

Tu función es analizar archivos Excel de máquinas tragamonedas usando Python
mediante Code Interpreter.

Debes trabajar únicamente con los datos disponibles en el archivo.
Nunca inventes datos, columnas, períodos ni conclusiones.

==================================================
1. DETECCIÓN DE LA TABLA
==================================================

Busca la fila que contiene estos encabezados:

LOCAL
MARCA
MOD_COMER
MAQUINA
fecha_op
COIN IN
COIN OUT
JP
GAMES PLAYED

Esa fila será considerada el encabezado real de la tabla.

Ignora filas superiores de resumen, títulos o metadatos.

Usa únicamente los registros ubicados debajo del encabezado real.

Ordena los datos cronológicamente por fecha_op.

==================================================
2. VALIDACIÓN DE DATOS
==================================================

Antes de realizar cualquier análisis:

- comprobar columnas obligatorias;
- comprobar fechas vacías o inválidas;
- comprobar valores negativos en:
  COIN IN,
  COIN OUT,
  JP,
  GAMES PLAYED;
- comprobar valores vacíos;
- identificar días sin juego.

Los valores negativos en contadores deben reportarse como inconsistencias.

Si:

COIN IN = 0
COIN OUT = 0
GAMES PLAYED = 0

se considera un día sin juego.

Los acumulados no deben reiniciarse en los días sin juego.

Si GAMES PLAYED está vacío, reportarlo claramente para revisión.
No inventar un valor para completar el dato.


TRATAMIENTO DE DÍAS SIN JUEGO Y VALORES VACÍOS

Si GAMES PLAYED está vacío y en ese mismo registro:

COIN IN = 0
COIN OUT = 0
y no existe actividad monetaria del juego,

interpretar ese GAMES PLAYED vacío como 0 para efectos de cálculo.

Entonces:

GAMES PLAYED = 0
GPD = 0
APUESTA PROMEDIO = 0

Los valores acumulados deben conservar el valor del registro anterior.
No reiniciar ningún acumulado.

El RTP acumulado debe conservar el RTP acumulado anterior.

Este tratamiento debe registrarse en la validación como una
normalización de un día sin juego, no como un dato inventado.

Si GAMES PLAYED está vacío pero existe COIN IN, COIN OUT o actividad
incompatible con un día sin juego, NO reemplazar automáticamente por 0;
reportar el registro para revisión.

==================================================
3. UNIDADES
==================================================

Los datos originales del Excel están expresados en soles.

Para las respuestas del agente:

COIN IN       -> USD
COIN OUT      -> USD
JP            -> USD
NETWIN        -> USD

APUESTA PROMEDIO -> soles

RTP -> porcentaje

GAMES PLAYED -> entero

GPD -> entero o valor numérico de Games Played por día.
GPD NO tiene unidades monetarias y nunca debe expresarse en USD.

==================================================
4. DEFINICIÓN DE GPD
==================================================

GPD significa GAMES PLAYED DÍA.

GAMES PLAYED representa la variación de juegos correspondiente
al período registrado.

Si el registro corresponde exactamente a un día:

GPD = GAMES PLAYED

Si un registro representa una variación consolidada de varios días:

GPD = GAMES PLAYED / cantidad de días del período

Solo realizar esta división si la cantidad de días puede determinarse
de forma confiable a partir de los datos o ha sido indicada por el usuario.

Nunca inventar la cantidad de días.

En archivos como BDTGM, donde cada fila representa un día:

GPD = GAMES PLAYED

==================================================
5. KPI
==================================================
REGLA OBLIGATORIA DE CÁLCULO

Todos los cálculos numéricos deben ejecutarse mediante Python en Code Interpreter.

No realizar operaciones aritméticas mentalmente ni calcular resultados
directamente durante la redacción de la respuesta.

Los valores mostrados en la respuesta deben provenir de las variables
calculadas por Python.

Para conversiones monetarias:

VALOR_USD = VALOR_SOLES / tipo_cambio

El tipo de cambio debe convertirse explícitamente a número decimal
(float) antes de realizar operaciones.

Para acumulados monetarios:

1. calcular primero el acumulado en soles;
2. dividir el resultado acumulado entre el tipo de cambio;
3. redondear únicamente el resultado final visible a 2 decimales.

NETWIN DIA USD:
(COIN IN - COIN OUT - JP) / tipo_cambio

APUESTA PROMEDIO:
COIN IN / GAMES PLAYED
La Apuesta Promedio se expresa en soles.

COIN IN ACUMULADO:
suma progresiva de COIN IN desde el primer registro.

COIN OUT ACUMULADO:
suma progresiva de COIN OUT desde el primer registro.

JP ACUMULADO:
suma progresiva de JP desde el primer registro.

GAMES PLAYED ACUMULADO:
suma progresiva de GAMES PLAYED.

RTP ACUMULADO:
(COIN OUT acumulado + JP acumulado)
/
COIN IN acumulado
* 100

Si no hubo juego durante un día, el RTP acumulado conserva
el valor acumulado anterior.

==================================================
6. GRÁFICO RTP ACUMULADO
==================================================

Cuando el usuario solicite el gráfico de RTP acumulado:

    A. DATOS

    - RTP acumulado debe calcularse diariamente.
    - GPD debe calcularse diariamente.
    - No realizar consolidación semanal.
    - No realizar promedios semanales.
    - La frecuencia semanal corresponde únicamente a las etiquetas del eje X.

    B. EJE X

    Usar fecha_op.

    Mostrar etiquetas exactamente con frecuencia aproximada de 7 días.

    Formato:

    dd/mm/yyyy

    Las etiquetas deben mostrarse verticalmente.

    No cambiar la serie diaria a frecuencia semanal.

    C. EJE Y PRIMARIO - RTP

    Mostrar RTP acumulado en porcentaje.

    El RTP teórico debe ser el centro del eje.

    Límite inferior:

    RTP_teorico - 6 puntos porcentuales

    Límite superior:

    RTP_teorico + 6 puntos porcentuales

    Mostrar:

    - línea de RTP acumulado;
    - línea horizontal discontinua de RTP teórico;
    - área roja cuando RTP acumulado > RTP teórico;
    - área verde cuando RTP acumulado < RTP teórico.

   El label del eje debe decir:

    RTP %

    Usar Matplotlib para aplicar el formato del label del eje.

    Para el eje RTP usar exactamente un formato equivalente a:

    ax1.set_ylabel(
        "RTP %",
        fontsize=14,
        fontweight="bold",
        fontname="Aptos Narrow",
        color=(1.0, 0.0, 1.0),
        bbox=dict(
            facecolor="black",
            edgecolor="black",
            boxstyle="square,pad=0.25"
        )
    )

    El fondo negro debe aplicarse únicamente al cuadro que contiene
    el texto de la etiqueta vertical, no al eje completo.

    D. EJE Y SECUNDARIO - GPD

    GPD debe representar los valores DIARIOS.

    En datos diarios:

    GPD = GAMES PLAYED

    No convertir GPD a USD.
    No agregar semanalmente.

    GPD debe graficarse como una LÍNEA, no como barras ni áreas.
    No sombrear el área debajo de la línea de GPD.

    Formato de la línea GPD:
    - línea sólida;
    - grosor aproximado 0.75 pt;
    - color verde RGB(0,176,80).

    Calcular:

    GPD_MAX_REAL = máximo valor diario de GPD

    Para ampliar visualmente la zona de operación del gráfico,
    usar como límite superior visual del eje secundario:

    GPD_ESCALA_MAX = GPD_MAX_REAL * 0.50
    En la leyenda debe mostrarse siempre el máximo real:

    En la leyenda debe mostrarse siempre el máximo real:

    GPD MAX = valor máximo real observado

    El label del eje secundario debe decir:

    GPD

    Usar Matplotlib para aplicar el formato del label del eje.

    Para el eje GPD usar exactamente un formato equivalente a:

    ax2.set_ylabel(
        "GPD",
        fontsize=14,
        fontweight="bold",
        fontname="Aptos Narrow",
        color=(1.0, 192/255, 0.0),
        bbox=dict(
            facecolor="black",
            edgecolor="black",
            boxstyle="square,pad=0.25"
        )
    )

    El fondo negro debe aplicarse únicamente al cuadro que contiene
    el texto de la etiqueta vertical, no al eje completo.
    Ejemplo:

    si GPD_MAX_REAL = 16000

    el límite superior visible del eje GPD será aproximadamente:

    8000

    Los valores mayores pueden quedar fuera del área visible
    debido a este zoom deliberado.

    En la leyenda debe mostrarse siempre el máximo real:

    GPD MAX = valor máximo real observado

    El label del eje secundario debe decir:

    GPD

    Formato visual del label:

    - fondo negro;
    - texto color naranja;
    - fuente visible y de tamaño mayor.

    E. MEDIA MÓVIL GPD

    Calcular una media móvil de 30 períodos diarios usando GPD diario.

    Antes de calcular la media móvil:

    - normalizar los días sin juego válidos a GPD = 0;
    - no dejar NaN en GPD para esos días.

    Calcular:

    GPD_MA30 = media móvil de GPD diario de 30 períodos.

    Usar una ventana estricta de 30 períodos:

    rolling(window=30, min_periods=30)

    Los primeros 29 registros deben quedar sin valor de GPD_MA30,
    porque todavía no existen 30 períodos completos.

    El primer valor válido de GPD_MA30 debe aparecer en el registro 30.

    La presencia de un día sin juego válido con GPD = 0 no debe interrumpir
    la curva de media móvil.

    Para el Excel final:

    - conservar una única columna llamada exactamente GPD_MA30;
    - no crear una columna auxiliar llamada GPD_MA30_INT;
    - mostrar GPD_MA30 redondeado como número entero;
    - mantener vacíos los primeros 29 registros;
    - desde el registro 30 en adelante, mostrar el valor de GPD_MA30;
    - eliminar cualquier columna cuyo nombre comience con "Unnamed:".

    La curva debe ser:

    - color negro;
    - grosor aproximado 2.5 pt;
    - línea segmentada o discontinua;
    - claramente visible.

    La media móvil NO es semanal.

    F. LEYENDA

    La leyenda debe incluir como mínimo:

    - RTP acumulado
    - RTP teórico
    - GPD diario
    - Media móvil GPD 30 períodos
    - GPD MAX = valor máximo real
    - Días analizados = cantidad total de registros diarios procesados

    G. TÍTULO

    Usar:

    RTP ACUMULADO - {MOD_COMER} - Máquina {MAQUINA}

==================================================
7. OTROS GRÁFICOS
==================================================

NETWIN:

- frecuencia diaria;
- unidad USD;
- gráfico temporal de línea;
- eje X fecha_op.

COIN IN:

- frecuencia diaria;
- unidad USD;
- gráfico temporal de línea;
- eje X fecha_op.

==================================================
8. EXCEL DE SALIDA
==================================================

Si el usuario solicita una tabla procesada o archivo de resultados:

Generar siempre:

.xlsx

Nunca generar CSV.

Mantener los datos originales y agregar únicamente las columnas
necesarias para el análisis.

No crear columnas redundantes sin necesidad.

No dejar una columna fecha_op_raw en el archivo final.

Conservar solamente:

fecha_op

La fecha debe mostrarse como fecha corta:

dd/mm/yyyy

No mostrar hora.

==================================================
9. FORMATOS NUMÉRICOS DEL EXCEL
==================================================

Usar 2 decimales en:

COIN IN
COIN OUT
JP
NETWIN
APUESTA PROMEDIO
RTP
RTP ACUMULADO
y demás valores monetarios o porcentuales.

Usar números enteros, sin decimales, en:

GAMES PLAYED
GPD
GAMES PLAYED ACUMULADO
GPD_MA30

Aplicar formato Excel real a las celdas,
no solamente redondear los valores internamente.

Formato monetario:

0.00

Formato porcentual según la forma en que se almacene el dato,
manteniendo visualmente dos decimales.

Formato de games:

0

Formato de fecha:

dd/mm/yyyy

==================================================
10. ARCHIVOS GENERADOS
==================================================

Si generas un gráfico, guardar preferentemente como PNG.

Si generas datos procesados, guardar como Excel .xlsx.

Nunca generar CSV salvo que el usuario lo solicite explícitamente.

No mostrar enlaces sandbox como si fueran enlaces locales.

Adjuntar los archivos generados para que el programa pueda descargarlos.

==================================================
11. RESPUESTA
==================================================

Responder siempre en español.

Explicar primero cualquier anomalía detectada.

No inventar datos.

Si los datos pasan correctamente la validación,
indicar explícitamente que la validación fue correcta.
"""


# =========================
# PROMPT DINÁMICO
# =========================
def construir_prompt(pregunta_usuario: str, tipo_cambio: float, rtp_teorico: str | None):
    prompt = f"""
Analiza el archivo Excel adjunto.

Datos de contexto:
- Tipo de cambio: {tipo_cambio} soles por USD.
"""

    if rtp_teorico:
        prompt += f"- RTP teórico: {rtp_teorico}%.\n"

    prompt += f"""
Tarea del usuario:
{pregunta_usuario}

Recuerda:
- Realizar todos los cálculos numéricos con Python en Code Interpreter.
- No efectuar cálculos aritméticos durante la redacción de la respuesta.
- Para USD usar exactamente VALOR_SOLES / tipo_cambio.
- Redondear solamente el resultado final visible a 2 decimales.
- Validar primero los datos.
- No inventar información.
- Aplicar exactamente las fórmulas definidas en las instrucciones del agente.
- GPD significa Games Played Día.
- Cuando cada fila corresponde a un día, GPD = GAMES PLAYED.
- El gráfico debe conservar frecuencia diaria.
- Las etiquetas semanales corresponden únicamente al eje X.
- La media móvil de GPD es de 30 períodos diarios.
- Si generas datos procesados, usar Excel .xlsx, nunca CSV.
- Usar fecha_op en formato dd/mm/yyyy y eliminar fecha_op_raw del Excel final.
- Valores monetarios y porcentuales visibles con 2 decimales.
- Games y GPD visibles como números enteros.
- Si generas archivos, adjuntarlos como archivos descargables.
- No mostrar enlaces sandbox en el texto.
"""
    return prompt.strip()


# =========================
# DESCARGAR ARCHIVOS GENERADOS
# =========================
import os

def descargar_archivos_generados(openai_client, response):
    archivos_descargados = []
    vistos = set()

    if not hasattr(response, "output") or not response.output:
        return archivos_descargados

    carpeta_salida = Path(__file__).resolve().parent

    citas = []
    container_ids = set()

    # -------------------------------------------------
    # 1. Buscar citas estructuradas de archivos
    # -------------------------------------------------
    for item in response.output:

        # Guardar también el container_id de Code Interpreter
        if getattr(item, "type", "") == "code_interpreter_call":
            container_id = getattr(item, "container_id", None)

            if container_id:
                container_ids.add(container_id)

        if getattr(item, "type", "") != "message":
            continue

        for content_item in getattr(item, "content", []):
            annotations = getattr(content_item, "annotations", []) or []

            for annotation in annotations:

                if getattr(annotation, "type", "") == "container_file_citation":

                    citas.append(annotation)

                    container_id = getattr(annotation, "container_id", None)

                    if container_id:
                        container_ids.add(container_id)

    print(f"\nCitas de archivos detectadas: {len(citas)}")

    # -------------------------------------------------
    # 2. Descargar archivos que sí llegaron como cita
    # -------------------------------------------------
    nombres_reales = {
        getattr(c, "filename", "")
        for c in citas
        if getattr(c, "filename", "")
        and not getattr(c, "filename", "").startswith("cfile_")
    }

    for annotation in citas:

        file_id = annotation.file_id
        container_id = annotation.container_id
        filename = getattr(
            annotation,
            "filename",
            f"{file_id}.bin"
        )

        # Evitar PNG auxiliar automático cfile_...
        if filename.startswith("cfile_"):

            extension = Path(filename).suffix.lower()

            existe_archivo_real = any(
                Path(nombre).suffix.lower() == extension
                for nombre in nombres_reales
            )

            if existe_archivo_real:
                print(f"Omitiendo archivo auxiliar: {filename}")
                continue

        clave = (container_id, file_id)

        if clave in vistos:
            continue

        vistos.add(clave)

        file_content = (
            openai_client
            .containers
            .files
            .content
            .retrieve(
                file_id=file_id,
                container_id=container_id,
            )
        )

        ruta_salida = carpeta_salida / filename

        with open(ruta_salida, "wb") as f:
            f.write(file_content.read())

        archivos_descargados.append(str(ruta_salida))

    # -------------------------------------------------
    # 3. Revisar directamente los archivos del contenedor
    # -------------------------------------------------
    for container_id in container_ids:

        try:
            archivos_container = openai_client.containers.files.list(
                container_id=container_id
            )

        except Exception as e:
            print(
                f"No se pudo listar el contenedor "
                f"{container_id}: {e}"
            )
            continue

        for archivo in getattr(archivos_container, "data", []):

            file_id = getattr(archivo, "id", None)

            filename = (
                getattr(archivo, "filename", None)
                or getattr(archivo, "name", None)
            )

            if not file_id or not filename:
                continue

            # No descargar el Excel original de entrada
            if file_id.startswith("assistant-"):
                continue

            # Nos interesan los archivos de salida
            extension = Path(filename).suffix.lower()

            if extension not in {".png", ".xlsx"}:
                continue

            # Evitar auxiliares cfile_ si ya hay PNG real
            if filename.startswith("cfile_"):

                existe_png_real = any(
                    Path(a).suffix.lower() == ".png"
                    and not Path(a).name.startswith("cfile_")
                    for a in archivos_descargados
                )

                if existe_png_real:
                    continue

            clave = (container_id, file_id)

            if clave in vistos:
                continue

            vistos.add(clave)

            try:
                file_content = (
                    openai_client
                    .containers
                    .files
                    .content
                    .retrieve(
                        file_id=file_id,
                        container_id=container_id,
                    )
                )

                ruta_salida = carpeta_salida / filename

                with open(ruta_salida, "wb") as f:
                    f.write(file_content.read())

                archivos_descargados.append(
                    str(ruta_salida)
                )

                print(
                    f"Archivo recuperado directamente "
                    f"del contenedor: {filename}"
                )

            except Exception as e:
                print(
                    f"No se pudo descargar "
                    f"{filename}: {e}"
                )

    return archivos_descargados


# =========================
# MAIN
# =========================
def main():
    print("=== AGENTE ANALISTA KPI TGM - FOUNDY + CODE INTERPRETER ===")

    archivo_excel = input("Ruta del archivo Excel: ").strip().strip('"')
    if not Path(archivo_excel).exists():
        print("ERROR: el archivo no existe.")
        return

    try:
        tipo_cambio = float(input("Tipo de cambio (S/ por USD): ").strip().replace(",", "."))
    except ValueError:
        print("ERROR: tipo de cambio inválido.")
        return

    rtp_teorico = input("RTP teórico (%) [déjalo vacío si no aplica]: ").strip()
    if rtp_teorico == "":
        rtp_teorico = None

    print("\nEjemplos de preguntas:")
    print("- ¿Cuál fue la máquina con mayor NetWin?")
    print("- Calcula el RTP acumulado final.")
    print("- Genera el gráfico de RTP acumulado.")
    print("- Genera el gráfico de Coin In diario.")
    print("- Valida la calidad de los datos y dame observaciones.\n")

    pregunta_usuario = input("Escribe tu pregunta: ").strip()

    project = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )

    openai_client = project.get_openai_client()

    file_obj = None
    agent = None
    conversation = None

    try:
        # 1) Subir archivo
        with open(archivo_excel, "rb") as f:
            file_obj = openai_client.files.create(
                purpose="assistants",
                file=f,
            )

        print(f"\nArchivo cargado correctamente: {file_obj.id}")

        # 2) Crear agente
        agent = project.agents.create_version(
            agent_name="agente-kpi-tgm-final",
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=AGENT_INSTRUCTIONS,
                tools=[
                    CodeInterpreterTool(
                        container=AutoCodeInterpreterToolParam(
                            file_ids=[file_obj.id]
                        )
                    )
                ],
            ),
        )

        print(f"Agente creado: {agent.name} - versión {agent.version}")

        # 3) Crear conversación
        conversation = openai_client.conversations.create()

        # 4) Construir prompt
        prompt = construir_prompt(
            pregunta_usuario=pregunta_usuario,
            tipo_cambio=tipo_cambio,
            rtp_teorico=rtp_teorico,
        )

        # 5) Ejecutar respuesta
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=prompt,
            extra_body={
                "agent_reference": {
                    "name": agent.name,
                    "type": "agent_reference",
                }
            },
        )

        print("\n=== RESPUESTA DEL AGENTE ===")
        print(response.output_text)
        # 6) Descargar archivos generados
        archivos = descargar_archivos_generados(openai_client, response)
        if archivos:
            print("\n=== ARCHIVOS GENERADOS ===")
            for a in archivos:
                print(f"- {a}")
        else:
            print("\nNo se generaron archivos descargables.")

    finally:
        # Limpieza
        try:
            if conversation is not None:
                openai_client.conversations.delete(conversation_id=conversation.id)
        except Exception:
            pass

        try:
            if agent is not None:
                project.agents.delete_version(
                    agent_name=agent.name,
                    agent_version=agent.version,
                )
        except Exception:
            pass

        try:
            if file_obj is not None:
                openai_client.files.delete(file_obj.id)
        except Exception:
            pass

        try:
            openai_client.close()
        except Exception:
            pass

        try:
            project.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
