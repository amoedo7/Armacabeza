from gestor_json import obtener_apis, agregar_api

def seleccionar_api(tipo):
    """Permite seleccionar o agregar una API del tipo necesario."""
    apis = {k: v for k, v in obtener_apis().items() if tipo in k}
    
    if not apis:
        print(f"⚠️ No hay APIs guardadas para {tipo}.")
        return ingresar_nueva_api(tipo)

    print(f"\n🔹 Se necesita una API para {tipo}.")
    opciones = list(apis.keys()) + ["Ingresar nueva API"]
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}) {opcion}")

    eleccion = input("Selecciona una opción: ")
    if eleccion.isdigit():
        indice = int(eleccion) - 1
        if 0 <= indice < len(opciones) - 1:
            return apis[opciones[indice]]
        elif indice == len(opciones) - 1:
            return ingresar_nueva_api(tipo)
    
    print("❌ Opción inválida.")
    return seleccionar_api(tipo)

def ingresar_nueva_api(tipo):
    """Solicita una nueva clave y la guarda con un nombre personalizado."""
    nombre = input(f"🔹 ¿Cómo quieres nombrar esta API? (Ej: {tipo}1): ")
    clave = input("🔹 Ingresa la clave/token: ")
    agregar_api(nombre, clave)
    return clave
