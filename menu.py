import sys
import pygame as pg
from pygame.locals import *
from colors import WHITE, GREEN
from settings import Settings

class Menu:
    def __init__(self): 
        pg.init()
        self.settings = Settings() 
        self.screen = pg.display.set_mode(self.settings.w_h) 
        self.font = pg.font.SysFont(None, 100)
        self.text1 = self.font.render("SPACE", self.settings.bg_color, WHITE)
        self.text2 = self.font.render("INVADERS", self.settings.bg_color, GREEN)

        self.text1_rect = self.text1.get_rect()
        self.text2_rect = self.text2.get_rect()
        
        self.text1_rect.centerx = self.screen.get_rect().centerx
        self.text1_rect.top = self.screen.get_rect().top + 10
        self.text2_rect.centerx = self.screen.get_rect().centerx
        self.text2_rect.top = self.screen.get_rect().top + 75

    def display_menu(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.text1, self.text1_rect)
        self.screen.blit(self.text2, self.text2_rect)

        

# Testing Purposes
if __name__ == '__main__':
    m = Menu()
    m.display_menu()
