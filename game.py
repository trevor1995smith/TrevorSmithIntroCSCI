#Trevor Smith
#Assignment 12
#4/12/25

import pygame
import sys
from gamefunctions import *

# Constants
SCREEN_SIZE = (320, 320)
GRID_SIZE, CELL_SIZE = 10, 32
COLORS = {
    'player': (0, 0, 255),
    'town': (0, 255, 0),
    'monster': (255, 0, 0),
    'bg': (255, 255, 255),
    'grid': (200, 200, 200)
}

class MapGame:
    def __init__(self, game_state):
        self.game_state = game_state
        self.init_pygame()
    
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Adventure Map")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        return self.game_state
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                new_pos = self.game_state['player_pos'].copy()
                
                if event.key == pygame.K_UP: new_pos[1] -= 1
                elif event.key == pygame.K_DOWN: new_pos[1] += 1
                elif event.key == pygame.K_LEFT: new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT: new_pos[0] += 1
                elif event.key == pygame.K_ESCAPE: 
                    self.running = False
                    show_save_menu(self.game_state)
                    return
                
                new_pos[0] = max(0, min(GRID_SIZE-1, new_pos[0]))
                new_pos[1] = max(0, min(GRID_SIZE-1, new_pos[1]))
                
                if new_pos != self.game_state['player_pos']:
                    self.game_state['player_pos'] = new_pos
                    save_game_state(self.game_state, "autosave.sav")
                    
                    if new_pos == self.game_state['town_pos']:
                        self.running = False
                    elif new_pos == self.game_state['monster_pos']:
                        self.handle_monster_encounter()
    
    def handle_monster_encounter(self):
        self.running = False
        pygame.quit()
        
        result = fight_monster(
            self.game_state['user_hp'],
            self.game_state['user_gold'],
            self.game_state['equipped_weapon'],
            self.game_state['inventory']
        )
        self.game_state['user_hp'], self.game_state['user_gold'], self.game_state['equipped_weapon'], self.game_state['inventory'] = result
        save_game_state(self.game_state, "autosave.sav")
        
        self.init_pygame()
        self.running = True

    def draw(self):
        try:
            self.screen.fill(COLORS['bg'])
            
            # Draw grid
            for x in range(0, SCREEN_SIZE[0], CELL_SIZE):
                pygame.draw.line(self.screen, COLORS['grid'], (x, 0), (x, SCREEN_SIZE[1]))
            for y in range(0, SCREEN_SIZE[1], CELL_SIZE):
                pygame.draw.line(self.screen, COLORS['grid'], (0, y), (SCREEN_SIZE[0], y))
            
            # Draw objects
            def draw_square(pos, color):
                pygame.draw.rect(self.screen, color, (
                    pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            draw_square(self.game_state['town_pos'], COLORS['town'])
            draw_square(self.game_state['monster_pos'], COLORS['monster'])
            draw_square(self.game_state['player_pos'], COLORS['player'])
            
            pygame.display.flip()
        except pygame.error:
            self.running = False

def town_menu(game_state):
    while True:
        display_town_menu(
            game_state['user_hp'],
            game_state['user_gold'],
            game_state['equipped_weapon']
        )
        
        choice = input("Choose an option: ")
        
        if choice == "1":  # Leave town
            map_game = MapGame(game_state.copy())
            updated_state = map_game.run()
            game_state.update(updated_state)
        elif choice == "2":  # Sleep
            game_state['user_hp'], game_state['user_gold'] = sleep(
                game_state['user_hp'], game_state['user_gold'])
            save_game_state(game_state, "autosave.sav")
        elif choice == "3":  # Visit Shop
            game_state['user_gold'], game_state['inventory'] = visit_shop(
                game_state['user_gold'], game_state['inventory'])
            save_game_state(game_state, "autosave.sav")
        elif choice == "4":  # Manage Inventory
            result = manage_inventory(
                game_state['equipped_weapon'],
                game_state['user_hp'],
                game_state['inventory'])
            game_state['equipped_weapon'], game_state['user_hp'], game_state['inventory'] = result
            save_game_state(game_state, "autosave.sav")
        elif choice == "5":  # Save and Quit
            show_save_menu(game_state)
            return

def main():
    print_welcome()
    game_state = show_main_menu()
    if game_state:
        town_menu(game_state)

if __name__ == "__main__":
    main()
