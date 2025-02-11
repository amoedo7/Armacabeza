import json
import os
from piezas import cargar_escenarios, guardar_escenarios, ejecutar_escenario

MESA_JSON = "mesa.json"

def crear_escenario():
    nombre = input("Nombre del escenario: ")
    descripcion = input("Descripción del escenario: ")
    escenario = {
        "name": nombre,
        "description": descripcion,
        "piezas": []
    }
    escenarios = cargar_escenarios()
    escenarios.append(escenario)
    guardar_escenarios(escenarios)
    print(f"Escenario '{nombre}' creado exitosamente.")

def agregar_pieza_a_escenario():
    escenarios = cargar_escenarios()
    if not escenarios:
        print("No hay escenarios. Crea uno primero.")
        return
    print("Escenarios disponibles:")
    for idx, esc in enumerate(escenarios, 1):
        print(f"{idx}) {esc['name']}")
    idx = int(input("Selecciona el escenario al que agregar la pieza: ")) - 1
    escenario = escenarios[idx]
    pieza_id = len(escenario["piezas"]) + 1
    name = input("Nombre de la pieza: ")
    description = input("Descripción de la pieza: ")
    type = input("Tipo de pieza (action, trigger, transformation): ")
    module = input("Módulo asociado (nombre del archivo en modules/ sin .py): ")
    enabled = True  # Por defecto habilitada
    requires_api = input("¿Requiere API? (s/n): ").strip().lower() == "s"
    provider = ""
    if requires_api:
        provider = input("Proveedor de API (ej: telegram, google, openai): ")
    params_input = input("Ingresa parámetros en formato clave1=valor1,clave2=valor2 (o deja vacío): ")
    params = {}
    if params_input:
        for item in params_input.split(","):
            key, value = item.split("=")
            params[key.strip()] = value.strip()
    dependencies = []  # Puede usarse para dependencias adicionales si se requiere
    auth_required = requires_api
    api_key_field = ""
    if requires_api:
        api_key_field = input("Nombre del campo de API key (ej: telegram_api_key): ")
    metadata = {
        "version": "1.0",
        "author": "El3imm"
    }
    timeout = int(input("Timeout en segundos: "))
    retry_input = input("Configura reintentos (max_attempts,delay) separados por coma (ej: 3,5) o deja vacío: ")
    retry = {}
    if retry_input:
        max_attempts, delay = retry_input.split(",")
        retry = {"max_attempts": int(max_attempts.strip()), "delay": int(delay.strip())}
    tags_input = input("Ingresa etiquetas separadas por coma: ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    status = "pending"
    depends_on_input = input("IDs de piezas de las que depende (separadas por coma, o deja vacío): ")
    depends_on = [int(x.strip()) for x in depends_on_input.split(",")] if depends_on_input else []

    pieza = {
        "id": pieza_id,
        "name": name,
        "description": description,
        "type": type,
        "module": module,
        "enabled": enabled,
        "requires_api": requires_api,
        "provider": provider,
        "params": params,
        "dependencies": dependencies,
        "auth_required": auth_required,
        "api_key_field": api_key_field,
        "metadata": metadata,
        "timeout": timeout,
        "retry": retry,
        "tags": tags,
        "status": status,
        "depends_on": depends_on
    }
    escenario["piezas"].append(pieza)
    guardar_escenarios(escenarios)
    print(f"Pieza '{name}' agregada al escenario '{escenario['name']}'.")

def listar_escenarios():
    escenarios = cargar_escenarios()
    if not escenarios:
        print("No hay escenarios guardados.")
    else:
        print("Escenarios guardados:")
        for esc in escenarios:
            print(f"Nombre: {esc['name']}, Descripción: {esc['description']}")
            print("Piezas:")
            for p in esc["piezas"]:
                print(f"  ID {p['id']}: {p['name']} (Estado: {p['status']})")
            print("----")

def menu():
    while True:
        print("\n--- Menú Principal de Armacabeza ---")
        print("1) Crear un nuevo escenario")
        print("2) Agregar una pieza a un escenario")
        print("3) Listar escenarios")
        print("4) Ejecutar un escenario")
        print("5) Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            crear_escenario()
        elif opcion == '2':
            agregar_pieza_a_escenario()
        elif opcion == '3':
            listar_escenarios()
        elif opcion == '4':
            escenarios = cargar_escenarios()
            if not escenarios:
                print("No hay escenarios para ejecutar.")
            else:
                print("Escenarios disponibles:")
                for idx, esc in enumerate(escenarios, 1):
                    print(f"{idx}) {esc['name']}")
                idx_e = int(input("Selecciona el escenario a ejecutar: ")) - 1
                ejecutar_escenario(escenarios[idx_e]["name"])
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
