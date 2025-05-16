class Bitboard:
    def __init__(self):
        self.player1 = 0
        self.player2 = 0
        self.height = [0] * 7
        self.current_player = 1

    # 05 12 19 26 33 40 47
    # 04 11 18 25 32 39 46
    # 03 10 17 24 31 38 45
    # 02 09 16 23 30 37 44
    # 01 08 15 22 29 36 43 
    # 00 07 14 21 28 35 42

    def make_move(self, col):
        
        if col == -1: return

        if self.height[col] >= 6:
            return False

        # Get position
        row = self.height[col]
        bit_position = col * 7 + row

        # Update bitboard
        if self.current_player == 1:
            self.player1 |= (1 << bit_position)
        else:
            self.player2 |= (1 << bit_position)

        # Update heightmap
        self.height[col] += 1

        # Switch to other player1
        self.current_player = 3 - self.current_player
        return True

    def check_player_win(self, player):
        # Diagonal \
        if player == 1:
            board = self.player1
        else:
            board = self.player2

        y = board & (board >> 6)
        if (y & (y >> 2 * 6)):
            return True
        
        # Horizontal
        y = board & (board >> 7)
        if (y & (y >> 2 * 7)):
            return True

        # Diagonal /
        y = board & (board >> 8)
        if (y & (y >> 2 * 8)):
            return True

        # Vertical
        y = board & (board >> 1)
        if (y & (y >> 2)):      
            return True
        return False

    def get_legal_moves(self):
        return [col for col in range(7) if self.height[col] < 6]
    
    def is_over(self):
        return self.check_player_win(1) or self.check_player_win(2) or all(h == 6 for h in self.height)

    def copy(self): # returns deep copy of self
        new_bitboard = Bitboard()
        new_bitboard.player1 = self.player1
        new_bitboard.player2 = self.player2
        new_bitboard.height = self.height.copy()
        new_bitboard.current_player = self.current_player
        return new_bitboard

    def matrix(self):

        matrix = [[0] * 7 for _ in range(6)]

        for bit_position in range(48):
            row = bit_position // 7  
            col = bit_position % 7

            # Check if the bit is set in player1's bitboard
            if self.player1 & (1 << bit_position):
                matrix[col][row] = 1
            # Check if the bit is set in player2's bitboard
            elif self.player2 & (1 << bit_position):
                matrix[col][row] = 2

        return matrix

    def __str__(self):
        # Print the matrix in a readable format
        matrix = self.matrix()
        resul = ""
        for row in matrix:
            for cell in row:
                if cell == 0:
                    resul += "- "
                elif cell == 1:
                    resul += "X "
                elif cell == 2:
                    resul += "O "
            resul += "\n"
        return resul
