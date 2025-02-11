import json

def guardar_json(archivo, data):
    try:
        with open(archivo, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Datos guardados en {archivo}")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def leer_json(archivo):
    try:
        with open(archivo, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al leer el archivo {archivo}: {e}")
        return []
