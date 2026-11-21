from dados import clientes

def gerar_id_cliente():
    if not clientes:
        return 1
    return max(c["id"] for c in clientes) + 1

def buscar_cliente_por_id(id_cliente):
    for c in clientes:
        if c["id"] == id_cliente:
            return c
    return None

def cadastrar_cliente():
    print("\n--- CADASTRAR NOVO CLIENTE ---")
    nome = input("Nome completo: ").strip()
    if not nome:
        print("[ERRO] O nome não pode ficar em branco.")
        return

    cpf = input("CPF (apenas 11 números): ").strip()
    if not cpf.isdigit() or len(cpf) != 11:
        print("[ERRO] CPF inválido! Digite exatamente 11 dígitos numéricos.")
        return

    # Regra de negócio: impedir CPF duplicado
    for c in clientes:
        if c["cpf"] == cpf:
            print("[ERRO] Já existe um cliente cadastrado com este CPF.")
            return

    try:
        idade = int(input("Idade do cliente: "))
        if idade < 10 or idade > 120:
            print("[ERRO] Idade inválida para cadastro (mínimo 10 anos).")
            return
    except ValueError:
        print("[ERRO] A idade deve ser um número inteiro.")
        return

    telefone = input("Telefone com DDD: ").strip()

    novo_cliente = {
        "id": gerar_id_cliente(),
        "nome": nome,
        "cpf": cpf,
        "idade": idade,
        "telefone": telefone
    }
    clientes.append(novo_cliente)
    print(f"[SUCESSO] Cliente '{nome}' cadastrado com ID {novo_cliente['id']}!")

def listar_clientes():
    print("\n--- LISTA DE CLIENTES ---")
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for c in clientes:
        print(f"ID: {c['id']} | Nome: {c['nome']} | CPF: {c['cpf']} | Idade: {c['idade']} anos | Tel: {c['telefone']}")

def alterar_cliente():
    listar_clientes()
    if not clientes:
        return
    try:
        id_busca = int(input("\nDigite o ID do cliente que deseja alterar: "))
    except ValueError:
        print("[ERRO] Digite um ID numérico válido.")
        return

    cliente = buscar_cliente_por_id(id_busca)
    if not cliente:
        print("[ERRO] Cliente não encontrado.")
        return

    print(f"Editando: {cliente['nome']} (Pressione ENTER para manter o valor atual)")
    novo_nome = input(f"Novo nome [{cliente['nome']}]: ").strip()
    novo_tel = input(f"Novo telefone [{cliente['telefone']}]: ").strip()

    if novo_nome:
        cliente["nome"] = novo_nome
    if novo_tel:
        cliente["telefone"] = novo_tel

    print("[SUCESSO] Dados do cliente atualizados!")

def excluir_cliente(locacoes):
    listar_clientes()
    if not clientes:
        return
    try:
        id_busca = int(input("\nDigite o ID do cliente que deseja excluir: "))
    except ValueError:
        print("[ERRO] Digite um ID numérico válido.")
        return

    cliente = buscar_cliente_por_id(id_busca)
    if not cliente:
        print("[ERRO] Cliente não encontrado.")
        return

    # Regra de negócio: impedir exclusão de cliente com filme pendente de devolução
    for loc in locacoes:
        if loc["cliente_id"] == id_busca and loc["ativa"]:
            print("[ERRO] Este cliente possui filmes alugados em aberto e não pode ser excluído.")
            return

    clientes.remove(cliente)
    print(f"[SUCESSO] Cliente '{cliente['nome']}' removido com sucesso.")

def menu_clientes(locacoes):
    while True:
        print("\n=== GERENCIAR CLIENTES ===")
        print("1 - Cadastrar Cliente")
        print("2 - Consultar Clientes")
        print("3 - Alterar Cliente")
        print("4 - Excluir Cliente")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            alterar_cliente()
        elif opcao == "4":
            excluir_cliente(locacoes)
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida!")