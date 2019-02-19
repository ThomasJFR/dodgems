from abc import ABC, abstractmethod
import game, sys


LEFT = 0
TOP = 1
RIGHT = 2
BOTTOM = 3


class Entity(ABC):

    entity_list = []

    def __init__(self, sprite, parent_world, is_visible=True):
        self.sprite = sprite
        self.spriterect = sprite.get_rect()
        self.parent_world = parent_world
        self.is_visible = is_visible
    
    @abstractmethod
    def update(self):
        pass
        
    def render(self, screen):
        if self.is_visible:
            screen.blit(self.sprite, self.spriterect)

    def set_visible(self, is_visible):
        self.is_visible = is_visible
        
    def add(self):
        Entity.entity_list.append(self)
        self.parent_world.add_entity(self)
        
    def remove(self):
        Entity.entity_list.remove(self)
        self.parent_world.remove_entity(self)
        
class MobEnt(Entity, ABC):
    def __init__(self, sprite, parent_world, speed=[0,0]):
        super().__init__(sprite, parent_world)
        self.speed = speed
        
    
    @abstractmethod
    def update(self):
        pass


class Enemy(MobEnt):
    def __init__(self, sprite, parent_world, speed=[0,0]):
        super().__init__(sprite, parent_world, speed)
        self.is_active = True
    
    def update(self):
        width = game.width
        height = game.height
        
        self.spriterect = self.spriterect.move(self.speed)
        
        if self.spriterect.left < 0 or self.spriterect.right > width:
            self.speed[0] = -self.speed[0]
    
        if self.spriterect.top < 0 or self.spriterect.bottom > height:
            self.speed[1] = -self.speed[1]
        
       
class TeleportMarker(MobEnt):
    def __init__(self,sprite, parent_world, speed=[0,0]):
        super().__init__(sprite, parent_world, speed)
        self.is_active = True
        
    def update(self):
        width = game.width
        height = game.height
        
        if not self.is_active:
            return
        
        self.spriterect = self.spriterect.move(self.speed)
        
        if self.spriterect.left < 0 or self.spriterect.right > width:
            self.speed[0] = -self.speed[0]
    
        if self.spriterect.top < 0 or self.spriterect.bottom > height:
            self.speed[1] = -self.speed[1]
        
    def set_active(self, is_active):
        self.is_active = is_active
        
    def render(self,screen):
        if self.is_active:
            super().render(screen)
            
            
class Player(Entity):
    def __init__(self, sprite, parent_world):
        super().__init__(sprite, parent_world)
        self.current_pos = TOP
        self.tp_markers = []
    
    def add_tp_marker(self, tp_marker, index):
        self.tp_markers.insert(index, tp_marker)
    
    def update(self):
        width = game.width
        height = game.height
        
        self.tp_markers[self.current_pos].is_active = False
        
        #handle keyboard events related to the guy
        for event in game.pygame.event.get(game.pygame.KEYDOWN):
        
            if event.type == game.pygame.KEYDOWN:
                
                for marker in self.tp_markers:
                    marker.is_active = True
                
                if event.key == game.pygame.K_a or event.key == game.pygame.K_LEFT:
                    self.current_pos = LEFT
                
                if event.key == game.pygame.K_d or event.key == game.pygame.K_RIGHT:
                    self.current_pos = RIGHT
                
                if event.key == game.pygame.K_w or event.key == game.pygame.K_UP:
                    self.current_pos = TOP
                    
                if event.key == game.pygame.K_s or event.key == game.pygame.K_DOWN:
                    self.current_pos = BOTTOM
                    
        # Update my guy
        if self.current_pos == LEFT:
            self.spriterect.left = self.tp_markers[LEFT].spriterect.left
            self.spriterect.y = self.tp_markers[LEFT].spriterect.y
        
        elif self.current_pos == RIGHT:
            self.spriterect.right = self.tp_markers[RIGHT].spriterect.right
            self.spriterect.y = self.tp_markers[RIGHT].spriterect.y
        
        elif self.current_pos == TOP:
            self.spriterect.top = self.tp_markers[TOP].spriterect.top
            self.spriterect.x = self.tp_markers[TOP].spriterect.x
            
        elif self.current_pos == BOTTOM:
            self.spriterect.bottom = self.tp_markers[BOTTOM].spriterect.bottom
            self.spriterect.x = self.tp_markers[BOTTOM].spriterect.x
        
        for entity in Entity.entity_list:
            if type(entity) is Enemy:
                if entity.is_active and entity.spriterect.colliderect(self.spriterect):
                    print("Collision detected with " + str(type(entity)) + "\n")
                    print("SCORE: " + str(self.parent_world.get_score()))
                    self.current_pos = TOP
                    self.parent_world.parent_state.restart()