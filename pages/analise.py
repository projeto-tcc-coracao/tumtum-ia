import streamlit as st
import pickle
import numpy as np

st.markdown(f"<h1 style='color: {"#FF4B6E"}; text-align: center;'>TumTum IA</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: {"#2C3E50"}; text-align: center;'>Previsão de Risco Cardíaco</h3>", unsafe_allow_html=True)


with st.form("formulario_risco_cardiaco"):
    st.html('''<h4 style="color: #FF4B6E; text-align: left; border-bottom: 2px solid #FF4B6E; padding-bottom: 5px;">
                Dados Básicos
            </h4>''')
    col1, col2 = st.columns(2)
    with col1:
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    with col2:
        sexo = st.selectbox("Sexo", options=["Masculino", "Feminino"])
        if sexo == "Masculino":
            sexo = 1
        elif sexo == "Feminino":
            sexo = 0

    st.html('''<h4 style="color: #FF4B6E; text-align: left; border-bottom: 2px solid #FF4B6E; padding-bottom: 5px;">
                Indicadores Vitais
            </h4>''')

    col3, col4 = st.columns(2)
    with col3:
        pressao = st.number_input("Pressão Arterial (mmHg)", min_value=0, step=1)
        st.caption("Em repouso")
    with col4:
        colesterol_ldl = st.number_input("Colesterol LDL (mg/dL)", min_value=0, step=1)


    col5, col6 = st.columns(2)
    with col5:
        glicemia = st.selectbox("Glicemia em Jejum", options=["Normal (≤ 120 mg/dL)", "Elevada (> 120 mg/dL)"])
        if glicemia == "Elevada (> 120 mg/dL)":
            glicemia = 1
        elif glicemia == "Normal (≤ 120 mg/dL)":
            glicemia = 0

    with col6:
        freq_cardiaca_max = st.number_input("Frequência Cardíaca Máxima", min_value=0, step=1)

    st.html('''<h4 style="color: #FF4B6E; text-align: left; border-bottom: 2px solid #FF4B6E; padding-bottom: 5px;">
                Exame Cardíaco
            </h4>''')


    tipo_dor = st.selectbox("Tipo de Dor no Peito", options=[
    "Sem Dor", 
    "Dor no peito com aperto/pressão, que piora com esforço e melhora em repouso (Angina Típica)", 
    "Dor no Peito que não segue um padrão claro, mas pode ser difusa (Dor Não-Anginal)", 
    "Dor no peito que não está relacionada ao esforço, pode ser em outras áreas do tórax(Angina Atípica)"
    ])

    if tipo_dor == "Sem Dor":
        tipo_dor = (0, 0, 0)
    elif tipo_dor == "Dor no peito com aperto/pressão, que piora com esforço e melhora em repouso (Angina Típica)":
        tipo_dor = (1, 0, 0)
    elif tipo_dor == "Dor no Peito que não segue um padrão claro, mas pode ser difusa (Dor Não-Anginal)":
        tipo_dor = (0, 1, 0)
    elif tipo_dor == "Dor no peito que não está relacionada ao esforço, pode ser em outras áreas do tórax(Angina Atípica)":
        tipo_dor = (0, 0, 1)



    ecg_repouso = st.selectbox("ECG em Repouso", options=["Normal", "Anormalidade ST", "Hipertrofia VE"])
    if ecg_repouso == "Normal":
        ecg_repouso = (1,0)
    elif ecg_repouso == "Anormalidade ST":
        ecg_repouso = (0,1)
    elif ecg_repouso == "Hipertrofia VE":
        ecg_repouso = (0,0)

    col9, col10 = st.columns(2)
    with col9:
        angina_exercicio = st.selectbox("Angina por Exercício", options=["Não", "Sim"])
        if angina_exercicio == "Sim":
            angina_exercicio =1
        elif angina_exercicio == "Não":
            angina_exercicio = 0

    with col10:
        fluxo_sanguineo = st.number_input("Insuficiência do Fluxo Sanguíneo")

    st.html('''<h4 style="color: #FF4B6E; text-align: left; border-bottom: 2px solid #FF4B6E; padding-bottom: 5px;">
                Outros Exames
            </h4>''')


    padrao_ecg = st.selectbox("Padrão ECG", options=["Elevação Suave do Segmento ST", "Segmento ST Plano", "Depressão do Segmento ST"])
    if padrao_ecg == "Elevação Suave do Segmento ST":
        padrao_ecg = (0,1)
    elif padrao_ecg == "Segmento ST Plano":
        padrao_ecg = (1,0)
    elif padrao_ecg == "Depressão do Segmento ST":
        padrao_ecg = (0,0)


    submit_button = st.form_submit_button(label="Avaliar Risco Cardíaco")

    with open('model_LogisticRegression.pkl', 'rb') as f:
        model_LogisticRegression = pickle.load(f)

    # with open('model_GaussianNB.pkl', 'rb') as f:
    #     model_GaussianNB = pickle.load(f)

if submit_button:
    # st.write("### Dados Coletados")
    # st.write(f"Idade: {idade}")
    # st.write(f"Sexo: {sexo}")
    # st.write(f"Pressão Arterial: {pressao} mmHg")
    # st.write(f"Colesterol LDL: {colesterol_ldl} mg/dL")
    # st.write(f"Glicemia: {glicemia}")
    # st.write(f"Frequência Cardíaca Máxima: {freq_cardiaca_max}")
    # st.write(f"Tipo de Dor no Peito: {tipo_dor}")
    # st.write(f"ECG em Repouso: {ecg_repouso}")
    # st.write(f"Angina por Exercício: {angina_exercicio}")
    # st.write(f"Insuficiência do Fluxo Sanguíneo: {fluxo_sanguineo}")
    # st.write(f"Padrão ECG: {padrao_ecg}")

    input_ML = (
    idade, pressao, colesterol_ldl, glicemia, freq_cardiaca_max, fluxo_sanguineo, 
    sexo, tipo_dor[0], tipo_dor[1], tipo_dor[2], ecg_repouso[0], ecg_repouso[1], 
    angina_exercicio, padrao_ecg[0], padrao_ecg[1]
    )

    st.write(input_ML)
    ########################################################################################

  
    input_data_as_numpy_array = np.asarray(input_ML)

 
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)


    prediction = model_LogisticRegression.predict(input_data_reshaped)
    st.write(prediction)

 
    if prediction[0] == 0:
        st.write('The Person does not have a Heart Disease')

        
    else:
        st.write('The Person has Heart Disease')
