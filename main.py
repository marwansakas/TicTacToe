import socket

import pygame

from Game import Game
from Menu import Menu


def start_client():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    HOST = '132.73.239.231'
    PORT = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen,client)
    board = Menu(screen, client, game)
    game.set_board(board)
    game.run()

if __name__ == '__main__':
    start_client()
