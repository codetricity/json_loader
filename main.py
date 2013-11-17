__author__ = 'craig'
import map_loader
import pygame
import sys
from map_loader import Loader

try:
    import android
except ImportError:
    android = None

class Hero(pygame.sprite.Sprite):
    def __init__(self, screensize):
        pygame.sprite.Sprite.__init__(self)
        self.screenwidth = screensize[0]
        self.screenheight = screensize[1]
        boy = pygame.image.load("boy.png")
        self.image = pygame.transform.scale(boy, (24, 24))
        self.rect = self.image.get_rect()
        #self.rect.center = (self.screenwidth / 2,
        #                    self.screenheight /2)
        self.rect.center = (self.screenwidth / 2, 50)
        # self.rect.center = (240, 160)
        self.speed = 2

    def update(self, direction):
        self.mapdirection = "stop"
        player_boundary = 10
        if direction == "right":
            if self.rect.right < self.screenwidth -player_boundary:
                self.rect.right += self.speed
            else:
                self.mapdirection = "right"
        elif direction == "left":
            if self.rect.left > player_boundary:
                self.rect.left -= self.speed
            else:
                self.mapdirection = "left"
        elif direction == "up":
            if self.rect.top > player_boundary:
                self.rect.top -= self.speed
            else:
                self.mapdirection = "up"
        elif direction == "down":
            if self.rect.bottom < self.screenheight - player_boundary:
                self.rect.bottom += self.speed
            else:
                self.mapdirection = "down"





SCREENSIZE = (480, 320)
SCREEN = pygame.display.set_mode(SCREENSIZE)
RED = (255, 0, 0)
# the offset is the start position of the map and character
offset = (-270, -1400)

pygame.init()

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

clock = pygame.time.Clock()

loader = Loader("test_map.json", SCREENSIZE)
#mapheight = loader.mapheight
#mapwidth = loader.mapwidth
hero = Hero(SCREENSIZE)

all_layers, collide_rects = loader.load_layers()
collide_tilesize = collide_rects[0].size
collision_tile = pygame.Surface(collide_tilesize)
collision_tile.set_alpha(75)
collision_tile.fill(RED)

layer_rect = all_layers[0].get_rect()
#layer_rect.center = SCREEN.get_rect().center
#layer_rect.bottom = mapheight

direction = "stop"
collide = False
previous_direction = "stop"


layer_rect, collide_rects = loader.initialize_map(offset, layer_rect, collide_rects)


while True:
    if android:
        if android.check_pause():
            android.wait_for_resume()


    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN
                 and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    mouse_pos = pygame.mouse.get_pos()
    if not collide:
        if mouse_pos[0] > 0 and mouse_pos[0] < 100:
            direction = "left"
        elif (mouse_pos[0] < SCREENSIZE[0]) and \
                (mouse_pos[0] > SCREENSIZE[0] -100):
            direction = "right"
        elif mouse_pos[1] > 0 and mouse_pos[1] < 100:
            direction = "up"
        elif (mouse_pos[1] < SCREENSIZE[1]) and \
                (mouse_pos[1] > SCREENSIZE[1] - 100):
            direction = "down"
        else:
            direction = "stop"


    if direction != "stop":
        previous_direction = direction

    for collidetile in collide_rects:
        # SCREEN.blit(collision_tile, collidetile)
        if hero.rect.colliderect(collidetile):
            direction = "stop"
            collide = True

    if collide:
        print("collision", previous_direction)

        bounce = 5
        if previous_direction == "right":
            hero.rect.centerx -= bounce
            direction = "stop"
            collide = False
        elif previous_direction == "left":
            hero.rect.centerx += bounce
            direction = "stop"
            collide = False
        elif previous_direction == "up":
            hero.rect.centery += bounce
            direction = "stop"
            collide = False
        elif previous_direction == "down":
            hero.rect.centery -= bounce
            direction = "stop"
            collide = False




    hero.update(direction)
    direction = hero.mapdirection
    loader.check_boundary(layer_rect)
    direction = loader.handle_boundary(direction)
    layer_rect, collide_rects = loader.move_map(direction, layer_rect, collide_rects)
    for layer in all_layers:
        SCREEN.blit(layer, layer_rect)


    SCREEN.blit(hero.image, hero.rect)
    clock.tick (50)
    pygame.display.update()
