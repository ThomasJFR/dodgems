import sys, time

import pygame
 
pygame.init()
pygame.font.init()

#Set up screen
infoObject = pygame.display.Info()

width = 0
height = 0
res_index = 0
while width + 500 < infoObject.current_w and height + 500 < infoObject.current_h:
    width += 300 
    height += 300
    res_index += 1

size = width,height
screen = pygame.display.set_mode(size)
    

#Initialize the game engine
def main():

    from entity import MobEnt, Player, TeleportMarker, Enemy
    from world import World
    from state import GameState, TitleState
    
    global size, width, height
    global screen
        
    game_state = TitleState()
    game_state.start()
    
    while True:
        tick_rate_target = 60.0
        ms_per_tick = 1000.0/tick_rate_target
        unprocessed = 0.0
        last_time = timer = pygame.time.get_ticks()
        fps = tps = 0;
        can_render = False;
        while True:
            now = pygame.time.get_ticks()
            unprocessed += (now - last_time) / ms_per_tick;
            last_time = now;
                    
            if unprocessed >= 1.0:
                unprocessed -= 1
                tps += 1
                can_render = True
                
                
                #UPDATE THE GAME
                next_state = game_state.update()
                if next_state is not None:
                    game_state.stop()
                    game_state = next_state
                    game_state.start()
            else: 
                can_render = False;
            
            try:
                time.sleep( 0.001 )
            except Exception:
                print("Failed to sleep!")
                
            if can_render:
                #Render the game
                game_state.render(screen)
            
                fps += 1
            
            if pygame.time.get_ticks() - 1000 > timer:
                timer += 1000
                print("FPS: " + str(fps) + " || TPS: " + str(tps))
                
                fps = 0
                tps = 0
            
            #Handle events
            for event in pygame.event.get(pygame.QUIT):
                sys.exit()
            
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()