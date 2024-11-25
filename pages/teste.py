import streamlit as st
import pickle
import numpy as np

if 'mostrar_resultado' not in st.session_state:
    st.session_state.mostrar_resultado = False

def reset_form():
    st.session_state.mostrar_resultado = False


if not st.session_state.mostrar_resultado:
    st.markdown(f"<h1 style='color: #FF4B6E; text-align: center;'>TumTum IA</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #2C3E50; text-align: center;'>Previsão de Risco Cardíaco</h3>", unsafe_allow_html=True)

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
                angina_exercicio = 1
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

        if submit_button:
            input_ML = (
                idade, pressao, colesterol_ldl, glicemia, freq_cardiaca_max, fluxo_sanguineo, 
                sexo, tipo_dor[0], tipo_dor[1], tipo_dor[2], ecg_repouso[0], ecg_repouso[1], 
                angina_exercicio, padrao_ecg[0], padrao_ecg[1]
            )

            input_data_as_numpy_array = np.asarray(input_ML)
            input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
            prediction = model_LogisticRegression.predict(input_data_reshaped)


            st.session_state.prediction = prediction[0]
            st.session_state.mostrar_resultado = True

            st.rerun()


else:
    st.markdown(f"<h1 style='color: #FF4B6E; text-align: center;'>TumTum IA</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #2C3E50; text-align: center;'>Resultado da Avaliação</h3>", unsafe_allow_html=True)

    
    st.markdown("""
        <style>
        .result-container {
            padding: 2rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.prediction == 0:
        st.markdown("""
            <div style='background-color: #FFE5E5; padding: 2rem; border-radius: 10px; border: 2px solid #FF4B4B; margin: 1rem 0;'>
                <h2 style='color: #FF4B4B; text-align: center;'>⚠️ Atenção: Risco Cardíaco Identificado</h2>
                <p style='text-align: center; font-size: 1.1em;'>Nossa análise detectou potenciais indicadores de risco cardíaco.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏥 Recomendações Importantes:")
        st.markdown("""
        - **Procure um Médico Imediatamente**
        - Realize exames complementares (Ecocardiograma, Teste de Esforço)
        - Monitore sua pressão arterial regularmente
        - Faça exames de sangue para avaliar marcadores cardíacos
        - Considere mudanças no estilo de vida
        """)

        st.warning("Este resultado indica a necessidade de avaliação médica profissional o mais breve possível!")

    else:
        st.markdown("""
            <div style='background-color: #E5FFE5; padding: 2rem; border-radius: 10px; border: 2px solid #4CAF50; margin: 1rem 0;'>
                <h2 style='color: #4CAF50; text-align: center;'>✅ Resultado Favorável</h2>
                <p style='text-align: center; font-size: 1.1em;'>Não foram identificados indicadores significativos de risco cardíaco.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💚 Recomendações para Manter sua Saúde:")
        st.markdown("""
        - Mantenha uma dieta equilibrada
        - Pratique exercícios físicos regularmente
        - Faça check-ups periódicos
        - Mantenha um bom padrão de sono
        - Continue monitorando sua saúde
        """)

        st.success("Continue mantendo seus bons hábitos de saúde!")


    if st.button("Realizar Nova Análise"):
        st.session_state.mostrar_resultado = False
        st.rerun()