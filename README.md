# Squativa - the Squat Game

Squativa is an interactive fitness game that combines rhythm and squats. Players perform squats in sync with a rhythm pattern while maintaining proper form to score points. The game supports two players and uses a webcam for squat detection.
Presented by Intania Hackathon

## Features
- **Rhythm-Based Gameplay**: Perform squats in sync with the rhythm pattern.
- **Real-Time Feedback**: Detects squat form and provides feedback on posture.
- **Multiplayer Support**: Two players can compete simultaneously.
- **Custom Songs and Difficulties**: Select songs and difficulty levels.
- **Dynamic Graphics**: Visual feedback with squat graphics and target zones.

## Requirements
- Python 3.8+
- Pygame
- OpenCV
- MediaPipe

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd intahack
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the game:
   ```bash
   python main.py
   ```
2. Use the menu to select a song and difficulty.
3. Follow the rhythm and perform squats in front of the webcam.

## Folder Structure
- `game.py`: Main game logic.
- `screens.py`: Handles different game screens (menu, countdown, game, results).
- `opcv/squat_late.py`: Squat detection using MediaPipe and OpenCV.
- `utils.py`: Utility functions for loading assets and rendering graphics.

## Controls
- **Menu Navigation**: Use the mouse to select options.
- **Quit**: Press `Q` or `Esc` to exit the game.

## License
This project is for educational purposes only.
