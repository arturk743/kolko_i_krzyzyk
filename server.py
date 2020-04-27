import pygame
from grid import Grid

import os


os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'

surface = pygame.display.set_mode((600, 700))
surface.fill((255, 255, 255))
pygame.init()
pygame.display.set_caption('Tic-tac-toe')

# create a separate thread to send and receive data from the client
import threading


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


# creating a TCP socket for the server
import socket

HOST = '127.0.0.1'
PORT = 65432
connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)


def receive_data():
    global turn
    while True:
        data = conn.recv(1024).decode()  # receive data from the client, it is a blocking method
        data = data.split('-')  # the format of the data after splitting is: ['x', 'y', 'yourturn', 'playing']
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'O')


def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept()  # wait for a connection, it is a blocking method
    print('client is connected')
    connection_established = True
    receive_data()


def button( msg, x, y, width, height, inactive_color, active_color, action=None):
    global grid
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, active_color, (x, y, width, height))

        if click[0] == 1 and action == "restart" and grid.game_over:
            restart()
        elif click[0] == 1 and action == "quit" and grid.game_over:
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
    global running
    running = False


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


# run the blocking functions in a separate thread
create_thread(waiting_for_connection)

grid = Grid()
running = True
player = "X"
turn = True
playing = 'True'

clock = pygame.time.Clock()  # limit and track fps

while running:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing).encode()
                    conn.send(send_data)
                    turn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = 'True'
            elif event.key == pygame.K_ESCAPE:
                running = False

    surface.fill((255, 255, 255))

    grid.draw(surface)

    button("TRY AGAIN!", 90, 625, 150, 50, (255, 100, 255), (255, 0, 255), "restart")
    button("EXIT", 360, 625, 150, 50, (255, 100, 255), (255, 0, 255), "quit")

    pygame.display.flip()
