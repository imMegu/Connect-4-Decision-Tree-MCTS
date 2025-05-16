from math import sqrt, log
import random

class Node:
    __slots__ = ['parent', 'move', 'children', 'wins', 'visits']
        
    def __init__(self, parent, move):
        self.parent = parent  # Node
        self.move = move  # move that led to this state
        self.children = {}  # Nodes
        self.wins = 0
        self.visits = 0

    def ucb_score(self, exploration_weight=5):
        if self.visits == 0:
            return float('inf')

        return (self.wins / self.visits) + exploration_weight * sqrt(log(self.parent.visits) / self.visits)

    def expand(self, bitboard):
        children = {Node(self, move) for move in bitboard.get_legal_moves()}
        self.children = children
        return random.choice(list(children))

class MCTS:

    def __init__(self, iterations):
        self.iterations = iterations

    def select(self, root, state):
        node = root
        while node.children: 
            node = max(node.children, key=lambda c: c.ucb_score())
            state.make_move(node.move)
        return node, state


    def simulate(self, state):
        moves = state.get_legal_moves()
        while moves:
            move = random.choice(moves)
            state.make_move(move)
            if state.is_over():
                break
            moves = state.get_legal_moves()
        if state.check_player_win(1): return 1
        if state.check_player_win(2): return 2
        return 0
        

    def backpropagate(self, winner, node, state):

        reward = 0 if state.current_player == winner else 1

        while node is not None:
            node.visits += 1
            if winner == 0:
                reward = 0
            else:
                node.wins += reward
                reward = 1 - reward
            node = node.parent


    def search(self, bitboard):
        root = Node(None, None)
        root.expand(bitboard);

        for _ in range(self.iterations):

            state = bitboard.copy()

            leaf, state = self.select(root, state)
            
            # only simulate if its not terminal state
            if not state.is_over():
                leaf = leaf.expand(state)
                state.make_move(leaf.move)
            
            winner = self.simulate(state.copy())
            
            self.backpropagate(winner, leaf, state)

        # stats for the display
        arr = [0] * 14
        for child in root.children:
            arr[child.move] = child.visits
            arr[7+child.move] = child.wins
    
        # return the child with MOST VISITS, we don't use winrate here
        return max(root.children, key=lambda c: c.visits).move, arr
