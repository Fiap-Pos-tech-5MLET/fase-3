# ===========================
# app/main.py
# ===========================
import joblib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import login, register
from app.config import get_settings
from huggingface_hub import hf_hub_download
from contextlib import asynccontextmanager
# Importa as rotas de pacientes e auditoria
from app.routes.patiente_route import router as patient_router
from app.routes.audit_route import router as audit_router
# Carrega as configurações do projeto, incluindo as variáveis do modelo
load_dotenv()
__SETTINGS__ = get_settings()

# Variáveis globais para armazenar o modelo e o scaler
__model__ = None
scaler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de contexto para a API.
    Carrega o modelo na inicialização e pode liberar recursos no desligamento.
    """
    try:
        model_path = hf_hub_download(repo_id=__SETTINGS__.MODEL_REPO_ID, filename=__SETTINGS__.MODEL_FILENAME)
        __SETTINGS__.MODEL = joblib.load(model_path)
        print("Modelo carregado com sucesso na inicialização da API!")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        __SETTINGS__.MODEL = None
    
    # O 'yield' é crucial! Ele permite que a API inicie e comece a processar requisições.
    yield
    # O código abaixo será executado quando a API for desligada.
    print("API desligada. Recursos liberados.")


app = FastAPI(
    title=__SETTINGS__.PROJECT_NAME,
    description=(
        "Uma API para prever a probabilidade de diabetes usando um modelo de Machine Learning. \n\n"
        "## Fluxo de Autenticação e Uso da API\n\n"
        "1. Para testar rotas protegidas, se registre em `/api/register` com seu usuário e senha.\n"
        "2. Faça login em `/api/login` para obter seu token JWT de acesso.\n"
        "3. Clique em 'Authorize' no Swagger UI, insira o token no campo 'Value' e clique em 'Authorize'.\n"
        "4. Com um token válido, você poderá acessar o endpoint protegido para fazer as predições.\n"
    ),
    version="1.0.0", 
    lifespan=lifespan
)


# Configurar CORS (mantido como estava)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas de autenticação (mantido como estava)
app.include_router(login.router)
app.include_router(register.router)
app.include_router(patient_router)
app.include_router(audit_router)

@app.get("/", tags=["Home"])
async def root():
    """
    Endpoint inicial da API.
    """
    return {
        "message": "Bem-vindo à API de Predição de Diabetes!",
        "info": "Para usar a API, registre-se e faça login para obter um token JWT.",
        "documentação": "/docs"
    }
