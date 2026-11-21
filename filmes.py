from dados import filmes

def gerar_id_filme():
    if not filmes:
        return 1
    return max(f["id"] for f in filmes) + 1

def buscar_filme_por_id(id_filme):
    for f in filmes:
        if f["id"] == id_filme:
            return f
    return None

def cadastrar_filme():
    print("\n--- CADASTRAR NOVO FILME ---")
    titulo = input("Título do filme: ").strip()
    if not titulo:
        print("[ERRO] O título não pode ficar em branco.")
        return

    # Regra de negócio: evitar duplicidade exata de título
    for f in filmes:
        if f["titulo"].lower() == titulo.lower():
            print("[ERRO] Este filme já está cadastrado no catálogo.")
            return

    genero = input("Gênero (ex: Ação, Comédia, Drama, Animação): ").strip()
    if not genero:
        genero = "Geral"

    try:
        classificacao = int(input("Classificação indicativa (0 para Livre, 10, 12, 14, 16 ou 18): "))
        if classificacao not in [0, 10, 12, 14, 16, 18]:
            print("[ERRO] Classificação inválida! Use 0 (Livre), 10, 12, 14, 16 ou 18.")
            return

        valor_diaria = float(input("Valor da diária (R$): ").replace(",", "."))
        if valor_diaria <= 0:
            print("[ERRO] O valor da diária deve ser maior que zero.")
            return

        copias = int(input("Quantidade de cópias em estoque: "))
        if copias < 1:
            print("[ERRO] É necessário cadastrar pelo menos 1 cópia.")
            return
    except ValueError:
        print("[ERRO] Classificação, diária e cópias devem ser números válidos.")
        return

    novo_filme = {
        "id": gerar_id_filme(),
        "titulo": titulo,
        "genero": genero,
        "classificacao": classificacao,
        "valor_diaria": valor_diaria,
        "copias_disponiveis": copias
    }
    filmes.append(novo_filme)
    print(f"[SUCESSO] Filme '{titulo}' cadastrado com ID {novo_filme['id']}!")

def listar_filmes(apenas_disponiveis=False):
    titulo_lista = "FILMES DISPONÍVEIS PARA LOCAÇÃO" if apenas_disponiveis else "CATÁLOGO COMPLETO DE FILMES"
    print(f"\n--- {titulo_lista} ---")
    encontrou = False
    for f in filmes:
        if apenas_disponiveis and f["copias_disponiveis"] <= 0:
            continue
        faixa = "Livre" if f["classificacao"] == 0 else f"+{f['classificacao']} anos"
        print(f"ID: {f['id']} | {f['titulo']} [{f['genero']}] | Classif.: {faixa} | Diária: R$ {f['valor_diaria']:.2f} | Disponíveis: {f['copias_disponiveis']}")
        encontrou = True
    if not encontrou:
        print("Nenhum filme encontrado.")

def alterar_filme():
    listar_filmes()
    if not filmes:
        return
    try:
        id_busca = int(input("\nDigite o ID do filme que deseja alterar: "))
    except ValueError:
        print("[ERRO] Digite um ID numérico válido.")
        return

    filme = buscar_filme_por_id(id_busca)
    if not filme:
        print("[ERRO] Filme não encontrado.")
        return

    print(f"Editando: {filme['titulo']} (ENTER para manter o valor atual)")
    novo_titulo = input(f"Novo título [{filme['titulo']}]: ").strip()
    nova_diaria = input(f"Nova diária R$ [{filme['valor_diaria']:.2f}]: ").strip().replace(",", ".")
    novas_copias = input(f"Nova qtd de cópias [{filme['copias_disponiveis']}]: ").strip()

    if novo_titulo:
        filme["titulo"] = novo_titulo
    if nova_diaria:
        try:
            val = float(nova_diaria)
            if val > 0:
                filme["valor_diaria"] = val
        except ValueError:
            print("[AVISO] Diária inválida, mantido valor anterior.")
    if novas_copias:
        try:
            qtd = int(novas_copias)
            if qtd >= 0:
                filme["copias_disponiveis"] = qtd
        except ValueError:
            print("[AVISO] Quantidade inválida, mantido valor anterior.")

    print("[SUCESSO] Dados do filme atualizados!")

def excluir_filme(locacoes):
    listar_filmes()
    if not filmes:
        return
    try:
        id_busca = int(input("\nDigite o ID do filme que deseja excluir: "))
    except ValueError:
        print("[ERRO] Digite um ID numérico válido.")
        return

    filme = buscar_filme_por_id(id_busca)
    if not filme:
        print("[ERRO] Filme não encontrado.")
        return

    # Regra de negócio: impedir exclusão se houver cópia alugada no momento
    for loc in locacoes:
        if loc["filme_id"] == id_busca and loc["ativa"]:
            print("[ERRO] Não é possível excluir este filme pois há cópias alugadas no momento.")
            return

    filmes.remove(filme)
    print(f"[SUCESSO] Filme '{filme['titulo']}' removido do catálogo.")

def menu_filmes(locacoes):
    while True:
        print("\n=== GERENCIAR FILMES ===")
        print("1 - Cadastrar Filme")
        print("2 - Consultar Catálogo")
        print("3 - Alterar Filme")
        print("4 - Excluir Filme")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_filme()
        elif opcao == "2":
            listar_filmes()
        elif opcao == "3":
            alterar_filme()
        elif opcao == "4":
            excluir_filme(locacoes)
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida!")