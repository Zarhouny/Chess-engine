import os
import copy
import ai
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

BOARD_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 250
SQUARE_SIZE = BOARD_SIZE // 8

PANEL_HEIGHT = 150
PANEL_COLOR = (35,35,35)
BUTTON_COLOR = (80,80,80)
TEXT_COLOR = (255,255,255)
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 50)
overlay_font = pygame.font.SysFont("Arial", 28, bold=True)
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT_COLOR = (0, 0, 0, 150) 
SELECTED_COLOR = (245, 245, 100, 150)   
pieces = {
    100: pygame.image.load("assets/white-pawn.png"),
    320: pygame.image.load("assets/white-knight.png"),
    330: pygame.image.load("assets/white-bishop.png"),
    500: pygame.image.load("assets/white-rook.png"),
    900: pygame.image.load("assets/white-queen.png"),
    20000: pygame.image.load("assets/white-king.png"),

    -100: pygame.image.load("assets/black-pawn.png"),
    -320: pygame.image.load("assets/black-knight.png"),
    -330: pygame.image.load("assets/black-bishop.png"),
    -500: pygame.image.load("assets/black-rook.png"),
    -900: pygame.image.load("assets/black-queen.png"),
    -20000: pygame.image.load("assets/black-king.png"),
}

Buttons = {
    "reset": [pygame.Rect(20, BOARD_SIZE + 90, 140, 40), 'Reset Board'],
    "overlay": [pygame.Rect(180, BOARD_SIZE + 90, 180, 40), 'Show Overlay']
}

#put pieces to scale
for piece in pieces:
    pieces[piece] = pygame.transform.scale(pieces[piece], (SQUARE_SIZE, SQUARE_SIZE))

STARTING_BOARD = [
    [-500, -320, -330, -900, -20000, -330, -320, -500],
    [-100, -100, -100, -100, -100, -100, -100, -100],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [100, 100, 100, 100, 100, 100, 100, 100],
    [500, 320, 330, 900, 20000, 330, 320 ,500]
]

BOARD = copy.deepcopy(STARTING_BOARD)

current_turn = 1       
selected_square = None 
valid_moves = []       
en_passant_square = None  
game_status_message = ""  
game_over = False         

# NControls whether to display piece point text strings instead of image assets
show_numeric_overlay = False

moved_status = {
    "W_KING": False, "W_ROOK_A": False, "W_ROOK_H": False,
    "B_KING": False, "B_ROOK_A": False, "B_ROOK_H": False
}

PAWN_PST = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],  
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],  
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_PST = [
    [-50,-40,-30,-30,-30,-30,-40,-50],  # rim is dim lol
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30], 
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_PST = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_PST = [
    [  0,  0,  0,  5,  5,  0,  0,  0], 
    [  5, 10, 10, 10, 10, 10, 10,  5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [ -5,  0,  0,  0,  0,  0,  0, -5],
    [  0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_PST = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_MIDDLEGAME_PST = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]  
]

KING_ENDGAME_PST = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30], 
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

def get_pst_value(piece_type, row, col, is_endgame, is_white):
    r = row if is_white else (7 - row)
    c = col if is_white else (7 - col)
    
    if piece_type == 100:   table = PAWN_PST
    elif piece_type == 320: table = KNIGHT_PST
    elif piece_type == 330: table = BISHOP_PST
    elif piece_type == 500: table = ROOK_PST
    elif piece_type == 900: table = QUEEN_PST
    elif piece_type == 20000:
        table = KING_ENDGAME_PST if is_endgame else KING_MIDDLEGAME_PST
    else:
        return 0
        
    return table[r][c]

def evaluate_board(board):
    material_score = 0
    positional_score = 0
    mobility_score = 0
    pawn_structure_score = 0
    
    non_pawn_material = 0
    for row in board:
        for piece in row:
            if abs(piece) in [320, 330, 500, 900]:
                non_pawn_material += abs(piece)
    is_endgame = non_pawn_material <= 1500

    white_pawn_files = [[] for _ in range(8)]
    black_pawn_files = [[] for _ in range(8)]
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == 100:
                white_pawn_files[c].append(r)
            elif board[r][c] == -100:
                black_pawn_files[c].append(r)

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == 0:
                continue
                
            piece_type = abs(piece)
            is_white = piece > 0
            sign = 1 if is_white else -1
            
            if piece_type != 20000:
                material_score += piece
                
            pst_val = get_pst_value(piece_type, r, c, is_endgame, is_white)
            positional_score += (pst_val * sign)
            
            raw_moves = get_valid_moves(r, c, board, calculate_castling=False)
            mobility_score += (len(raw_moves) * 2 * sign)

            if piece_type == 100:
                my_files = white_pawn_files if is_white else black_pawn_files
                enemy_files = black_pawn_files if is_white else white_pawn_files
                
                if len(my_files[c]) > 1:
                    pawn_structure_score -= (15 * sign)
                    
                has_neighbor = False
                if c > 0 and len(my_files[c - 1]) > 0: has_neighbor = True
                if c < 7 and len(my_files[c + 1]) > 0: has_neighbor = True
                if not has_neighbor:
                    pawn_structure_score -= (20 * sign)
                    
                is_passed = True
                lanes_to_check = [c]
                if c > 0: lanes_to_check.append(c - 1)
                if c < 7: lanes_to_check.append(c + 1)
                
                for lane in lanes_to_check:
                    for enemy_pawn_row in enemy_files[lane]:
                        if is_white and enemy_pawn_row < r:
                            is_passed = False
                        elif not is_white and enemy_pawn_row > r:
                            is_passed = False
                            
                if is_passed:
                    pawn_structure_score += (25 * sign)

    total_score = (material_score + 
                   (positional_score / 100.0) + 
                   (mobility_score / 100.0) + 
                   (pawn_structure_score / 100.0))
    return total_score

def is_square_attacked(row, col, board, attacker_color):
    orthogonal = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in orthogonal:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            p = board[r][c]
            if p != 0:
                if (attacker_color == 1 and p > 0) or (attacker_color == -1 and p < 0):
                    if abs(p) in [500, 900]: return True
                break
            r += dr
            c += dc

    diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in diagonal:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            p = board[r][c]
            if p != 0:
                if (attacker_color == 1 and p > 0) or (attacker_color == -1 and p < 0):
                    if abs(p) in [330, 900]: return True
                break
            r += dr
            c += dc

    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            p = board[r][c]
            if (attacker_color == 1 and p > 0) or (attacker_color == -1 and p < 0):
                if abs(p) == 320: return True

    pawn_dir = 1 if attacker_color == 1 else -1
    for dc in [-1, 1]:
        r, c = row + pawn_dir, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            p = board[r][c]
            if (attacker_color == 1 and p > 0) or (attacker_color == -1 and p < 0):
                if abs(p) == 100: return True

    for dr, dc in orthogonal + diagonal:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            p = board[r][c]
            if (attacker_color == 1 and p > 0) or (attacker_color == -1 and p < 0):
                if abs(p) == 20000: return True

    return False

def get_valid_moves(row, col, board, ep_square=None, has_moved=None, calculate_castling=True):
    piece = board[row][col]
    if piece == 0:
        return []
        
    color = 1 if piece > 0 else -1
    enemy_color = -1 if color == 1 else 1
    piece_type = abs(piece)
    moves = []
    #base canonique
    orthogonal = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    if piece_type in [500, 330, 900]:
        directions = []
        if piece_type == 500 or piece_type == 900: directions += orthogonal
        if piece_type == 330 or piece_type == 900: directions += diagonal
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == 0:
                    moves.append((r, c))
                elif (target > 0 and color < 0) or (target < 0 and color > 0):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    elif piece_type == 320:
        #L-shaped moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == 0 or (target > 0 and color < 0) or (target < 0 and color > 0):
                    moves.append((r, c))

    elif piece_type == 20000:
        for dr, dc in orthogonal + diagonal:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == 0 or (target > 0 and color < 0) or (target < 0 and color > 0):
                    moves.append((r, c))

        if has_moved and calculate_castling:
            prefix = "W_" if color == 1 else "B_"
            r_idx = 7 if color == 1 else 0
            
            if not has_moved[prefix + "KING"] and not is_square_attacked(r_idx, 4, board, enemy_color):
                if not has_moved[prefix + "ROOK_H"]:
                    if board[r_idx][5] == 0 and board[r_idx][6] == 0:
                        if not is_square_attacked(r_idx, 5, board, enemy_color) and not is_square_attacked(r_idx, 6, board, enemy_color):
                            moves.append((r_idx, 6))
                        
                if not has_moved[prefix + "ROOK_A"]:
                    if board[r_idx][1] == 0 and board[r_idx][2] == 0 and board[r_idx][3] == 0:
                        if not is_square_attacked(r_idx, 3, board, enemy_color) and not is_square_attacked(r_idx, 2, board, enemy_color):
                            moves.append((r_idx, 2))

    elif piece_type == 100:
        direction = -1 if color == 1 else 1
        start_row = 6 if color == 1 else 1

        if 0 <= row + direction < 8 and board[row + direction][col] == 0:
            moves.append((row + direction, col))
            if row == start_row and board[row + 2 * direction][col] == 0:
                moves.append((row + 2 * direction, col))

        for dc in [-1, 1]:
            target_col = col + dc
            target_row = row + direction
            if 0 <= target_row < 8 and 0 <= target_col < 8:
                target = board[target_row][target_col]
                if target != 0 and ((target > 0 and color < 0) or (target < 0 and color > 0)):
                    moves.append((target_row, target_col))
                elif (target_row, target_col) == ep_square:
                    moves.append((target_row, target_col))

    return moves

def filter_illegal_moves(src_r, src_c, legal_targets, board, ep_square):
    moving_piece = board[src_r][src_c]
    color = 1 if moving_piece > 0 else -1
    enemy_color = -1 if color == 1 else 1
    filtered_moves = []

    for target_r, target_c in legal_targets:
        original_target = board[target_r][target_c]
        ep_pulled_piece = None
        ep_pulled_pos = None
        
        if abs(moving_piece) == 100 and (target_r, target_c) == ep_square:
            ep_pulled_pos = (src_r, target_c)
            ep_pulled_piece = board[src_r][target_c]
            board[src_r][target_c] = 0

        board[target_r][target_c] = moving_piece
        board[src_r][src_c] = 0

        king_pos = None
        for r in range(8):
            for c in range(8):
                if board[r][c] == (20000 if color == 1 else -20000):
                    king_pos = (r, c)
                    break
            if king_pos: break

        if king_pos and not is_square_attacked(king_pos[0], king_pos[1], board, enemy_color):
            filtered_moves.append((target_r, target_c))
            
        board[src_r][src_c] = moving_piece
        board[target_r][target_c] = original_target
        if ep_pulled_pos:
            board[ep_pulled_pos[0]][ep_pulled_pos[1]] = ep_pulled_piece
                
    return filtered_moves

def check_game_status(board, turn, ep_square, moved_status_dict):
    total_moves = 0
    king_pos = None
    enemy_color = -1 if turn == 1 else 1

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and ((piece > 0 and turn == 1) or (piece < 0 and turn == -1)):
                if abs(piece) == 20000:
                    king_pos = (r, c)
                raw = get_valid_moves(r, c, board, ep_square, moved_status_dict)
                legal = filter_illegal_moves(r, c, raw, board, ep_square)
                total_moves += len(legal)

    if total_moves == 0:
        if king_pos and is_square_attacked(king_pos[0], king_pos[1], board, enemy_color):
            return "CHECKMATE!"
        else:
            return "STALEMATE!"
    return ""

screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + PANEL_HEIGHT))
pygame.display.set_caption("Chess engine but it's woke")
clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    hovering_clickable = False

    if Buttons["reset"][0].collidepoint(mouse_pos) or Buttons["overlay"][0].collidepoint(mouse_pos):
        hovering_clickable = True
    elif mouse_pos[1] < BOARD_SIZE and not game_over:
        col = mouse_pos[0] // SQUARE_SIZE
        row = mouse_pos[1] // SQUARE_SIZE
        if 0 <= row < 8 and 0 <= col < 8:
            if selected_square and (row, col) in valid_moves:
                hovering_clickable = True
            else:
                piece = BOARD[row][col]
                if piece != 0 and ((piece > 0 and current_turn == 1) or (piece < 0 and current_turn == -1)):
                    hovering_clickable = True

    if hovering_clickable:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if Buttons["reset"][0].collidepoint(mouse_pos):
                BOARD = copy.deepcopy(STARTING_BOARD)
                current_turn = 1
                selected_square = None
                valid_moves = []
                en_passant_square = None
                game_status_message = ""
                game_over = False
                moved_status = {
                    "W_KING": False, "W_ROOK_A": False, "W_ROOK_H": False,
                    "B_KING": False, "B_ROOK_A": False, "B_ROOK_H": False
                }
                print("Board Reset")
            
            elif Buttons["overlay"][0].collidepoint(mouse_pos):
                show_numeric_overlay = not show_numeric_overlay
                if show_numeric_overlay:
                    Buttons["overlay"][1] = 'Hide Overlay'
                else:
                    Buttons["overlay"][1] = 'Show Overlay'
                    
            elif mouse_pos[1] < BOARD_SIZE and not game_over:
                col = mouse_pos[0] // SQUARE_SIZE
                row = mouse_pos[1] // SQUARE_SIZE
                
                if 0 <= row < 8 and 0 <= col < 8:
                    if selected_square and (row, col) in valid_moves:
                        src_r, src_c = selected_square
                        moving_piece = BOARD[src_r][src_c]
                        next_ep_square = None
                        is_promotion = False
                        
                        target_square_piece = BOARD[row][col]
                        if abs(target_square_piece) == 500:
                            if row == 7 and col == 0: moved_status["W_ROOK_A"] = True
                            if row == 7 and col == 7: moved_status["W_ROOK_H"] = True
                            if row == 0 and col == 0: moved_status["B_ROOK_A"] = True
                            if row == 0 and col == 7: moved_status["B_ROOK_H"] = True

                        if abs(moving_piece) == 100:
                            if (row, col) == en_passant_square: BOARD[src_r][col] = 0
                            if abs(row - src_r) == 2: next_ep_square = ((src_r + row) // 2, col)
                            if row == 0 or row == 7: is_promotion = True
                        
                        if abs(moving_piece) == 20000:
                            if col - src_c == 2:    
                                BOARD[row][5] = BOARD[row][7]
                                BOARD[row][7] = 0
                            elif col - src_c == -2: 
                                BOARD[row][3] = BOARD[row][0]
                                BOARD[row][0] = 0
                            prefix = "W_" if moving_piece > 0 else "B_"
                            moved_status[prefix + "KING"] = True

                        if abs(moving_piece) == 500:
                            prefix = "W_" if moving_piece > 0 else "B_"
                            if src_c == 0 and src_r == (7 if moving_piece > 0 else 0): moved_status[prefix + "ROOK_A"] = True
                            if src_c == 7 and src_r == (7 if moving_piece > 0 else 0): moved_status[prefix + "ROOK_H"] = True
                        
                        if is_promotion: BOARD[row][col] = 900 if moving_piece > 0 else -900
                        else: BOARD[row][col] = BOARD[src_r][src_c]
                            
                        BOARD[src_r][src_c] = 0
                        en_passant_square = next_ep_square
                        
                        current_turn *= -1
                        selected_square = None
                        valid_moves = []

                        status = check_game_status(BOARD, current_turn, en_passant_square, moved_status)
                        if status != "":
                            game_status_message = status
                            game_over = True
                            
                        if not game_over and current_turn == -1:
                            turn_text = font.render("AI is thinking...", True, TEXT_COLOR)
                            screen.blit(turn_text, (20, BOARD_SIZE + 50))
                            pygame.display.flip()

                            _, ai_move = ai.minimax(
                                BOARD, 3, float('-inf'), float('inf'), False, en_passant_square, moved_status,
                                evaluate_board, get_valid_moves, filter_illegal_moves, is_square_attacked
                            )
                            
                            if ai_move:
                                ai_src_r, ai_src_c, ai_tgt_r, ai_tgt_c = ai_move
                                ai_piece = BOARD[ai_src_r][ai_src_c]
                                
                                is_promo = abs(ai_piece) == 100 and (ai_tgt_r == 0 or ai_tgt_r == 7)
                                if is_promo:
                                    BOARD[ai_tgt_r][ai_tgt_c] = -900  
                                else:
                                    BOARD[ai_tgt_r][ai_tgt_c] = ai_piece
                                    
                                BOARD[ai_src_r][ai_src_c] = 0
                                current_turn *= -1  
                                
                                status = check_game_status(BOARD, current_turn, None, moved_status)
                                if status != "":
                                    game_status_message = status
                                    game_over = True
                    else:
                        piece = BOARD[row][col]
                        if piece != 0 and ((piece > 0 and current_turn == 1) or (piece < 0 and current_turn == -1)):
                            selected_square = (row, col)
                            raw_moves = get_valid_moves(row, col, BOARD, en_passant_square, moved_status)
                            valid_moves = filter_illegal_moves(row, col, raw_moves, BOARD, en_passant_square)
                        else:
                            selected_square = None
                            valid_moves = []

    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    if selected_square and not game_over:
        s_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s_surface.fill(SELECTED_COLOR)
        screen.blit(s_surface, (selected_square[1] * SQUARE_SIZE, selected_square[0] * SQUARE_SIZE))
        
        for move in valid_moves:
            m_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            if BOARD[move[0]][move[1]] != 0 or move == en_passant_square:
                pygame.draw.rect(m_surface, (255, 90, 90, 140), (0, 0, SQUARE_SIZE, SQUARE_SIZE), 5)
            else:
                pygame.draw.circle(m_surface, HIGHLIGHT_COLOR, (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 6)
            screen.blit(m_surface, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE))

    for row in range(8):
        for col in range(8):
            piece = BOARD[row][col]
            if piece != 0:
                if show_numeric_overlay:
                    text_color = (25, 115, 230) if piece > 0 else (215, 35, 35)
                    piece_val_text = overlay_font.render(str(abs(piece)), True, text_color)
                    
                    text_x = col * SQUARE_SIZE + (SQUARE_SIZE // 2 - piece_val_text.get_width() // 2)
                    text_y = row * SQUARE_SIZE + (SQUARE_SIZE // 2 - piece_val_text.get_height() // 2)
                    screen.blit(piece_val_text, (text_x, text_y))
                else:
                    screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    pygame.draw.rect(screen, PANEL_COLOR, (0, BOARD_SIZE, BOARD_SIZE, PANEL_HEIGHT))

    turn_str = "Turn: WHITE" if current_turn == 1 else "Turn: BLACK"
    turn_text = font.render(turn_str, True, TEXT_COLOR)
    screen.blit(turn_text, (20, BOARD_SIZE + 20))

    eval_score = evaluate_board(BOARD)
    eval_str = f"Evaluation: {eval_score:+.1f}" if eval_score != 0 else "Evaluation: 0.0"
    eval_color = (140, 230, 140) if eval_score > 0 else ((240, 130, 130) if eval_score < 0 else (255, 255, 255))
    eval_text = font.render(eval_str, True, eval_color)
    screen.blit(eval_text, (200, BOARD_SIZE + 20))

    if game_status_message != "":
        banner_text = large_font.render(game_status_message, True, (255, 50, 50))
        screen.blit(banner_text, (20, BOARD_SIZE + 55))

    pygame.draw.rect(screen, BUTTON_COLOR, Buttons["reset"][0])
    reset_text = font.render(Buttons["reset"][1], True, TEXT_COLOR)
    screen.blit(reset_text, (Buttons["reset"][0].centerx - reset_text.get_width() // 2, Buttons["reset"][0].centery - reset_text.get_height() // 2))
    
    pygame.draw.rect(screen, BUTTON_COLOR, Buttons["overlay"][0])
    overlay_text = font.render(Buttons["overlay"][1], True, TEXT_COLOR)
    screen.blit(overlay_text, (Buttons["overlay"][0].centerx - overlay_text.get_width() // 2, Buttons["overlay"][0].centery - overlay_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
