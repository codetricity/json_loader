__author__ = 'craig'

import pygame, sys
from controller import *
# code specific to running games on Android
try:
    import android
except ImportError:
    android = None


class Event():
    def __init__(self, initial):
        self.direction = "stop"
        self.initial = initial
        self.virtual_game_controller = GameController(initial)
        self.jump = False
        self.fall = False

    def update(self):
        # check for android pause event
        if android:
            if android.check_pause():
                android.wait_for_resume()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"
                elif event.key == pygame.K_SPACE:
                    self.jump = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_buttons()
        self.mouse_direction()

    def game_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.initial.test_rect.collidepoint(mouse_pos):
            if self.initial.test:
                self.initial.test = False
            else:
                self.initial.test = True


    def mouse_direction(self):
        """
        Sets direction based on touchscreen input.
        Checks for mouse position (same as touchscreen)
        """
        mouse_pos = pygame.mouse.get_pos()

        for button in self.virtual_game_controller.gamebuttons:
            if button.rect.collidepoint(mouse_pos):
                self.direction = button.name
