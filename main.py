import tkinter as tk
from tkinter import messagebox
import random
from tkinter import font as tkfont

class ModernTicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Tic-Tac-Toe")
        self.root.config(bg="#121212")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Custom fonts
        self.title_font = ("Segoe UI", 32, "bold")
        self.button_font = ("Segoe UI", 14)
        self.board_font = ("Segoe UI", 36, "bold")
        self.status_font = ("Segoe UI", 16, "bold")
        
        # Game variables
        self.player_symbol = "O"
        self.ai_symbol = "X"
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        self.buttons = []
        self.board = []
        self.turn = "Player"
        self.game_active = False
        self.controls_frame = None
        self.status_label = None
        self.score_label = None
        self.difficulty = "Hard"  # Default difficulty
        self.first_turn = "Player"  # Track who starts first
        
        # Animation variables
        self.animating = False
        self.animation_sequence = []
        self.current_animation_index = 0
        
        # Sound effects
        self.sound_enabled = True
        
        self.create_main_menu()
    
    def create_main_menu(self):
        self.clear_screen()
        self.game_active = False
        
        # Main title
        tk.Label(self.root, text="Tic-Tac-Toe AI", font=self.title_font, 
                bg="#121212", fg="#4CAF50").pack(pady=(40, 20))
        
        # Menu buttons frame
        menu_frame = tk.Frame(self.root, bg="#121212")
        menu_frame.pack(pady=20)
        
        # Player first button
        player_first_btn = tk.Button(menu_frame, text="Human vs AI (You first)", font=self.button_font, 
                                    bg="#333333", fg="#FFFFFF", activebackground="#4CAF50",
                                    width=25, height=2, command=lambda: self.start_game("Player"))
        player_first_btn.pack(pady=10)
        
        # AI first button
        ai_first_btn = tk.Button(menu_frame, text="AI vs Human (AI first)", font=self.button_font, 
                                bg="#333333", fg="#FFFFFF", activebackground="#F44336",
                                width=25, height=2, command=lambda: self.start_game("AI"))
        ai_first_btn.pack(pady=10)
        
        # Settings button
        settings_btn = tk.Button(menu_frame, text="Settings", font=self.button_font, 
                                bg="#333333", fg="#FFFFFF", activebackground="#2196F3",
                                width=25, height=2, command=self.show_settings)
        settings_btn.pack(pady=10)
        
        # Footer
        tk.Label(self.root, text="By Sairaj Naikwade", font=("Arial", 10), 
                bg="#121212", fg="#444").pack(side="bottom", pady=10)
    
    def show_settings(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Game Settings", font=self.title_font, 
                bg="#121212", fg="#2196F3").pack(pady=(40, 20))
        
        settings_frame = tk.Frame(self.root, bg="#121212")
        settings_frame.pack(pady=20)
        
        # Symbol selection
        tk.Label(settings_frame, text="Choose Your Symbol:", font=self.button_font, 
                bg="#121212", fg="#FFFFFF").pack(pady=10)
        
        symbol_frame = tk.Frame(settings_frame, bg="#121212")
        symbol_frame.pack()
        
        self.symbol_var = tk.StringVar(value=self.player_symbol)
        tk.Radiobutton(symbol_frame, text="X", font=self.button_font, variable=self.symbol_var, 
                      value="X", bg="#121212", fg="#FFFFFF", selectcolor="#333333", 
                      activebackground="#121212").pack(side="left", padx=10)
        tk.Radiobutton(symbol_frame, text="O", font=self.button_font, variable=self.symbol_var, 
                      value="O", bg="#121212", fg="#FFFFFF", selectcolor="#333333", 
                      activebackground="#121212").pack(side="left", padx=10)
        
        # Difficulty selection
        tk.Label(settings_frame, text="AI Difficulty:", font=self.button_font, 
                bg="#121212", fg="#FFFFFF").pack(pady=10)
        
        difficulty_frame = tk.Frame(settings_frame, bg="#121212")
        difficulty_frame.pack()
        
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulties = ["Easy", "Medium", "Hard"]
        for diff in difficulties:
            tk.Radiobutton(difficulty_frame, text=diff, font=self.button_font, variable=self.difficulty_var, 
                          value=diff, bg="#121212", fg="#FFFFFF", selectcolor="#333333", 
                          activebackground="#121212").pack(side="left", padx=10)
        
        # Sound toggle
        self.sound_var = tk.IntVar(value=int(self.sound_enabled))
        tk.Checkbutton(settings_frame, text="Enable Sound Effects", font=self.button_font, 
                      variable=self.sound_var, bg="#121212", fg="#FFFFFF", 
                      selectcolor="#333333", activebackground="#121212").pack(pady=10)
        
        # Save button
        tk.Button(settings_frame, text="Save Settings", font=self.button_font, 
                bg="#333333", fg="#FFFFFF", activebackground="#4CAF50",
                width=20, height=2, command=self.save_settings).pack(pady=20)
        
        # Back button
        tk.Button(settings_frame, text="Back to Menu", font=self.button_font, 
                bg="#333333", fg="#FFFFFF", activebackground="#F44336",
                width=20, height=2, command=self.create_main_menu).pack(pady=10)
    
    def save_settings(self):
        self.player_symbol = self.symbol_var.get()
        self.ai_symbol = "X" if self.player_symbol == "O" else "O"
        self.sound_enabled = bool(self.sound_var.get())
        self.difficulty = self.difficulty_var.get()
        self.create_main_menu()
    
    def play_sound(self, sound_type):
        if self.sound_enabled:
            try:
                import winsound
                if sound_type == "move":
                    winsound.Beep(800, 100)
                elif sound_type == "win":
                    winsound.Beep(1000, 300)
                elif sound_type == "lose":
                    winsound.Beep(400, 300)
                elif sound_type == "draw":
                    winsound.Beep(600, 200)
                    winsound.Beep(500, 200)
            except:
                pass
    
    def start_game(self, first_turn):
        self.clear_screen()
        self.game_active = True
        self.first_turn = first_turn
        self.turn = first_turn
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Header with symbols and scores
        header_frame = tk.Frame(self.root, bg="#121212")
        header_frame.pack(pady=(10, 5))
        
        title = f"You: {self.player_symbol}   AI: {self.ai_symbol} (Difficulty: {self.difficulty})"
        tk.Label(header_frame, text=title, font=self.button_font, 
               bg="#121212", fg="#4CAF50").pack(side="left", padx=10)
        
        self.score_label = tk.Label(header_frame, 
                                  text=f"Score: You {self.player_score} - {self.ai_score} AI | Draws: {self.draws}", 
                                  font=("Segoe UI", 12), bg="#121212", fg="#BBBBBB")
        self.score_label.pack(side="right", padx=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="", font=self.status_font, 
                                   bg="#121212", fg="#FFFFFF")
        self.status_label.pack(pady=5)
        
        # Main game board frame
        board_frame = tk.Frame(self.root, bg="#121212")
        board_frame.pack(pady=15)
        
        # Create board buttons with hover effects
        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=self.board_font, 
                              width=3, height=1, bg="#222222", fg="#4CAF50",
                              activebackground="#333333", relief="flat",
                              command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5, ipadx=10, ipady=10)
                
                # Add hover effects
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#333333") if self.game_active else None)
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#222222") if self.game_active else None)
                
                self.buttons[i][j] = btn
        
        # Controls frame
        self.controls_frame = tk.Frame(self.root, bg="#121212")
        self.controls_frame.pack(side="bottom", fill="x", pady=(20, 10))
        
        # Control buttons
        btn_reset = tk.Button(self.controls_frame, text="New Game", font=self.button_font,
                            bg="#333333", fg="#FFFFFF", activebackground="#4CAF50",
                            width=12, height=1, command=self.reset_game)
        btn_menu = tk.Button(self.controls_frame, text="Main Menu", font=self.button_font,
                           bg="#333333", fg="#FFFFFF", activebackground="#2196F3",
                           width=12, height=1, command=self.create_main_menu)
        btn_quit = tk.Button(self.controls_frame, text="Quit", font=self.button_font,
                           bg="#333333", fg="#FFFFFF", activebackground="#F44336",
                           width=12, height=1, command=self.root.quit)
        
        btn_reset.pack(side="left", padx=10, ipady=5)
        btn_menu.pack(side="left", padx=10, ipady=5)
        btn_quit.pack(side="left", padx=10, ipady=5)
        
        self.update_status()
        
        # If AI goes first, make the move after a slight delay
        if self.turn == "AI":
            self.root.after(800, self.ai_move)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def reset_game(self):
        # Reset the game while keeping scores and settings
        self.start_game(self.first_turn)
    
    def player_move(self, r, c):
        if not self.animating and self.board[r][c] == "" and self.turn == "Player" and self.game_active:
            self.board[r][c] = self.player_symbol
            self.buttons[r][c].config(text=self.player_symbol, state="disabled", 
                                     disabledforeground="#4CAF50", bg="#222222")
            self.play_sound("move")
            
            winner = self.check_winner()
            if winner:
                self.end_game(winner)
            elif self.is_draw():
                self.end_game("Draw")
            else:
                self.turn = "AI"
                self.update_status()
                self.root.after(800, self.ai_move)
    
    def ai_move(self):
        if self.turn != "AI" or not self.game_active or self.animating:
            return
            
        move = self.get_ai_move()
        if move:
            r, c = move
            self.board[r][c] = self.ai_symbol
            self.buttons[r][c].config(text=self.ai_symbol, state="disabled", 
                                      disabledforeground="#F44336", bg="#222222")
            self.play_sound("move")
            
            winner = self.check_winner()
            if winner:
                self.end_game(winner)
            elif self.is_draw():
                self.end_game("Draw")
            else:
                self.turn = "Player"
                self.update_status()
    
    def get_ai_move(self):
        if self.difficulty == "Easy":
            return self.easy_ai_move()
        elif self.difficulty == "Medium":
            return self.medium_ai_move()
        else:  # Hard
            return self.best_ai_move()
    
    def easy_ai_move(self):
        # Random moves
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(empty) if empty else None
    
    def medium_ai_move(self):
        # 50% chance to make a smart move, 50% random
        if random.random() < 0.5:
            # Try to win if possible
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = self.ai_symbol
                        if self.check_winner_simple() == self.ai_symbol:
                            self.board[i][j] = ""
                            return (i, j)
                        self.board[i][j] = ""
            
            # Block player if they can win
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = self.player_symbol
                        if self.check_winner_simple() == self.player_symbol:
                            self.board[i][j] = ""
                            return (i, j)
                        self.board[i][j] = ""
        
        # Otherwise make a random move
        return self.easy_ai_move()
    
    def best_ai_move(self):
        # Minimax algorithm for unbeatable AI
        best_score = -float("inf")
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = self.ai_symbol
                    score = self.minimax(False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move
    
    def minimax(self, is_max):
        winner = self.check_winner_simple()
        if winner == self.ai_symbol:
            return 1
        if winner == self.player_symbol:
            return -1
        if self.is_draw():
            return 0
        
        scores = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = self.ai_symbol if is_max else self.player_symbol
                    score = self.minimax(not is_max)
                    self.board[i][j] = ""
                    scores.append(score)
        return max(scores) if is_max else min(scores)
    
    def update_status(self):
        if self.turn == "Player":
            self.status_label.config(text="Your Turn", fg="#4CAF50")
        else:
            self.status_label.config(text="AI Thinking...", fg="#F44336")
    
    def end_game(self, winner):
        self.game_active = False
        
        # Update scores
        if winner == self.player_symbol:
            self.player_score += 1
            self.play_sound("win")
            self.status_label.config(text="You Win! 🎉", fg="#4CAF50")
            messagebox.showinfo("Game Over", "Congratulations! You won!")
        elif winner == self.ai_symbol:
            self.ai_score += 1
            self.play_sound("lose")
            self.status_label.config(text="AI Wins! 🤖", fg="#F44336")
            messagebox.showinfo("Game Over", "The AI won this round!")
        else:
            self.draws += 1
            self.play_sound("draw")
            self.status_label.config(text="Game Draw! 🤝", fg="#2196F3")
            messagebox.showinfo("Game Over", "It's a draw!")
        
        # Update score display
        self.score_label.config(text=f"Score: You {self.player_score} - {self.ai_score} AI | Draws: {self.draws}")
        
        # Disable all buttons
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")
    
    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))
    
    def check_winner(self):
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                self.highlight_winning_cells([(i, 0), (i, 1), (i, 2)])
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                self.highlight_winning_cells([(0, i), (1, i), (2, i)])
                return self.board[0][i]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.highlight_winning_cells([(0, 0), (1, 1), (2, 2)])
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.highlight_winning_cells([(0, 2), (1, 1), (2, 0)])
            return self.board[0][2]
        
        return None
    
    def highlight_winning_cells(self, cells):
        self.animating = True
        self.animation_sequence = cells
        self.current_animation_index = 0
        self.animate_winning_cells()
    
    def animate_winning_cells(self):
        if self.current_animation_index < len(self.animation_sequence):
            i, j = self.animation_sequence[self.current_animation_index]
            current_bg = self.buttons[i][j].cget("bg")
            
            # Alternate between highlight color and original color
            if current_bg == "#222222" or current_bg == "#333333":
                self.buttons[i][j].config(bg="#4CAF50" if self.board[i][j] == self.player_symbol else "#F44336")
            else:
                self.buttons[i][j].config(bg="#222222")
            
            self.current_animation_index += 1
            self.root.after(200, self.animate_winning_cells)
        else:
            if self.current_animation_index == len(self.animation_sequence):
                # Restart the animation
                self.current_animation_index = 0
                self.root.after(200, self.animate_winning_cells)
            else:
                self.animating = False
    
    def check_winner_simple(self):
        # Simplified version without animation for AI calculations
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        
        return None

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("tic_tac_toe.ico")  # You can provide an icon file
    except:
        pass
    ModernTicTacToeAI(root)
    root.mainloop()
