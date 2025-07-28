import openai
import os
import json
from dotenv import load_dotenv

# Carrega a chave da OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Etapa 1: Identificador único ===
user_id = input("🔐 Identificador do usuário (ex: yara_sp_32): ").strip().lower()
filename = "user_profiles.json"

# === Etapa 2: Entrada descritiva ===
print("\n📝 Descreva seu estado de saúde, exames, rotina e objetivos alimentares.\n")
entrada_usuario = input("➡️ Sua descrição: ")

# === Etapa 3: Prompt enviado ao GPT ===
prompt = f"""
Você é um agente nutricional que ajuda a construir perfis de usuários com base em uma descrição livre.

A descrição do usuário é:
\"\"\"{entrada_usuario}\"\"\"

Com base nisso, crie um objeto JSON com os seguintes campos:
- idade
- peso
- altura
- sexo (se for possível inferir)
- país
- estado
- atividade_fisica (tipo e frequência)
- tipo_trabalho
- condicoes_clinicas
- exames_relevantes (insulina, colesterol, glicemia etc.)
- objetivos (como emagrecer, controlar glicemia, melhorar energia)
- sugestao_macros_diarias (proteinas, carb, gorduras em gramas)
- sugestao_vitaminas (principais vitaminas e minerais a monitorar)
- sugestoes_dinamicas (como jejum intermitente, horários de alimentação, dias de treino etc.)

Responda apenas com o JSON, sem explicações adicionais.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.5,
)

perfil_gerado = response.choices[0].message.content.strip()

# === Etapa 4: Salvar em user_profiles.json ===

# Verifica se o arquivo já existe
if os.path.exists(filename):
    with open(filename, "r") as f:
        all_profiles = json.load(f)
else:
    all_profiles = {}

# Adiciona ou atualiza o perfil do usuário
try:
    all_profiles[user_id] = json.loads(perfil_gerado)
except json.JSONDecodeError:
    print("❌ Erro: A resposta do GPT não está em formato JSON válido.")
    exit()

# Salva o arquivo com todos os perfis
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_profiles, f, indent=2, ensure_ascii=False)

print(f"\n✅ Perfil de '{user_id}' salvo/atualizado em '{filename}' com sucesso!")
