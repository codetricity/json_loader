__author__ = 'craig'
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, center, filename):
        pygame.sprite.Sprite.__init__(self)

        try:
            self.image = pygame.image.load(filename).convert_alpha()
        except IOError:
            print("Cannot find player file {}".format(filename))
        self.rect = self.image.get_rect()
        self.rect.center = center