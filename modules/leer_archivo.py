def run(params, context):
    archivo = params.get("archivo", "output.txt")
    try:
        with open(archivo, "r") as f:
            contenido = f.read()
        print(f"[Leer] Contenido de {archivo}:\n{contenido}")
    except Exception as e:
        print(f"[Leer] Error al leer {archivo}: {e}")
