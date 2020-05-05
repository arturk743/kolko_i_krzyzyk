import pygame
from grid import Grid
import threading
import os
import socket
from communication import Communication


class Player:
    HOST = '127.0.0.1'
    PORT = 5008
    grid = Grid()
    running = True
    player = "O"
    turn = False
    playing = 'True'
    sock = None
    try_again_me = False
    try_again_opponent = False

    def __init__(self):
        self.turn = False
        self.surface = create_board()
        self.HOST = str(Communication().client_multicast_communication())
        print(self.HOST)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        self.create_thread(self.receive_data)
        self.game()

    def resetup(self):
        self.turn = False
        self.surface = create_board()
        self.HOST = str(Communication().client_multicast_communication())
        print(self.HOST)
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        self.game()

    def create_thread(self, target):
        thread = threading.Thread(target=target, args=())
        thread.daemon = True
        thread.start()

    def receive_data(self):
        while True:
            data = self.sock.recv(1024).decode()  # receive data from the server, it is a blocking method
            data = data.split('-')
            if data[0] == '1':
                print("Get message type : " + data[0])
                self.player = data[1]
                if data[2] == 'True':
                    self.turn = True
                else:
                    self.turn = False
            elif data[0] == '2':
                print("Get message type : " + data[0])
                x, y = int(data[1]), int(data[2])
                if data[3] == 'yourturn':
                    self.turn = True
                if data[4] == 'False':
                    self.grid.game_over = True
                if self.grid.get_cell_value(x, y) == 0:
                    if self.player == "O":
                        self.grid.set_cell_value(x, y, 'X')
                    else:
                        self.grid.set_cell_value(x, y, 'O')
            elif data[0] == '3':
                print("Get message type : " + data[0])
                if data[1]:
                    self.playing = 'True'
                    self.grid.clear_grid()
                else:
                    print("Koniec gry")
            elif data[0] == '4':
                print("Get message type : " + data[0])
                if data[1] == 'True':
                    self.setup()

    def game(self):  # zmienic na play

        clock = pygame.time.Clock()  # limit and track fps
        while self.running:
            clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.grid.game_over:
                    if pygame.mouse.get_pressed()[0]:
                        if self.turn and not self.grid.game_over:
                            pos = pygame.mouse.get_pos()
                            cellX, cellY = pos[0] // 200, pos[1] // 200
                            if cellX > 2 or cellY > 2:
                                continue
                            self.grid.get_mouse(cellX, cellY, self.player)
                            if self.grid.game_over:
                                self.playing = 'False'
                            send_data = '{}-{}-{}-{}-{}'.format('2', cellX, cellY, 'yourturn', self.playing).encode()
                            self.sock.send(send_data)
                            self.turn = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.grid.game_over:
                        send_data = '{}-{}'.format('3', 'True').encode()
                        self.sock.send(send_data)
                    elif event.key == pygame.K_ESCAPE:
                        # running = False
                        self.sock.close()
                        exit(10)

            self.surface.fill((255, 255, 255))

            self.grid.draw(self.surface)

            self.button("TRY AGAIN!", 90, 625, 150, 50, (255, 100, 255), (255, 0, 255), "restart")
            self.button("EXIT", 360, 625, 150, 50, (255, 100, 255), (255, 0, 255), "exit_game")

            pygame.display.flip()

    def button(self, msg, x, y, width, height, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.surface, active_color, (x, y, width, height))

            if click[0] == 1 and action == "restart" and self.grid.game_over:
                self.grid.game_over = False
                # restart()
                send_data = '{}-{}'.format('3', 'True').encode()
                self.sock.send(send_data)
            elif click[0] == 1 and action == "exit_game":
                self.exit_game()
        else:
            pygame.draw.rect(self.surface, inactive_color, (x, y, width, height))

        smallText = pygame.font.Font(None, 25)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (width / 2)), (y + (height / 2)))
        self.surface.blit(textSurf, textRect)

    def restart(self):
        global playing
        self.grid.clear_grid()
        self.grid.game_over = False
        playing = 'True'

    def exit_game(self):
        self.sock.close()
        exit(10)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()


def create_board():
    os.environ['SDL_VIDEO_WINDOW_POS'] = '850,100'
    surface = pygame.display.set_mode((600, 700))
    surface.fill((255, 255, 255))
    pygame.init()
    pygame.display.set_caption('Tic-tac-toe')
    return surface


if __name__ == "__main__":
    player = Player()
    # Communication().client_multicast_communication()
