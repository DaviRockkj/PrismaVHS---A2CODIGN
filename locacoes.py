from dados import locacoes, filmes, clientes
from clientes import listar_clientes, buscar_cliente_por_id
from filmes import listar_filmes, buscar_filme_por_id


LIMITE_FILMES_POR_CLIENTE = 3
PRAZO_MINIMO_DIAS = 1
PRAZO_MAXIMO_DIAS = 7
DESCONTO_COMBO = 0.15       # 15% quando o cliente já tem filme alugado
MULTA_FIXA_POR_DIA = 5.00   # somado a 1 diária do filme, por dia de atraso



def ler_inteiro(mensagem, erro="[ERRO] ID inválido."):
    """Lê um inteiro do teclado. Retorna None (e mostra o erro) se for inválido."""
    try:
        return int(input(mensagem))
    except ValueError:
        if erro:
            print(erro)
        return None


def gerar_id_locacao():
    if not locacoes:
        return 1
    return max(l["id"] for l in locacoes) + 1


def locacoes_ativas():
    return [l for l in locacoes if l["ativa"]]


def locacoes_ativas_do_cliente(id_cliente):
    return [l for l in locacoes_ativas() if l["cliente_id"] == id_cliente]



def calcular_valor_locacao(valor_diaria, dias, tem_locacao_ativa):
    """Retorna (total, desconto). O desconto combo vale só para quem já tem filme alugado."""
    subtotal = dias * valor_diaria
    desconto = subtotal * DESCONTO_COMBO if tem_locacao_ativa else 0.0
    return subtotal - desconto, desconto


def calcular_multa(valor_diaria, dias_atraso):
    return dias_atraso * (valor_diaria + MULTA_FIXA_POR_DIA)



def escolher_cliente():
    listar_clientes()
    id_cliente = ler_inteiro("\nDigite o ID do Cliente: ")
    if id_cliente is None:
        return None

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        print("[ERRO] Cliente não encontrado.")
    return cliente


def escolher_filme(cliente):
    """Pede o filme e valida estoque e classificação indicativa para o cliente."""
    listar_filmes(apenas_disponiveis=True)
    id_filme = ler_inteiro("\nDigite o ID do Filme desejado: ")
    if id_filme is None:
        return None

    filme = buscar_filme_por_id(id_filme)
    if not filme or filme["copias_disponiveis"] <= 0:
        print("[ERRO] Filme inexistente ou sem cópias disponíveis em estoque.")
        return None

    if cliente["idade"] < filme["classificacao"]:
        print(f"[BLOQUEADO] O cliente tem {cliente['idade']} anos e o filme "
              f"'{filme['titulo']}' tem classificação +{filme['classificacao']} anos.")
        return None

    return filme


def ler_prazo():
    dias = ler_inteiro(
        f"Quantidade de dias de locação ({PRAZO_MINIMO_DIAS} a {PRAZO_MAXIMO_DIAS}): ",
        erro="[ERRO] Informe um número válido de dias.",
    )
    if dias is None:
        return None

    if not PRAZO_MINIMO_DIAS <= dias <= PRAZO_MAXIMO_DIAS:
        print(f"[ERRO] O prazo de locação deve ser entre {PRAZO_MINIMO_DIAS} e {PRAZO_MAXIMO_DIAS} dias.")
        return None
    return dias


def registrar_locacao(cliente, filme, dias, total):
    """Cria o contrato e dá baixa de uma cópia no estoque."""
    filme["copias_disponiveis"] -= 1

    nova_locacao = {
        "id": gerar_id_locacao(),
        "cliente_id": cliente["id"],
        "cliente_nome": cliente["nome"],
        "filme_id": filme["id"],
        "filme_titulo": filme["titulo"],
        "dias": dias,
        "valor_total": total,
        "ativa": True,
    }
    locacoes.append(nova_locacao)
    return nova_locacao


def exibir_comprovante(locacao, desconto):
    print("\n[SUCESSO] Locação registrada!")
    print(f"Contrato #{locacao['id']} | Cliente: {locacao['cliente_nome']} | "
          f"Filme: {locacao['filme_titulo']} ({locacao['dias']} dia(s))")
    if desconto > 0:
        print(f"Desconto Combo ({DESCONTO_COMBO:.0%} por múltiplas locações): -R$ {desconto:.2f}")
    print(f"Valor Total: R$ {locacao['valor_total']:.2f}")


def alugar_filme():
    print("\n--- REGISTRAR NOVA LOCAÇÃO ---")
    if not clientes or not filmes:
        print("[ERRO] É necessário ter clientes e filmes cadastrados.")
        return

    cliente = escolher_cliente()
    if not cliente:
        return

    ativas_cliente = locacoes_ativas_do_cliente(cliente["id"])
    if len(ativas_cliente) >= LIMITE_FILMES_POR_CLIENTE:
        print(f"[ERRO] Limite atingido! Este cliente já possui "
              f"{LIMITE_FILMES_POR_CLIENTE} filmes alugados simultaneamente.")
        return

    filme = escolher_filme(cliente)
    if not filme:
        return

    dias = ler_prazo()
    if dias is None:
        return

    total, desconto = calcular_valor_locacao(filme["valor_diaria"], dias, bool(ativas_cliente))
    locacao = registrar_locacao(cliente, filme, dias, total)
    exibir_comprovante(locacao, desconto)


def escolher_locacao_ativa(ativas):
    for l in ativas:
        print(f"Contrato ID: {l['id']} | Cliente: {l['cliente_nome']} | "
              f"Filme: {l['filme_titulo']} | Prazo: {l['dias']} dia(s)")

    id_loc = ler_inteiro("\nDigite o ID do Contrato para devolução: ")
    if id_loc is None:
        return None

    locacao = next((l for l in ativas if l["id"] == id_loc), None)
    if not locacao:
        print("[ERRO] Contrato ativo não encontrado.")
    return locacao


def ler_dias_atraso():
    """Dias de atraso informados; entrada inválida ou negativa conta como 0 (no prazo)."""
    dias = ler_inteiro("Houve dias de atraso na entrega? (0 se no prazo): ", erro=None)
    return max(dias or 0, 0)


def devolver_filme():
    print("\n--- DEVOLUÇÃO DE FILME ---")
    ativas = locacoes_ativas()
    if not ativas:
        print("Não há locações ativas no momento.")
        return

    locacao = escolher_locacao_ativa(ativas)
    if not locacao:
        return

    filme = buscar_filme_por_id(locacao["filme_id"])
    dias_atraso = ler_dias_atraso()

    if dias_atraso > 0 and filme:
        multa = calcular_multa(filme["valor_diaria"], dias_atraso)
        locacao["valor_total"] += multa
        print(f"[AVISO] Multa por atraso ({dias_atraso} dia(s)): R$ {multa:.2f}")

    locacao["ativa"] = False
    if filme:
        filme["copias_disponiveis"] += 1

    print(f"[SUCESSO] Filme devolvido ao estoque! Valor final acertado: R$ {locacao['valor_total']:.2f}")


def relatorio_resumo():
    print("\n--- RESUMO GERAL ---")
    copias_estoque = sum(f["copias_disponiveis"] for f in filmes)
    faturamento = sum(l["valor_total"] for l in locacoes)

    print(f"Clientes Cadastrados          : {len(clientes)}")
    print(f"Títulos no Catálogo           : {len(filmes)}")
    print(f"Cópias Disponíveis na Loja    : {copias_estoque}")
    print(f"Filmes Atualmente Alugados    : {len(locacoes_ativas())}")
    print(f"Total de Locações Realizadas  : {len(locacoes)}")
    print(f"Faturamento Total Acumulado   : R$ {faturamento:.2f}")


def relatorio_clientes():
    print("\n--- RELATÓRIO DE CLIENTES ---")
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for c in clientes:
        suas = [l for l in locacoes if l["cliente_id"] == c["id"]]
        em_aberto = sum(1 for l in suas if l["ativa"])
        gasto = sum(l["valor_total"] for l in suas)
        print(f"ID: {c['id']} | {c['nome']} | {c['idade']} anos | "
              f"Locações: {len(suas)} | Em aberto: {em_aberto} | Total gasto: R$ {gasto:.2f}")


def relatorio_catalogo():
    print("\n--- RELATÓRIO DO CATÁLOGO (DISPONÍVEIS x ALUGADAS) ---")
    if not filmes:
        print("Nenhum filme cadastrado.")
        return
    for f in filmes:
        suas = [l for l in locacoes if l["filme_id"] == f["id"]]
        alugadas = sum(1 for l in suas if l["ativa"])
        print(f"ID: {f['id']} | {f['titulo']} | Disponíveis: {f['copias_disponiveis']} | "
              f"Alugadas agora: {alugadas} | Vezes alugado: {len(suas)}")


def relatorio_historico():
    print("\n--- HISTÓRICO DE LOCAÇÕES ---")
    if not locacoes:
        print("Nenhuma locação registrada ainda.")
        return
    for l in locacoes:
        status = "ALUGADO" if l["ativa"] else "DEVOLVIDO"
        print(f"#{l['id']} | {l['cliente_nome']} -> '{l['filme_titulo']}' | "
              f"{l['dias']} dia(s) | R$ {l['valor_total']:.2f} | [{status}]")


def relatorio_faturamento():
    print("\n--- FATURAMENTO ---")
    recebido = sum(l["valor_total"] for l in locacoes if not l["ativa"])
    a_receber = sum(l["valor_total"] for l in locacoes if l["ativa"])
    print(f"Já recebido (devolvidos)      : R$ {recebido:.2f}")
    print(f"Em aberto (ainda alugados)    : R$ {a_receber:.2f}")
    print(f"Faturamento total             : R$ {recebido + a_receber:.2f}")


def executar_menu(titulo, opcoes):
    """Mostra um menu e executa a ação escolhida até o usuário voltar (0).

    `opcoes` é uma lista de tuplas (texto, função); a numeração é automática.
    """
    acoes = {str(n): funcao for n, (_, funcao) in enumerate(opcoes, start=1)}

    while True:
        print(f"\n=== {titulo} ===")
        for n, (texto, _) in enumerate(opcoes, start=1):
            print(f"{n} - {texto}")
        print("0 - Voltar ao Menu Principal")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            break
        acao = acoes.get(escolha)
        if acao:
            acao()
        else:
            print("[ERRO] Opção inválida!")


def exibir_relatorios():
    executar_menu("RELATÓRIOS GERENCIAIS", [
        ("Resumo Geral", relatorio_resumo),
        ("Clientes", relatorio_clientes),
        ("Catálogo (disponíveis x alugadas)", relatorio_catalogo),
        ("Histórico de Locações", relatorio_historico),
        ("Faturamento", relatorio_faturamento),
    ])


def menu_locacoes():
    executar_menu("GERENCIAR LOCAÇÕES", [
        ("Alugar Filme", alugar_filme),
        ("Devolver Filme", devolver_filme),
    ])