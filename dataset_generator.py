import csv
import random
from tqdm import tqdm
from game import Bitboard
from mcts import MCTS

def encode_board(board):
    # Positions of unused bits (0-based index)
    unused_bits = {5, 13, 20, 27, 34, 41}
            
    # Initialize the result array (41 positions)
    positions = [0] * 42    
    
    # Current position in the output array (0-based)
    pos_idx = 0
    
    # Iterate through all 48 bits (1-based)
    for i in range(48):
        if i in unused_bits:
            continue  # Skip unused bits
            
        p1_bit = (board.player1 >> i) & 1
        p2_bit = (board.player2 >> i) & 1
        if p1_bit:
            positions[pos_idx] = 1
        elif p2_bit:
            positions[pos_idx] = -1
  
        pos_idx += 1
    
    return positions

def generate_dataset(n_games=1000, batch_size=500, mcts_iterations=10000, max_random_moves=20):
    mcts = MCTS(mcts_iterations)
    buffer = []
    with open("connect4_dataset.csv", 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # File is empty
            writer.writerow([f"pos_{i}" for i in range(42)] + ["move"])
        for _ in tqdm(range(n_games), desc="Gerando Exemplos"):
            board = Bitboard()
            # Make 0 to k random moves
            # This gives us more state diversity, instead of always repeating board states
            k = random.randint(0, max_random_moves)

            for _ in range(k):
                if board.is_over(): break
                legal = board.get_legal_moves()
                move = random.choice(legal)
                board.make_move(move)
            
            if board.is_over(): continue

            encoded = encode_board(board)
            move, _ = mcts.search(board.copy())
            buffer.append(encoded + [move])

            if len(buffer) >= batch_size:
                writer.writerows(buffer)
                buffer.clear()

        #write remaining
        if buffer:
            writer.writerows(buffer)



generate_dataset()
