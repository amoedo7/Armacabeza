import json
import os
import importlib
import time

MESA_JSON = "mesa.json"
LOG_FILE = "log.txt"

def log_message(message):
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

class Pieza:
    def __init__(self, id, name, description, type, module, enabled, requires_api, provider, params, dependencies, auth_required, api_key_field, metadata, timeout, retry, tags, status, depends_on):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.module = module
        self.enabled = enabled
        self.requires_api = requires_api
        self.provider = provider
        self.params = params
        self.dependencies = dependencies  # Campo adicional si se necesita
        self.auth_required = auth_required
        self.api_key_field = api_key_field
        self.metadata = metadata
        self.timeout = timeout
        self.retry = retry
        self.tags = tags
        self.status = status
        self.depends_on = depends_on

    def ejecutar(self, context):
        if not self.enabled:
            log_message(f"[{self.name}] No está habilitada. Saltando ejecución.")
            return False

        log_message(f"[{self.name}] Iniciando ejecución...")
        attempts = self.retry.get("max_attempts", 1) if self.retry else 1
        delay = self.retry.get("delay", 0) if self.retry else 0

        for attempt in range(1, attempts + 1):
            try:
                # Importar dinámicamente el módulo de la pieza
                mod = importlib.import_module(f"modules.{self.module}")
                # Se espera que cada módulo tenga una función run(params, context)
                mod.run(self.params, context)
                self.status = "completed"
                log_message(f"[{self.name}] Ejecutado con éxito en el intento {attempt}.")
                return True
            except Exception as e:
                log_message(f"[{self.name}] Error en intento {attempt}: {e}")
                if attempt < attempts:
                    log_message(f"[{self.name}] Reintentando en {delay} segundos...")
                    time.sleep(delay)
                else:
                    self.status = "failed"
                    log_message(f"[{self.name}] Falló después de {attempts} intentos.")
                    return False

def cargar_escenarios():
    if not os.path.exists(MESA_JSON):
        return []
    with open(MESA_JSON, "r") as f:
        return json.load(f)

def guardar_escenarios(escenarios):
    with open(MESA_JSON, "w") as f:
        json.dump(escenarios, f, indent=4)

def ejecutar_escenario(escenario_name):
    escenarios = cargar_escenarios()
    escenario = None
    for esc in escenarios:
        if esc.get("name") == escenario_name:
            escenario = esc
            break
    if not escenario:
        log_message(f"Escenario '{escenario_name}' no encontrado.")
        return

    # Crear un diccionario de piezas para acceso rápido
    piezas_dict = {p["id"]: p for p in escenario["piezas"]}
    context = {}  # Contexto compartido entre piezas (puede almacenar resultados intermedios)
    executed_ids = set()
    pending = True

    log_message(f"=== Iniciando ejecución del escenario '{escenario_name}' ===")

    # Se ejecutan las piezas mientras haya progreso
    while pending:
        progress = False
        for pid, pieza_data in piezas_dict.items():
            if pieza_data["status"] != "pending":
                continue
            # Verificar dependencias: se requiere que todos los IDs en depends_on estén en executed_ids
            if all(dep in executed_ids for dep in pieza_data.get("depends_on", [])):
                log_message(f"Ejecutando pieza ID {pid}: {pieza_data['name']}")
                # Convertir el diccionario en objeto Pieza
                pieza = Pieza(
                    id=pieza_data.get("id"),
                    name=pieza_data.get("name"),
                    description=pieza_data.get("description"),
                    type=pieza_data.get("type"),
                    module=pieza_data.get("module"),
                    enabled=pieza_data.get("enabled"),
                    requires_api=pieza_data.get("requires_api"),
                    provider=pieza_data.get("provider"),
                    params=pieza_data.get("params"),
                    dependencies=pieza_data.get("dependencies"),
                    auth_required=pieza_data.get("auth_required"),
                    api_key_field=pieza_data.get("api_key_field"),
                    metadata=pieza_data.get("metadata"),
                    timeout=pieza_data.get("timeout"),
                    retry=pieza_data.get("retry"),
                    tags=pieza_data.get("tags"),
                    status=pieza_data.get("status"),
                    depends_on=pieza_data.get("depends_on")
                )
                success = pieza.ejecutar(context)
                pieza_data["status"] = pieza.status
                if success:
                    executed_ids.add(pieza.id)
                progress = True
        if not progress:
            pending = False

    guardar_escenarios(escenarios)
    log_message("=== Ejecución del escenario completada ===")
