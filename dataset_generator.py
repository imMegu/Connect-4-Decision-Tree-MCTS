import csv
import random
from tqdm import tqdm
from game import Bitboard
from mcts import MCTS
import multiprocessing as mp
from multiprocessing import Pool
import os

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

def worker_process(args):
    """Worker function that generates a single game sample"""
    mcts_iterations, min_random_moves, max_random_moves, process_id = args
    # Create MCTS instance per process to avoid sharing issues
    mcts = MCTS(mcts_iterations)
    
    board = Bitboard()
    # Make 0 to k random moves
     
    for _ in range(random.randint(min_random_moves, max_random_moves)):
        legal = board.get_legal_moves()
        if not legal or board.is_over():
            return (None, True)
        board.make_move(random.choice(legal))
    
    if board.is_over(): return (None, True)

    encoded = encode_board(board)
    move, _ = mcts.search(board.copy())
    return (encoded + [move], False)

def generate_dataset_parallel(n_games=1000, batch_size=500, mcts_iterations=10000, min_random_moves=8, max_random_moves=25):
    # Determine number of CPU cores to use e
    num_processes = mp.cpu_count()
    completed = 0
    terminated_early = 0

    # Create a pool of worker processes e
    with Pool(processes=num_processes) as pool:
        # Prepare arguments for each worker
        worker_args = [(mcts_iterations, min_random_moves, max_random_moves, i) for i in range(n_games)]
        
        # Open the output file  
        with open("dataset.csv", 'a', newline='') as f:
            writer = csv.writer(f)  
            if f.tell() == 0:  # File is empty
                writer.writerow([f"pos_{i}" for i in range(42)] + ["move"])
            
            buffer = []
            buffer_size = 0
            
            # Use imap_unordered for faster results as they become available
            with tqdm(total=n_games, desc="Generating Examples") as pbar:
                for result in pool.imap_unordered(worker_process, worker_args):
                    if result[1]: terminated_early += 1
                    elif result[0] is not None:

                        completed += 1

                        buffer.append(result[0])
                        buffer_size += 1
                        # Write in batches
                        if buffer_size >= batch_size:
                            writer.writerows(buffer)
                            buffer.clear()
                            buffer_size = 0


                    pbar.update(1)

                # Write remaining samples
                if buffer:
                    writer.writerows(buffer)

    print(f"Completed games: {completed} ({completed/n_games:.1%})")
    print(f"Terminated Early: {terminated_early} ({terminated_early/n_games:.1%})")

if __name__ == '__main__':
    # Required for Windows multiprocessing support
    generate_dataset_parallel(n_games=180000, batch_size=1000, min_random_moves=10, max_random_moves=30)
