import numpy as np

def aplicar_transformacao_log(df, colunas):
    """
    Aplica a transformação logarítmica (log1p) a uma lista de colunas
    de um DataFrame e cria novas colunas com o sufixo '_log'.

    Args:
        df (pd.DataFrame): O DataFrame de entrada.
        colunas (list): Uma lista de nomes de colunas para transformar.

    Returns:
        pd.DataFrame: O DataFrame com as novas colunas transformadas.
    """
    df_transformado = df.copy()
    for col in colunas:
        # Verifica se a coluna existe no DataFrame
        if col in df_transformado.columns:
            df_transformado[col + '_log'] = np.log1p(df_transformado[col])
        else:
            print(f"Aviso: A coluna '{col}' não foi encontrada no DataFrame.")

    return df_transformado


def converter_mgdl_para_si(substancia, valor_mgdl):
    """
    Converte um valor de mg/dL para a unidade do Sistema Internacional (SI)
    apropriada (mmol/L ou μmol/L).

    :param substancia: A substância a ser convertida (string). Opções: 
                       'colesterol', 'tg', 'ureia', 'creatinina', 'glicose'.
    :param valor_mgdl: O valor numérico em mg/dL.
    :return: O valor convertido na unidade SI (mmol/L ou μmol/L).
    """
    
    # Fatores para converter mg/dL PARA SI (divisor)
    # Fator = Massa Molar (g/mol) * 10
    fatores_conversao = {
        # Colesterol e Lipídios (mg/dL -> mmol/L)
        'colesterol': 38.67,
        'chol': 38.67,
        'hdl': 38.67,
        'ldl': 38.67,
        'vldl': 38.67,
        'tg': 88.57,  # Triglicerídeos (TG)
        
        # Glicose (mg/dL -> mmol/L)
        'glicose': 18.0, 
        
        # Ureia (mg/dL -> mmol/L)
        'urea': 6.0,
        
        # Creatinina (mg/dL -> μmol/L) - Note a unidade final diferente!
        'creatinina': 0.0113,  # Multiplicador (inverso de 88.4) para obter μmol/L
        'cr': 0.0113  # Multiplicador (inverso de 88.4) para obter μmol/L
    }
    
    # Normaliza a entrada
    substancia = substancia.lower().strip()
    
    if substancia in fatores_conversao:
        fator = fatores_conversao[substancia]
        
        if substancia in ['creatinina', 'cr']:
            # Creatinina: mg/dL * 88.4 = μmol/L.
            # Como a Creatinina é um caso especial (mg/dL -> μmol/L), 
            # usamos o multiplicador (inverso do divisor) para ser mais preciso
            valor_si = valor_mgdl * 88.4
        else:
            # Demais substâncias: mg/dL / Fator = mmol/L
            valor_si = valor_mgdl / fator

        return round(valor_si, 2)
            
    else:
        return f"Erro: Substância '{substancia}' não reconhecida ou fator indisponível."