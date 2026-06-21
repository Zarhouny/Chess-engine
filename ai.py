import random

def get_all_legal_moves(board, turn, ep_square, moved_status_dict, get_valid_moves, filter_illegal_moves):
    # Gathers all valid, legal moves for the player's turnn
    legal_moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and ((piece > 0 and turn == 1) or (piece < 0 and turn == -1)):
                raw = get_valid_moves(r, c, board, ep_square, moved_status_dict)
                legal = filter_illegal_moves(r, c, raw, board, ep_square)
                for target_r, target_c in legal:
                    legal_moves.append((r, c, target_r, target_c))
    return legal_moves

# Minimax search with Alpha-Beta trunctuating ( pruning ) and random move ordering for better performance
def minimax(board, depth, alpha, beta, maximizing_player, ep_square, moved_status_dict, 
            evaluate_board, get_valid_moves, filter_illegal_moves, is_square_attacked):
    """
    Should Return: (best_score, best_move)
    """
    if depth == 0:
        return evaluate_board(board), None

    turn = 1 if maximizing_player else -1
    moves = get_all_legal_moves(board, turn, ep_square, moved_status_dict, get_valid_moves, filter_illegal_moves)

    if not moves:
        king_val = 20000 if turn == 1 else -20000
        king_pos = next((r, c) for r in range(8) for c in range(8) if board[r][c] == king_val)
        enemy_color = -1 if turn == 1 else 1
        
        if is_square_attacked(king_pos[0], king_pos[1], board, enemy_color):
            return (-100000 - depth) if maximizing_player else (100000 + depth), None
        return 0, None  # draw

    random.shuffle(moves)
    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for src_r, src_c, tgt_r, tgt_c in moves:
            moving_piece = board[src_r][src_c]
            original_target = board[tgt_r][tgt_c]
            
            board[tgt_r][tgt_c] = moving_piece
            board[src_r][src_c] = 0
            
            is_promo = abs(moving_piece) == 100 and (tgt_r == 0 or tgt_r == 7)
            if is_promo: board[tgt_r][tgt_c] = 900 if moving_piece > 0 else -900

            evaluation, _ = minimax(board, depth - 1, alpha, beta, False, None, moved_status_dict,
                                    evaluate_board, get_valid_moves, filter_illegal_moves, is_square_attacked)
            
            board[src_r][src_c] = moving_piece
            board[tgt_r][tgt_c] = original_target

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = (src_r, src_c, tgt_r, tgt_c)
            
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
                
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for src_r, src_c, tgt_r, tgt_c in moves:
            moving_piece = board[src_r][src_c]
            original_target = board[tgt_r][tgt_c]
            
            board[tgt_r][tgt_c] = moving_piece
            board[src_r][src_c] = 0
            
            is_promo = abs(moving_piece) == 100 and (tgt_r == 0 or tgt_r == 7)
            if is_promo: board[tgt_r][tgt_c] = 900 if moving_piece > 0 else -900

            evaluation, _ = minimax(board, depth - 1, alpha, beta, True, None, moved_status_dict,
                                    evaluate_board, get_valid_moves, filter_illegal_moves, is_square_attacked)
            
            board[src_r][src_c] = moving_piece
            board[tgt_r][tgt_c] = original_target

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = (src_r, src_c, tgt_r, tgt_c)
                
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
                
        return min_eval, best_move
