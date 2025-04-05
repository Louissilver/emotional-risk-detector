# 🧠 Como Você Está Hoje?

Uma aplicação de autoconsciência emocional com apoio de IA, feita para te ajudar a entender melhor o seu estado emocional ao longo do tempo.

---

## ✨ Funcionalidades

- **Checklist diário guiado** com 4 perguntas específicas
- **Análise emocional por IA** com classificação de emoção e risco
- **Recomendações personalizadas** baseadas no histórico
- **Gráficos de evolução emocional** e alertas preventivos
- **Histórico completo com filtros por data e emoção**
- **Exportação de dados** em PDF, CSV e Excel

---

## 📋 Perguntas do diário

1. Qual foi o melhor momento do seu dia?
2. Qual foi o maior desafio que você enfrentou hoje?
3. Como você lidou com suas emoções hoje?
4. Você fez algo por você hoje?

---

## 🧠 Como a IA ajuda?

- Classifica emoções predominantes
- Calcula nível de risco emocional com base em similaridade semântica
- Gera mensagens acolhedoras
- Produz recomendações personalizadas com base no padrão emocional

---

## 🛠️ Como rodar localmente

```bash
# Clone o repositório
https://github.com/seu-usuario/burnout-detector.git
cd burnout-detector

# Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Configure a chave da OpenAI (opcional, mas recomendado)
cp .env.example .env
# edite o .env com sua chave OPENAI_API_KEY

# Rode a aplicação
streamlit run main.py
```

---

## 📂 Estrutura do projeto

```
.
├── app/                # Lógica de IA e armazenamento
├── data/               # Respostas e recomendações salvas
├── pages/              # Páginas do app (diário, evolução, histórico, recomendações)
├── main.py             # Página inicial
├── requirements.txt    # Dependências do projeto
```

---

## 📦 Dependências principais

- `streamlit`
- `openai`
- `transformers`
- `sentence-transformers`
- `matplotlib`
- `pandas`
- `reportlab`
- `python-dotenv`

---

## 🧪 Sugestões de evolução futura

- Personalizar perguntas por tipo de dia (trabalho, pessoal, fim de semana)
- Adicionar login e histórico por usuário
- Criar dashboard analítico por semana/mês
- Sincronizar com Google Calendar para lembretes diários

---

## 🧡 Licença

Este projeto foi feito com carinho para promover saúde emocional e bem-estar.
Use, compartilhe e melhore como quiser 💙

> Feito com ❤️ e inteligência artificial ✨
