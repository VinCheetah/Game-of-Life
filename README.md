# Game of Life

Welcome to the Game of Life! This is a Python implementation of the famous cellular automaton devised by the mathematician John Conway. The Game of Life is a zero-player game that simulates the evolution of cells in a grid based on a set of simple rules. This README file will guide you through the setup and usage of this project.

## Installation

1. Ensure that you have Python 3 and pygame installed on your system.
2. Clone the project repository from GitHub or download it manually:

   ```
   git clone https://github.com/your-username/game-of-life.git
   ```

3. Navigate to the project directory:

   ```
   cd game-of-life
   ```


## Usage

To run the Game of Life simulation, you need to execute the `gol_final.py` file. You can do this by running the following command:

```
python gol_final.py
```

Once the simulation starts, you will see a graphical window displaying a grid of cells. The cells will evolve over time according to the rules of the Game of Life.

If you want to run the previous version of the project you need to execute `main.py` file. You can do this by running the following command:

```
python main.py
```

### Controls

#### Placing Cells:

- **Flip Alive Cell**: Click on a cell to make it alive.
- **Multiple Flip Alive Cells**: Press and hold the mouse button to draw multiple alive cells.

#### Simulation:

- **Next Generation**: Press the `SPACE` key to advance to the next generation.
- **Clean Board**: Press the `C` key to clear the entire board (kill all cells).
- **Fill Board**: Press the `W` key to fill the entire board with random alive cells.

#### Project Management:

- **New Project**: Press the keys `0`, `1`, `2`, ..., `9` to create a new project with a specific key.
- **Move Project**: Use the arrow keys to move around the board.
- **Boost Move**: Press the `B` key while using the arrow keys to move faster.
- **Destroy Project**: Press the `ESC` key to destroy the current project.
- **Build Project**: Press the `SPACE` key to build a new project.

#### Automation:

- **Flip Auto Generation**: Press the `A` key to enable/disable automatic generation.
- **Speed Up**: Press the `P` key to increase the speed of automatic generation.
- **Speed Down**: Press the `M` key to decrease the speed of automatic generation.

#### Cell Color:

- **Flip Color**: Press the `F` key to change the color of the alive cells.

## Class Descriptions

### `Color` class

This class defines various colors used in the simulation.

### `Cell` class

This class represents a single cell in the Game of Life. It has methods for handling birth, death, updating its state based on the number of neighbors, and changing its color.

### `Corallien_cell` class (Subclass of `Cell`)

This class inherits from `Cell` and adds an extra attribute for handling cells in a "skeleton" state. The `consider_alive` method is redefined to include the skeleton state in determining whether the cell is considered alive.

### `Game` class

This class manages the overall game mechanics, including initializing the board, handling neighbor connections, updating the entire board to the next generation, displaying the grid, and managing user input and project management.

### `Cora` class (Subclass of `Game`)

The `Cora` class is a subclass of `Game` and represents a variant of the Game of Life called "Cora."
It overrides the `new_generation` method to provide custom rules for cell updates specific to the Cora variant.

## Contributing

If you wish to contribute to this project, you can follow these steps:

1. Fork the repository on GitHub.
2. Make your desired changes to the codebase.
3. Write tests to ensure the functionality is not compromised (if applicable).
4. Submit a pull request, explaining the changes you have made.

Your contributions are greatly appreciated!

## License

You are free to use, modify, and distribute the code for both commercial and non-commercial purposes.

## Acknowledgments

This implementation of the Game of Life is based on the original rules and concepts developed by John Conway. The code structure and project setup were inspired by various open-source projects and tutorials available online.
Some predefined patterns with amazing properties are saved and can be placed by pressing a number.
The corallien version of the game of life is a different version where a dead cell become a skeleton which is considered as alive by its neighbours.
You can relatively easily implement your own rules in the game, by creating a new son class of Game and one for Cell.
Have Fun !

If you have any questions or need further assistance, please don't hesitate to reach out to us. Have fun exploring the fascinating patterns that emerge from the Game of Life simulation. Feel free to experiment with different initial configurations, colors, and automation settings to create interesting and complex patterns. Happy gaming!

