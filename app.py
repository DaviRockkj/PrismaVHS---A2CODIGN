from dados import locacoes
from clientes import menu_clientes
from filmes import menu_filmes
from locacoes import menu_locacoes, exibir_relatorios

def menu_principal():
    while True:
        print("\n========================================")
        print("          PrismaVHS LOCADORA           ")
        print("       Sistema de Gerenciamento         ")
        print("========================================")
        print("MENU PRINCIPAL")
        print("1 - Gerenciar Clientes")
        print("2 - Gerenciar Filmes")
        print("3 - Locações (Alugar / Devolver)")
        print("4 - Relatórios")
        print("0 - Sair do Sistema")
        print("========================================")

        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            menu_clientes(locacoes)
        elif opcao == "2":
            menu_filmes(locacoes)
        elif opcao == "3":
            menu_locacoes()
        elif opcao == "4":
            exibir_relatorios()
        elif opcao == "0":
            print("\nEncerrando o sistema. Obrigado por utilizar a PrismaVHS Locadora!")
            break
        else:
            print("\n[ERRO] Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu_principal()