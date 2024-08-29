import math
import random
import time

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = [c for c in range(COLUMNS) if board[0][c] == ' ']
    is_terminal = win_condition(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if maximizingPlayer:
                return (None, -100000000000000)  # Peça do adversário ganhou
            else:
                return (None, 10000000000000)  # Peça do jogador ganhou
        else:
            return (None, score_position(board, 'X'))  # Retorna a pontuação do tabuleiro
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, col, 'X')
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, col, 'O')
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value



ROWS = 6
COLUMNS = 7



GREEN = '\033[32m'
AZUL = '\033[34m'
YELLOW = '\033[33m'
RED = '\033[31m'
RESET = '\033[0m'

def create_board():
    
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    
    print()
    for row in board:
        colored_row = []
        for cell in row:
            if cell == 'X':
                colored_row.append(f"{AZUL}X{RESET}")
            elif cell == 'O':
                colored_row.append(f"{YELLOW}O{RESET}")
            else:
                colored_row.append(' ')
        print('| ' + ' | '.join(colored_row) + ' |')  # Corrigido: Removeu o espaço vazio adicional no início da linha
    print('  ' + '   '.join(str(i) for i in range(COLUMNS)))  
    print()


def drop_piece(board, column, piece):  
    for row in reversed(board):  # Começa da última linha (parte inferior do tabuleiro)
        if row[column] == ' ':
            row[column] = piece
            return True
    return False  


def win_condition(board):
    # Verifica as linhas horizontais
    for row in range(ROWS):
        for col in range(COLUMNS - 3):  # -3 para evitar índice fora do tabuleiro
            if board[row][col] != ' ' and \
               board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                return True

    # Verifica as colunas verticais
    for col in range(COLUMNS):
        for row in range(ROWS - 3):  # -3 para evitar índice fora do tabuleiro
            if board[row][col] != ' ' and \
               board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                return True

    # Verifica as diagonais ascendentes (da esquerda para a direita e de baixo para cima)
    for row in range(3, ROWS):  # Começa da linha 3 (a quarta linha) para cima
        for col in range(COLUMNS - 3):  # -3 para evitar índice fora do tabuleiro
            if board[row][col] != ' ' and \
               board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return True

    # Verifica as diagonais descendentes (da esquerda para a direita e de cima para baixo)
    for row in range(ROWS - 3):  # -3 para evitar índice fora do tabuleiro
        for col in range(COLUMNS - 3):  # -3 para evitar índice fora do tabuleiro
            if board[row][col] != ' ' and \
               board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return True

    return False





def evaluate_window(window, piece):
    score = 0
    opponent_piece = 'O' if piece == 'X' else 'X'

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(' ') == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(' ') == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(' ') == 1:
        score -= 4

    return score



def score_position(board, piece):
    score = 0

    # Pontuação Horizontal
    for row in range(ROWS):
        row_array = [board[row][col] for col in range(COLUMNS)]
        for col in range(COLUMNS - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, piece)

    # Pontuação Vertical
    for col in range(COLUMNS):
        col_array = [board[row][col] for row in range(ROWS)]
        for row in range(ROWS - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, piece)

    # Pontuação Diagonal Ascendente
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Pontuação Diagonal Descendente
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def menu():
    while True:
        modo_jogo = input(f"Escolha que modo de jogo deseja jogar:\n {GREEN}1.{RESET} Pessoa vs Pessoa\n {GREEN}2.{RESET} Pessoa vs Máquina\n:")
        if modo_jogo == "1":
            return 1
        elif modo_jogo == "2":
            return 2
        else:
            print(f"{RED}Entrada inválida. Por favor insira o número 1 ou 2.{RESET}")



def jogar_deNovo():
    while True:
        print()
        modo_jogo = input(f"Deseja Jogar outra vez?\n:").strip().lower()
        if modo_jogo[0] == "s" or modo_jogo[0] == "y":
            return 1
        elif modo_jogo[0] == "n":
            return 2
        else:
            print(f"{RED}Entrada inválida..{RESET}")


def vs_IA():
    board = create_board()
    print_board(board)
    jogador_atual = "jogador1"

    while True:
        if jogador_atual == "jogador1":
            current_piece = 'X'
            print("Jogar a peça: %s" % current_piece)
            try:
                column = int(input("Escolha uma coluna (0-6): "))
                if column < 0 or column >= COLUMNS:
                    print(f"{RED}Coluna inválida. Tente novamente.{RESET}")
                    continue
            except ValueError:
                print(f"{RED}Entrada inválida. Por favor, insira um número entre 0 e 6.{RESET}")
                continue
        else:
            time.sleep(1)       # pausa breve para resposta não ser instantanea
            current_piece = 'O'
            column, minimax_score = minimax(board, 4, -math.inf, math.inf, True)  

        if not drop_piece(board, column, current_piece):
            print(f"{RED}Coluna cheia. Tente outra coluna.{RESET}")
            continue

        print_board(board)
        if win_condition(board):
            print(f"Peça {AZUL if current_piece == 'X' else YELLOW}{current_piece}{RESET} ganhou!!!!🎉🎉🎉🎉🎉")
            return
        jogador_atual = "jogador2" if jogador_atual == "jogador1" else "jogador1"



def vs_Pessoa():
    board = create_board()
    print_board(board)
    jogador_atual = "jogador1"

    while True:
        current_piece = 'X' if jogador_atual == "jogador1" else 'O'
        print("Jogar a peça: %s" % current_piece)
        try:
            column = int(input("Escolha uma coluna (0-6): "))
            if column < 0 or column >= COLUMNS:
                print(f"{RED}Coluna inválida. Tente novamente.{RESET}")
                continue
        except ValueError:
            print(f"{RED}Entrada inválida. Por favor, insira um número entre 0 e 6.{RESET}")
            continue

        
        if not drop_piece(board, column, current_piece):
            print(f"{RED}Coluna cheia. Tente outra coluna.{RESET}")
            continue

        
        print_board(board)
        if win_condition(board):
            print(f"Peça {AZUL if current_piece == 'X' else YELLOW}{current_piece}{RESET} ganhou!!!!🎉🎉🎉🎉🎉")
            return
        jogador_atual = "jogador2" if jogador_atual == "jogador1" else "jogador1"


def main():
    while True:
        menu_selecionado = menu()

        if menu_selecionado == 2:
            vs_IA()
        
        if menu_selecionado == 1:
            vs_Pessoa()

        repetir = jogar_deNovo()

        if repetir == 2:
            return
        
        
if __name__ == "__main__":
    main()
