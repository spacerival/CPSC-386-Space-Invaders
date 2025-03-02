import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from pathlib import Path

class GameStats:
    def __init__(self, ai_game):
        self.path = ai_game.path
        self.points = self.path.read_text().splitlines()
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = int(self.points[0])

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
