# app/analysis.py

from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Carrega classificador emocional (HuggingFace)
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,  # substitui return_all_scores=True
)

# Carrega modelo de embeddings (p/ burnout similarity)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Sintomas clássicos de burnout como referência
SINTOMAS_BURNOUT = [
    "me sinto emocionalmente esgotado",
    "não tenho motivação para trabalhar",
    "estou constantemente cansado",
    "não vejo sentido no que faço",
    "minha produtividade caiu",
    "tenho dificuldade de concentração",
    "me sinto distante das pessoas",
]

# Pré-vetorização dos sintomas
SINTOMAS_EMBED = embedding_model.encode(SINTOMAS_BURNOUT, convert_to_tensor=True)

# GPT setup (opcional - só se quiser usar agora)
openai_api_key = os.getenv("OPENAI_API_KEY")
use_gpt = openai_api_key is not None
if use_gpt:
    client = OpenAI(api_key=openai_api_key)


def classificar_emocao(texto: str) -> str:
    emotion_classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True,
    )
    resultados = emotion_classifier(texto)[0]
    resultado_principal = max(resultados, key=lambda x: x["score"])
    emocao_en = resultado_principal["label"]

    # Mapeia para português
    mapa_emocoes = {
        "joy": "alegria",
        "anger": "raiva",
        "sadness": "tristeza",
        "fear": "medo",
        "surprise": "surpresa",
        "disgust": "nojo",
        "neutral": "neutra",
    }

    return mapa_emocoes.get(emocao_en, emocao_en)


def calcular_similaridade_burnout(texto: str) -> float:
    emb_resposta = embedding_model.encode(texto, convert_to_tensor=True)
    scores = util.cos_sim(emb_resposta, SINTOMAS_EMBED)
    return scores.max().item()  # pega a maior similaridade


def gerar_mensagem_gpt(texto: str, risco: str, emocao: str) -> str:
    prompt = f"""
Você é um terapeuta virtual empático. Analise o seguinte texto e forneça uma resposta acolhedora com base no nível de risco emocional ({risco}) e na emoção predominante ({emocao}).
Texto: "{texto}"
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um terapeuta empático e cuidadoso."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


def gerar_mensagem_placeholder(emocao: str, risco: str) -> str:
    if risco == "Alto":
        return f"Sua resposta indica sinais fortes de esgotamento. Você mencionou emoções como '{emocao}'. Considere conversar com alguém de confiança ou procurar ajuda profissional."
    elif risco == "Moderado":
        return f"Você demonstrou sinais moderados de estresse, com emoções como '{emocao}'. Cuide-se bem e não ignore os sinais."
    else:
        return f"Tudo parece sob controle no momento. Emoções como '{emocao}' são normais. Continue se observando com carinho!"


def analisar_resposta(resposta: str) -> dict:
    emocao = classificar_emocao(resposta)
    similaridade = calcular_similaridade_burnout(resposta)

    if similaridade > 0.65:
        risco = "Alto"
    elif similaridade > 0.45:
        risco = "Moderado"
    else:
        risco = "Baixo"

    if use_gpt:
        mensagem = gerar_mensagem_gpt(resposta, risco, emocao)
    else:
        mensagem = gerar_mensagem_placeholder(emocao, risco)

    return {
        "emocao": emocao,
        "risco_emocional": risco,
        "mensagem": mensagem,
        "similaridade_score": round(similaridade, 2),
    }


def gerar_recomendacao_personalizada(df):
    # Emoções mais comuns
    emocao_freq = df["emotion"].value_counts().idxmax()
    risco_freq = df["risco_emocional"].value_counts().idxmax()
    ultimas_respostas = df.tail(3)["input"].tolist()

    prompt = f"""
Você é um assistente empático especializado em saúde mental.

Com base nos dados abaixo, gere uma recomendação personalizada e encorajadora para o usuário. Use uma linguagem acolhedora, direta e focada em equilíbrio emocional:

- Emoção mais frequente: {emocao_freq}
- Nível de burnout mais recorrente: {risco_freq}
- Últimas respostas do usuário:
{chr(10).join(f"- {resp}" for resp in ultimas_respostas)}

Evite repetir informações já ditas, e traga sugestões práticas com leveza.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um terapeuta empático e cuidadoso."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=400,
    )

    return response.choices[0].message.content.strip()
