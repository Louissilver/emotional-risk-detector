# pages/02_evolucao.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Evolução emocional")

try:
    df = pd.read_csv("data/responses.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    st.subheader("🔥 Evolução do nível de risco emocional")
    risco_map = {"Baixo": 0, "Moderado": 1, "Alto": 2}
    df["risco_emocional_level"] = df["risco_emocional"].map(risco_map)
    st.line_chart(df.set_index("timestamp")["risco_emocional_level"])
    st.caption("0 = Baixo, 1 = Moderado, 2 = Alto")

    st.subheader("😊 Emoções mais frequentes")
    df["emotion"] = df["emotion"].replace("neutral", "neutra")
    emocao_counts = df["emotion"].value_counts()

    fig, ax = plt.subplots(facecolor="#0e1117")
    ax.bar(
        emocao_counts.index,
        emocao_counts.values,
        width=0.4,
        color="#4FC3F7",
        edgecolor="white",
    )
    ax.set_facecolor("#0e1117")
    ax.tick_params(colors="white")
    ax.set_title("Distribuição das emoções detectadas", color="white")
    ax.set_xlabel("Emoções", color="white")
    ax.set_ylabel("Frequência", color="white")
    ax.set_xticks(range(len(emocao_counts.index)))
    ax.set_xticklabels(emocao_counts.index, rotation=0, color="white")
    for label in ax.get_yticklabels():
        label.set_color("white")

    st.pyplot(fig)

    st.subheader("⚠️ Monitoramento preventivo")
    df = df.sort_values("timestamp")
    df["risk_level"] = df["risco_emocional"].map(risco_map)
    df["is_high"] = df["risk_level"] == 2
    df["high_streak"] = df["is_high"].rolling(2).sum()

    if (df["high_streak"] >= 2).any():
        st.error(
            "🚨 Foram detectados 2 ou mais dias seguidos com risco ALTO de burnout."
        )

    ultimos_5 = df.tail(5)
    dias_de_risco = (ultimos_5["risk_level"] >= 1).sum()

    if dias_de_risco >= 3:
        st.warning(
            "⚠️ Nos últimos 5 dias, você teve risco Moderado ou Alto em 3 ou mais ocasiões."
        )
    elif dias_de_risco < 3 and (df["high_streak"] >= 2).any() is False:
        st.success(
            "✅ Nenhum sinal crítico detectado recentemente. Continue se cuidando!"
        )

except Exception as e:
    st.warning("Não foi possível carregar os dados.")
    st.text(f"Erro: {e}")
