# ==============================================================
# Project: Jogo do Moinho (Nine Men’s Morris simplified 3x3)
# ==============================================================

# ==============================================================
# TAD POSITION
# ==============================================================

def create_position(c, l):
    """
    create_position: str x str -> position
    Creates a position from column (c) and row (r).
    Valid columns: 'a', 'b', 'c'
    Valid rows: '1', '2', '3'
    If the arguments are invalid, raises:
        ValueError('create_position: invalid arguments')
    """
    if c not in ('a', 'b', 'c') or l not in ('1', '2', '3'):
        raise ValueError('create_position: invalid arguments')
    return (c, l)  # internal representation: tuple (column, row)


def create_copy_position(p):
    """create_copy_position: position -> position"""
    return (p[0], p[1])


def get_pos_c(p):
    """get_pos_c: position -> str (column)"""
    return p[0]


def get_pos_l(p):
    """get_pos_l: position -> str (line)"""
    return p[1]


def eh_position(arg):
    """eh_position: universal -> boolean"""
    return (
        isinstance(arg, tuple) and
        len(arg) == 2 and
        arg[0] in ('a', 'b', 'c') and
        arg[1] in ('1', '2', '3')
    )


def eh_position(p1, p2):
    """eh_position: position x position -> boolean"""
    return eh_position(p1) and eh_position(p2) and p1 == p2


def position_for_str(p):
    """position_for_str: position -> str (ex: 'a1')"""
    return p[0] + p[1]


def get_adjacent_positions(p):
    """
    get_adjacent_positions: position -> tuple of positions
    Returns the positions adjacent to p, according to the reading order of the board.
    """
    adj = {
        ('a', '1'): [('b', '1'), ('a', '2')],
        ('b', '1'): [('a', '1'), ('c', '1'), ('b', '2')],
        ('c', '1'): [('b', '1'), ('c', '2')],
        ('a', '2'): [('a', '1'), ('b', '2'), ('a', '3')],
        ('b', '2'): [('b', '1'), ('a', '2'), ('c', '2'), ('b', '3')],
        ('c', '2'): [('c', '1'), ('b', '2'), ('c', '3')],
        ('a', '3'): [('a', '2'), ('b', '3')],
        ('b', '3'): [('b', '2'), ('a', '3'), ('c', '3')],
        ('c', '3'): [('c', '2'), ('b', '3')],
    }
    return tuple(adj[p])

# ==============================================================
# TAD PECA
# ==============================================================

def create_item(s):
    """
    create_item: str -> peca
    Creates a piece for player 'X', 'O' or free (' ').
    Internal representation: simple string ('X', 'O' or ' ').
    Throws ValueError if the argument is invalid.
    """
    if s not in ('X', 'O', ' '):
        raise ValueError('create_item: invalid argument')
    return s


def create_copy_part(j):
    """create_copy_part: part -> part"""
    return j


def eh_peca(arg):
    """eh_peca: universal -> booleano"""
    return arg in ('X', 'O', ' ')


def pecas_iguais(j1, j2):
    """pecas_iguais: peca x peca -> booleano"""
    return eh_peca(j1) and eh_peca(j2) and j1 == j2


def peca_para_str(j):
    """peca_para_str: peca -> str ('[X]', '[O]', '[ ]')"""
    return f"[{j}]"


def peca_para_inteiro(j):
    """
    peca_para_inteiro: peca -> int
    Devolve 1 se for 'X', -1 se for 'O', 0 se for livre.
    """
    if j == 'X':
        return 1
    if j == 'O':
        return -1
    return 0

# ==============================================================
# TAD TABULEIRO
# ==============================================================

def cria_tabuleiro():
    """
    cria_tabuleiro: {} -> tabuleiro
    Cria um tabuleiro vazio 3x3 (todas as posicoes livres).
    Representacao interna: dicionario {posicao_str: peca}
    """
    posicoes = [c + l for l in ('1', '2', '3') for c in ('a', 'b', 'c')]
    return {p: ' ' for p in posicoes}


def cria_copia_tabuleiro(t):
    """cria_copia_tabuleiro: tabuleiro -> tabuleiro"""
    return dict(t)


def obter_peca(t, p):
    """obter_peca: tabuleiro x posicao -> peca"""
    return t[position_for_str(p)]


def obter_vetor(t, s):
    """
    obter_vetor: tabuleiro x str -> tuplo de pecas
    Se s for coluna ('a','b','c'), devolve a coluna.
    Se s for linha ('1','2','3'), devolve a linha.
    """
    if s in ('a', 'b', 'c'):  # coluna
        return tuple(t[s + l] for l in ('1', '2', '3'))
    elif s in ('1', '2', '3'):  # linha
        return tuple(t[c + s] for c in ('a', 'b', 'c'))
    else:
        raise ValueError("obter_vetor: argumento invalido")


def coloca_peca(t, j, p):
    """coloca_peca: tabuleiro x peca x posicao -> tabuleiro"""
    t[position_for_str(p)] = j
    return t


def remove_peca(t, p):
    """remove_peca: tabuleiro x posicao -> tabuleiro"""
    t[position_for_str(p)] = ' '
    return t


def move_peca(t, p1, p2):
    """move_peca: tabuleiro x posicao x posicao -> tabuleiro"""
    j = t[position_for_str(p1)]
    t[position_for_str(p1)] = ' '
    t[position_for_str(p2)] = j
    return t


def eh_tabuleiro(arg):
    """
    eh_tabuleiro: universal -> booleano
    Um tabuleiro valido:
    - Tem todas as posicoes de 'a1'..'c3'
    - Cada posicao tem peca valida
    - Maximo 3 pecas de cada jogador
    - A diferenca de pecas entre jogadores <= 1
    - Nao pode haver dois ganhadores em simultaneo
    """
    if not isinstance(arg, dict):
        return False

    posicoes = [c + l for l in ('1', '2', '3') for c in ('a', 'b', 'c')]
    if set(arg.keys()) != set(posicoes):
        return False

    if not all(eh_peca(v) for v in arg.values()):
        return False

    nX = sum(1 for v in arg.values() if v == 'X')
    nO = sum(1 for v in arg.values() if v == 'O')

    if nX > 3 or nO > 3:
        return False
    if abs(nX - nO) > 1:
        return False

    g = obter_ganhador(arg)
    if g != ' ':
        copia = dict(arg)
        copia_ganhador = g
        # Verificar se o outro jogador tambem ganhou
        copia_g = 'X' if g == 'O' else 'O'
        copia_res = obter_ganhador({k: (copia_g if v == copia_g else ' ') for k, v in arg.items()})
        if copia_res != ' ':
            return False

    return True


def eh_position_livre(t, p):
    """eh_position_livre: tabuleiro x posicao -> booleano"""
    return t[position_for_str(p)] == ' '


def tabuleiros_iguais(t1, t2):
    """tabuleiros_iguais: tabuleiro x tabuleiro -> booleano"""
    return t1 == t2


def tabuleiro_para_str(t):
    """
    tabuleiro_para_str: tabuleiro -> str
    Devolve uma string formatada com o tabuleiro.
    """
    def linha(n):
        return " " + str(n) + " " + "-".join(peca_para_str(t[c + str(n)]) for c in ('a', 'b', 'c'))

    s = "   a   b   c\n"
    s += linha(1) + "\n   | \\ | / |\n"
    s += linha(2) + "\n   | / | \\ |\n"
    s += linha(3)
    return s


def tuplo_para_tabuleiro(tuplo):
    """
    tuplo_para_tabuleiro: tuplo -> tabuleiro
    Tuplo com 3 tuplos, cada um com valores (1, -1, 0).
    1 -> 'X', -1 -> 'O', 0 -> ' '.
    """
    tab = cria_tabuleiro()
    linhas = ('1', '2', '3')
    colunas = ('a', 'b', 'c')
    for i, l in enumerate(linhas):
        for j, c in enumerate(colunas):
            if tuplo[i][j] == 1:
                tab[c + l] = 'X'
            elif tuplo[i][j] == -1:
                tab[c + l] = 'O'
            else:
                tab[c + l] = ' '
    return tab


def obter_ganhador(t):
    """
    obter_ganhador: tabuleiro -> peca
    Devolve 'X' ou 'O' se houver 3 em linha horizontal ou vertical.
    Caso contrario devolve ' '.
    """
    linhas = [('a1','b1','c1'), ('a2','b2','c2'), ('a3','b3','c3')]
    colunas = [('a1','a2','a3'), ('b1','b2','b3'), ('c1','c2','c3')]

    for grupo in linhas + colunas:
        pecas = [t[p] for p in grupo]
        if pecas[0] != ' ' and all(p == pecas[0] for p in pecas):
            return pecas[0]
    return ' '


def obter_posicoes_livres(t):
    """obter_posicoes_livres: tabuleiro -> tuplo de posicoes"""
    return tuple(create_position(p[0], p[1]) for p, j in t.items() if j == ' ')


def obter_posicoes_jogador(t, j):
    """obter_posicoes_jogador: tabuleiro x peca -> tuplo de posicoes"""
    return tuple(create_position(p[0], p[1]) for p, jj in t.items() if jj == j)

# ==============================================================
# FUNCOES AUXILIARES - movimento manual
# ==============================================================

def obter_movimento_manual(t, j):
    """
    obter_movimento_manual: tabuleiro x peca -> tuplo de posicoes
    Pede input ao jogador e devolve a jogada:
      - Na fase de colocacao -> (pos,)
      - Na fase de movimento -> (p1, p2)
    Regras:
      - Jogador escreve posicao (ex: 'a1') para colocar peca.
      - Jogador escreve movimento (ex: 'a1b2') para mover peca.
      - Jogador pode passar o turno com movimento 'a1a1'
        se a peca estiver bloqueada.
    Se a escolha for invalida, lanca:
        ValueError('obter_movimento_manual: escolha invalida')
    """

    # contar pecas do jogador
    pecas_jogador = obter_posicoes_jogador(t, j)
    total_pecas = len(pecas_jogador)

    # fase de colocacao: jogador tem menos de 3 pecas
    if total_pecas < 3:
        escolha = input("Turno do jogador. Escolha uma posicao: ")
        if len(escolha) != 2:
            raise ValueError("obter_movimento_manual: escolha invalida")

        c, l = escolha[0], escolha[1]
        try:
            p = create_position(c, l)
        except ValueError:
            raise ValueError("obter_movimento_manual: escolha invalida")

        if not eh_position_livre(t, p):
            raise ValueError("obter_movimento_manual: escolha invalida")

        return (p,)

    # fase de movimento: jogador ja tem 3 pecas
    else:
        escolha = input("Turno do jogador. Escolha um movimento: ")
        if len(escolha) != 4:
            raise ValueError("obter_movimento_manual: escolha invalida")

        c1, l1, c2, l2 = escolha[0], escolha[1], escolha[2], escolha[3]
        try:
            p1 = create_position(c1, l1)
            p2 = create_position(c2, l2)
        except ValueError:
            raise ValueError("obter_movimento_manual: escolha invalida")

        # origem tem de ser peca do jogador
        if obter_peca(t, p1) != j:
            raise ValueError("obter_movimento_manual: escolha invalida")

        # se p1 == p2 (passar turno), permitido
        if eh_position(p1, p2):
            return (p1, p2)

        # destino tem de ser livre
        if not eh_position_livre(t, p2):
            raise ValueError("obter_movimento_manual: escolha invalida")

        # destino tem de ser adjacente à origem
        if p2 not in get_adjacent_positions(p1):
            raise ValueError("obter_movimento_manual: escolha invalida")

        return (p1, p2)

# ==============================================================
# FUNCOES AUXILIARES - movimento automatico
# ==============================================================

def obter_movimento_auto(t, j, nivel):
    """
    obter_movimento_auto: tabuleiro x peca x str -> tuplo de posicoes
    Devolve o movimento automatico do computador consoante a fase do jogo.
    - Na colocacao: (pos,)
    - Na fase de movimento: (p1, p2)
    """
    # contar pecas do jogador
    pecas_jogador = obter_posicoes_jogador(t, j)
    total_pecas = len(pecas_jogador)

    # ---------------------------
    # FASE DE COLOCACAO
    # ---------------------------
    if total_pecas < 3:
        # 1. Vitoria: se jogador pode ganhar, coloca la
        for p in obter_posicoes_livres(t):
            copia = cria_copia_tabuleiro(t)
            coloca_peca(copia, j, p)
            if obter_ganhador(copia) == j:
                return (p,)

        # 2. Bloqueio: se adversario pode ganhar, bloquear
        adversario = 'O' if j == 'X' else 'X'
        for p in obter_posicoes_livres(t):
            copia = cria_copia_tabuleiro(t)
            coloca_peca(copia, adversario, p)
            if obter_ganhador(copia) == adversario:
                return (p,)

        # 3. Centro
        centro = create_position('b', '2')
        if eh_position_livre(t, centro):
            return (centro,)

        # 4. Canto
        for p in [create_position('a','1'), create_position('c','1'),
                  create_position('a','3'), create_position('c','3')]:
            if eh_position_livre(t, p):
                return (p,)

        # 5. Lateral
        for p in [create_position('b','1'), create_position('a','2'),
                  create_position('c','2'), create_position('b','3')]:
            if eh_position_livre(t, p):
                return (p,)

    # ---------------------------
    # FASE DE MOVIMENTO
    # ---------------------------
    else:
        if nivel == 'facil':
            # primeira peca que possa mover
            for p1 in obter_posicoes_jogador(t, j):
                for p2 in get_adjacent_positions(p1):
                    if eh_position_livre(t, p2):
                        return (p1, p2)
            # se todas bloqueadas -> passa turno
            return (pecas_jogador[0], pecas_jogador[0])

        elif nivel == 'normal':
            # minimax com profundidade = 1
            return minimax_escolha(t, j, profundidade=1)[1]

        elif nivel == 'dificil':
            # minimax com profundidade = 5
            return minimax_escolha(t, j, profundidade=5)[1]

        else:
            raise ValueError("obter_movimento_auto: nivel invalido")

def minimax_escolha(t, jogador, profundidade):
    """
    minimax_escolha: tabuleiro x peca x int -> (valor, movimento)
    Devolve (melhor_valor, melhor_movimento)
    """
    adversario = 'O' if jogador == 'X' else 'X'

    # Condicao de paragem
    vencedor = obter_ganhador(t)
    if vencedor != ' ':
        return (1 if vencedor == 'X' else -1, None)
    if profundidade == 0:
        return (0, None)

    movimentos = []

    # Gerar todos os movimentos possiveis
    for p1 in obter_posicoes_jogador(t, jogador):
        for p2 in get_adjacent_positions(p1):
            if eh_position_livre(t, p2):
                copia = cria_copia_tabuleiro(t)
                move_peca(copia, p1, p2)
                valor, _ = minimax_escolha(copia, adversario, profundidade-1)
                movimentos.append((valor, (p1, p2)))

    if not movimentos:  # sem movimentos, jogador passa
        return (0, (pecas_jogador[0], pecas_jogador[0]))

    # Escolher max para 'X', min para 'O'
    if jogador == 'X':
        return max(movimentos, key=lambda x: x[0])
    else:
        return min(movimentos, key=lambda x: x[0])



# ==============================================================
# FUNCAO PRINCIPAL
# ==============================================================

def moinho(jogador, dificuldade):
    """
    moinho: str x str -> str
    Jogo completo do moinho humano vs computador.
    Argumentos:
      jogador -> '[X]' ou '[O]'
      dificuldade -> 'facil', 'normal' ou 'dificil'
    Devolve a peca ganhadora ('[X]' ou '[O]').
    """

    # validar argumentos
    if jogador not in ('[X]', '[O]') or dificuldade not in ('facil', 'normal', 'dificil'):
        raise ValueError("moinho: argumentos invalidos")

    # mapear para representacao interna
    humano = 'X' if jogador == '[X]' else 'O'
    computador = 'O' if humano == 'X' else 'X'

    print(f"Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {dificuldade}.\n")

    # criar tabuleiro vazio
    t = cria_tabuleiro()
    turno = 'X'  # X comeca sempre

    # ciclo do jogo
    while True:
        print(tabuleiro_para_str(t))

        # verificar se ha vencedor
        vencedor = obter_ganhador(t)
        if vencedor != ' ':
            return peca_para_str(vencedor)

        # turno do jogador humano
        if turno == humano:
            if len(obter_posicoes_jogador(t, humano)) < 3:
                mov = obter_movimento_manual(t, humano)  # fase colocacao
                coloca_peca(t, humano, mov[0])
            else:
                mov = obter_movimento_manual(t, humano)  # fase movimento
                if eh_position(mov[0], mov[1]):  # passar turno
                    pass
                else:
                    move_peca(t, mov[0], mov[1])

        # turno do computador
        else:
            print(f"Turno do computador ({dificuldade}):")
            if len(obter_posicoes_jogador(t, computador)) < 3:
                mov = obter_movimento_auto(t, computador, dificuldade)  # colocacao
                coloca_peca(t, computador, mov[0])
            else:
                mov = obter_movimento_auto(t, computador, dificuldade)  # movimento
                if eh_position(mov[0], mov[1]):  # passar turno
                    pass
                else:
                    move_peca(t, mov[0], mov[1])

        # alternar turno
        turno = computador if turno == humano else humano

if __name__ == "__main__":
    vencedor = moinho('[X]', 'facil')
    print("Resultado final:", vencedor)
