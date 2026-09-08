# Python F1 Car Simulator

This repository contains the final version of the racing game, developed in the `Iteration 5` folder. It is a full Pygame-based F1 simulator with a menu flow, track selection, car selection, login system, lap timing, and an AI opponent.

## What this project is

The final game is a local racing simulator where the player:
- chooses a car
- selects a track
- drives around the circuit using keyboard controls
- races against a computer-controlled opponent
- records lap times and results
- views leaderboard information


## Final game features

- car selection screen
- track selection menu
- login/signup flow
- password and user data handling
- race HUD with time and gap display
- AI competitor pathing
- collision detection and boundary handling
- lap result / leaderboard tracking
- multiple track assets and custom UI graphics

## Project structure

The main game logic is in the final iteration folder:

- `Iteration 5/main_game.py` — main racing game logic
- `Iteration 5/game_states_handler.py` — starts the game flow
- `Iteration 5/track_selection_menu.py` — track picker
- `Iteration 5/car_selection.py` — car selection
- `Iteration 5/login.py` and related files — account flow
- `Iteration 5/tracks.py` — track definitions and assets
- `Iteration 5/utils.py` — graphics and helper functions
- `Iteration 5/leaderbord_handler.py` — leaderboard and best lap tracking

## How to run the final game

1. Open the `Iteration 5` folder in VS Code or your terminal.
2. Make sure Python and Pygame are installed.
3. Run the main game state handler:

```bash
python game_states_handler.py
```

If you are using VS Code, the project is also set up so you can simply open `game_states_handler.py` and press Run.

## Controls

Use either of these schemes while racing:
- `W`, `A`, `S`, `D`
- arrow keys

## Requirements

- Python 3
- Pygame
- The asset folders and project files in the `Iteration 5` folder

## Notes

- The final game is in the `Iteration 5` directory rather than the older root-level prototype files.
- This project is a coursework/demo racing game and is intended for local play and testing.
- Some files rely on the relative folder structure staying intact, so keep the project files together.
