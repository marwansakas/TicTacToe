import pygame

import socket
import threading

from TicTacToe import TicTacToe
from Menu import Menu


def receive_messages(game):
    while True:
        try:
            message = game.client.recv(1024).decode()
            print(f"Received: {message}")
            game.board.receive_server_message(message)
        except Exception as e:
            print(e)
            print("Connection closed.")
            break

class Game:


    def __init__(self,screen,client,board = None):
        self.screen = screen
        self.board = board
        self.client = client
        self.running = False

    def set_board(self,board = None):
        if board is not None:
            self.board = board
        else:
            self.board = Menu(self.screen,self.client,self)
    def set_running(self,running):
        self.running = running


    def run(self):



        self.running = True

        # Initialize Pygame before creating the game instance
        pygame.init()
        screen = pygame.display.set_mode((400, 500))

        self.board = Menu(screen, self.client,self)

        threading.Thread(target=receive_messages, args=((self,)), daemon=True).start()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.handle_click(event)
                elif event.type == pygame.KEYDOWN and isinstance(self.board, Menu):
                    self.board.handle_keypress(event)

            self.board.draw_board()

        pygame.quit()
        print("\nDisconnecting from server...")
        self.client.close()



