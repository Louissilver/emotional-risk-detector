# pages/04_recomendacoes.py

import streamlit as st
import pandas as pd
from app.analysis import gerar_recomendacao_personalizada
from app.storage import salvar_recomendacao
from app.utils import gerar_pdf_recomendacao
import os

st.title("🧭 Recomendação personalizada com IA")

try:
    df = pd.read_csv("data/responses.csv")

    if len(df) >= 3:
        if st.button("✨ Gerar recomendação agora"):
            with st.spinner("Analisando seu histórico emocional..."):
                texto = gerar_recomendacao_personalizada(df)

                emocao_freq = df["emotion"].value_counts().idxmax()
                risco_freq = df["risco_emocional"].value_counts().idxmax()

                salvar_recomendacao(texto, emocao_freq, risco_freq)

                st.success("Recomendação gerada e salva com sucesso!")
                st.markdown(f"> {texto}")

                pdf_buffer = gerar_pdf_recomendacao(texto, emocao_freq, risco_freq)
                st.download_button(
                    label="📄 Baixar recomendação em PDF",
                    data=pdf_buffer,
                    file_name="recomendacao_burnout.pdf",
                    mime="application/pdf",
                )
    else:
        st.info(
            "Adicione pelo menos 3 registros para gerar uma recomendação significativa."
        )

    st.divider()
    st.subheader("📜 Histórico de recomendações")
    rec_path = "data/recommendations.csv"
    if not st.session_state.get("recs_loaded"):
        st.session_state.recs_loaded = os.path.exists(rec_path)

    if st.session_state.recs_loaded:
        recs = pd.read_csv(rec_path)
        recs["timestamp"] = pd.to_datetime(recs["timestamp"])

        for _, row in recs.sort_values("timestamp", ascending=False).iterrows():
            st.markdown(f"**🗓️ Data:** {row['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown(
                f"**🧠 Emoção:** {row['emocao_frequente']} | **🔥 Risco:** {row['risco_frequente']}"
            )
            st.markdown(f"**💬 Recomendação:** {row['mensagem']}")
            st.markdown("---")
    else:
        st.info("Nenhuma recomendação gerada ainda.")

except Exception as e:
    st.error("Erro ao gerar ou carregar recomendações.")
    st.text(str(e))
