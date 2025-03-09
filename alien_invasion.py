import sys
import pygame as pg
from colors import OFF_WHITE, DARK_GREY, BLUE
from settings import Settings
from ship import Ship
from vector import Vector
from fleet import Fleet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from event import Event
from menu import Menu
from pathlib import Path


class AlienInvasion:
    # di = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1, 0),
    #       pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1),
    #       pg.K_d: Vector(1, 0), pg.K_a: Vector(-1, 0),
    #       pg.K_w: Vector(0, -1), pg.K_s: Vector(0, 1)}
    def __init__(self):
        pg.init()   
        self.path = Path("high_score.txt")
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.menu = Menu(self)
        self.ship = Ship(ai_game=self)
        self.fleet = Fleet(ai_game=self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)

        pg.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color

        # Start Alien Invasion in an inactive state.           
        self.game_active = False
        self.first = True
        self.menu_toggle = True

        self.play_button = Button(self, "Play", 175)
        self.high_score_button = Button(self, "High Scores", 250, BLUE)
        self.back_button = Button(self, "Back", 350, BLUE)
        self.event = Event(self)
        pg.mixer.music.load("Space Invaders Audio/Space Invader Project Menu Theme.mp3")
        pg.mixer.music.set_volume(0.3)


    def game_over(self):
        self.restart_game()
        print(f"High Score: {self.stats.high_score}\n")     # Testing purposes
        print("Game over!")
        self.game_active = False
        self.menu_toggle = True
        pg.mouse.set_visible(True)
        self.settings.play_menu_theme()
    

    def reset_game(self):
        self.settings.play_game_music()
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True
        self.ship.reset_ship()
        self.fleet.reset_fleet()
        pg.mouse.set_visible(False)

    def restart_game(self):
        self.game_active = False
        self.first = True
        self.play_button.reset_message("Play again?")
        self.menu.update_score_list(self.stats.score)
        self.reset_game()


    def run_game(self):
        self.finished = False
        self.first = True
        self.game_active = False
        pg.mixer.music.play(-1, 0)
        while not self.finished:
            if self.ship.is_dying == False:     # Locks controls if ship is dying, otherwise proceed
                self.finished = self.event.check_events()
            if self.first or self.game_active:
                self.first = False
                self.screen.fill(self.bg_color)
                self.ship.update()
                self.fleet.update()
                self.sb.show_score()

            if not self.game_active:
                if self.menu_toggle == True:
                    self.menu.display_start_menu()
                    self.play_button.draw_button()
                    self.high_score_button.draw_button()
                else:
                    self.menu.display_high_scores()
                    self.back_button.draw_button()
                
            pg.display.flip()

            self.clock.tick(60)
        sys.exit()

      

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
