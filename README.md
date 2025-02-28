                   ,     \    /      ,
                  / \    )\__/(     / \
                 /   \  (_\  /_)   /   \
           ____/______\__\@  @/___/______\____
          |             |\../|              |
          |              \VV/               |
          |         DUNGEON CRAWLER         |
          |_________________________________|
           |    /\ /      \\       \ /\    |
           |  /   V        ))       V   \  |
           |/     `       //        '     \|

# Dungeon Crawler: A Professional Pygame Adventure

## Overview

Dungeon Crawler is a retro-inspired, tile-based adventure game developed using Python and Pygame. This project incorporates classic arcade gameplay with modern programming practices. Players navigate intricate dungeons filled with enemies, obstacles, and valuable collectibles, while using precise combat mechanics to overcome challenges.

## Features

- **Dynamic Gameplay:** Navigate procedurally generated dungeons with increasing complexity.
- **Responsive Combat:** Engage with enemies using finely-tuned controls for movement and attacks.
- **Modular Architecture:** Well-organized codebase with distinct modules handling game world generation, character behavior, weapon mechanics, and item interactions.
- **Customizable Levels:** Includes CSV-based level designs, which can be easily modified or expanded.
- **Professional Asset Management:** Optimized loading and usage of pixel art assets, sounds, and fonts.

## Requirements

- **Python:** Version 3.9 or later
- **Pygame:** Install via pip

```bash
pip install pygame
```

## Installation and Setup

### Quick Start Guide for Beginners

Follow these simple steps to get started quickly:

1. **Install Python**

   - Ensure you have Python (version 3.9 or later) installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Clone the Repository**

   - Open your terminal or command prompt and run:
     ```bash
     git clone https://github.com/yourusername/dungeon-crawler.git
     cd dungeon-crawler
     ```
   - This downloads the project code to your computer and navigates into the project folder.

3. **Set Up a Virtual Environment (Optional but Recommended)**

   - Create a virtual environment to keep your dependencies organized:
     ```bash
     python -m venv venv
     ```
   - Activate it:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

4. **Install Dependencies**

   - With the virtual environment activated (or your system Python), install Pygame by running:
     ```bash
     pip install pygame
     ```
   - This command installs all necessary libraries for the game.

5. **Launch the Game**
   - Once dependencies are installed, start the game by running:
     ```bash
     python main.py
     ```
   - A game window should open, and you can start playing immediately.

### Additional Tips for New Users

- **Troubleshooting Installation Issues:**

  - If you encounter issues during installation, make sure your Python version is 3.9 or above.
  - Verify that pip is installed and updated by running `pip --version`.

- **Learning Python:**

  - If you are new to Python, consider following some beginner tutorials online to understand basic concepts.
  - The official [Python documentation](https://docs.python.org/3/tutorial/) is a great resource.

- **Getting Help:**
  - If you need further assistance, feel free to open an issue on the [GitHub repository](https://github.com/yourusername/dungeon-crawler) or search for answers online.

---

## Project Structure

- **main.py:** Initializes the game window, manages the game loop, and orchestrates state transitions.
- **world.py:** Responsible for procedural generation and management of the game world, including loading level layouts from CSV files found in the `levels/` directory.
- **character.py:** Defines the behavior and properties of both player characters and enemies, including movement and collision detection.
- **weapon.py:** Implements weapon mechanics, such as projectile (arrow) behavior, trajectory, and collision with targets.
- **items.py:** Manages game collectibles and power-ups, ensuring appropriate effects when collected by the player.
- **powerup.py:** Specializes in handling temporary buffs and power-ups that modify gameplay, such as increased damage or speed.
- **button.py:** Contains UI elements for interactive menus and buttons, enhancing the user experience.
- **constants.py:** Centralizes configuration values such as screen dimensions, color schemes, and other constants used throughout the project.

## Contribution

Contributions are welcome! Feel free to fork this repository, create feature branches, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements

Thank you for exploring Dungeon Crawler. Your feedback and contributions are highly valued as we continue to refine and expand this game.
