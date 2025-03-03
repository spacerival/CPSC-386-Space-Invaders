import pygame as pg
from pygame.sprite import Sprite
from random import randint

class Laser(Sprite):
    @staticmethod
    def random_color(): 
        return (randint(0, 255), randint(0, 255), randint(0, 255))
    def __init__(self, ai_game, isAlien=False, midtop_rect=(0,0)):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # self.color = self.settings.laser_color
        self.color = Laser.random_color()
        self.rect = pg.Rect(0, 0, self.settings.laser_width,
                                self.settings.laser_height)
        if isAlien == True:
            self.rect.midtop = midtop_rect
        else:
            self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self, direction=1):
        self.y -= self.settings.laser_speed * direction
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

def main():
    print("\nYou have to run from alien_invasion.py\n")

if __name__ == "__main__":
    main()
