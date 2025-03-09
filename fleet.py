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
        self.ufo = pg.sprite.GroupSingle()
        self.lasers = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)
        self.v_ufo = Vector(self.settings.alien_speed, 0)
        # alien = Alien(ai_game=ai_game)
        # self.aliens.add(alien)
        self.spacing = 1.2
        self.create_fleet()
        self.ufo_on = False
        self.ufo_level = 0
        # self.create_row()

    def reset_fleet(self):
        self.aliens.empty()
        self.ufo.empty()
        self.create_fleet()


    def create_fleet(self):
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_height = alien.rect.height
        current_y = alien_height + 65
        type = 2
        while current_y < (self.settings.scr_height - self.spacing * 6 * alien_height):
            if type == -1:
                type = 0
            self.create_row(current_y, type)
            current_y += self.spacing * alien_height
            type -= 1
        

    def create_row(self, y, alien_type):
        alien = Alien(ai_game=self.ai_game, v=self.v, type=alien_type)
        alien_width = alien.rect.width
        current_x = alien_width 
        while current_x < (self.settings.scr_width - self.spacing * alien_width):
             new_alien = Alien(self, v=self.v, type=alien_type)
             new_alien.rect.y = y
             new_alien.y = y
             new_alien.x = current_x
             new_alien.rect.x = current_x
             self.aliens.add(new_alien)
             current_x += self.spacing * alien_width

    
    def spawn_ufo(self):
        alien = Alien(self.ai_game, self.v_ufo, 3)
        x, y = alien.rect.width, alien.rect.height * 3
        alien.x, alien.rect.x = x, x
        alien.y, alien.rect.y = y, y
        self.ufo.add(alien)
        print("UFO SPAWNED")
        self.ufo_on = True
        self.ufo_level += 1


    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): 
                return True 
        return False


    def check_ufo_edges(self):
        for ufo in self.ufo:
            if ufo.check_edges():
                return True
        return False
    
    
    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False


    def check_ufo_bottom(self):
        for ufo in self.ufo:
            if ufo.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False


    def fire_laser(self, rect):
        laser = Laser(self.ai_game, True, rect)
        self.lasers.add(laser) 
    

    def update_laser(self):
        count = 0
        while count < 13:
            self.lasers.update(-0.1)
            for laser in self.lasers.copy():
                if laser.rect.bottom >= self.settings.scr_height:
                    self.lasers.remove(laser)
            for laser in self.lasers.sprites():
                laser.draw()  
            count += 1  


    def update(self): 
        # Different types of collisions that can occur
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, False)
        ufo_defeated = pg.sprite.groupcollide(self.ship.lasers, self.ufo, True, False)
        ship_alien_hit = pg.sprite.spritecollideany(self.ship, self.aliens)
        ship_alien_laser_hit =  pg.sprite.spritecollideany(self.ship, self.lasers)
        ship_ufo_hit = pg.sprite.spritecollideany(self.ship, self.ufo)
        pg.sprite.groupcollide(self.ship.lasers, self.lasers, True, True)             

        # If either an alien or ufo is hit by a ship laser
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    alien.hit()
                    if alien.is_dying == True and alien.pts_earned == False:
                        pts = alien.check_pts()
                        self.stats.score += pts * len(aliens)
                        self.settings.alien_speed *= 1.003
                        alien.pts_earned = True
            self.sb.prep_score()
            self.sb.check_high_score()
        elif ufo_defeated:
            for ufo in self.ufo:
                ufo.hit()
                if ufo.is_dying == True and ufo.pts_earned == False:
                        self.stats.score += Alien.alien3.get("points")
                        self.settings.alien_speed *= 1.003
                        ufo.pts_earned = True
            self.ufo_on = False
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens and not self.ufo:    # if there's no more aliens or ufo
            self.ship.lasers.empty()
            self.create_fleet()
                    # Increase level.
            self.settings.alien_speed = self.settings.alien_base_speed
            pg.mixer.music.rewind()
            self.stats.level += 1
            self.sb.prep_level()
            return
        
        if ship_alien_hit or ship_alien_laser_hit or ship_ufo_hit:  # if the ship gets hit by an alien, ufo, or enemy laser
            self.ship.ship_hit()
            
        if self.ship.is_dead == True:
            print("Ship hit!")
            pg.mixer.music.rewind()
            self.settings.alien_speed = self.settings.alien_base_speed
            self.ship.ship_down()
            self.lasers.empty()
            return
        
        if self.check_bottom() or self.check_ufo_bottom():  # if aliens/ufo gets to the bottom of the screen
            self.settings.alien_speed = self.settings.alien_base_speed
            return 
        
        if self.check_edges():
            self.v.x *= -1 
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed

        if self.check_ufo_edges():
            self.v_ufo.x *= -1 
            for ufo in self.ufo:
                ufo.v.x = self.v_ufo.x
                ufo.y += self.settings.fleet_drop_speed
        
        # Randomly spawns a ufo, and only one ufo will spawn per level
        if pg.time.get_ticks() % randint(600, 700) == 0 and self.ufo_level != self.stats.level:
            if self.ufo_on == False:
                self.spawn_ufo()

        for alien in self.aliens:
            alien.update()
            # Each alien has a random chance of firing a laser
            if pg.time.get_ticks() % randint(500, 675) == 0:
                if randint(1, 22) == 1:                 
                    self.fire_laser(alien.rect.midtop)
        for ufo in self.ufo:
            ufo.update()

        self.update_laser()
        
        

    def draw(self): pass
        # for alien in self.aliens:
        #     alien.draw()

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
