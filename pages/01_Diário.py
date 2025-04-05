# pages/01_diario.py

import streamlit as st
import pandas as pd
from datetime import datetime
from app.analysis import analisar_resposta
from app.storage import save_response

st.title("📝 Diário emocional")
st.markdown("Responda com sinceridade. Isso é só entre você e o sistema.")

st.subheader("Checklist do seu dia")

# Checklist guiado com perguntas específicas
with st.form("diario_emocional_form"):
    melhor_momento = st.text_area(
        "1. Qual foi o melhor momento do seu dia?", height=100
    )
    desafio = st.text_area(
        "2. Qual foi o maior desafio que você enfrentou hoje?", height=100
    )
    emocoes = st.text_area("3. Como você lidou com suas emoções hoje?", height=100)
    autocuidado = st.text_area("4. Você fez algo por você hoje?", height=100)

    submit = st.form_submit_button("Analisar e registrar")

if submit:
    respostas_consolidadas = f"Melhor momento: {melhor_momento}\nDesafio: {desafio}\nEmoções: {emocoes}\nAutocuidado: {autocuidado}"

    with st.spinner("Analisando sua resposta com carinho..."):
        resultado = analisar_resposta(respostas_consolidadas)

    st.success("Análise concluída!")
    st.markdown(f"**Resultado emocional:** {resultado['emocao']}")
    st.markdown(f"**Nível de risco emocional:** {resultado['risco_emocional']}")
    st.markdown(f"**Mensagem do sistema:**\n\n{resultado['mensagem']}")

    save_response(respostas_consolidadas, resultado)
