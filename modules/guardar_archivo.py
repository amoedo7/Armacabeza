def run(params, context):
    archivo = params.get("archivo", "output.txt")
    texto = params.get("texto", "")
    try:
        with open(archivo, "a") as f:
            f.write(texto + "\n")
        print(f"[Guardar] Texto guardado en {archivo}.")
    except Exception as e:
        print(f"[Guardar] Error al guardar en {archivo}: {e}")
