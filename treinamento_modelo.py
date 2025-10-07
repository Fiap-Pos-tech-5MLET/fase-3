# bibliotecas padrão
import joblib
import pandas as pd
import numpy as np

from utils import aplicar_transformacao_log

from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, f1_score, recall_score, precision_score
)
from sklearn.pipeline import Pipeline

RANDOM_STATE = 2025

data_raw = pd.read_csv("data/Dataset of Diabetes.csv")

# Remove as colunas 'ID' e 'No_Pation'
data = data_raw.drop(columns=['ID', 'No_Pation'])

data.drop(columns=['CLASS'])

num_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_features = data.drop(columns=['CLASS']).select_dtypes(include=['object', 'category']).columns.tolist()

# Padronizando variavel Gender

mappig_gender = {'F': 0, 'M': 1, 'f': 0}
data['Gender'] = data['Gender'].map(mappig_gender)

# Ajustando variável resposta

mapping_class = {'Y': 0, 'N': 1, 'P': 2, 'Y ': 0, 'N ':1}
data['CLASS'] = data['CLASS'].map(mapping_class)

# Removendo duplicatas
data_without_duplicates = data.drop_duplicates().reset_index(drop=True)

"""# Pré-processamento

## Transformação logarítmica
"""
skewness = data_without_duplicates[num_features].skew()

# Selecionando colunas com skewness >= 1 ou <= -1
high_skew_columns = skewness[(skewness >= 1) | (skewness <= -1)]

# Nomes das colunas com alta skewness
skew_column_names = high_skew_columns.index.tolist()

df_log = aplicar_transformacao_log(data_without_duplicates, skew_column_names)


# Reorganizando as colunas do DataFrame para treinamento do modelo

# Identificar colunas que terminam com "_log"
cols_with_log = [col for col in df_log.columns if col.endswith('_log')]

# Obter os nomes originais (sem o sufixo "_log")
original_names_of_transformed = [col.replace('_log', '') for col in cols_with_log]

# Identificar colunas que NÃO foram transformadas (não têm versão "_log")
cols_not_transformed = [col for col in df_log[num_features].columns
                        if not col.endswith('_log') and col not in original_names_of_transformed]

final_columns = cols_not_transformed + cols_with_log + cat_features + ['CLASS']

final_columns.remove('HbA1c') # removendo feature HbA1c

"""### Dividindo entre treino, teste e validação"""

X = df_log[final_columns].drop(columns=['CLASS'])
y = df_log['CLASS']

X_train, X_test, y_train, y_test = train_test_split(
    df_log[final_columns].drop(columns=['CLASS']),
    df_log['CLASS'],
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=df_log['CLASS']
)


# efetua o treinamento do modelo e retorna o modelo treinado e as métricas de avaliação
def train_model(model, X_train, X_test, y_train, y_test):
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])

    # Treina o pipeline nos dados de treino
    pipeline.fit(X_train, y_train)

    # efetua a predição com os dados de teste
    y_pred = pipeline.predict(X_test)

    # Avaliando o modelo
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=1)

    # retorna um dict com os dados de avaliação
    print(f"Avaliação do Modelo {model}:")
    print(f"Acurácia: {accuracy:.4f}")
    print(f"Precisão: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

    return model, metrics

    
def xgboost_model_func(X_train, X_test, y_train, y_test):
    # Criando e treinando o modelo de XGBoost

    xgb_params = {
        'objective': 'multi:softprob',  # Define o problema como classificação multiclasse e retorna probabilidades.
        'n_estimators': 150,            # Um número razoável de árvores para começar.
        'learning_rate': 0.05,           # Taxa de aprendizado. Um valor mais baixo torna o modelo mais robusto.
        'max_depth': 5,                 # Profundidade máxima das árvores. Essencial para evitar overfitting em dados pequenos.
        #'subsample': 0.8,               # Usa 80% das amostras para treinar cada árvore, previne overfitting.
        #'colsample_bytree': 0.8,        # Usa 80% das features para treinar cada árvore, previne overfitting.
        'eval_metric': 'mlogloss',      # Métrica de avaliação a ser usada (multiclass logloss).
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    }


    xgb_model = XGBClassifier(**xgb_params)

    return train_model(xgb_model, X_train, X_test, y_train, y_test)


model, metrics = xgboost_model_func(X_train, X_test, y_train, y_test)

print(metrics)

# Criação do pipeline com scaler + modelo
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', model)
])

# Treina o pipeline nos dados de treino
pipeline.fit(X, y)

# Exporta o pipeline completo para arquivo
joblib.dump(pipeline, 'pipeline_modelo.joblib')

print("Modelo exportado com sucesso!")