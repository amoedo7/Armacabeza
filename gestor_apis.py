import json
import re

# Función para guardar una nueva API en el archivo JSON
def guardar_api(nombre, datos):
    try:
        # Cargar los datos existentes
        apis = leer_apis()
        
        # Agregar la nueva API
        apis[nombre] = datos
        
        # Guardar el archivo actualizado
        with open('apis.json', 'w') as f:
            json.dump(apis, f, indent=4)
        
        print(f"API '{nombre}' guardada correctamente.")
    except Exception as e:
        print(f"Error al guardar la API: {e}")

# Función para leer todas las APIs guardadas
def leer_apis():
    try:
        with open('apis.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Función para extraer el token de Telegram de un mensaje de BotFather
def extraer_token_telegram(texto):
    match = re.search(r'(\d{10}:\S+)', texto)
    if match:
        return match.group(1)
    return None

# Función para extraer información de un usuario de userinfobot
def extraer_info_usuario(texto):
    user_info = {}
    
    # Buscando ID, First Name, Last Name y Lang
    user_info["id"] = re.search(r'Id:\s*(\d+)', texto).group(1) if re.search(r'Id:\s*(\d+)', texto) else None
    user_info["first_name"] = re.search(r'First:\s*(\w+)', texto).group(1) if re.search(r'First:\s*(\w+)', texto) else None
    user_info["last_name"] = re.search(r'Last:\s*(\w+)', texto).group(1) if re.search(r'Last:\s*(\w+)', texto) else None
    user_info["lang"] = re.search(r'Lang:\s*(\w+)', texto).group(1) if re.search(r'Lang:\s*(\w+)', texto) else None
    
    return user_info

# Función para listar las APIs disponibles
def listar_apis():
    apis = leer_apis()
    if not apis:
        print("No se han registrado APIs.")
        return []
    return list(apis.keys())

# Función para seleccionar una API
def seleccionar_api():
    apis = listar_apis()
    if not apis:
        return None
    
    print("Seleccione una API:")
    for idx, api in enumerate(apis, 1):
        print(f"{idx}) {api}")
    
    seleccion = input("Ingrese el número de la API que desea usar: ")
    try:
        seleccion = int(seleccion)
        if 1 <= seleccion <= len(apis):
            return apis[seleccion - 1]
        else:
            print("Selección inválida.")
            return None
    except ValueError:
        print("Entrada no válida.")
        return None
