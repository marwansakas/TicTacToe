import pygame
import time

from Board import Board
from Client.socket_functions import send_message


class TicTacToe(Board):
    def __init__(self, screen, client, game, player, roomID):
        super().__init__(screen, client, game)
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
        self.game_over = False

        # Fonts
        self.font = pygame.font.Font(None, 60)
        self.text_font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 20)

        # Game Info
        self.current_player = "X"
        self.turn_text = "Turn: X"
        self.player = player
        self.roomID = roomID

        # Button
        self.leave_button = pygame.Rect(20, screen.get_height() - 50, 100, 30)

        # Temporary Message
        self.temp_message = None
        self.temp_message_time = 0

    def display_timed_message(self, text, position):
        self.temp_message = (text, position)
        self.temp_message_time = time.time()

    def draw_board(self):
        board_size = 300
        offset_x = (self.screen.get_width() - board_size) // 2
        offset_y = 80

        self.screen.fill((0, 150, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (offset_x, offset_y, board_size, board_size))
        pygame.draw.rect(self.screen, (0, 0, 0), (offset_x, offset_y, board_size, board_size), 5)

        for i in range(1, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (offset_x, offset_y + i * 100),
                             (offset_x + board_size, offset_y + i * 100), 3)
            pygame.draw.line(self.screen, (0, 0, 0), (offset_x + i * 100, offset_y),
                             (offset_x + i * 100, offset_y + board_size), 3)

        for r in range(3):
            for c in range(3):
                if self.grid[r][c] != " ":
                    color = (255, 0, 0) if self.grid[r][c] == "O" else (0, 0, 0)
                    text = self.font.render(self.grid[r][c], True, color)
                    text_rect = text.get_rect(center=(offset_x + c * 100 + 50, offset_y + r * 100 + 50))
                    self.screen.blit(text, text_rect)

        player_info = self.text_font.render(f"You are: {self.player}", True, (255, 255, 255))
        turn_info = self.text_font.render(f"{self.turn_text}", True, (255, 255, 255))
        self.screen.blit(player_info, (offset_x, 20))
        self.screen.blit(turn_info, (offset_x + 150, 20))

        room_surface = self.small_font.render(f"Room ID: {self.roomID}", True, (255, 255, 255))
        self.screen.blit(room_surface, (self.screen.get_width() - 100, self.screen.get_height() - 30))

        pygame.draw.rect(self.screen, (200, 0, 0), self.leave_button, border_radius=5)
        leave_text = self.small_font.render("Leave", True, (255, 255, 255))
        text_rect = leave_text.get_rect(center=self.leave_button.center)
        self.screen.blit(leave_text, text_rect)

        if self.temp_message and time.time() - self.temp_message_time < 5:
            message_surface = self.text_font.render(self.temp_message[0], True, (255, 0, 0))
            self.screen.blit(message_surface, self.temp_message[1])
        else:
            self.temp_message = None

        pygame.display.flip()

    def handle_click(self, event):
        x, y = event.pos
        offset_x = (self.screen.get_width() - 300) // 2
        offset_y = 80

        if self.leave_button.collidepoint(x, y):
            send_message(self.client, "LEAVE")
            self.game.set_board()
            return

        if self.game_over:
            self.display_timed_message("Game Is Over", (offset_x + 50, offset_y + 320))
            return

        if offset_x <= x < offset_x + 300 and offset_y <= y < offset_y + 300:
            row = (y - offset_y) // 100
            col = (x - offset_x) // 100
            if self.grid[row][col] == " " and self.current_player == self.player:
                send_message(self.client, f"PLAY {row} {col}")
            else:
                self.display_timed_message("Invalid Move!", (offset_x + 50, offset_y + 320))

    def receive_server_message(self, message):
        if not message:
            return
        parts = message.split()
        opcode = parts[0]

        if opcode == "PLAY":
            try:
                row, col, player = int(parts[1]), int(parts[2]), self.current_player
                self.grid[row][col] = player
                winner = self.check_winner()
                if winner:
                    send_message(self.client, f"END {winner}")
                    self.turn_text = f"Winner: {winner}" if winner != "Tie" else "Game is a tie!"
                    self.game_over = True
                else:
                    self.turn_text = f"Turn: {'O' if player == 'X' else 'X'}"
                    self.current_player = 'X' if player == 'O' else 'O'
            except (ValueError, IndexError):
                self.display_timed_message("Error: Invalid move data!", (50, 350))

        elif opcode == "ERROR":
            self.display_timed_message(f"Error: {message}", (50, 350))

        elif opcode == "LEAVE":
            self.turn_text = f"Player {'X' if self.player == 'O' else 'O'} has left the game. You WIN!"
            self.game_over = True

    def check_winner(self):
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] and self.grid[i][0] != " ":
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] and self.grid[0][i] != " ":
                return self.grid[0][i]

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] != " ":
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] != " ":
            return self.grid[0][2]

        if all(self.grid[r][c] != " " for r in range(3) for c in range(3)):
            return "Tie"
        return None
