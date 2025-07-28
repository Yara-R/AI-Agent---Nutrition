from profile_constructor import criar_ou_carregar_perfil
from recommender import analisar_refeicao, registrar_refeicao
from agent_chat import responder_pergunta

def menu():
    print("\n--- Menu Principal ---")
    print("1. Registrar refeição")
    print("2. Ver refeições anteriores")
    print("3. Fazer pergunta livre ao agente")
    print("4. Sair")
    return input("Escolha uma opção: ")

def main():
    print("👋 Bem-vindo ao Agente Nutricional!")
    
    nome = input("Digite seu nome: ").strip().lower()
    idade = input("Sua idade: ").strip()
    estado = input("Estado (UF): ").strip().lower()
    
    user_id = f"{nome}_{estado}_{idade}"
    perfil = criar_ou_carregar_perfil(user_id)

    while True:
        opcao = menu()

        if opcao == "1":
            entrada = input("Digite a refeição (ex: almoço: arroz, feijão, frango):\n")
            print("\n⏳ Analisando refeição com base no seu histórico...\n")
            resposta = analisar_refeicao(entrada, perfil, user_id)
            print(f"\n🤖 Agente: {resposta}\n")

        elif opcao == "2":
            print("\n📋 Refeições registradas:")
            registrar_refeicao(user_id, None, mostrar=True)

        elif opcao == "3":
            pergunta = input("Digite sua pergunta para o agente nutricional:\n")
            resposta = responder_pergunta(pergunta, perfil)
            print(f"\n🤖 Agente: {resposta}\n")

        elif opcao == "4":
            print("👋 Até mais!")
            break

        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
