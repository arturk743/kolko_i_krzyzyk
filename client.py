#utworzyc klase player, rozwiaze problem zmiennych globalnych

import pygame
from grid import Grid
import threading
import os
import socket

HOST = '127.0.0.1'
PORT = 65432
grid = Grid()
running = True
player = "O"
turn = False
playing = 'True'
sock = None


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


def receive_data():
    global turn, player, sock, playing, grid
    while True:
        data = sock.recv(1024).decode()  # receive data from the server, it is a blocking method
        data = data.split('-')
        if data[0] == '1':
            print("Get message type : " + data[0])
            player = data[1]
            if data[2] == 'True':
                turn = True
            else:
                turn = False
        elif data[0] == '2':
            print("Get message type : " + data[0])
            x, y = int(data[1]), int(data[2])
            if data[3] == 'yourturn':
                turn = True
            if data[4] == 'False':
                grid.game_over = True
            if grid.get_cell_value(x, y) == 0:
                if player == "O":
                    grid.set_cell_value(x, y, 'X')
                else:
                    grid.set_cell_value(x, y, 'O')
        elif data[0] == '3':
            print("Get message type : " + data[0])
            if data[1] == True:
                grid.clear_grid()
                grid.game_over = False
                playing = 'True'
                if data[2] == 'True':
                    send_data = '{}-{}-{}'.format('3', 'True', 'False').encode()
                    sock.send(send_data)




def game(): #zmienic na play
    global turn
    global running
    global player
    global turn
    global playing
    clock = pygame.time.Clock()  # limit and track fps

    while running:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
                if pygame.mouse.get_pressed()[0]:
                    if turn and not grid.game_over:
                        pos = pygame.mouse.get_pos()
                        cellX, cellY = pos[0] // 200, pos[1] // 200
                        grid.get_mouse(cellX, cellY, player)
                        if grid.game_over:
                            playing = 'False'
                        send_data = '{}-{}-{}-{}-{}'.format('2',cellX, cellY, 'yourturn', playing).encode()
                        sock.send(send_data)
                        turn = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and grid.game_over:
                    send_data = '{}-{}-{}'.format('3', 'True', 'True').encode()
                    sock.send(send_data)
                elif event.key == pygame.K_ESCAPE:
                    # running = False
                    sock.close()
                    exit(10)

        surface.fill((255, 255, 255))

        grid.draw(surface)

        button("TRY AGAIN!", 90, 625, 150, 50, (255, 100, 255), (255, 0, 255), "restart")
        button("EXIT", 360, 625, 150, 50, (255, 100, 255), (255, 0, 255), "exit_game")

        pygame.display.flip()


def button(msg, x, y, width, height, inactive_color, active_color, action=None):
    global grid
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, active_color, (x, y, width, height))

        if click[0] == 1 and action == "restart" and grid.game_over:
            restart()
        elif click[0] == 1 and action == "exit_game" and grid.game_over:
            exit_game()
    else:
        pygame.draw.rect(surface, inactive_color, (x, y, width, height))

    smallText = pygame.font.Font(None, 25)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    surface.blit(textSurf, textRect)


def restart():
    global playing
    grid.clear_grid()
    grid.game_over = False
    playing = 'True'


def exit_game():
    # global running
    # running = False
    sock.close()
    exit(10)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


if __name__ == "__main__":
    turn = False
    os.environ['SDL_VIDEO_WINDOW_POS'] = '850,100'

    surface = pygame.display.set_mode((600, 700))
    surface.fill((255, 255, 255))
    pygame.init()
    pygame.display.set_caption('Tic-tac-toe')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # run the blocking functions in a separate thread
    create_thread(receive_data)

    game()
