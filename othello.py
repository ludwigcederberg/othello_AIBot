class OthelloGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 'B'  # 'B' for Black, 'W' for White

    def initialize_board(self):
        """Initialize the board with the starting position."""
        board = [['.' for _ in range(8)] for _ in range(8)]
        board[3][3], board[4][4] = 'W', 'W'
        board[3][4], board[4][3] = 'B', 'B'
        return board

    def print_board(self):
        """Display the current board."""
        print("  " + " ".join(map(str, range(8))))
        for i, row in enumerate(self.board):
            print(i, " ".join(row))
        print()

    def is_valid_move(self, row, col, player):
        """Check if a move is valid for the current player."""
        if self.board[row][col] != '.':
            return False
        
        opponent = 'B' if player == 'W' else 'W'
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            has_opponent_between = False
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == opponent:
                    has_opponent_between = True
                elif self.board[r][c] == player:
                    if has_opponent_between:
                        return True
                    break
                else:
                    break
                r += dr
                c += dc
        return False

    def get_valid_moves(self, player):
        """Get all valid moves for the current player."""
        return [(r, c) for r in range(8) for c in range(8) if self.is_valid_move(r, c, player)]

    def make_move(self, row, col, player):
        """Make a move and flip pieces."""
        if not self.is_valid_move(row, col, player):
            return False

        self.board[row][col] = player
        opponent = 'B' if player == 'W' else 'W'
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                for rr, cc in pieces_to_flip:
                    self.board[rr][cc] = player

        return True

    def is_game_over(self):
        """Check if the game is over."""
        return not self.get_valid_moves('B') and not self.get_valid_moves('W')
    
    def evaluate_board(self, player):
        opponent = 'B' if player == 'W' else 'W'
        bot_score = sum(row.count(player) for row in self.board)
        opp_score = sum(row.count(opponent) for row in self.board)
        return bot_score - opp_score

    def minimax(self, depth, maximizing_player):
        """
        Placeholder for the minimax algorithm.
        To be implemented to determine the best move for the bot.
        """
        self.evaluate_board(maximizing_player)
        pass
    
            
        

    def play(self):
        """Main game loop."""
        while not self.is_game_over():
            self.print_board()
            valid_moves = self.get_valid_moves(self.current_player)
            if not valid_moves:
                print(f"No valid moves for {self.current_player}. Skipping turn.")
                self.current_player = 'B' if self.current_player == 'W' else 'W'
                continue

            if self.current_player == 'B':  # Human player (can be swapped for bot)
                print(f"{self.current_player}'s turn. Valid moves: {valid_moves}")
                row, col = map(int, input("Enter your move (row col): ").split())
                if (row, col) in valid_moves:
                    self.make_move(row, col, self.current_player)
                    self.current_player = 'B' if self.current_player == 'W' else 'W'
                else:
                    print("Invalid move. Try again.")
            else:  # Bot's turn
                print(f"{self.current_player}'s turn (Bot).")
                # Placeholder for bot's move using minimax
                row, col = valid_moves[0]  # Temporary: choosing the first valid move
                #row, col = self.minimax(0, maximizing_player=True)
                self.make_move(row, col, self.current_player)
                self.current_player = 'B' if self.current_player == 'W' else 'W'

        self.print_board()
        print("Game over!")

# Example of running the game
if __name__ == "__main__":
    game = OthelloGame()
    game.play()
