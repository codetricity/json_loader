__author__ = 'craig'

import pygame
from controller import *

class Tile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Map():
    def __init__(self, initial):
        self.initial = initial
        self.all_layers = initial.all_layers
        self.collision_layers = initial.collision_layers
        self.mapheight = initial.mapheight
        self.mapwidth = initial.mapwidth
        self.speed = 3

        topleft = self.all_layers[0][0].rect.topleft
        self.mapx = topleft[0]
        self.mapy = topleft[1]
        self.player = initial.player
        self.phone_width = initial.phone_rect.width
        self.phone_height = initial. phone_rect.height
        self.virtual_game_controller = GameController(initial)
        basefont = pygame.font.Font("assets/fnt/ASTONISH.TTF", 30)
        self.test_message = basefont.render("Test Button", True, (0,0,0), (255, 255, 255))
        initial.test_rect = self.test_message.get_rect()



    def check_collision(self):
        adjust = [0, 0]
        if self.direction == "left":
            adjust = [self.speed, 0]
        elif self.direction == "right":
            adjust = [0- self.speed, 0]
        elif self.direction == "up":
            adjust = [0, self.speed]
        elif self.direction == "down":
            adjust = [0, 0 - self.speed]
        for collision_layer in self.collision_layers:
            tmp_list = []
            tmp_list.extend(collision_layer)
            for tile in tmp_list:
                tmp_rect = tile.rect.move(adjust)
                if tmp_rect.colliderect(self.player.rect):
                    self.clear_move = False


    def clear_to_move(self):
        self.clear_move = True

        if self.direction == "left" and self.mapx + self.speed > 0:
            self.clear_move = False
        if self.direction == "right" and self.mapx < self.phone_width - self.mapwidth - self.speed:
            self.clear_move = False
        if self.direction == "up" and self.mapy + self.speed > 0:
            self.clear_move = False
        if self.direction == "down" and self.mapy < self.phone_height - self.mapheight + self.speed:
            self.clear_move = False

        if self.clear_move:
            self.check_collision()
        return (self.clear_move)



    def update(self, direction):
        x = 0
        y = 0
        self.direction = direction
        if self.clear_to_move():
            if direction == "right":
                x -= self.speed
            elif direction == "left":
                x += self.speed
            elif direction == "up":
                y += self.speed
            elif direction == "down":
                y -= self.speed
        self.move(x, y)


    def move(self, x = 0, y = 0):
        self.mapx += x
        self.mapy += y
        for current_layer in self.all_layers:
            for tile in current_layer:
                tile.rect.move_ip(x, y)
        for collision_layer in self.collision_layers:
            for tile in collision_layer:
                tile.rect.move_ip(x,y)

    def display(self, screen):
        for layer in self.all_layers:
            for tile in layer:
                screen.blit(tile.image, tile.rect)
        if self.initial.test:
            for layer in self.collision_layers:
                for collision_tile in layer:
                    screen.blit(collision_tile.image, collision_tile.rect)

            self.virtual_game_controller.gamebuttons.draw(screen)
        screen.blit(self.test_message, (5, 5))
        screen.blit(self.player.image, self.player.rect)
