import sys
import pygame as pg
from pygame.locals import *
from colors import WHITE, GREEN
from settings import Settings
from game_stats import GameStats

class Menu:
    MAX_HIGH_SCORES = 10

    def __init__(self, ai_game): 
        pg.init()
        self.settings = Settings() 
        self.stats = GameStats(ai_game)
        self.path = self.stats.path
        self.screen = pg.display.set_mode(self.settings.w_h) 
        self.font1 = pg.font.SysFont(None, 100)
        self.font2 = pg.font.SysFont(None, 75)
        self.text1 = self.font1.render("SPACE", self.settings.bg_color, WHITE)
        self.text2 = self.font1.render("INVADERS", self.settings.bg_color, GREEN)
        self.text3 = self.font1.render("TOP 10 HIGH SCORES", self.settings.bg_color, GREEN)
        self.text4 = self.font1.render("TOP 10 HIGH SCORES", self.settings.bg_color, WHITE)
        

    def prep_menu(self):
        self.text1_rect = self.text1.get_rect()
        self.text2_rect = self.text2.get_rect()
        self.text1_rect.centerx = self.screen.get_rect().centerx
        self.text1_rect.top = self.screen.get_rect().top + 10
        self.text2_rect.centerx = self.screen.get_rect().centerx
        self.text2_rect.top = self.screen.get_rect().top + 75


    def prep_score_menu(self):
        self.text3_rect = self.text3.get_rect()
        self.text4_rect = self.text4.get_rect()
        self.text3_rect.centerx = self.screen.get_rect().centerx 
        self.text3_rect.top = self.screen.get_rect().top + 15
        self.text4_rect.centerx = self.screen.get_rect().centerx
        self.text4_rect.top = self.screen.get_rect().top + 10

    
    def prep_points(self, text, offset):
        text_rect = text.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.top = self.screen.get_rect().top + offset
        return text_rect


    def display_menu(self):
        self.prep_menu()
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.text1, self.text1_rect)
        self.screen.blit(self.text2, self.text2_rect)

    
    def display_high_scores(self):
        self.prep_score_menu()
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.text3, self.text3_rect)
        self.screen.blit(self.text4, self.text4_rect)
        self.draw_high_scores()
    
    def draw_high_scores(self):
        self.points = self.stats.points
        offset = 150
        for point in self.points:
            text = self.font2.render(str(point), self.settings.bg_color, WHITE)
            text_rect = self.prep_points(text, offset)
            self.screen.blit(text, text_rect)
            offset += 50

    def update_score_list(self, new_score):
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

