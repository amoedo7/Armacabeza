import os
import time
import json
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Ruta del archivo JSON donde se guardarán los escenarios
archivo_escenarios = "escenarios.json"

# Lista de módulos y tipos de piezas
modulos = ["imprimir", "guardar_archivo", "leer_archivo"]
tipos_pieza = ["action", "trigger", "transformation"]

# Función para cargar los escenarios desde el archivo JSON
def cargar_escenarios():
    if os.path.exists(archivo_escenarios):
        with open(archivo_escenarios, "r") as archivo:
            return json.load(archivo)
    return []

# Función para guardar los escenarios en el archivo JSON
def guardar_escenarios():
    with open(archivo_escenarios, "w") as archivo:
        json.dump(escenarios, archivo, indent=4)

# Lista de escenarios cargada al inicio
escenarios = cargar_escenarios()

# Función para ingresar parámetros con claves posibles
def ingresar_parametros():
    claves_posibles = {
        "mensaje": "Mensaje a mostrar",
        "tiempo": "Tiempo de espera",
        "usuario": "Nombre del usuario",
        "id": "ID de la pieza"
        # Añade más claves según tus necesidades
    }
    
    print(Fore.YELLOW + "Claves posibles para los parámetros:")
    for i, clave in enumerate(claves_posibles, start=1):
        print(Fore.YELLOW + f"{i}) {clave}: {claves_posibles[clave]}")
    
    parametros = {}
    while True:
        opcion = input(Fore.GREEN + "Selecciona una clave (o presiona Enter para finalizar): ")
        if not opcion:
            break
        
        # Verificar si la opción es válida
        if opcion.isdigit() and 1 <= int(opcion) <= len(claves_posibles):
            clave_seleccionada = list(claves_posibles.keys())[int(opcion) - 1]
            valor = input(Fore.GREEN + f"Introduce el valor para '{clave_seleccionada}': ")
            parametros[clave_seleccionada] = valor
        else:
            print(Fore.RED + "Opción no válida. Intenta de nuevo.")
    
    return parametros

# Función para agregar pieza
def agregar_pieza():
    if not escenarios:
        print(Fore.RED + "No hay escenarios creados.")
        return

    print(Fore.YELLOW + "Escenarios guardados:")
    for i, escenario in enumerate(escenarios, start=1):
        print(Fore.YELLOW + f"{i}) {escenario['nombre']} - {escenario['descripcion']}")

    escena_index = int(input(Fore.GREEN + "Selecciona el escenario al que agregar la pieza: ")) - 1
    escenario = escenarios[escena_index]

    nombre_pieza = input(Fore.GREEN + "Nombre de la pieza: ")
    descripcion_pieza = input(Fore.GREEN + "Descripción de la pieza: ")

    print(Fore.YELLOW + "Tipo de pieza:")
    for i, tipo in enumerate(tipos_pieza, start=1):
        print(Fore.YELLOW + f"{i}) {tipo}")

    tipo_pieza = tipos_pieza[int(input(Fore.GREEN + "Selecciona una opción: ")) - 1]

    print(Fore.YELLOW + "Módulos disponibles:")
    for i, modulo in enumerate(modulos, start=1):
        print(Fore.YELLOW + f"{i}) {modulo}")

    modulo_seleccionado = modulos[int(input(Fore.GREEN + "Selecciona un módulo: ")) - 1]

    api = input(Fore.GREEN + "¿Requiere API? (s/n): ")
    parametros = ingresar_parametros()  # Obtener los parámetros con claves posibles
    timeout = input(Fore.GREEN + "Timeout en segundos: ")
    reintentos = input(Fore.GREEN + "Configura reintentos (max_attempts,delay) separados por coma (ej: 3,5) o deja vacío: ")
    etiquetas = input(Fore.GREEN + "Ingresa etiquetas separadas por coma: ")
    dependencias = input(Fore.GREEN + "IDs de piezas de las que depende (separadas por coma, o deja vacío): ")

    pieza = {
        "nombre": nombre_pieza,
        "descripcion": descripcion_pieza,
        "tipo": tipo_pieza,
        "modulo": modulo_seleccionado,
        "api": api,
        "parametros": parametros,
        "timeout": timeout,
        "reintentos": reintentos,
        "etiquetas": etiquetas,
        "dependencias": dependencias,
        "estado": "pending"
    }

    escenario["piezas"].append(pieza)
    guardar_escenarios()
    print(Fore.CYAN + f"Pieza '{nombre_pieza}' agregada al escenario '{escenario['nombre']}'.")

# Funciones para interactuar con el programa
def crear_escenario():
    nombre = input(Fore.GREEN + "Nombre del escenario: ")
    descripcion = input(Fore.GREEN + "Descripción del escenario: ")
    escenarios.append({"nombre": nombre, "descripcion": descripcion, "piezas": []})
    guardar_escenarios()
    print(Fore.CYAN + f"Escenario '{nombre}' creado con éxito.")

def listar_escenarios():
    if not escenarios:
        print(Fore.RED + "No hay escenarios creados.")
        return

    print(Fore.YELLOW + "Escenarios guardados:")
    for i, escenario in enumerate(escenarios, start=1):
        print(Fore.YELLOW + f"Nombre: {escenario['nombre']}, Descripción: {escenario['descripcion']}")
        if escenario["piezas"]:
            print(Fore.YELLOW + "Piezas:")
            for j, pieza in enumerate(escenario["piezas"], start=1):
                print(Fore.YELLOW + f"  ID {j}: {pieza['nombre']} (Estado: {pieza['estado']})")
        else:
            print(Fore.YELLOW + "  No hay piezas en este escenario.")

def ejecutar_escenario():
    if not escenarios:
        print(Fore.RED + "No hay escenarios creados.")
        return

    print(Fore.YELLOW + "Escenarios disponibles:")
    for i, escenario in enumerate(escenarios, start=1):
        print(Fore.YELLOW + f"{i}) {escenario['nombre']}")

    escena_index = int(input(Fore.GREEN + "Selecciona el escenario a ejecutar: ")) - 1
    escenario = escenarios[escena_index]

    print(Fore.CYAN + f"=== Iniciando ejecución del escenario '{escenario['nombre']}' ===")

    for pieza in escenario["piezas"]:
        print(Fore.CYAN + f"Ejecutando pieza ID: {escenario['piezas'].index(pieza) + 1}: {pieza['nombre']}")
        print(Fore.CYAN + f"[{pieza['nombre']}] Iniciando ejecución... [{pieza['modulo']}]")
        # Simulación de ejecución (reemplazar por la ejecución real)
        time.sleep(1)

        print(Fore.GREEN + f"[{pieza['nombre']}] Ejecutado con éxito en el intento 1.")

    print(Fore.CYAN + "=== Ejecución del escenario completada ===")

# Menú Principal
def menu():
    while True:
        print(Fore.MAGENTA + "\n--- Menú Principal de Armacabeza ---")
        print(Fore.YELLOW + "1) Crear un nuevo escenario")
        print(Fore.YELLOW + "2) Agregar una pieza a un escenario")
        print(Fore.YELLOW + "3) Listar escenarios")
        print(Fore.RED + "4) Ejecutar un escenario")
        print(Fore.RED + "5) Salir")

        opcion = input(Fore.GREEN + "Selecciona una opción: ")

        if opcion == "1":
            crear_escenario()
        elif opcion == "2":
            agregar_pieza()
        elif opcion == "3":
            listar_escenarios()
        elif opcion == "4":
            ejecutar_escenario()
        elif opcion == "5":
            print(Fore.RED + "¡Hasta luego!")
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, selecciona una opción correcta.")

# Iniciar el programa
if __name__ == "__main__":
    menu()
