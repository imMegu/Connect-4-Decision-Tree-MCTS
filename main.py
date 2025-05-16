import game
import mcts
from pygame import gfxdraw
import pygame
from os import environ
import time
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


def draw_statistics(stats):
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    my_font = pygame.font.SysFont('Helvetica', 39)
    for x in range(7):
        visits = stats[x]/iterations
        wins = stats[7+x]/iterations
        pygame.draw.rect(screen, (229, 192, 123), pygame.Rect(
            740 + 95*x, 562 - 540 * visits, 70, 540 * visits))
        pygame.draw.rect(screen, (85, 104, 79), pygame.Rect(
            740 + 95*x, 562 - 540 * wins, 70, 540 * wins))

        text_surface = my_font.render("{:.2f}".format(
            visits), True, (229, 192, 123), (39, 56, 73))
        textRect = text_surface.get_rect()
        textRect.center = (772 + 96 * x, 600)
        screen.blit(text_surface, textRect)

        text_surface = my_font.render("{:.2f}".format(
            wins), True, (85, 104, 79), (39, 56, 73))
        textRect = text_surface.get_rect()
        textRect.center = (772 + 96 * x, 640)
        screen.blit(text_surface, textRect)

        text_surface = my_font.render(
            str(x+1), True, (255, 255, 255), (39, 56, 73))
        textRect = text_surface.get_rect()
        textRect.center = (772 + 96 * x, 680)
        screen.blit(text_surface, textRect)

        draw_circle(screen, 50, 660, 20, (229, 192, 123))
        text_surface = my_font.render(
            "Visits", True, (229, 192, 123), (39, 56, 73))
        textRect = text_surface.get_rect()
        textRect.center = (120, 660)
        screen.blit(text_surface, textRect)

        draw_circle(screen, 200, 660, 20, (85, 104, 79))
        text_surface = my_font.render(
            "Wins", True, (85, 104, 79), (39, 56, 73))
        textRect = text_surface.get_rect()
        textRect.center = (270, 660)
        screen.blit(text_surface, textRect)

        text_surface = my_font.render(
            "Iterations: " + str(iterations), True, (255, 255, 255), (39, 56, 73))
        textRect = text_surface.get_rect()
        textRect.center = (525, 660)
        screen.blit(text_surface, textRect)


def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


def drawGrid(mat):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for x in range(7):
        background = (16, 27, 39)
        if (mouse_x // 100) == x:
            background = (28, 39, 51)
        for y in range(6):
            if mat[5 - y][x] == 0:
                draw_circle(screen, 100*x+60, 100*y+60, 45, background)
            elif mat[5 - y][x] == 1:
                draw_circle(screen, 100*x+60, 100*y+60, 45, (24, 188, 156))
            elif mat[5 - y][x] == 2:
                draw_circle(screen, 100*x+60, 100*y+60, 45, (238, 102, 119))


def main():
    bitboard = game.Bitboard()

    #bitboard.player1 = 0b0000000000000100010100010101001010100000000000000
    #bitboard.player2 = 0b0000000000000000001010101010000101000000010000000
    #bitboard.height = [0, 1, 5, 6, 4, 1, 0]
    #bitboard.current_player = 2
    #player_move = -1

    bitboard.player1 = 0b101110_0000001_0000100_0100111_0111000_0100110_0001011
    bitboard.player2 = 0b010001_0000110_0111011_0011000_0000111_0011001_0000100
    bitboard.height = [4,6,6,6,6,3,6]
    bitboard.current_player = 2
    player_move = -1

    global iterations
    iterations = int(input("How many iterations?: "))
    bot = mcts.MCTS(iterations)
    running = True
    global screen
    pygame.init()
    running = True
    WINDOW_HEIGHT = 6 * 100 + 20 + 100
    WINDOW_WIDTH = 7 * 100 + 20 + 680
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    stats = [0] * 14
    while not bitboard.is_over() and running:

        if bitboard.current_player == 2:
            print("AI is thinking...")
            start = time.time()
            best_move, stats = bot.search(bitboard)
            end = time.time()
            print(f"Took {end - start} seconds.")
            bitboard.make_move(best_move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player_move = mouse_x // 100
                if player_move <= 6:
                    bitboard.make_move(player_move)

        screen.fill((39, 56, 73))
        drawGrid(bitboard.matrix())
        draw_statistics(stats)
        pygame.display.update()

        if bitboard.check_player_win(1):
            print("Congratulations! You win!")
            time.sleep(4)
            return
        elif bitboard.check_player_win(2):
            print("AI wins. Better luck next time!")
            time.sleep(4)
            return
        elif bitboard.is_over():
            print("It's a draw!'")
            time.sleep(4)
            return


main()
