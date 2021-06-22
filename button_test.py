import pygame
import sys
from button import Button
from settings import Settings


class Test:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500,500))
        self.pygame = pygame
        self.settings = Settings()
        self.button = Button(self, "play")

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.button.draw_button()
            self.pygame.display.flip()


if __name__ == '__main__':
    test = Test()
    test.main()
