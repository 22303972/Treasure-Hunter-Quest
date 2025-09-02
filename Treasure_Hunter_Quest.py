import pygame
import sys
import random
import time
import os
import unittest

# =========================
# Constants & Config
# =========================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
LEVEL_WIDTH = 20   # tiles
LEVEL_HEIGHT = 15  # tiles

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)

TIME_LIMIT = 300  # 5 minutes in seconds
DAMAGE_COOLDOWN_MS = 500  # minimum time between enemy hits
HEALTH_DRAIN_PERIOD = 10  # seconds

# =========================
# Items
# =========================
def get_emoji_font(font_size):
    # Try emoji fonts, fallback to Arial
    for font_name in ["Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", "arial"]:
        try:
            font = pygame.font.SysFont(font_name, font_size)
            # Test rendering an emoji
            if font.render('💎', True, (255,255,255)).get_width() > 0:
                return font
        except Exception:
            continue
    return pygame.font.SysFont("arial", font_size)

def load_sprite(filename):
    path = os.path.join(os.path.dirname(__file__), "assets", filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

class Item(pygame.sprite.Sprite):
    """Base class for all collectible items."""
    def __init__(self, x, y, item_type):
        super().__init__()
        self.type = item_type
        sprite_map = {
            'potion': "potion.png",
            'key': "key.png",
            'treasure': "treasure.png"
        }
        self.image = load_sprite(sprite_map[item_type])
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))

class Potion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'potion')

    def use(self, player):
        player.health = min(player.health + 20, 100)
        # pygame.mixer.Sound('heal.wav').play()

class Key(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'key')

    def use(self, player):
        # Keys are auto-consumed at doors
        pass

class Treasure(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'treasure')

# =========================
# Player
# =========================
class Player(pygame.sprite.Sprite):
    """Controllable player character."""
    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("player.png")
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.health = 100
        self.inventory = []
        self.keys = 0
        self.treasures_collected = 0
        self._last_damage_ms = 0  # for enemy hit cooldown

    def move(self, dx, dy, level):
        new_x = self.rect.x + dx * TILE_SIZE
        new_y = self.rect.y + dy * TILE_SIZE
        if level.is_valid_move(new_x // TILE_SIZE, new_y // TILE_SIZE, self):
            self.rect.x = new_x
            self.rect.y = new_y

    def collect_item(self, item):
        self.inventory.append(item)
        if item.type == 'key':
            self.keys += 1
        elif item.type == 'treasure':
            self.treasures_collected += 1
        item.kill()  # remove from world
        # pygame.mixer.Sound('collect.wav').play()

    def use_item(self, item_type):
        for item in self.inventory:
            if item.type == item_type:
                if item_type == 'potion':
                    item.use(self)
                # keys are auto-used at doors, but allow manual removal if needed
                self.inventory.remove(item)
                return True
        return False

    def take_damage(self, amount):
        now = pygame.time.get_ticks()
        if now - self._last_damage_ms < DAMAGE_COOLDOWN_MS:
            return  # still in cooldown
        self._last_damage_ms = now
        self.health = max(self.health - amount, 0)
        # pygame.mixer.Sound('hurt.wav').play()

# =========================
# Enemy
# =========================
class Enemy(pygame.sprite.Sprite):
    """Simple patrolling enemy with random movement."""
    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("enemy.png")
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))

    def patrol(self, level):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dx, dy = random.choice(directions)
        new_x = self.rect.x + dx * TILE_SIZE
        new_y = self.rect.y + dy * TILE_SIZE
        if level.is_valid_move(new_x // TILE_SIZE, new_y // TILE_SIZE, self):
            self.rect.x = new_x
            self.rect.y = new_y

# =========================
# Level
# =========================
class Level:
    """Tile-based map with walls (1) and locked door (2)."""
    def __init__(self):
        # 0: open, 1: wall, 2: locked door
        self.map = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
            [1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
            [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],  # 2 = door
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.exit_pos = (18, 13)  # door position

    def is_valid_move(self, x, y, entity):
        if 0 <= x < LEVEL_WIDTH and 0 <= y < LEVEL_HEIGHT:
            tile = self.map[y][x]
            if tile == 1:
                return False  # Wall
            if tile == 2:  # Door
                # Player with a key unlocks and proceeds
                if isinstance(entity, Player) and entity.keys > 0:
                    entity.keys -= 1
                    self.map[y][x] = 0  # Unlock door
                    return True
                return False
            return True
        return False

    def draw(self, screen):
        wall_img = load_sprite("wall.png")
        door_img = load_sprite("door.png")
        for y in range(LEVEL_HEIGHT):
            for x in range(LEVEL_WIDTH):
                if self.map[y][x] == 1:
                    screen.blit(wall_img, (x * TILE_SIZE, y * TILE_SIZE))
                elif self.map[y][x] == 2:
                    screen.blit(door_img, (x * TILE_SIZE, y * TILE_SIZE))

# =========================
# Game
# =========================
class Game:
    """Main game orchestrator."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Treasure Hunter Quest")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.running = True
        self.state = "playing"  # playing | win | lose

        self.start_time = time.time()
        self._last_health_drain_at = self.start_time

        self.level = Level()

        # Start near bottom-left for safer spawn or (1,1) if you prefer:
        # self.player = Player(1, 13)
        self.player = Player(1, 1)

        self.all_sprites = pygame.sprite.Group(self.player)

        # Items
        self.items = pygame.sprite.Group(
            Potion(3, 2), Key(5, 5), Treasure(10, 10),
            Potion(15, 3), Key(8, 12), Treasure(2, 8), Treasure(17, 7)
        )

        # Enemies
        self.enemies = pygame.sprite.Group(
            Enemy(10, 5), Enemy(15, 10), Enemy(5, 12)
        )

        self.all_sprites.add(self.items, self.enemies)

        # High score file
        self.high_score_file = "highscore.txt"
        if not os.path.exists(self.high_score_file):
            with open(self.high_score_file, 'w') as f:
                f.write("0")

    # ---------------------
    # Main loop
    # ---------------------
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            if self.state == "playing":
                self.update()
            self.render()
        pygame.quit()
        sys.exit()

    # ---------------------
    # Event handling
    # ---------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == "playing":
                    if event.key == pygame.K_w:
                        self.player.move(0, -1, self.level)
                    elif event.key == pygame.K_s:
                        self.player.move(0, 1, self.level)
                    elif event.key == pygame.K_a:
                        self.player.move(-1, 0, self.level)
                    elif event.key == pygame.K_d:
                        self.player.move(1, 0, self.level)
                    elif event.key == pygame.K_p:
                        self.player.use_item('potion')

                if self.state in ("win", "lose") and event.key == pygame.K_r:
                    self.__init__()  # Restart

    # ---------------------
    # Update logic
    # ---------------------
    def update(self):
        # Enemy movement (randomly, to slow the AI)
        if random.randint(1, 10) == 1:
            for enemy in self.enemies:
                enemy.patrol(self.level)

        # Item collection
        item_hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for item in item_hits:
            self.player.collect_item(item)

        # Enemy collisions (with cooldown inside take_damage)
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            self.player.take_damage(10)

        # Health drain over time (once every HEALTH_DRAIN_PERIOD seconds)
        now = time.time()
        if now - self._last_health_drain_at >= HEALTH_DRAIN_PERIOD and self.state == "playing":
            self.player.take_damage(1)
            self._last_health_drain_at += HEALTH_DRAIN_PERIOD

        # Time check
        elapsed = now - self.start_time
        if elapsed > TIME_LIMIT:
            self.state = "lose"

        # Win check: have all treasures AND stand on exit tile (after unlocking)
        if (self.player.treasures_collected == 3 and
            (self.player.rect.x // TILE_SIZE, self.player.rect.y // TILE_SIZE) == self.level.exit_pos):
            self.state = "win"
            score = max(0, int((TIME_LIMIT - elapsed) * (self.player.health / 100)))
            self.save_high_score(score)

        if self.player.health <= 0:
            self.state = "lose"

    # ---------------------
    # Render
    # ---------------------
    def render(self):
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        self.all_sprites.draw(self.screen)

        # Horizontal UI at the top
        ui_y = 10
        ui_spacing = 30

        # Health: draw hearts
        heart_img = load_sprite("heart.png")
        for i in range(self.player.health // 20):  # 1 heart per 20 HP
            self.screen.blit(heart_img, (10 + i * (heart_img.get_width() + 5), ui_y))

        # Time: draw clock icon and time left
        clock_img = load_sprite("clock.png")
        time_left = max(0, TIME_LIMIT - int(time.time() - self.start_time))
        time_color = RED if time_left < 60 else WHITE
        clock_x = 10 + 5 * (heart_img.get_width() + 5) + ui_spacing
        self.screen.blit(clock_img, (clock_x, ui_y))
        time_text = self.font.render(f"{time_left}s", True, time_color)
        self.screen.blit(time_text, (clock_x + clock_img.get_width() + 5, ui_y))

        # Treasures: draw treasure icon and count
        treasure_img = load_sprite("treasure.png")
        treasure_x = clock_x + clock_img.get_width() + time_text.get_width() + ui_spacing + 10
        self.screen.blit(treasure_img, (treasure_x, ui_y))
        treasures_text = self.font.render(f"{self.player.treasures_collected}/3", True, WHITE)
        self.screen.blit(treasures_text, (treasure_x + treasure_img.get_width() + 5, ui_y))

        # Game state messages
        if self.state == "win":
            win_text = self.font.render("*** YOU WIN! *** Press R to Restart", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            bg_rect = win_rect.inflate(30, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, GREEN, bg_rect, 3)
            self.screen.blit(win_text, win_rect)
        elif self.state == "lose":
            lose_text = self.font.render("*** GAME OVER *** Press R to Restart", True, RED)
            lose_rect = lose_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            bg_rect = lose_rect.inflate(30, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, RED, bg_rect, 3)
            self.screen.blit(lose_text, lose_rect)

        # Instructions at bottom
        if self.state == "playing":
            instructions = self.font.render("WASD to move, P to use potion", True, WHITE)
            instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
            self.screen.blit(instructions, instructions_rect)

        pygame.display.flip()

    # ---------------------
    # High score
    # ---------------------
    def save_high_score(self, score):
        try:
            with open(self.high_score_file, 'r') as f:
                current = int(f.read().strip() or "0")
        except (ValueError, FileNotFoundError):
            current = 0
        if score > current:
            with open(self.high_score_file, 'w') as f:
                f.write(str(score))

# ====================================
# Unit Tests
# =========================
class TestGame(unittest.TestCase):
    def setUp(self):
        # Optional: headless mode for CI
        # os.environ["SDL_VIDEODRIVER"] = "dummy"
        self.game = Game()
        self.player = self.game.player

    def test_health_increase(self):
        self.player.health = 60
        potion = Potion(0, 0)
        self.player.collect_item(potion)
        self.player.use_item('potion')
        self.assertEqual(self.player.health, 80)

    def test_damage(self):
        self.player.health = 100
        # Reset cooldown to allow immediate damage
        self.player._last_damage_ms = -DAMAGE_COOLDOWN_MS
        self.player.take_damage(10)
        self.assertEqual(self.player.health, 90)

    def test_collection(self):
        item = Item(0, 0, 'treasure')
        initial_len = len(self.player.inventory)
        self.player.collect_item(item)
        self.assertEqual(len(self.player.inventory), initial_len + 1)
        self.assertEqual(self.player.treasures_collected, 1)

if __name__ == "__main__":
    # Uncomment to run tests directly:
    # unittest.main()

    game = Game()
    game.run()