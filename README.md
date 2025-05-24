# Valorant Pathfinding Project

This project implements an A* pathfinding algorithm for Valorant maps, specifically designed to help visualize and navigate through the game's environment. The project includes tools for both visualizing paths on the minimap and simulating movement based on the calculated paths.

## Features

- Interactive minimap visualization of Valorant maps (currently supports Ascent)
- A* pathfinding algorithm with customizable start and end points
- Real-time path visualization
- Movement simulation using keyboard inputs
- Grid-based navigation system

## Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - OpenCV (`cv2`)
  - NumPy
  - Matplotlib
  - PyAutoGUI
  - MSS (for screen capture)
  - PyQt5 or Tkinter (for GUI components)

## Installation

1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd valo_project
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install them manually:
   ```bash
   pip install opencv-python numpy matplotlib pyautogui mss PyQt5
   ```

## Usage

### Visualizing Paths (pathfind.py)

1. Run the visualization tool:
   ```bash
   python pathfind.py
   ```

2. In the displayed window:
   - Left-click to set the starting point (green)
   - Right-click to set the goal (red)
   - The path will be automatically calculated and displayed
   - Use the 'Reset' button to clear all points

### Automated Movement (main_pathfind.py)

1. Make sure Valorant is running in windowed or windowed fullscreen mode
2. Run the main script:
   ```bash
   python main_pathfind.py
   ```

3. In the displayed minimap window:
   - Click anywhere on the minimap to set the destination
   - The script will calculate the path and simulate movement
   - Press 'q' to quit the application

## Project Structure

- `pathfind.py`: Visualization tool for pathfinding on the minimap
- `main_pathfind.py`: Main script for automated movement
- `matrix_ascent50.txt`/`matrix_ascent60.txt`: Grid representations of the Ascent map
- `images/`: Directory containing minimap images and templates

## Customization

### Adding New Maps

1. Add a new minimap image to the `images/` directory
2. Create a corresponding grid file (0 for walls, 1 for walkable areas)
3. Update the code to load your new map and grid

### Adjusting Parameters

- Modify `region` in `main_pathfind.py` to match your screen resolution and minimap position
- Adjust `GRID_SIZE` to match your grid file dimensions
- Tune movement timing in `smooth_interpolated_move()` for better control

## Important Notes

- This is a proof-of-concept project and may not work perfectly in all game situations
- Use at your own risk - while this doesn't modify game memory, automated inputs might be against the game's terms of service
- The pathfinding is based on a simplified grid and may not account for all in-game obstacles

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- A* pathfinding algorithm
- Valorant game assets are property of Riot Games
