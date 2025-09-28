import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from typing import Optional, List, Dict

from app.models.patient_data import PatientData
from app.config import get_settings
from app.auth.schemas.dependencies import get_current_user
from app.utils.audit_log import audit_prediction, get_audit_logs

router = APIRouter(
    prefix="/api/prediction", 
    tags=["Predição de Diabetes"],
    dependencies=[Depends(get_current_user)]
    )

__SETTINGS__ = get_settings()

@router.post("/predict", response_model=dict, status_code=status.HTTP_200_OK)
def predict_diabetes(request: Request,data: PatientData) -> dict:
    """
    Realiza a predição de diabetes com base nos dados do paciente.

    Este endpoint recebe 11 características de saúde de um paciente e utiliza
    um modelo de Machine Learning pré-treinado para classificar se o paciente
    tem um resultado "Positive" (positivo) ou "Negative" (negativo) para diabetes.

    - **Entrada:** `PatientData` (objeto JSON com 11 características de saúde).
    - **Saída:** Objeto JSON com o resultado da predição ("Positive" ou "Negative").

    Raises:
    - `HTTPException` com status 503 se o modelo não estiver disponível.
    - `HTTPException` com status 500 se ocorrer um erro interno durante a predição.

    Returns:
        dict: Um dicionário com a predição e o status da operação.
    """
    model_instance= __SETTINGS__.MODEL
    # 1. Tratamento de Erro: Modelo Não Carregado (Status 503 Service Unavailable)
    if model_instance is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="O modelo de Machine Learning não foi carregado corretamente. O serviço está indisponível."
        )

    try:
        # Prepara os dados de entrada na ordem correta (11 features)
        features = np.array([[
            data.Gender, 
            data.AGE, 
            data.Urea, 
            data.Cr, 
            data.HbA1c, 
            data.Chol, 
            data.TG, 
            data.HDL, 
            data.LDL, 
            data.VLDL, 
            data.BMI
        ]])

        # 2. Faz a predição com o modelo injetado
        prediction = model_instance.predict(features)
        
        # Converte a predição para um resultado legível
        result_text = "Positive" if prediction[0] == 1 else "Negative"
        
        # 3. Retorno de Sucesso (Status 200 OK)

        
        input_dict = data.dict()
        output_dict = {"prediction_class": result_text}
        
        # Auditoria: Passando o nome da rota dinamicamente
        audit_prediction(
            input_data=input_dict,
            output_data=output_dict,
            route_name=request.url.path
        )
        
        return {
            "prediction": result_text, 
            "status": "success",
            "message": "Predição realizada com sucesso."
        }
        
    except Exception as e:
        # Registre o erro 'e' em um log aqui (prática recomendada)
        print(f"Erro durante a predição: {e}") 
        audit_prediction(
            input_data=data.dict(),
            output_data={"error": str(e)},
            route_name=request.url.path
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor durante a predição: {str(e)}"
        )