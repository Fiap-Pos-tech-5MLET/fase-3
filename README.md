# 🏥 Modelo de Classificação de Risco Diabético

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-FF4B4B.svg)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.0.5-orange.svg)](https://xgboost.readthedocs.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7.2-F7931E.svg)](https://scikit-learn.org/)

## 📋 Sobre o Projeto

Este projeto implementa um modelo de Machine Learning para classificação de risco diabético, capaz de prever se uma pessoa é **Diabética**, **Não-Diabética** ou **Pré-Diabética** com base em métricas de saúde e exames laboratoriais.

O projeto foi desenvolvido como parte da **Fase 3** do curso de **Pós-Tech em Machine Learning Engineering** da **FIAP**.

### 🎯 Objetivo

Desenvolver uma aplicação web interativa que auxilie profissionais de saúde na avaliação rápida do risco diabético de pacientes, utilizando técnicas avançadas de Machine Learning.

## 🚀 Funcionalidades

- ✅ Predição de risco diabético em três categorias
- ✅ Interface web intuitiva desenvolvida com Streamlit
- ✅ Conversão automática de unidades (mg/dL para SI)
- ✅ Pipeline completo de pré-processamento e predição
- ✅ Modelo treinado com XGBoost otimizado
- ✅ Transformações logarítmicas para normalização de dados

## 📊 Dataset

O modelo foi treinado com o **Dataset of Diabetes**, que contém informações sobre:

- **Variáveis demográficas**: Gênero, Idade
- **Exames laboratoriais**: Ureia, Creatinina, Colesterol, Triglicerídeos, HDL, LDL, VLDL
- **Métricas físicas**: IMC (Índice de Massa Corporal)
- **Variável alvo**: Classificação em Diabético (Y), Não-Diabético (N) ou Pré-Diabético (P)

## 🛠️ Tecnologias Utilizadas

### Machine Learning & Data Science
- **XGBoost**: Modelo de classificação principal
- **scikit-learn**: Pipeline, preprocessamento e métricas
- **Pandas & NumPy**: Manipulação e análise de dados
- **Joblib**: Serialização do modelo

### Visualização & Interface
- **Streamlit**: Framework para aplicação web
- **Matplotlib & Seaborn**: Visualizações (análise exploratória)
- **Plotly**: Gráficos interativos

### Outras Bibliotecas
- **SHAP**: Interpretabilidade do modelo
- **CatBoost**: Modelo adicional testado

## 📁 Estrutura do Projeto

```
fase-3/
├── app.py                      # Aplicação Streamlit
├── treinamento_modelo.py       # Script de treinamento do modelo
├── utils.py                    # Funções auxiliares
├── pipeline_modelo.joblib      # Modelo treinado (pipeline completo)
├── requirements.txt            # Dependências do projeto
├── data/
│   └── Dataset of Diabetes.csv # Dataset original
└── README.md                   # Documentação do projeto
```

## 🔧 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/Fiap-Pos-tech-5MLET/fase-3.git
cd fase-3
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

### 1. Treinar o Modelo (Opcional)

Se desejar retreinar o modelo com novos dados ou parâmetros:

```bash
python treinamento_modelo.py
```

Este script irá:
- Carregar e preprocessar os dados
- Aplicar transformações logarítmicas
- Treinar o modelo XGBoost
- Avaliar métricas de performance
- Salvar o pipeline completo em `pipeline_modelo.joblib`

### 2. Executar a Aplicação Web

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador (geralmente em `http://localhost:8501`).

### 3. Realizar Predições

Na interface web:

1. Selecione o **gênero** do paciente
2. Insira a **idade**
3. Preencha os valores dos **exames laboratoriais** (em mg/dL):
   - Ureia
   - Creatinina
   - Colesterol Total
   - Triglicerídeos
   - HDL
   - LDL
   - VLDL
4. Informe o **IMC** (Índice de Massa Corporal)
5. Clique em **"Prever"**

O sistema retornará a classificação: **Diabético**, **Não-Diabético** ou **Pré-Diabético**.

## 🧠 Pipeline do Modelo

### Pré-processamento

1. **Limpeza de dados**
   - Remoção de duplicatas
   - Tratamento de valores ausentes

2. **Transformações**
   - Transformação logarítmica (log1p) para features com alta assimetria
   - Conversão de unidades (mg/dL → SI)
   - Padronização com StandardScaler

3. **Feature Engineering**
   - Seleção de features relevantes
   - Codificação de variáveis categóricas

### Modelo

- **Algoritmo**: XGBoost (Extreme Gradient Boosting)
- **Parâmetros otimizados**:
  - `n_estimators`: 150
  - `learning_rate`: 0.05
  - `max_depth`: 5
  - `objective`: multi:softprob
  - `eval_metric`: mlogloss

### Métricas de Avaliação

O modelo é avaliado utilizando:
- **Acurácia**: Proporção de predições corretas
- **Precisão**: Taxa de verdadeiros positivos
- **Recall**: Sensibilidade do modelo
- **F1-Score**: Média harmônica entre precisão e recall

## 📈 Resultados

O modelo treinado apresenta métricas robustas de classificação multiclasse, com pipeline completo incluindo:
- Normalização e padronização de dados
- Transformações logarítmicas para redução de assimetria
- Predições calibradas com probabilidades

## 🔬 Funções Auxiliares (utils.py)

### `aplicar_transformacao_log(df, colunas)`
Aplica transformação logarítmica (log1p) para normalizar distribuições assimétricas.

### `converter_mgdl_para_si(substancia, valor_mgdl)`
Converte valores de mg/dL para unidades do Sistema Internacional (SI):
- Colesterol, lipídios: mg/dL → mmol/L
- Creatinina: mg/dL → μmol/L
- Glicose: mg/dL → mmol/L
- Ureia: mg/dL → mmol/L

## 👥 Autores

Projeto desenvolvido pelos alunos do curso de Pós-Tech em Machine Learning Engineering da FIAP.

- **Repositório**: [Fiap-Pos-tech-5MLET/fase-3](https://github.com/Fiap-Pos-tech-5MLET/fase-3)

## 📝 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📧 Contato

Para dúvidas ou sugestões, entre em contato através do repositório no GitHub.

---

**Desenvolvido com ❤️ para auxiliar na prevenção e diagnóstico precoce do diabetes**
