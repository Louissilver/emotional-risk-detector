# app/storage.py

import pandas as pd
import os
from datetime import datetime

RECOMMENDATIONS_PATH = "data/recommendations.csv"


RESPONSES_PATH = "data/responses.csv"


def save_response(user_input: str, result: dict):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    new_row = {
        "timestamp": timestamp,
        "input": user_input,
        "emotion": result["emocao"],
        "risco_emocional": result["risco_emocional"],
        "message": result["mensagem"],
        "similarity_score": result["similaridade_score"],
    }

    # Verifica se o arquivo existe e está vazio
    file_exists = os.path.exists(RESPONSES_PATH)
    file_empty = file_exists and os.stat(RESPONSES_PATH).st_size == 0

    if not file_exists or file_empty:
        df = pd.DataFrame([new_row])
    else:
        df = pd.read_csv(RESPONSES_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(RESPONSES_PATH, index=False)


def salvar_recomendacao(texto: str, emocao: str, risco: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    nova = {
        "timestamp": timestamp,
        "emocao_frequente": emocao,
        "risco_frequente": risco,
        "mensagem": texto,
    }

    if not os.path.exists(RECOMMENDATIONS_PATH):
        df = pd.DataFrame([nova])
    else:
        df = pd.read_csv(RECOMMENDATIONS_PATH)
        df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)

    df.to_csv(RECOMMENDATIONS_PATH, index=False)
