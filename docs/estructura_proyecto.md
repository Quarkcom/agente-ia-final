# Estructura del Proyecto – Agente Analista KPI TGM

## 1.- agente-ia-final

### 1.1.- agente_kpi_tgm_final.py
Script principal del proyecto.

Funciones principales:
- solicita la ruta del archivo Excel
- solicita el tipo de cambio
- solicita el RTP teórico
- recibe preguntas en lenguaje natural
- se conecta a Microsoft Foundry
- crea el agente con Code Interpreter
- valida los datos
- calcula KPI
- genera gráficos y archivos Excel procesados
- descarga los archivos generados
- elimina recursos temporales al finalizar.

### 1.2.- README.md
Documento principal del proyecto.

Incluye:
- descripción
- objetivo
- arquitectura
- tecnologías utilizadas
- fórmulas de KPI
- definición de GPD
- reglas de validación
- tratamiento de días sin juego
- tratamiento de errores
- instalación
- ejecución
- ejemplos
- pruebas realizadas
- limitaciones

### 1.3.- requirements.txt
Lista de dependencias necesarias para ejecutar el proyecto.

Principales librerías:
- azure-ai-projects==2.4.0
- azure-identity
- python-dotenv
- pandas
- matplotlib
- openpyxl

### 1.4.- .env.example
Archivo de ejemplo para las variables de entorno necesarias.

Contiene:

```env
PROJECT_ENDPOINT=https://<tu-recurso>.services.ai.azure.com/api/projects/<tu-proyecto>
MODEL_DEPLOYMENT_NAME=gpt-5-mini
```

No contiene credenciales ni información sensible.

### 1.5.- .gitignore
Archivo que indica qué elementos no deben subirse al repositorio.

Incluye exclusiones para:
- .env
- archivos temporales
- caché de Python
- entornos virtuales
- archivos generados
- archivos de prueba locales.

### 1.6.- docs
Carpeta destinada a la documentación técnica adicional del proyecto.

#### 1.6.1.- pruebas.md
Documento con las tres pruebas funcionales realizadas al agente.

Incluye:
- objetivo
- archivo utilizado
- parámetros
- pregunta enviada
- resultado esperado
- resultado obtenido
- conclusión.

Pruebas documentadas:
1. cálculos normales y conversiones
2. tratamiento de día sin juego
3. detección de errores de calidad de datos.

## Estructura visual

1.- agente-ia-final

    1.1.- agente_kpi_tgm_final.py
    1.2.- README.md
    1.3.- requirements.txt
    1.4.- .env.example
    1.5.- .gitignore
    1.6.- docs
          1.6.1.- pruebas.md

> Nota: la numeración se utiliza únicamente para documentar la estructura. Los archivos físicos conservan sus nombres reales sin prefijos numéricos.
