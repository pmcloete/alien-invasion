import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pressed = 0
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            break
        elif event.type == pygame.KEYDOWN:
            pressed += 1
            print(f"A key was pressed...{pressed}")
            print(pygame.key.get_pressed)
            if event.key == pygame.K_q:
                sys.exit()
                break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('The mouse was clicked')
            print(pygame.mouse.get_pos())
            print(pygame.mouse.get_pressed()[0] == True)

    screen.fill((122, 10, 19))
    pygame.display.flip()
