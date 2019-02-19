from abc import ABC, abstractmethod
from entity import *
import time
from world import World
from game import pygame, size

class State(ABC):

    def __init__(self):
        pass
        
    @abstractmethod
    def start(self):
        pass
        
    def restart(self):
        self.stop()
        self.start()
        
    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def render(self, screen):
        pass
        

class GameState(State):

    def __init__(self):
        self.world = World(self)
        super().__init__()
        
    def start(self):
        
        width, height = game.size
        
        sprite = pygame.transform.scale(pygame.image.load("sprite.png"), (40,40))
        user_char = Player(sprite, self.world)
        crosshair_sprite = pygame.transform.scale(pygame.image.load("crosshair.png"), (40,40))
        
        tploc_1 = TeleportMarker(crosshair_sprite, self.world, [0,2])
        tploc_1.spriterect.y = height/2
        tploc_1.add()
        user_char.add_tp_marker(tploc_1, 0)
        
        tploc_2 = TeleportMarker(crosshair_sprite, self.world, [2,0])
        tploc_2.spriterect.x = width / 2
        tploc_2.add()
        user_char.add_tp_marker(tploc_2, 1)
        
        tploc_3 = TeleportMarker(crosshair_sprite, self.world, [0,2])
        tploc_3.spriterect.bottom = height
        tploc_3.spriterect.right = width
        tploc_3.add()
        user_char.add_tp_marker(tploc_3, 2)
        
        tploc_4 = TeleportMarker(crosshair_sprite, self.world, [2,0])
        tploc_4.spriterect.bottom = height
        tploc_4.spriterect.right = width
        tploc_4.add()
        user_char.add_tp_marker(tploc_4, 3)
        
        user_char.add()
        
        
    def stop(self):
        self.world.clear_entities()
        self.world.counter = -1
    
    def update(self):
        self.world.update()
        
    def render(self, screen):
        white = (150,150,150)
    
        screen.fill(white)
        self.world.render(screen)
        pygame.display.flip()
     
     
class TitleState(State): 
    
    def __init__(self):
        pass
        
    
    def start(self):
        pass
    
    
    def stop(self):
        pass
    
    def update(self):    
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return GameState()

    
    def render(self, screen):
        gray = (100, 100, 125)
        title_font = pygame.font.SysFont("Comic Sans MS", 50)
        
        screen.fill(gray)
        width,height = size
        title_surf = title_font.render("DODGEMS", False, (0,0,0))
        screen.blit(title_surf,(10,10))
        pygame.display.flip()
    