import streamlit as st
import pandas as pd
import joblib
import numpy as np

from utils import aplicar_transformacao_log, converter_mgdl_para_si


pipeline = joblib.load("pipeline_modelo.joblib")

st.title("Modelo de Classificação de Risco Diabético")
st.write("Este aplicativo prevê se uma pessoa é Diabética, Não-Diabética ou Pré-Diabética com base em métricas de saúde.")

def predict():
    # Carrega o modelo treinado
    print("Modelo carregado com sucesso.")

    # Create a DataFrame for the input data
    input_data = pd.DataFrame({
        'Gender': [1 if gender == 'Masculino' else 0],
        'AGE': [age],
        'Urea': [converter_mgdl_para_si('urea', urea)],
        'Cr': [converter_mgdl_para_si('cr', cr)],
        'Chol': [converter_mgdl_para_si('chol', chol)],
        'TG': [converter_mgdl_para_si('tg', tg)],
        'HDL': [converter_mgdl_para_si('hdl', hdl)],
        'LDL': [converter_mgdl_para_si('ldl', ldl)],
        'VLDL': [converter_mgdl_para_si('vldl', vldl)],
        'BMI': [bmi],
        
    })

    num_features = ['AGE', 'Urea', 'Cr', 'Chol', 'TG', 'HDL', 'LDL', 'VLDL', 'BMI']
    cat_features = ['Gender']

    df_log = aplicar_transformacao_log(input_data, ['Urea', 'Cr', 'TG', 'HDL', 'LDL', 'VLDL'])
    
    # Identificar colunas que terminam com "_log"
    cols_with_log = [col for col in df_log.columns if col.endswith('_log')]

    # Obter os nomes originais (sem o sufixo "_log")
    original_names_of_transformed = [col.replace('_log', '') for col in cols_with_log]

    # Identificar colunas que NÃO foram transformadas (não têm versão "_log")
    cols_not_transformed = [col for col in df_log[num_features].columns
                            if not col.endswith('_log') and col not in original_names_of_transformed]

    final_columns = cols_not_transformed + cols_with_log + cat_features

    df_final = df_log[final_columns]

    prediction = pipeline.predict(df_final)

    class_label = {0: 'Diabético', 1: 'Não-Diabético', 2: 'Pré-Diabético'}
    result = class_label[prediction[0]]

    st.write(f"A classe prevista é: **{result}**")

with st.form("prediction_form"):
    gender = st.selectbox("Gênero", options=["Masculino", "Feminino"])
    age = st.number_input("Idade", min_value=1, max_value=120, value=39)
    urea = st.number_input("Ureia em mg/dL", value=23.0)
    cr = st.number_input("Creatinina em mg/dL", value=1.05)
    # hba1c = st.number_input("Hemoglobina Glicada(%)", value=5.3)
    chol = st.number_input("Colesterol em mg/dL", value=184.8)
    tg = st.number_input("Triglicerídeos em mg/dL", value=115.0)
    hdl = st.number_input("HDL em mg/dL", value=62.1)
    ldl = st.number_input("LDL em mg/dL", value=99.7)
    vldl = st.number_input("VLDL em mg/dL", value=23.0)
    bmi = st.number_input("Indice de Massa Corporal (IMC)", value=24.4)

    submit = st.form_submit_button("Prever")


if submit:
    predict()
