import csv
import os


def cargar_telemetria(ruta_archivo: str) -> list[dict]:
    # 1. Validar existencia del archivo
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"El archivo especificado no existe: {ruta_archivo}"
        )

    # Definición de campos para casteo explícito
    campos_int = {"id_sesion", "ping_promedio", "fps_promedio", "intentos_fallidos", "reportes_trampa"}
    campos_float = {"duracion_minutos"}

    registros = []

    # 2. Abrir archivo con UTF-8
    with open(ruta_archivo, 'r', encoding="utf-8") as archivo:
        # 3. Mapeo automático de columnas
        lector = csv.DictReader(archivo)

        for fila in lector:
            registro_casteado = {}

            for clave, valor in fila.items():
                if valor is None:
                    registro_casteado[clave] = None
                    continue

                valor_limpio = valor.strip()

                # 4. Casteo explícito de tipos
                if clave in campos_int:
                    registro_casteado[clave] = int(valor_limpio)
                elif clave in campos_float:
                    registro_casteado[clave] = float(valor_limpio)
                else:
                    registro_casteado[clave] = (
                        valor_limpio  # Permanece como str
                    )

            registros.append(registro_casteado)

    # 5. Validar que contenga al menos un registro
    if not registros:
        raise ValueError(
            f"El archivo '{ruta_archivo}' está vacío o solo contiene la cabecera."
        )

    return registros