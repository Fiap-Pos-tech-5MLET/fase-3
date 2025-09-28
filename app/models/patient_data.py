from pydantic import BaseModel, Field

# A classe Pydantic define a estrutura dos dados que a API vai receber.
# Cada campo corresponde a uma feature do seu dataset.
class PatientData(BaseModel):
    Gender: int = Field(..., description="Gênero do paciente (0=Feminino, 1=Masculino)")
    AGE: int = Field(..., description="Idade do paciente em anos", ge=0, le=120)
    Urea: float = Field(..., description="Nível de ureia no sangue em mg/dL")
    Cr: float = Field(..., description="Nível de creatinina no sangue em mg/dL")
    HbA1c: float = Field(..., description="Nível de HbA1c no sangue")
    Chol: float = Field(..., description="Nível de colesterol no sangue")
    TG: float = Field(..., description="Nível de triglicerídeos no sangue")
    HDL: float = Field(..., description="Nível de colesterol HDL no sangue")
    LDL: float = Field(..., description="Nível de colesterol LDL no sangue")
    VLDL: float = Field(..., description="Nível de colesterol VLDL no sangue")
    BMI: float = Field(..., description="Índice de Massa Corporal")