from datetime import date
# Importación de las funciones de análisis desarrolladas en los pasos anteriores
from carga import cargar_telemetria
from procesamiento import (
    analizar_por_servidor,
    calcular_estadisticas_globales,
    clasificar_incidentes,
)


def exportar_reporte(sesiones, ruta_salida = "reporte_gamesec.txt", conclusiones = None):
    """Genera un archivo de texto consolidando todos los análisis realizados.

    Si no se proporcionan 'conclusiones', se solicitan interactiva por consola.
    """
    if not sesiones:
        raise ValueError("No hay datos cargados para exportar el reporte.")

    
    if conclusiones is None or len(conclusiones) < 3:
            print("\n--- INGRESO DE CONCLUSIONES TÉCNICAS (OBLIGATORIO) ---")
            conclusiones = []
            for i in range(1, 4):
                texto = input(f"Ingrese la conclusión #{i}: ").strip()
                # Validación simple para que no quede vacía
                while not texto:
                    texto = input(f"La conclusión #{i} no puede estar vacía. Reintente: ").strip()
                conclusiones.append(texto)


    globales = calcular_estadisticas_globales(sesiones)
    por_servidor = analizar_por_servidor(sesiones)
    frecuencias, criticos = clasificar_incidentes(sesiones)

    with open(ruta_salida, 'w', encoding="utf-8") as archivo:
        archivo.write("============================================\n")
        archivo.write("REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC\n")
        archivo.write("============================================\n")
        archivo.write("Fecha de generación: " + date.today().strftime("%d-%m-%Y") + "\n\n")

        # 1. Estadísticas Globales
        archivo.write("[1] RESUMEN GLOBAL OPERATIVO\n")
        archivo.write("----------------------------------------------------------------------\n")
        archivo.write(
            f"Total de sesiones procesadas: {globales['total_sesiones']}\n"
        )
        archivo.write(
            f"Ping promedio global: {globales['ping_promedio']} ms\n"
        )
        archivo.write(
            f"Duración media de partida: {globales['duracion_promedio']} min\n"
        )
        archivo.write(
            f"Partidas de alta competencia (Ranked/Torneo): {globales['porcentaje_competitivas']}%\n\n"
        )

        # 2. Rendimiento por Servidor
        archivo.write("[2] RENDIMIENTO REGIONAL POR SERVIDOR\n")
        archivo.write("----------------------------------------------------------------------\n")
        archivo.write(
            f"{'Servidor':<18} | {'Sesiones':<8} | {'Ping Promedio':<13} | {'FPS Promedio':<12}\n"
        )
        archivo.write(
            "----------------------------------------------------------------------\n")

        for srv, datos in por_servidor.items():
            ping_str = f"{datos['ping_promedio']:.2f} ms"
            fps_str = f"{datos['fps_promedio']:.2f} fps"
            # Se aplica el alineado a la izquierda (<) manteniendo el ancho exacto de cada columna
            archivo.write(
                f"{srv:<18} | {datos['cantidad']:<8} | {ping_str:<13} | {fps_str:<12}\n"
        )
        archivo.write("\n")

        # 3. Auditoría de Seguridad
        archivo.write("[3] AUDITORÍA DE SEGURIDAD E INCIDENTES\n")
        archivo.write("----------------------------------------------------------------------\n")
        # 3.1. Obtenemos el total de sesiones
        total_sesiones = globales["total_sesiones"]

        # 3.2. Calculamos los porcentajes de cada estado
        pct_normal = round((frecuencias["Normal"] / total_sesiones) * 100, 2)
        pct_sospechoso = round((frecuencias["Sospechoso"] / total_sesiones) * 100, 2)
        pct_critico = round((frecuencias["Crítico"] / total_sesiones) * 100, 2)

        # 3.3. Escribimos las líneas en el archivo de texto
        archivo.write("Distribución de estados de seguridad:\n")
        archivo.write(f"  • Normales:    {frecuencias['Normal']:>3} sesiones ({pct_normal:>6.2f}%)\n")
        archivo.write(f"  • Sospechosos: {frecuencias['Sospechoso']:>3} sesiones ({pct_sospechoso:>6.2f}%)\n")
        archivo.write(f"  • Críticos:    {frecuencias['Crítico']:>3} sesiones ({pct_critico:>6.2f}%)\n\n")

        archivo.write("Detalle de Sesiones Críticas Detectadas:\n")
        for c in criticos:
            archivo.write(
                f"[!] Sesión: #{c['id_sesion']} | Jugador: {c['jugador_id']} | Servidor: {c['servidor']}\n"
            )
            archivo.write(f"  Motivo: {c['motivo']}\n")
        archivo.write("\n")

        archivo.write("[4] CONCLUSIONES TÉCNICAS DEL EQUIPO\n")
        archivo.write("----------------------------------------------------------------------\n")
        archivo.write(f"1. {conclusiones[0]}\n")
        archivo.write(f"2. {conclusiones[1]}\n")
        archivo.write(f"3. {conclusiones[2]}\n")
        archivo.write("======================================================================\n")
        archivo.write("                    FIN DEL REPORTE GAMESEC\n")
        archivo.write("======================================================================\n")

    print(f"\n[+] Reporte exportado exitosamente a '{ruta_salida}'")


def mostrar_menu():
    print("\n=========================================")
    print("     GAMESEC MONITOR - PANEL DE CONTROL  ")
    print("=========================================")
    print("1. Cargar y validar dataset")
    print("2. Ver estadísticas globales de servidores")
    print("3. Ver rendimiento por región de servidor")
    print("4. Auditar incidentes de seguridad (Críticos y Sospechosos)")
    print("5. Exportar reporte consolidado (reporte_gamesec.txt)")
    print("6. Salir")
    print("=========================================")


def main():
    sesiones = []
    ruta_defecto = "gamesec_logs.csv"

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ruta = input(
                f"Ingrese la ruta del archivo CSV [{ruta_defecto}]: "
            ).strip()
            if not ruta:
                ruta = ruta_defecto

            try:
                sesiones = cargar_telemetria(ruta)
                print(
                    f"\n[+] ¡Éxito! Se cargaron {len(sesiones)} registros correctamente."
                )
            except Exception as e:
                print(f"\n[-] Error al cargar el archivo: {e}")

        elif opcion == "2":
            if not sesiones:
                print("\n[-] Primero debe cargar un dataset (Opción 1).")
                continue

            try:
                stats = calcular_estadisticas_globales(sesiones)
                print("\n--- ESTADÍSTICAS GLOBALES ---")
                print(
                    f"Total de sesiones:        {stats['total_sesiones']}"
                )
                print(
                    f"Ping promedio global:     {stats['ping_promedio']} ms"
                )
                print(
                    f"Duración promedio:        {stats['duracion_promedio']} min"
                )
                print(
                    f"Sesiones competitivas:    {stats['porcentaje_competitivas']}%"
                )
            except Exception as e:
                print(f"\n[-] Error al calcular estadísticas: {e}")

        elif opcion == "3":
            if not sesiones:
                print("\n[-] Primero debe cargar un dataset (Opción 1).")
                continue

            try:
                servidores = analizar_por_servidor(sesiones)
                print("\n--- RENDIMIENTO POR REGIÓN DE SERVIDOR ---")
                for srv, datos in servidores.items():
                    print(f"\nServidor: {srv}")
                    print(f"  - Total sesiones: {datos['cantidad']}")
                    print(
                        f"  - Ping promedio:  {datos['ping_promedio']} ms"
                    )
                    print(f"  - FPS promedio:   {datos['fps_promedio']}")
            except Exception as e:
                print(f"\n[-] Error al analizar servidores: {e}")

        elif opcion == "4":
            if not sesiones:
                print("\n[-] Primero debe cargar un dataset (Opción 1).")
                continue

            try:
                frecuencias, criticos = clasificar_incidentes(sesiones)
                print("\n--- RESUMEN DE INCIDENTES DE SEGURIDAD ---")
                print(f"Normales:    {frecuencias['Normal']}")
                print(f"Sospechosos: {frecuencias['Sospechoso']}")
                print(f"Críticos:    {frecuencias['Crítico']}")

                if criticos:
                    print(
                        f"\n--- DETALLE DE EVENTOS CRÍTICOS ({len(criticos)}) ---"
                    )
                    for ev in criticos:
                        print(
                            f"• ID: {ev['id_sesion']} | Jugador: {ev['jugador_id']} | Servidor: {ev['servidor']}"
                        )
                        print(f"  Motivo: {ev['motivo']}")
            except Exception as e:
                print(f"\n[-] Error al clasificar incidentes: {e}")

        elif opcion == "5":
            if not sesiones:
                print("\n[-] Primero debe cargar un dataset (Opción 1).")
                continue

            try:
                exportar_reporte(sesiones)
            except Exception as e:
                print(f"\n[-] Error al exportar el reporte: {e}")

        elif opcion == "6":
            print("\nSaliendo del sistema GameSec Monitor. ¡Hasta luego!")
            break

        else:
            print("\n[-] Opción no válida. Por favor, seleccione entre 1 y 6.")


if __name__ == "__main__":
    main()