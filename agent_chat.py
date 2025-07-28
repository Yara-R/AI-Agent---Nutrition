import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_analise_com_gpt(alimentos, tipo_refeicao, perfil, resumo_refeicoes):
    prompt = f"""
Você é um agente nutricional inteligente e responsável.

O usuário tem o seguinte perfil:
{perfil}

Histórico recente de refeições:
{resumo_refeicoes}

Nova refeição registrada: {tipo_refeicao} com {', '.join(alimentos)}.

1. Avalie se esta refeição está equilibrada considerando o que já foi ingerido hoje e ontem.
2. Alerte sobre excessos ou deficiências (carboidratos, gorduras, proteínas, fibras).
3. Sugira ajustes ou complementos saudáveis, respeitando as condições clínicas e objetivos do usuário.
Responda de forma clara, empática e objetiva.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


def responder_pergunta(pergunta, perfil):
    prompt = f"""
Você é um agente nutricional com conhecimento clínico e cultural. O usuário tem o seguinte perfil:
{perfil}

Pergunta do usuário:
\"\"\"{pergunta}\"\"\"

Forneça uma resposta empática, prática e personalizada.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
