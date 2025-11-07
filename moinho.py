# ==============================================================
# Projeto: Jogo do Moinho (Nine Men’s Morris simplificado 3x3)
# ==============================================================
# NOTA IMPORTANTE:
# - Todo o código deve estar neste único ficheiro.
# - Não usar acentos nem caracteres fora do ASCII.
# ==============================================================

# ==============================================================
# TAD POSITION
# ==============================================================

def cria_posicao(c, l):
    if c not in ('a', 'b', 'c') or l not in ('1', '2', '3'):
        raise ValueError('cria_posicao: argumentos invalidos')
    return (c, l)

def cria_copia_posicao(p):
    return (p[0], p[1])

def obter_pos_c(p):
    return p[0]

def obter_pos_l(p):
    return p[1]

def eh_posicao(arg):
    return isinstance(arg, tuple) and len(arg) == 2 and arg[0] in ('a','b','c') and arg[1] in ('1','2','3')

def posicoes_iguais(p1, p2):
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2

def posicao_para_str(p):
    return p[0] + p[1]

def obter_posicoes_adjacentes(p):
    adj = {
        ('a','1'): [('b','1'), ('a','2')],
        ('b','1'): [('a','1'), ('c','1'), ('b','2')],
        ('c','1'): [('b','1'), ('c','2')],
        ('a','2'): [('a','1'), ('b','2'), ('a','3')],
        ('b','2'): [('b','1'), ('a','2'), ('c','2'), ('b','3')],
        ('c','2'): [('c','1'), ('b','2'), ('c','3')],
        ('a','3'): [('a','2'), ('b','3')],
        ('b','3'): [('b','2'), ('a','3'), ('c','3')],
        ('c','3'): [('c','2'), ('b','3')]
    }
    return tuple(adj[p])

# ==============================================================
# TAD PECA
# ==============================================================

def cria_peca(s):
    if s not in ('X','O',' '):
        raise ValueError('cria_peca: argumento invalido')
    return s

def cria_copia_peca(j):
    return j

def eh_peca(arg):
    return arg in ('X','O',' ')

def pecas_iguais(j1, j2):
    return eh_peca(j1) and eh_peca(j2) and j1 == j2

def peca_para_str(j):
    return "[" + j + "]"

def peca_para_inteiro(j):
    if j == 'X':
        return 1
    if j == 'O':
        return -1
    return 0

# ==============================================================
# TAD TABULEIRO
# ==============================================================

def cria_tabuleiro():
    pos = [c + l for l in ('1','2','3') for c in ('a','b','c')]
    return {p: ' ' for p in pos}

def cria_copia_tabuleiro(t):
    return dict(t)

def obter_peca(t, p):
    return t[posicao_para_str(p)]

def obter_vetor(t, s):
    if s in ('a','b','c'):
        return tuple(t[s + l] for l in ('1','2','3'))
    elif s in ('1','2','3'):
        return tuple(t[c + s] for c in ('a','b','c'))
    else:
        raise ValueError('obter_vetor: argumento invalido')

def coloca_peca(t, j, p):
    t[posicao_para_str(p)] = j
    return t

def remove_peca(t, p):
    t[posicao_para_str(p)] = ' '
    return t

def move_peca(t, p1, p2):
    j = t[posicao_para_str(p1)]
    t[posicao_para_str(p1)] = ' '
    t[posicao_para_str(p2)] = j
    return t

def eh_tabuleiro(arg):
    if not isinstance(arg, dict):
        return False
    posicoes = [c + l for l in ('1','2','3') for c in ('a','b','c')]
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
        outro = 'O' if g == 'X' else 'X'
        copia = cria_copia_tabuleiro(arg)
        for k in copia:
            if copia[k] == outro:
                copia[k] = ' '
        if obter_ganhador(copia) != ' ':
            return False
    return True

def eh_posicao_livre(t, p):
    return t[posicao_para_str(p)] == ' '

def tabuleiros_iguais(t1, t2):
    return t1 == t2

def tabuleiro_para_str(t):
    def linha(n):
        return str(n) + " " + "-".join(peca_para_str(t[c + str(n)]) for c in ('a','b','c'))
    s = "   a   b   c\n"
    s += " " + linha(1) + "\n   | \\ | / |\n"
    s += " " + linha(2) + "\n   | / | \\ |\n"
    s += " " + linha(3)
    return s

def tuplo_para_tabuleiro(tuplo):
    tab = cria_tabuleiro()
    for i in range(3):
        for j in range(3):
            c = ('a','b','c')[j]
            l = ('1','2','3')[i]
            if tuplo[i][j] == 1:
                tab[c+l] = 'X'
            elif tuplo[i][j] == -1:
                tab[c+l] = 'O'
            else:
                tab[c+l] = ' '
    return tab

def obter_ganhador(t):
    linhas = [('a1','b1','c1'),('a2','b2','c2'),('a3','b3','c3')]
    colunas = [('a1','a2','a3'),('b1','b2','b3'),('c1','c2','c3')]
    for grupo in linhas + colunas:
        pecas = [t[p] for p in grupo]
        if pecas[0] != ' ' and pecas.count(pecas[0]) == 3:
            return pecas[0]
    return ' '

def obter_posicoes_livres(t):
    return tuple(cria_posicao(p[0], p[1]) for p, j in t.items() if j == ' ')

def obter_posicoes_jogador(t, j):
    return tuple(cria_posicao(p[0], p[1]) for p, jj in t.items() if jj == j)

# ==============================================================
# FUNCOES AUXILIARES - movimento manual
# ==============================================================

def obter_movimento_manual(t, j):
    pecas_jogador = obter_posicoes_jogador(t, j)
    if len(pecas_jogador) < 3:
        escolha = input("Turno do jogador. Escolha uma posicao: ")
        if len(escolha) != 2:
            raise ValueError("obter_movimento_manual: escolha invalida")
        c, l = escolha[0], escolha[1]
        try:
            p = cria_posicao(c, l)
        except:
            raise ValueError("obter_movimento_manual: escolha invalida")
        if not eh_posicao_livre(t, p):
            raise ValueError("obter_movimento_manual: escolha invalida")
        return (p,)
    else:
        escolha = input("Turno do jogador. Escolha um movimento: ")
        if len(escolha) != 4:
            raise ValueError("obter_movimento_manual: escolha invalida")
        c1, l1, c2, l2 = escolha[0], escolha[1], escolha[2], escolha[3]
        try:
            p1 = cria_posicao(c1, l1)
            p2 = cria_posicao(c2, l2)
        except:
            raise ValueError("obter_movimento_manual: escolha invalida")
        if obter_peca(t, p1) != j:
            raise ValueError("obter_movimento_manual: escolha invalida")
        if posicoes_iguais(p1, p2):
            return (p1, p2)
        if not eh_posicao_livre(t, p2):
            raise ValueError("obter_movimento_manual: escolha invalida")
        if p2 not in obter_posicoes_adjacentes(p1):
            raise ValueError("obter_movimento_manual: escolha invalida")
        return (p1, p2)

# ==============================================================
# FUNCOES AUXILIARES - movimento automatico
# ==============================================================

def obter_movimento_auto(t, j, nivel):
    pecas_jogador = obter_posicoes_jogador(t, j)
    if len(pecas_jogador) < 3:
        for p in obter_posicoes_livres(t):
            copia = cria_copia_tabuleiro(t)
            coloca_peca(copia, j, p)
            if obter_ganhador(copia) == j:
                return (p,)
        adversario = 'O' if j == 'X' else 'X'
        for p in obter_posicoes_livres(t):
            copia = cria_copia_tabuleiro(t)
            coloca_peca(copia, adversario, p)
            if obter_ganhador(copia) == adversario:
                return (p,)
        centro = cria_posicao('b','2')
        if eh_posicao_livre(t, centro):
            return (centro,)
        for p in [cria_posicao('a','1'), cria_posicao('c','1'), cria_posicao('a','3'), cria_posicao('c','3')]:
            if eh_posicao_livre(t, p):
                return (p,)
        for p in [cria_posicao('b','1'), cria_posicao('a','2'), cria_posicao('c','2'), cria_posicao('b','3')]:
            if eh_posicao_livre(t, p):
                return (p,)
    else:
        if nivel == 'facil':
            for p1 in obter_posicoes_jogador(t, j):
                for p2 in get_adjacent_positions(p1):
                    if eh_position_livre(t, p2):
                        return (p1, p2)
            return (pecas_jogador[0], pecas_jogador[0])
        if nivel == 'normal':
            for p1 in obter_posicoes_jogador(t, j):
                for p2 in obter_posicoes_adjacentes(p1):
                    if eh_posicao_livre(t, p2):
                        copia = cria_copia_tabuleiro(t)
                        move_peca(copia, p1, p2)
                        if obter_ganhador(copia) == j:
                            return (p1, p2)
            for p1 in obter_posicoes_jogador(t, j):
                for p2 in obter_posicoes_adjacentes(p1):
                    if eh_posicao_livre(t, p2):
                        return (p1, p2)
            return (pecas_jogador[0], pecas_jogador[0])
        if nivel == 'dificil':
            return minimax_escolha(t, j, 5)[1]
        raise ValueError("obter_movimento_auto: nivel invalido")

def minimax_escolha(t, jogador, profundidade):
    adversario = 'O' if jogador == 'X' else 'X'
    vencedor = obter_ganhador(t)
    if vencedor != ' ':
        if vencedor == 'X':
            return (1, None)
        else:
            return (-1, None)
    if profundidade == 0:
        return (0, None)
    movimentos = []
    for p1 in obter_posicoes_jogador(t, jogador):
        for p2 in get_adjacent_positions(p1):
            if eh_position_livre(t, p2):
                copia = cria_copia_tabuleiro(t)
                move_peca(copia, p1, p2)
                valor, _ = minimax_escolha(copia, adversario, profundidade - 1)
                movimentos.append((valor, (p1, p2)))
    pecas_jogador = obter_posicoes_jogador(t, jogador)
    if not movimentos:
        return (0, (pecas_jogador[0], pecas_jogador[0]))
    if jogador == 'X':
        return max(movimentos, key=lambda x: x[0])
    else:
        return min(movimentos, key=lambda x: x[0])

# ==============================================================
# FUNCAO PRINCIPAL
# ==============================================================

def moinho(jogador, dificuldade):
    if jogador not in ('[X]','[O]') or dificuldade not in ('facil','normal','dificil'):
        raise ValueError("moinho: argumentos invalidos")
    humano = 'X' if jogador == '[X]' else 'O'
    computador = 'O' if humano == 'X' else 'X'
    print("Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade " + dificuldade + ".\n")
    t = cria_tabuleiro()
    turno = 'X'
    while True:
        print(tabuleiro_para_str(t))
        vencedor = obter_ganhador(t)
        if vencedor != ' ':
            return peca_para_str(vencedor)
        if turno == humano:
            if len(obter_posicoes_jogador(t, humano)) < 3:
                mov = obter_movimento_manual(t, humano)
                coloca_peca(t, humano, mov[0])
            else:
                mov = obter_movimento_manual(t, humano)
                if not posicoes_iguais(mov[0], mov[1]):
                    move_peca(t, mov[0], mov[1])
        else:
            print("Turno do computador (" + dificuldade + "):")
            if len(obter_posicoes_jogador(t, computador)) < 3:
                mov = obter_movimento_auto(t, computador, dificuldade)
                coloca_peca(t, computador, mov[0])
            else:
                mov = obter_movimento_auto(t, computador, dificuldade)
                if not posicoes_iguais(mov[0], mov[1]):
                    move_peca(t, mov[0], mov[1])
        turno = computador if turno == humano else humano

if __name__ == "__main__":
    vencedor = moinho('[X]', 'facil')
    print("Resultado final:", vencedor)
