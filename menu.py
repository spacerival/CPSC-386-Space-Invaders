import sys
import pygame as pg
from pygame.locals import *
from colors import WHITE, GREEN
from settings import Settings
from game_stats import GameStats

from alien import Alien

class Menu:
    MAX_HIGH_SCORES = 10
    pink_alien_img = pg.image.load(f"animation/pinkAlien_rd-1.png.png")    # 100 points
    blue_alien_img = pg.image.load(f"animation/blueAlien_rd-1.png.png")    # 200 points
    green_alien_img = pg.image.load(f"animation/greenAlien_rd-1.png.png")  # 300 points
    alien_ship_img = pg.image.load(f"animation/alienShip_rd-1.png.png")   # 500 points

    #alien_img = pg.image.load(f"images/alien00.png")        # To be removed later

    def __init__(self, ai_game): 
        pg.init()
        self.settings = Settings() 
        self.stats = GameStats(ai_game)
        self.path = self.stats.path
        self.screen = pg.display.set_mode(self.settings.w_h) 
        self.font1 = pg.font.SysFont(None, 100)
        self.font2 = pg.font.SysFont(None, 75)
        self.font3 = pg.font.SysFont(None, 50)

        self.text1 = self.font1.render("SPACE", self.settings.bg_color, WHITE)
        self.text2 = self.font1.render("INVADERS", self.settings.bg_color, GREEN)
        self.text3 = self.font1.render("TOP 10 HIGH SCORES", self.settings.bg_color, GREEN)
        self.text4 = self.font1.render("TOP 10 HIGH SCORES", self.settings.bg_color, WHITE)
        self.text5 = self.font3.render("Press 'q' to quit", self.settings.bg_color, WHITE)
        self.pink_alien_pts = self.font3.render("= 100 pts", self.settings.bg_color, WHITE)
        self.blue_alien_pts = self.font3.render("= 200 pts", self.settings.bg_color, WHITE)
        self.green_alien_pts = self.font3.render("= 300 pts", self.settings.bg_color, WHITE)
        self.ufo_alien_pts = self.font3.render("= 500 pts", self.settings.bg_color, WHITE)
        
    
    def prep_start_text(self):
        self.text1_rect = self.text1.get_rect()
        self.text2_rect = self.text2.get_rect()
        self.text5_rect = self.text5.get_rect()
        self.text1_rect.centerx = self.screen.get_rect().centerx
        self.text1_rect.top = self.screen.get_rect().top + 10
        self.text2_rect.centerx = self.screen.get_rect().centerx
        self.text2_rect.top = self.screen.get_rect().top + 75
        self.text5_rect.right = self.screen.get_rect().right
        self.text5_rect.bottom = self.screen.get_rect().bottom

    
    def prep_alien_imgs(self):
        self.pink_alien_rect = Menu.pink_alien_img.get_rect()
        self.blue_alien_rect = Menu.blue_alien_img.get_rect()
        self.green_alien_rect = Menu.green_alien_img.get_rect()
        self.alien_ship_rect = Menu.alien_ship_img.get_rect()

        #self.alien_rect = Menu.alien_img.get_rect()     # To be removed later

        self.pink_alien_rect.centerx = self.screen.get_rect().centerx - 100
        self.pink_alien_rect.top = self.screen.get_rect().top + 150
        self.blue_alien_rect.centerx = self.screen.get_rect().centerx - 100
        self.blue_alien_rect.top = self.screen.get_rect().top + 250
        self.green_alien_rect.centerx = self.screen.get_rect().centerx - 100
        self.green_alien_rect.top = self.screen.get_rect().top + 350
        self.alien_ship_rect.centerx = self.screen.get_rect().centerx - 100
        self.alien_ship_rect.top = self.screen.get_rect().top + 450
        
        #self.alien_rect.centerx = self.screen.get_rect().centerx    # To be removed later
        #self.alien_rect.top = self.screen.get_rect().top + 200      # To be removed later

    
    def prep_alien_scores(self):
        self.pink_pts_rect = self.pink_alien_pts.get_rect()
        self.blue_pts_rect = self.blue_alien_pts.get_rect()
        self.green_pts_rect = self.green_alien_pts.get_rect()
        self.ufo_pts_rect = self.ufo_alien_pts.get_rect()

        self.pink_pts_rect.centerx = self.screen.get_rect().centerx + 30
        self.pink_pts_rect.top = self.screen.get_rect().top + 160
        self.blue_pts_rect.centerx = self.screen.get_rect().centerx + 30
        self.blue_pts_rect.top = self.screen.get_rect().top + 260
        self.green_pts_rect.centerx = self.screen.get_rect().centerx + 30
        self.green_pts_rect.top = self.screen.get_rect().top + 360
        self.ufo_pts_rect.centerx = self.screen.get_rect().centerx + 30
        self.ufo_pts_rect.top = self.screen.get_rect().top + 460


    def prep_score_menu(self):
        self.text3_rect = self.text3.get_rect()
        self.text4_rect = self.text4.get_rect()
        self.text3_rect.centerx = self.screen.get_rect().centerx 
        self.text3_rect.top = self.screen.get_rect().top + 15
        self.text4_rect.centerx = self.screen.get_rect().centerx
        self.text4_rect.top = self.screen.get_rect().top + 10
        
 
    def prep_points(self, text, offset):
        """Helper function for draw_high_scores() function.
            Returns rects for each of the 10 high scores"""
        text_rect = text.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.top = self.screen.get_rect().top + offset
        return text_rect
    

    def prep_start_menu(self):
        self.prep_start_text()
        self.prep_alien_imgs()
        self.prep_alien_scores()
    

    def draw_high_scores(self):
        self.points = self.stats.points
        offset = 150
        for point in self.points:
            text = self.font2.render(str(point), self.settings.bg_color, WHITE)
            text_rect = self.prep_points(text, offset)
            self.screen.blit(text, text_rect)
            offset += 50

    
    def display_start_text(self):
        self.screen.blit(self.text1, self.text1_rect)
        self.screen.blit(self.text2, self.text2_rect)
        self.screen.blit(self.text5, self.text5_rect)
    

    def display_alien_imgs(self):
        self.screen.blit(Menu.pink_alien_img, self.pink_alien_rect)
        self.screen.blit(Menu.blue_alien_img, self.blue_alien_rect)
        self.screen.blit(Menu.green_alien_img, self.green_alien_rect)
        self.screen.blit(Menu.alien_ship_img, self.alien_ship_rect)

        #self.screen.blit(Menu.alien_img, self.alien_rect)       # To be removed later

    def display_alien_pts(self):
        self.screen.blit(self.pink_alien_pts, self.pink_pts_rect)
        self.screen.blit(self.blue_alien_pts, self.blue_pts_rect)
        self.screen.blit(self.green_alien_pts, self.green_pts_rect)
        self.screen.blit(self.ufo_alien_pts, self.ufo_pts_rect)


    def display_start_menu(self):
        self.prep_start_menu()
        self.screen.fill(self.settings.bg_color)
        self.display_alien_imgs()
        self.display_alien_pts()
        self.display_start_text()

    
    def display_high_scores(self):
        self.prep_score_menu()
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.text3, self.text3_rect)
        self.screen.blit(self.text4, self.text4_rect)
        self.draw_high_scores()
    
    
    def update_score_list(self, new_score):
        """Stores top 10 highest scores on file. If new score is greater than old score,
         it'll take the old score's place in top 10 listing and the rest of the listing
         positions shifts down. Only the top 10 highest scores will be retained."""
        count, score1, value = 0, new_score, ""
        self.points = self.stats.points
        while count < self.MAX_HIGH_SCORES:
            score2 = int(self.points[count])
            if score1 == score2:
                break
            if score1 < score2:
                score2 += 1
                count += 1
                continue
            self.points[count] = score1
            score1 = score2
            count += 1
        for point in self.points:
            point = str(point)
            value += point + "\n"
        print(value)    # Testing Purposes
        self.path.write_text(value)

