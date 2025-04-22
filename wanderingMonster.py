#Trevor Smith
#Assignment 14
#4/21/25

import random
import pygame

class WanderingMonster:
    """A class representing a wandering monster in the game."""

    MONSTER_TYPES = [
        {'name': 'Zombie', 'health_range': (15,25), 'power_range': (5,8), 
         'money_range': (5,10), 'color': (255, 0, 0), 'image': 'zombie.png'},
        {'name': 'Slime', 'health_range': (20,30), 'power_range': (6,9), 
         'money_range': (8,15), 'color': (0, 255, 0), 'image': 'slime.png'},
        {'name': 'Ghost', 'health_range': (25,40), 'power_range': (8,12), 
         'money_range': (15,25), 'color': (200, 200, 255), 'image': 'ghost.png'}
    ]
    
    def __init__(self, grid_size=10, town_pos=None, data=None):
        """Initialize a monster, either randomly or from saved data."""
        if data:
            # Initialize from saved data
            self.name = data['name']
            self.health = data['health']
            self.power = data['power']
            self.money = data['money']
            self.color = tuple(data['color'])
            self.position = data['position']
            self.image = data.get('image')
        else:
            # Initialize new random monster
            monster_type = random.choice(self.MONSTER_TYPES)
            self.name = monster_type['name']
            self.health = random.randint(*monster_type['health_range'])
            self.power = random.randint(*monster_type['power_range'])
            self.money = random.randint(*monster_type['money_range'])
            self.color = monster_type['color']
            self.image = monster_type['image']
            self.position = self._get_valid_position(grid_size, town_pos)
        
        # Load image with fallback to colored rectangle
        self.surface = self._load_image()
    
    def _load_image(self):
        """Load monster image with fallback to colored rectangle."""
        try:
            if self.image:
                img = pygame.image.load(self.image)
                return pygame.transform.scale(img, (32, 32))
        except (pygame.error, FileNotFoundError):
            pass
        
        # Fallback: create colored rectangle
        surface = pygame.Surface((32, 32))
        surface.fill(self.color)
        return surface
    
    def _get_valid_position(self, grid_size, town_pos):
        """Get a valid random position for the monster."""
        while True:
            pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]
            if town_pos is None or pos != town_pos:
                return pos
    
    def move(self, grid_size, town_pos, player_pos):
        """Attempt to move the monster."""
        directions = [
            [0, 1], [1, 0], [0, -1], [-1, 0],  # Cardinal directions
            [1, 1], [1, -1], [-1, 1], [-1, -1]   # Diagonal directions
        ]
        
        # Try moving toward player 50% of time
        if random.random() < 0.5:
            dx = 1 if player_pos[0] > self.position[0] else -1 if player_pos[0] < self.position[0] else 0
            dy = 1 if player_pos[1] > self.position[1] else -1 if player_pos[1] < self.position[1] else 0
            new_pos = [self.position[0] + dx, self.position[1] + dy]
        else:
            direction = random.choice(directions)
            new_pos = [self.position[0] + direction[0], self.position[1] + direction[1]]
        
        # Check if new position is valid
        if (0 <= new_pos[0] < grid_size and 
            0 <= new_pos[1] < grid_size and 
            new_pos != town_pos):
            self.position = new_pos
            return True
        return False

    def to_dict(self):
        """Convert monster to serializable dictionary."""
        return {
            'name': self.name,
            'health': self.health,
            'power': self.power,
            'money': self.money,
            'color': self.color,
            'position': self.position,
            'image': self.image
        }

