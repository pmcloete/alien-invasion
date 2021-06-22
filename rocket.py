import pygame
import sys
import colors


BACKGROUND = colors.LIGHT_GREY
ALIEN_IMAGE = pygame.image.load('red_alien.png')
MAIN_IMAGE = pygame.image.load('background.png')
pygame.init()
screen = pygame.display.set_mode(
    (MAIN_IMAGE.get_width(), MAIN_IMAGE.get_height()))
pygame.display.set_caption("Bouncy Alien")

image_rect = ALIEN_IMAGE.get_rect()

screen_rect = screen.get_rect()
image_rect.midtop = screen_rect.midtop

game_run = True
game_loop = False
alien_move_down = False
alien_move_up = False
alien_move_left = False
alien_move_right = False

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
            sys.exit()

    screen.blit(MAIN_IMAGE, (0, 0))
    pygame.display.flip()
    game_loop += 1
    if game_loop == 1000:
        while game_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        alien_move_down = True
                    elif event.key == pygame.K_UP:
                        alien_move_up = True
                    elif event.key == pygame.K_LEFT:
                        alien_move_left = True
                    elif event.key == pygame.K_RIGHT:
                        alien_move_right = True
                    elif event.key == pygame.K_q:
                        game_run = False
                        sys.exit()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        alien_move_down = False
                    elif event.key == pygame.K_UP:
                        alien_move_up = False
                    elif event.key == pygame.K_LEFT:
                        alien_move_left = False
                    elif event.key == pygame.K_RIGHT:
                        alien_move_right = False

            if alien_move_down and image_rect.bottom < screen_rect.height:
                image_rect.y += 4
            if alien_move_up and image_rect.y > screen_rect.y:
                image_rect.y -= 4
            if alien_move_left and image_rect.x > 0:
                image_rect.x -= 4
            if alien_move_right and image_rect.right < screen_rect.width:
                image_rect.x += 4
            screen.fill(BACKGROUND)
            screen.blit(ALIEN_IMAGE, image_rect)
            pygame.display.flip()
