# pages/03_historico.py

import streamlit as st
import pandas as pd
import io
from app.utils import gerar_pdf_respostas

st.title("📘 Histórico de respostas")

try:
    df = pd.read_csv("data/responses.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    with st.expander("🔍 Filtrar histórico"):
        col1, col2, col3 = st.columns(3)
        with col1:
            data_inicial = st.date_input("De:", df["timestamp"].min().date())
        with col2:
            data_final = st.date_input("Até:", df["timestamp"].max().date())
        with col3:
            emocao_selecionada = st.selectbox(
                "Emoção:", ["Todas"] + sorted(df["emotion"].unique().tolist())
            )

    filtrado = df[
        (df["timestamp"].dt.date >= data_inicial)
        & (df["timestamp"].dt.date <= data_final)
    ]
    if emocao_selecionada != "Todas":
        filtrado = filtrado[filtrado["emotion"] == emocao_selecionada]

    if filtrado.empty:
        st.warning("Nenhuma entrada encontrada com esses filtros.")
    else:
        for _, row in filtrado.iterrows():
            with st.container():
                st.markdown(
                    f"**🗓️ Data:** {row['timestamp'].strftime('%Y-%m-%d %H:%M')}"
                )
                st.markdown(
                    f"**🧠 Emoção:** {row['emotion']} | **🔥 Nível de risco emocional:** {row['risco_emocional']}"
                )
                st.markdown(f"**✍️ Resposta:** {row['input']}")
                st.markdown(f"**💬 Mensagem do sistema:** {row['message']}")
                st.markdown("---")

    st.subheader("📥 Exportar histórico")

    # CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv_buffer.getvalue(),
        file_name="historico_emocional.csv",
        mime="text/csv",
    )

    # Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Histórico")
    excel_buffer.seek(0)

    st.download_button(
        label="⬇️ Baixar Excel (.xlsx)",
        data=excel_buffer,
        file_name="historico_emocional.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # PDF
    pdf_buffer = gerar_pdf_respostas(df)
    st.download_button(
        label="⬇️ Baixar PDF",
        data=pdf_buffer,
        file_name="historico_emocional.pdf",
        mime="application/pdf",
    )

except Exception as e:
    st.error("Erro ao carregar histórico ou exportar.")
    st.text(str(e))
