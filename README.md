# GameSec Monitor 🎮🛡️

**GameSec Monitor** es una herramienta de terminal escrita en Python diseñada para el procesamiento, análisis y auditoría de datos de telemetría y seguridad en servidores de videojuegos en línea. Permite identificar anomalías de red, patrones sospechosos e incidentes críticos de trampas (*cheating*) o intentos fallidos de autenticación.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Formato de Datos Esperado](#-formato-de-datos-esperado)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Uso](#-instalación-y-uso)
- [Módulos del Sistema](#-módulos-del-sistema)
- [Reglas de Clasificación de Incidentes](#-reglas-de-clasificación-de-incidentes)

---

## ✨ Características Principales

- **Carga e Ingesta de Telemetría**: Ingesta archivos `.csv` con casting automático e implícito de tipos (`int`, `float`, `str`).
- **Métricas Globales Operativas**: Cálculo en tiempo real de promedios de *ping*, duración de partida y porcentaje de sesiones competitivas.
- **Rendimiento Regional**: Análisis de la calidad de conexión (*ping* y *FPS*) agrupado por servidor/región.
- **Auditoría de Seguridad**: Detección avanzada de incidentes clasificándolos en *Normal*, *Sospechoso* y *Crítico*.
- **Generación de Reportes**: Exportación de informes técnicos consolidados en formato de texto plano (`reporte_gamesec.txt`), incluyendo conclusiones personalizadas.

---

## 📁 Estructura del Proyecto

```text
.
├── carga.py            # Lectura, validación y formateo del archivo CSV
├── procesamiento.py    # Lógica de negocio, métricas y clasificación de incidentes
├── main.py             # Interfaz de usuario (CLI) e integración del sistema
├── gamesec_logs.csv    # Dataset de telemetría (archivo fuente)
└── README.md           # Documentación del proyecto
```

---

## 📊 Formato de Datos Esperado (`gamesec_logs.csv`)

El archivo CSV debe contener las siguientes columnas para garantizar un correcto procesamiento:

| Columna | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `id_sesion` | Integer | Identificador único de la sesión de juego. |
| `jugador_id` | String | Identificador o username del jugador. |
| `servidor` | String | Servidor/Región asignada (ej: `SA-East`, `NA-East`). |
| `tipo_partida` | String | Modalidad de juego (`Competitiva`, `Torneo`, `Casual`, etc.). |
| `ping_promedio` | Integer | Latencia promedio durante la sesión (ms). |
| `fps_promedio` | Integer | Cuadros por segundo promedio en la sesión. |
| `duracion_minutos`| Float | Duración total de la partida en minutos. |
| `intentos_fallidos`| Integer | Cantidad de reintentos de conexión/autenticación. |
| `reportes_trampa` | Integer | Número de reportes por trampas recibidos. |

---

## ⚙️ Requisitos Previos

- **Python**: Versión 3.9 o superior.
- No se requieren bibliotecas de terceros (utiliza exclusivamente módulos de la librería estándar de Python: `csv`, `os`, `datetime`).

---

## 🚀 Instalación y Uso

1. **Clonar o descargar el repositorio**:
   Asegúrate de colocar todos los archivos en un mismo directorio.

2. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

3. **Navegación interactiva**:
   Utiliza el menú en consola para explorar las distintas funcionalidades:
   ```text
   =========================================
        GAMESEC MONITOR - PANEL DE CONTROL  
   =========================================
   1. Cargar y validar dataset
   2. Ver estadísticas globales de servidores
   3. Ver rendimiento por región de servidor
   4. Auditar incidentes de seguridad (Críticos y Sospechosos)
   5. Exportar reporte consolidado (reporte_gamesec.txt)
   6. Salir
   =========================================
   ```

---

## 🔍 Reglas de Clasificación de Incidentes

El módulo de seguridad categoriza las sesiones en tres niveles mediante las siguientes reglas:

1. 🔴 **Crítico**:
   - `reportes_trampa >= 3` **O** `intentos_fallidos >= 4`.
   - *Acción*: Genera un registro detallado en el reporte indicando el motivo exacto.

2. 🟡 **Sospechoso**:
   - (`ping_promedio > 200` **Y** `intentos_fallidos >= 2`) **O** `reportes_trampa == 2`.

3. 🟢 **Normal**:
   - Sesiones que no cumplen con los criterios de riesgo anteriores.

---

## 📝 Módulos del Sistema

- **`carga.py`**:
  - `cargar_telemetria(ruta_archivo)`: Válida la ruta, abre el archivo bajo codificación `utf-8`, remueve espacios innecesarios y realiza la conversión explícita de tipos.
- **`procesamiento.py`**:
  - `calcular_estadisticas_globales(sesiones)`: Genera consolidados cuantitativos.
  - `analizar_por_servidor(sesiones)`: Agrupa estadísticas de rendimiento por región.
  - `clasificar_incidentes(sesiones)`: Clasifica el estado de riesgo de cada sesión.
- **`main.py`**:
  - Bucle principal, gestión del menú CLI y formato final de salida para la exportación de reportes.