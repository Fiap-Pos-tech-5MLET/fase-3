import os
import json
from typing import Dict, List, Optional
import uuid
from datetime import datetime

# Definindo o caminho do diretório de auditoria
AUDIT_LOG_DIR = "data/audit"
AUDIT_LOG_FILE = os.path.join(AUDIT_LOG_DIR, "predictions.json")

def setup_audit_directory():
    """Garante que o diretório de auditoria exista."""
    os.makedirs(AUDIT_LOG_DIR, exist_ok=True)

def audit_prediction(
    input_data: dict,
    output_data: dict,
    route_name: str
):
    """
    Registra uma auditoria da requisição de predição.

    Args:
        input_data (dict): Os dados de entrada da requisição.
        output_data (dict): Os dados de saída da predição.
        route_name (str): O nome da rota que processou a requisição.
    """
    setup_audit_directory()
    
    # Gera um ID único e a data de processamento
    request_id = str(uuid.uuid4())
    processing_date = datetime.now().isoformat()
    
    # Estrutura o log da requisição
    log_entry = {
        "request_id": request_id,
        "route": route_name,
        "processing_date": processing_date,
        "input": input_data,
        "output": output_data
    }
    
    # Salva o log em um arquivo JSON
    with open(AUDIT_LOG_FILE, "a") as f:
        json.dump(log_entry, f)
        f.write("\n") # Adiciona uma nova linha para cada entrada

def get_audit_logs(date_filter: Optional[str] = None, route_filter: Optional[str] = None) -> List[Dict]:
    """
    Lê o arquivo de logs e retorna as entradas filtradas.
    
    Args:
        date_filter (str, opcional): Data no formato YYYY-MM-DD para filtrar logs.
        route_filter (str, opcional): Nome da rota para filtrar logs.

    Returns:
        List[Dict]: Uma lista de dicionários com os logs filtrados.
    """
    if not os.path.exists(AUDIT_LOG_FILE):
        return []

    filtered_logs = []
    try:
        with open(AUDIT_LOG_FILE, "r") as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    
                    # Filtro por data
                    date_match = True
                    if date_filter:
                        log_date = log_entry.get("processing_date", "")[:10]
                        if log_date != date_filter:
                            date_match = False
                    
                    # Filtro por nome da rota
                    route_match = True
                    if route_filter:
                        if log_entry.get("route", "") != route_filter:
                            route_match = False
                    
                    if date_match and route_match:
                        filtered_logs.append(log_entry)
                except json.JSONDecodeError:
                    continue  # Ignora linhas mal formatadas
    except IOError as e:
        print(f"Erro ao ler o arquivo de auditoria: {e}")
        return []
    
    return filtered_logs

# --- NOVO: Função para buscar log por ID ---
def get_audit_log_by_id(request_id: str) -> Optional[Dict]:
    """
    Busca um log de auditoria específico pelo seu ID de requisição.

    Args:
        request_id (str): O ID único da requisição.

    Returns:
        Optional[Dict]: O log da requisição se encontrado, caso contrário, None.
    """
    if not os.path.exists(AUDIT_LOG_FILE):
        return None
    
    try:
        with open(AUDIT_LOG_FILE, "r") as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    if log_entry.get("request_id") == request_id:
                        return log_entry
                except json.JSONDecodeError:
                    continue
    except IOError as e:
        print(f"Erro ao ler o arquivo de auditoria: {e}")
        return None
    
    return None