from abc import ABC,abstractmethod


class Board(ABC):


    def __init__(self,screen,client,game):
        self.screen = screen
        self.client = client
        self.game = game

    @abstractmethod
    def draw_board(self):
        pass

    @abstractmethod
    def handle_click(self, event):
        pass

    @abstractmethod
    def receive_server_message(self, message):
        pass