from fastapi import APIRouter, Depends, status, Query
from typing import Optional, List, Dict
from app.auth.schemas.dependencies import get_current_user
from app.utils.audit_log import get_audit_logs

router = APIRouter(
    prefix="/api/audit", 
    tags=["Auditoria"],
    dependencies=[Depends(get_current_user)]
    )

@router.get("/audit", status_code=status.HTTP_200_OK, response_model=List[Dict])
def get_audit(
    date: Optional[str] = Query(None, description="Filtrar por data (YYYY-MM-DD)"),
    route: Optional[str] = Query(None, description="Filtrar por nome da rota, ex: /api/prediction/predict")
) -> List[Dict]:
    """
    Retorna os logs de auditoria das requisições de predição.

    É possível filtrar os logs por data e/ou nome da rota.
    
    Args:
        date (str, opcional): Filtra os logs por data de processamento.
        route (str, opcional): Filtra os logs por nome da rota.
        
    Returns:
        List[Dict]: Uma lista de logs de auditoria correspondentes aos filtros.
    """
    return get_audit_logs(date_filter=date, route_filter=route)