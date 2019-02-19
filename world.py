from random import randint

from entity import Player, Enemy
from game import pygame, width, height

class World():
    
    def __init__(self, parent_state):
        from entity import Entity, MobEnt
        self.entity_list = []
        self.player = None
        self.counter = 0
        self.score = 0
        self.seconds_per_spawn = 5
        self.parent_state = parent_state
    
    def add_entity(self, entity):
        self.entity_list.append(entity)
        
        if type(entity) == Player:
            self.player = entity
    
    
    def remove_entity(self, entity):
        self.entity_list.remove(entity)
    
    
    def clear_entities(self):
        self.entity_list.clear()
    
    
    def update(self):
        if self.player is None:
            print("Can't start game without player!")
            return
            
        if self.counter % (self.seconds_per_spawn * 60) == 0:
            enemy_sprite = pygame.transform.scale(pygame.image.load("thwomp.png"), (40,40))
            time_scale = int(self.counter / (self.seconds_per_spawn * 60))
            
            x,y = randint(-5 - time_scale, 5 + time_scale), randint(-5 - time_scale, 5 + time_scale)
            enemy = Enemy(enemy_sprite, self, [x,y])
            enemy.spriterect.x = width / 2
            enemy.spriterect.y = height / 2
            enemy.add()
        
        for entity in self.entity_list:
            entity.update()
    
        self.counter += 1
        self.score = self.counter
        
        
    def render(self, screen):
        for entity in self.entity_list:
            entity.render(screen)
            
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(self.score), False, (0, 0, 0))
        screen.blit(textsurface, (0,0))
        
    def get_score(self):
        return self.score