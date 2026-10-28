def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    # 1. Validar que la lista no esté vacía
    if not sesiones:
        raise ValueError(
            "La lista de sesiones está vacía. No se pueden calcular las estadísticas."
        )

    # 2. Total de registros analizados
    total_sesiones = len(sesiones)

    # 3. Acumuladores para el cálculo de métricas
    suma_ping = 0
    suma_duracion = 0
    sesiones_competitivas = 0

    # Modalidades consideradas competitivas
    modalidades_competitivas = {"Competitiva", "Torneo"}

    # 4. Procesamiento en un solo recorrido
    for sesion in sesiones:
        suma_ping += sesion["ping_promedio"]
        suma_duracion += sesion["duracion_minutos"]

        if sesion.get("tipo_partida") in modalidades_competitivas:
            sesiones_competitivas += 1

    # 5. Cálculo de promedios y porcentajes con redondeo
    ping_promedio = round(suma_ping / total_sesiones, 2)
    duracion_promedio = round(suma_duracion / total_sesiones, 2)
    porcentaje_competitivas = round(
        (sesiones_competitivas / total_sesiones) * 100, 2
    )

    # 6. Retorno de métricas consolidadas
    return {
        "total_sesiones": total_sesiones,
        "ping_promedio": ping_promedio,
        "duracion_promedio": duracion_promedio,
        "porcentaje_competitivas": porcentaje_competitivas,
    }

def analizar_por_servidor(sesiones: list[dict]) -> dict:
    if not sesiones:
        raise ValueError(
            "La lista de sesiones está vacía. No se pueden analizar los datos por servidor."
        )

    # 1. Diccionario acumulador temporal
    acumuladores = {}

    # Soporte para claves cargadas desde cargar_telemetria (ping/fps) o del CSV (ping_promedio/fps_promedio)
    for sesion in sesiones:
        servidor = sesion.get("servidor")
        if not servidor:
            continue

        ping = sesion.get("ping", sesion.get("ping_promedio", 0))
        fps = sesion.get("fps", sesion.get("fps_promedio", 0))

        # 2. Poblar dinámicamente nuevas regiones de servidor
        if servidor not in acumuladores:
            acumuladores[servidor] = {
                "cantidad": 0,
                "suma_ping": 0,
                "suma_fps": 0,
            }

        # 3. Acumulación de totales
        acumuladores[servidor]["cantidad"] += 1
        acumuladores[servidor]["suma_ping"] += ping
        acumuladores[servidor]["suma_fps"] += fps

    # 4. Construcción del resultado final con promedios calculados
    resultado = {}
    for servidor, datos in acumuladores.items():
        cantidad = datos["cantidad"]
        resultado[servidor] = {
            "cantidad": cantidad,
            "ping_promedio": round(datos["suma_ping"] / cantidad, 2),
            "fps_promedio": round(datos["suma_fps"] / cantidad, 2),
        }

    return resultado

def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    frecuencias = {"Normal": 0, "Sospechoso": 0, "Crítico": 0}
    eventos_criticos = []

    for sesion in sesiones:
        # Obtener valores soportando distintas nomenclaturas de claves
        id_sesion = sesion.get("id_sesion", sesion.get("id"))
        jugador_id = sesion.get("jugador_id", sesion.get("jugador"))
        servidor = sesion.get("servidor")

        reportes = sesion.get(
            "reportes_trampa", sesion.get("reportes", 0)
        )
        intentos = sesion.get(
            "intentos_fallidos", sesion.get("intentos", 0)
        )
        ping = sesion.get("ping_promedio", sesion.get("ping", 0))

        # 1. Evaluación de Regla CRÍTICO
        if reportes >= 3 or intentos >= 4:
            frecuencias["Crítico"] += 1

            # Generar el motivo específico del incidente
            motivos = []
            if reportes >= 3:
                motivos.append(f"Exceso de reportes por trampa ({reportes})")
            if intentos >= 4:
                motivos.append(f"intentos fallidos ({intentos})")

            motivo_str = " e ".join(motivos)

            eventos_criticos.append({
                "id_sesion": id_sesion,
                "jugador_id": jugador_id,
                "servidor": servidor,
                "motivo": motivo_str,
            })

        # 2. Evaluación de Regla SOSPECHOSO
        elif (ping > 200 and intentos >= 2) or reportes == 2:
            frecuencias["Sospechoso"] += 1

        # 3. Evaluación de Regla NORMAL
        else:
            frecuencias["Normal"] += 1

    return frecuencias, eventos_criticos