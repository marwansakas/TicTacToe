import pygame

from Board import Board
from TicTacToe import TicTacToe


class Menu(Board):
    def __init__(self, screen, client, game):
        super().__init__(screen, client, game)

        # UI Constants
        self.WIDTH, self.HEIGHT = 400, 600
        self.BG_COLOR = (30, 30, 30)
        self.TEXT_COLOR = (200, 200, 200)

        # Pygame setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.font = pygame.font.Font(None, 30)

        # Input box setup
        self.input_box = pygame.Rect(50, 10, 200, 30)
        self.connect_button = pygame.Rect(260, 10, 80, 30)
        self.new_game_button = pygame.Rect(50, 60, 290, 40)

        self.user_text = ""
        self.active = False
        self.button_clicked = False

    def handle_click(self, event):
        if event.type == pygame.QUIT:
            self.game.set_running(False)
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.join_room(self.user_text)
                    self.user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.input_box.collidepoint(mouse_x, mouse_y):
                self.active = True
            else:
                self.active = False

            if self.connect_button.collidepoint(mouse_x, mouse_y):
                self.join_room(self.user_text)
            elif self.new_game_button.collidepoint(mouse_x, mouse_y):
                self.handle_new_game()

    def handle_new_game(self):
        self.client.send("MENU CREATE TICTACTOE".encode())

    def join_room(self, room_name):
        if room_name:
            self.client.send(f"MENU JOIN {room_name}".encode())
            self.user_text = ""

    def receive_server_message(self, message):
        messages = message.split(' ')
        OPCODE = messages[0]
        roomID = messages[2]
        if OPCODE == 'CREATE' and messages[1] == 'TICTACTOE':
            self.game.set_board(TicTacToe(self.screen, self.client, self.game, 'X', roomID))
        elif OPCODE == 'JOIN' and messages[1] == 'TICTACTOE':
            self.game.set_board(TicTacToe(self.screen, self.client, self.game, 'O', roomID))
        elif OPCODE == 'ERROR':
            print("Error:", message)

    def draw_board(self):
        self.screen.fill(self.BG_COLOR)

        # Draw input box
        pygame.draw.rect(self.screen, (200, 200, 200), self.input_box, 2)
        text_surface = self.font.render(self.user_text, True, self.TEXT_COLOR)
        self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Draw "Connect" button
        pygame.draw.rect(self.screen, (50, 150, 50), self.connect_button)
        button_text = self.font.render("Connect", True, self.TEXT_COLOR)
        self.screen.blit(button_text, (self.connect_button.x + 10, self.connect_button.y + 5))

        # Draw "New Game" button
        pygame.draw.rect(self.screen, (0, 120, 200), self.new_game_button)
        new_game_text = self.font.render("New Game", True, self.TEXT_COLOR)
        self.screen.blit(new_game_text, (self.new_game_button.x + 90, self.new_game_button.y + 5))

        pygame.display.flip()
