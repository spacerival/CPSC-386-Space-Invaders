import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 

from alien import Alien
from pygame.sprite import Sprite
from random import randint

class Fleet(Sprite):
    def __init__(self, ai_game): 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)
        # alien = Alien(ai_game=ai_game)
        # self.aliens.add(alien)
        self.spacing = 1.4
        self.create_fleet()
        # self.create_row()

    def reset_fleet(self):
        self.aliens.empty()
        self.create_fleet()

    def create_fleet(self):
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_height = alien.rect.height
        current_y = alien_height
        type = 2
        while current_y < (self.settings.scr_height - self.spacing * 6 * alien_height):
            if type == -1:
                type = 0
            self.create_row(current_y, type)
            current_y += self.spacing * alien_height
            type -= 1
        
    def create_row(self, y, type):
        alien = Alien(ai_game=self.ai_game, v=self.v, type=type)
        alien_width = alien.rect.width
        current_x = alien_width 
        while current_x < (self.settings.scr_width - self.spacing * alien_width):
             new_alien = Alien(self, v=self.v, type=type)
             new_alien.rect.y = y
             new_alien.y = y
             new_alien.x = current_x
             new_alien.rect.x = current_x
             self.aliens.add(new_alien)
             current_x += self.spacing * alien_width

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): 
                return True 
        return False
    
    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False


    def fire_laser(self, rect):
        laser = Laser(self.ai_game, True, rect)
        self.lasers.add(laser) 
    

    def update(self): 
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, True)
        pg.sprite.groupcollide(self.ship.lasers, self.lasers, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.settings.alien_speed *= 1.03
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.ship.lasers.empty()
            self.create_fleet()
                    # Increase level.
            self.settings.alien_speed = self.settings.alien_base_speed
            pg.mixer.music.rewind()
            self.stats.level += 1
            self.sb.prep_level()
            return
        if pg.sprite.spritecollideany(self.ship, self.aliens) or pg.sprite.spritecollideany(self.ship, self.lasers):
            print("Ship hit!")
            self.ship.ship_hit()
            self.lasers.empty()
            return
        
        if self.check_bottom():
            return 
        
        if self.check_edges():
            self.v.x *= -1 
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed
            
        for alien in self.aliens:
            alien.update()
            if pg.time.get_ticks() % randint(500, 650) == 0:
                if randint(1, 25) == 1:                 
                    self.fire_laser(alien.rect.midtop)
        
        count = 0
        while count < 13:
            self.lasers.update(-0.1)
            for laser in self.lasers.copy():
                if laser.rect.bottom >= self.settings.scr_height:
                    self.lasers.remove(laser)
            for laser in self.lasers.sprites():
                laser.draw()  
            count += 1  

    def draw(self): pass
        # for alien in self.aliens:
        #     alien.draw()

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
