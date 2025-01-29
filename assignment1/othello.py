class OthelloGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.human_player = None
        self.bot_player = None
        self.current_player = None

    position_scores = [[100, -30, 6, 2, 2, 6, -30, 100],
                        [-30, -50, 0, 0, 0, 0, -50, -30],
                        [6, 0, 0, 0, 0, 0, 0, 6],
                        [2, 0, 0, 3, 3, 0, 0, 2],
                        [2, 0, 0, 3, 3, 0, 0, 2],
                        [6, 0, 0, 0, 0, 0, 0, 6],
                        [-30, -50, 0, 0, 0, 0, -50, -30],
                        [100, -30, 6, 2, 2, 6, -30, 100]]

    def initialize_board(self):
        """Initialize the board with the standard Othello starting position."""
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

    def get_valid_moves(self, player):
        """Get all valid moves for a given player."""
        return [(r, c) for r in range(8) for c in range(8) if self.is_valid_move(r, c, player)]

    def is_valid_move(self, row, col, player):
        """Check if a move is valid for the given player."""
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

    def make_move(self, row, col, player):
        """Make a move and flip the opponent's pieces."""
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
        """Evaluate the board score for a given player."""
        opponent = 'B' if player == 'W' else 'W'
        bot_score = 0
        opp_score = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == player:
                    bot_score += self.position_scores[i][j]
                if self.board[i][j] == opponent:
                    opp_score += self.position_scores[i][j]
        return bot_score - opp_score

    def get_best_move(self, depth):
        """Find the best move for the bot using Minimax."""
        best_move = None
        best_score = float('-inf')
        valid_moves = self.get_valid_moves(self.bot_player)

        for move in valid_moves:
            temp_board = [row[:] for row in self.board]
            self.make_move(move[0], move[1], self.bot_player)
            score = self.minimax(depth - 1, False, self.human_player)
            self.board = temp_board

            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move else (-1, -1)

    def minimax(self, depth, maximizing, player, alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm with Alpha-Beta Pruning."""
        opponent = 'B' if player == 'W' else 'W'
        valid_moves = self.get_valid_moves(player)

        if depth == 0 or self.is_game_over():
            return self.evaluate_board(self.bot_player)

        if not valid_moves:
            return self.minimax(depth - 1, not maximizing, opponent, alpha, beta)

        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                temp_board = [row[:] for row in self.board]
                self.make_move(move[0], move[1], player)
                eval = self.minimax(depth - 1, False, opponent, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                self.board = temp_board
                if alpha >= beta:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                temp_board = [row[:] for row in self.board]
                self.make_move(move[0], move[1], player)
                eval = self.minimax(depth - 1, True, opponent, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                self.board = temp_board
                if beta <= alpha:
                    break
            return min_eval

    def choose_player_color(self):
        """Ask the user to choose their color before starting the game."""
        while True:
            choice = input("Choose your color (B for Black, W for White): ").strip().upper()
            if choice in ['B', 'W']:
                self.human_player = choice
                self.bot_player = 'W' if choice == 'B' else 'B'
                self.current_player = 'B'  
                break
            else:
                print("Invalid choice. Please enter 'B' or 'W'.")

    def play(self):
        """Main game loop."""
        self.choose_player_color()

        while not self.is_game_over():
            self.print_board()
            valid_moves = self.get_valid_moves(self.current_player)

            if not valid_moves:
                print(f"{self.current_player} has no moves. Skipping turn.")
                self.current_player = 'B' if self.current_player == 'W' else 'W'
                continue

            if self.current_player == self.human_player:  
                print(f"Your turn ({self.current_player}). Valid moves: {valid_moves}")
                
                usr_input = input("Enter move (row col): ").split()
                
                
                
                if len(usr_input) != 2:
                    print("Invalid choice, try again")
                    continue
                

                
                row, col = map(int, usr_input)
                if (row, col) in valid_moves:
                    self.make_move(row, col, self.current_player)
                else:
                    print("Invalid choice, try again")
                    continue
            else:  
                print(f"Bot's turn ({self.bot_player}).")
                row, col = self.get_best_move(4)
                self.make_move(row, col, self.bot_player)

            self.current_player = 'B' if self.current_player == 'W' else 'W'

        self.print_board()
        w_score = sum(row.count('W') for row in self.board)
        b_score = sum(row.count('B') for row in self.board)
        
        if w_score > b_score:
            print("Game over! White won!")
        elif w_score < b_score:
            print("Game over! Black won!")
        else:
            print("Game over! It's a tie!")



if __name__ == "__main__":
    game = OthelloGame()
    game.play()
