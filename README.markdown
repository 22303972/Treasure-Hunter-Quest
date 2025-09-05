# Treasure Hunter Quest

## Overview
Treasure Hunter Quest is a 2D tile-based adventure game built using Python and the Pygame library. The player navigates a maze-like level to collect three treasures, avoid enemies, and reach an exit door within a 5-minute time limit. The game features health management, item collection (potions and keys), and a high-score system. The objective is to collect all treasures and exit the level while maintaining health, which gradually drains over time and upon enemy contact.

## Features
- **Tile-based Gameplay**: Navigate a 20x15 grid with walls, open spaces, and a locked door requiring a key.
- **Player Mechanics**: Move with WASD keys, collect items (potions, keys, treasures), and use potions (P key) to restore health.
- **Health System**: Player starts with 100 HP, loses 1 HP every 10 seconds, and 10 HP upon enemy contact (with a 500ms cooldown).
- **Enemies**: Three enemies patrol randomly, posing a threat upon collision.
- **Items**:
  - **Potions**: Restore 20 HP (up to 100 max).
  - **Keys**: Unlock the exit door.
  - **Treasures**: Collect all three to win.
- **Time Limit**: 5 minutes to complete the objective.
- **Win/Lose Conditions**:
  - **Win**: Collect all treasures and reach the unlocked exit.
  - **Lose**: Run out of time or health.
- **High Score**: Saves the highest score based on remaining time and health upon winning.
- **UI**: Displays health (hearts), time (clock), treasure count, and instructions.
- **Unit Tests**: Tests for health increase, damage, and item collection.

## Installation
To run Treasure Hunter Quest, you need Python and Pygame installed, along with the required sprite assets.

### Prerequisites
- **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/).
- **Pygame**: Install via pip:
  ```bash
  pip install pygame
  ```

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/treasure-hunter-quest.git
   cd treasure-hunter-quest
   ```

2. **Asset Files**:
   Ensure the `assets` folder contains the following sprite images (40x40 pixels):
   - `player.png`: Player character sprite.
   - `enemy.png`: Enemy sprite.
   - `wall.png`: Wall tile sprite.
   - `door.png`: Locked door sprite.
   - `potion.png`: Potion sprite.
   - `key.png`: Key sprite.
   - `treasure.png`: Treasure sprite.
   - `heart.png`: Health indicator sprite.
   - `clock.png`: Timer sprite.
   > Note: You may need to create or source these images, as they are not included in the repository. Place them in an `assets` subfolder.

3. **Run the Game**:
   ```bash
   python Treasure_Hunter_Quest.py
   ```

4. **Run Unit Tests** (optional):
   Uncomment the `unittest.main()` line in `Treasure_Hunter_Quest.py` and run:
   ```bash
   python Treasure_Hunter_Quest.py
   ```

## Gameplay
- **Objective**: Collect 3 treasures and reach the exit door (requires a key) within 5 minutes.
- **Controls**:
  - **WASD**: Move up, down, left, right.
  - **P**: Use a potion to restore 20 HP.
  - **R**: Restart after win/lose.
- **Mechanics**:
  - Navigate a maze with walls and a locked door.
  - Collect potions (2), keys (2), and treasures (3).
  - Avoid enemies that move randomly and deal 10 HP damage on contact.
  - Health drains by 1 HP every 10 seconds.
  - Time limit is 5 minutes; a red timer indicates <60 seconds left.
- **Win**: Collect all treasures and stand on the exit tile after unlocking the door.
- **Lose**: Health reaches 0 or time runs out.
- **Score**: Calculated as `max(0, int((300 - elapsed_time) * (health / 100)))` upon winning, saved to `highscore.txt`.

## File Structure
```
treasure-hunter-quest/
├── assets/
│   ├── player.png
│   ├── enemy.png
│   ├── wall.png
│   ├── door.png
│   ├── potion.png
│   ├── key.png
│   ├── treasure.png
│   ├── heart.png
│   ├── clock.png
├── Treasure_Hunter_Quest.py
├── highscore.txt
└── README.md
```

## Development Notes
- **Dependencies**: Pygame for rendering and game mechanics; `os`, `sys`, `random`, `time` for system operations.
- **Font Handling**: Attempts to use emoji-compatible fonts (`Apple Color Emoji`, `Segoe UI Emoji`, `Noto Color Emoji`) with fallback to Arial.
- **Sprite Loading**: Sprites are scaled to 40x40 pixels (TILE_SIZE) and loaded from the `assets` folder.
- **Enemy AI**: Simple random movement (10% chance per frame) to reduce performance impact.
- **Health Drain**: Occurs every 10 seconds to add urgency.
- **Damage Cooldown**: 500ms to prevent rapid health loss from enemies.
- **Unit Tests**: Cover health increase, damage application, and item collection.
- **Limitations**:
  - Sound effects (`heal.wav`, `collect.wav`, `hurt.wav`) are commented out due to missing assets.
  - File I/O (e.g., `highscore.txt`) assumes local write permissions.
  - No support for Pyodide/browser execution; requires desktop Python environment.

## Future Improvements
- Add sound effects and background music.
- Implement multiple levels or procedurally generated maps.
- Add more enemy behaviors (e.g., chasing the player).
- Include a main menu and pause functionality.
- Support Pyodide for browser-based gameplay.
- Add visual effects for item collection and damage.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.