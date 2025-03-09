import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Alien(Sprite):

    
    alien_images0 = [pg.image.load(f"animation/pinkAlien_rd-{n+1}.png.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"animation/blueAlien_rd-{n+1}.png.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"animation/greenAlien_rd-{n+1}.png.png") for n in range(2)]
    alien_images3 = [pg.image.load(f"animation/alienShip_rd-{n+1}.png.png") for n in range(2)]
    alien_images = [alien_images0, alien_images1, alien_images2, alien_images3]
    alien_explosion_images = [pg.image.load(f"animation/explosion_rd-{n+1}.png.png") for n in range(4)]  # fill in explosion images here
    ufo_explosion_images = [pg.image.load(f"animation/explosion_points-{n+1}.png.png") for n in range(4)]

    # Dictionaries for each alien type
    alien0 = {"type": "pink", "points": 100, "type_value": 0}
    alien1 = {"type": "blue", "points": 200, "type_value": 1}
    alien2 = {"type": "green", "points": 300, "type_value": 2}
    alien3 = {"type": "ufo", "points": 500, "type_value": 3}
    alien_types = [alien0, alien1, alien2, alien3]              # A list of dictionaries holding all alien types
    

    def __init__(self, ai_game, v, type=0): 
        super().__init__()
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.v = v
        self.is_dying = False
        self.is_dead = False
        self.pts_earned = False

        #type = randint(0, 2)
        self.type = type    
        self.timer = Timer(images=Alien.alien_images[self.type], delta=self.type*350, start_index=self.type % 2)
        self.explosion_timer = Timer(images=Alien.alien_explosion_images, loop_continuously=False, running=False)
        self.ufo_explosion_timer = Timer(images=Alien.ufo_explosion_images, loop_continuously=False, running=False)
        self.image = self.timer.current_image()
        #print(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def hit(self):
        if not self.is_dying:
            #print('ALIEN HIT! Alien is dying')
            self.is_dying = True
            if self.type == Alien.alien3.get("type_value"):
                self.timer = self.ufo_explosion_timer
            else:
                self.timer = self.explosion_timer
            self.timer.start()
        

    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        r = self.rect 
        return self.x + self.rect.width >= sr.right or self.x <= 0
    
    
    def check_pts(self):
        """Checks the type of alien and returns 
            the appropriate point value. """
        for alien in Alien.alien_types:
            if alien["type_value"] == self.type:
                return alien["points"]
    

    def update(self):
        if self.is_dead: return
        if self.is_dying and (self.explosion_timer.finished() or self.ufo_explosion_timer.finished()):
            self.is_dying = False
            self.is_dead = True
            #print('Alien is dead')
            self.kill()
            return

        self.x += self.v.x * self.settings.alien_speed
        self.y += self.v.y
        self.image = self.timer.current_image()
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)
    

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
