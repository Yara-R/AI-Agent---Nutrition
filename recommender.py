import json
import pandas as pd
from datetime import datetime
from agent_chat import gerar_analise_com_gpt

# Carrega base de alimentos
df_alimentos = pd.read_csv("alimentos.csv")

REGISTRO_PATH = "registro_refeicoes.json"

def registrar_refeicao(user_id, entrada, mostrar=False):
    if mostrar:
        with open(REGISTRO_PATH, "r") as f:
            registros = json.load(f)
        if user_id not in registros:
            print("Nenhuma refeição registrada ainda.")
            return
        for data, refeicoes in registros[user_id].items():
            print(f"📅 {data}:")
            for tipo, itens in refeicoes.items():
                print(f"  🍽️ {tipo}: {', '.join(itens)}")
        return

    # entrada do tipo: "almoço: arroz e banana"
    tipo, alimentos_str = entrada.split(":", 1)
    tipo = tipo.strip().lower()
    alimentos = [a.strip().lower() for a in alimentos_str.split(",")]

    hoje = datetime.today().strftime("%Y-%m-%d")

    try:
        with open(REGISTRO_PATH, "r") as f:
            registros = json.load(f)
    except FileNotFoundError:
        registros = {}

    if user_id not in registros:
        registros[user_id] = {}
    if hoje not in registros[user_id]:
        registros[user_id][hoje] = {}

    registros[user_id][hoje][tipo] = alimentos

    with open(REGISTRO_PATH, "w") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)

def analisar_refeicao(entrada, perfil, user_id):
    tipo, alimentos_str = entrada.split(":", 1)
    tipo = tipo.strip().lower()
    alimentos = [a.strip().lower() for a in alimentos_str.split(",")]

    registrar_refeicao(user_id, entrada)

    # Obtém refeições anteriores
    try:
        with open(REGISTRO_PATH, "r") as f:
            registros = json.load(f)
    except FileNotFoundError:
        registros = {}

    historico_usuario = registros.get(user_id, {})

    # Extrai todas as refeições de hoje e ontem
    contexto_refeicoes = []
    for dia in sorted(historico_usuario.keys(), reverse=True)[-2:]:
        for refeicao, itens in historico_usuario[dia].items():
            contexto_refeicoes.append(f"{dia} - {refeicao}: {', '.join(itens)}")

    resumo_refeicoes = "\n".join(contexto_refeicoes)

    return gerar_analise_com_gpt(alimentos, tipo, perfil, resumo_refeicoes)
