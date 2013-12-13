__author__ = 'craig'

import pygame

class GameController():
    def __init__(self, initial):

        self.gamebuttons = pygame.sprite.Group()
        #adjust the size of the controller button.
        size = 100
        screen = initial.phone_rect.copy()

        self.gamebuttons.add(GameButton("left",
                            pygame.Surface((size, screen.height - size *2)),
                            pygame.Rect(0, size, size, screen.height - size *2)))

        self.gamebuttons.add(GameButton("right",
                                        pygame.Surface((size,
                                                       screen.height - size * 2)),
                                        pygame.Rect(screen.width - size,
                                                    size,
                                                    size,
                                                    screen.height - size * 2)))

        self.gamebuttons.add(GameButton("up",
                                        pygame.Surface((screen.width -
                                                       size * 2, size)),
                                        pygame.Rect(size,
                                                    0,
                                                    screen.width -
                                                    size * 2, size)))

        self.gamebuttons.add(GameButton("down",
                                        pygame.Surface((screen.width - size * 2, size)),
                                        pygame.Rect(size, screen.height - size,
                                screen.width - size * 2, size)))

        # color of controller.  It is hidden by default
        blue = (0, 0, 255)

        for button in self.gamebuttons:
            button.image.fill(blue)
            button.image.set_alpha(40)

class GameButton(pygame.sprite.Sprite):
    def __init__(self, name, image, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect
        self.name = name