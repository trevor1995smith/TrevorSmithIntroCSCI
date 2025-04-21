#Trevor Smith
#Assignment 13
#4/20/25

import pygame
import sys
import random
from gamefunctions import *
from wanderingMonster import WanderingMonster

# Game display constants
SCREEN_SIZE = (320, 320)
CELL_SIZE = 32
COLORS = {
    'player': (0, 0, 255),      # Blue
    'town': (0, 255, 0),        # Green
    'bg': (255, 255, 255),      # White
    'grid': (200, 200, 200)     # Light gray
}

class MapGame:
    def __init__(self, game_state):
        """Initialize the game map with monsters and pygame."""
        self.game_state = game_state
        self._initialize_monsters()
        self.init_pygame()
    
    def _initialize_monsters(self):
        """Ensure proper monster initialization in game state."""
        if 'monsters' not in self.game_state:
            self.game_state['monsters'] = []
        
        # Create new monsters if none exist or if they're not valid
        if len(self.game_state['monsters']) == 0 or not isinstance(self.game_state['monsters'][0], WanderingMonster):
            self.game_state['monsters'] = [
                WanderingMonster(GRID_SIZE, self.game_state['town_pos']),
                WanderingMonster(GRID_SIZE, self.game_state['town_pos'])
            ]
    
    def init_pygame(self):
        """Initialize pygame components."""
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Adventure Map")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        return self.game_state
    
    def handle_events(self):
        """Handle user input and game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                new_pos = self.game_state['player_pos'].copy()
                
                # Handle movement keys
                if event.key == pygame.K_UP: new_pos[1] -= 1
                elif event.key == pygame.K_DOWN: new_pos[1] += 1
                elif event.key == pygame.K_LEFT: new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT: new_pos[0] += 1
                elif event.key == pygame.K_ESCAPE: 
                    self.running = False
                    show_save_menu(self.game_state)
                    return
                
                # Keep player within bounds
                new_pos[0] = max(0, min(GRID_SIZE-1, new_pos[0]))
                new_pos[1] = max(0, min(GRID_SIZE-1, new_pos[1]))
                
                if new_pos != self.game_state['player_pos']:
                    self.game_state['player_pos'] = new_pos
                    save_game_state(self.game_state, "autosave.sav")
                    
                    # Check for town entry
                    if new_pos == self.game_state['town_pos']:
                        self.running = False
                    else:
                        self._handle_monster_collisions()
                    
                    # Move monsters every other player move (50% chance)
                    if len(self.game_state['monsters']) > 0 and random.random() < 0.5:
                        for monster in self.game_state['monsters']:
                            monster.move(
                                GRID_SIZE,
                                self.game_state['town_pos'],
                                self.game_state['player_pos']
                            )
    
    def _handle_monster_collisions(self):
        """Check for and handle player-monster collisions."""
        monsters_to_remove = []
        for i, monster in enumerate(self.game_state['monsters']):
            if self.game_state['player_pos'] == monster.position:
                # Pause pygame to handle text-based combat
                self.running = False
                pygame.quit()
                
                # Fight the monster
                result = fight_monster(
                    self.game_state['user_hp'],
                    self.game_state['user_gold'],
                    self.game_state['equipped_weapon'],
                    self.game_state['inventory'],
                    monster
                )
                # Update game state with combat results
                self.game_state['user_hp'], self.game_state['user_gold'], \
                self.game_state['equipped_weapon'], self.game_state['inventory'], defeated = result
                
                if defeated:
                    monsters_to_remove.append(i)
                
                # Save after combat
                save_game_state(self.game_state, "autosave.sav")
                
                # Restart pygame
                self.init_pygame()
                self.running = True
                break
        
        # Remove defeated monsters
        for i in sorted(monsters_to_remove, reverse=True):
            self.game_state['monsters'].pop(i)
        
        # Respawn monsters if all were defeated
        if len(self.game_state['monsters']) == 0:
            self.game_state['monsters'] = [
                WanderingMonster(GRID_SIZE, self.game_state['town_pos']),
                WanderingMonster(GRID_SIZE, self.game_state['town_pos'])
            ]
    
    def draw(self):
        """Render the game state."""
        try:
            # Clear screen
            self.screen.fill(COLORS['bg'])
            
            # Draw grid lines
            for x in range(0, SCREEN_SIZE[0], CELL_SIZE):
                pygame.draw.line(self.screen, COLORS['grid'], (x, 0), (x, SCREEN_SIZE[1]))
            for y in range(0, SCREEN_SIZE[1], CELL_SIZE):
                pygame.draw.line(self.screen, COLORS['grid'], (0, y), (SCREEN_SIZE[0], y))
            
            # Helper function to draw colored squares
            def draw_square(pos, color):
                pygame.draw.rect(self.screen, color, (
                    pos[0] * CELL_SIZE, 
                    pos[1] * CELL_SIZE, 
                    CELL_SIZE, 
                    CELL_SIZE
                ))
            
            # Draw game objects
            draw_square(self.game_state['town_pos'], COLORS['town'])
            
            # Draw each monster with its specific color
            for monster in self.game_state['monsters']:
                draw_square(monster.position, monster.color)
            
            draw_square(self.game_state['player_pos'], COLORS['player'])
            
            pygame.display.flip()
        except pygame.error:
            self.running = False

def town_menu(game_state):
    """Handle the town menu interface."""
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
    """Main game entry point."""
    print_welcome()
    game_state = show_main_menu()
    if game_state:
        town_menu(game_state)

if __name__ == "__main__":
    main()
