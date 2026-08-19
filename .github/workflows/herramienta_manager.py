import os
import json
from datetime import datetime

REPORTS_DIR = "reports"
REPARACIONES_FILE = os.path.join(REPORTS_DIR, "reparaciones.json")
INVENTARIO_FILE = "herramientas_mock.json"

def inicializar_archivos():
    """Asegura que las carpetas y archivos necesarios existan."""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    if not os.path.exists(REPARACIONES_FILE):
        with open(REPARACIONES_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def registrar_reparacion(id_herramienta, fecha_inicio, fecha_estimada, observaciones):
    """
    Registra una herramienta en estado de reparación si cumple las validaciones.
    """
    inicializar_archivos()
    inventario = cargar_json(INVENTARIO_FILE)
    reparaciones = cargar_json(REPARACIONES_FILE)

    # 1. Validar que la herramienta exista en el inventario
    if id_herramienta not in inventario:
        return False, f"❌ Error: La herramienta con ID '{id_herramienta}' no existe en el inventario."

    herramienta = inventario[id_herramienta]

    # 2. Validar que no esté ya en reparación
    if herramienta["estado"] == "En reparación":
        return False, f"⚠️ Advertencia: La herramienta '{herramienta['nombre']}' ya se encuentra en estado de reparación."

    # 3. Actualizar estado en el inventario
    herramienta["estado"] = "En reparación"
    guardar_json(INVENTARIO_FILE, inventario)

    # 4. Guardar registro detallado en /reports/reparaciones.json
    reparaciones[id_herramienta] = {
        "id_herramienta": id_herramienta,
        "nombre": herramienta["nombre"],
        "fecha_inicio_reparacion": fecha_inicio,
        "fecha_estimada_de_finalizacion": fecha_estimada,
        "observaciones": observaciones,
        "estado_registro": "Abierto"
    }
    guardar_json(REPARACIONES_FILE, reparaciones)
    return True, f"✅ Éxito: '{herramienta['nombre']}' ha cambiado a estado 'En reparación'."

def listar_reparaciones():
    """Devuelve la lista de herramientas actualmente en reparación."""
    inicializar_archivos()
    reparaciones = cargar_json(REPARACIONES_FILE)
    return [rep for rep in reparaciones.values() if rep["estado_registro"] == "Abierto"]

def finalizar_reparacion(id_herramienta):
    """Devuelve la herramienta al estado 'Activa'."""
    inventario = cargar_json(INVENTARIO_FILE)
    reparaciones = cargar_json(REPARACIONES_FILE)

    if id_herramienta not in reparaciones or reparaciones[id_herramienta]["estado_registro"] != "Abierto":
        return False, "❌ Esta herramienta no está registrada bajo una reparación activa."

    # Actualizar inventario
    if id_herramienta in inventario:
        inventario[id_herramienta]["estado"] = "Activa"
        guardar_json(INVENTARIO_FILE, inventario)

    # Cerrar registro en reparaciones.json
    reparaciones[id_herramienta]["estado_registro"] = "Finalizado"
    guardar_json(REPARACIONES_FILE, reparaciones)
    return True, f"🔄 Éxito: La herramienta '{reparaciones[id_herramienta]['nombre']}' vuelve a estar 'Activa' en el inventario."
