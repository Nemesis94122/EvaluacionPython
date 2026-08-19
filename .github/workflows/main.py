import herramienta_manager as manager

def mostrar_menu():
    print("\n" + "="*50)
    print(" 🛠️  SISTEMA DE CONTROL DE HERRAMIENTAS DE LA COMUNIDAD ")
    print("="*50)
    print("1. [Comando] registrar_reparacion")
    print("2. Listar herramientas en reparación")
    print("3. Finalizar tiempo de reparación (Activar de nuevo)")
    print("4. Salir")
    print("="*50)

def ejecutar_registrar_reparacion():
    print("\n--- Ejecutando comando: registrar_reparacion ---")
    id_h = input("Ingrese ID de la herramienta: ").strip()
    f_inicio = input("Fecha de inicio (AAAA-MM-DD) [Hoy]: ").strip()
    f_fin = input("Fecha estimada de finalización (AAAA-MM-DD): ").strip()
    obs = input("Observaciones / Detalles del daño: ").strip()

    if not id_h or not f_fin:
        print("❌ Error: El ID de la herramienta y la fecha de finalización son obligatorios.")
        return

    exito, mensaje = manager.registrar_reparacion(id_h, f_inicio, f_fin, obs)
    print(mensaje)

def ejecutar_listar():
    print("\n--- Listado de Herramientas en Reparación ---")
    lista = manager.listar_reparaciones()
    if not lista:
        print("🟢 No hay herramientas registradas en reparación en este momento.")
        return

    for item in lista:
        print(f"\n🔧 ID: {item['id_herramienta']} | Nombre: {item['nombre']}")
        print(f"   📅 Inicio: {item['fecha_inicio_reparacion']} | Est. Fin: {item['fecha_estimada_de_finalizacion']}")
        print(f"   📝 Obs: {item['observaciones']}")

def ejecutar_finalizar():
    print("\n--- Finalizar Tiempo de Reparación ---")
    id_h = input("Ingrese ID de la herramienta que terminó reparación: ").strip()
    exito, mensaje = manager.finalizar_reparacion(id_h)
    print(mensaje)

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ").strip()
        if opcion == "1":
            ejecutar_registrar_reparacion()
        elif opcion == "2":
            ejecutar_listar()
        elif opcion == "3":
            ejecutar_finalizar()
        elif opcion == "4":
            print("\n👋 ¡Gracias por usar el sistema de control!")
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
