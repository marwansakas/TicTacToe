# Multiplayer Tic-Tac-Toe

## Overview
This project is a real-time multiplayer Tic-Tac-Toe game built using Python and Pygame, with client-server communication handled via sockets. Players can create or join game rooms and compete in turn-based matches with synchronized gameplay.

## Features
- Real-time multiplayer gameplay
- Pygame-based graphical user interface
- Interactive menu for creating and joining game rooms
- Server architecture to manage multiple game sessions
- Smooth event handling and animations for an engaging user experience

## Installation
### Prerequisites
- Python 3.x
- Pygame (`pip install pygame`)

### Running the Server
1. Navigate to the project directory.
2. Run the server script:
   ```sh
   python server.py
   ```

### Running the Client
1. Navigate to the project directory.
2. Run the client script:
   ```sh
   python main.py
   ```

## How to Play
1. Start the server.
2. Run the client and either create a new game or join an existing room using its ID.
3. Take turns placing marks (X or O) on the board until a player wins or the game ends in a draw.

## Project Structure
- `server.py` – Handles game sessions, player connections, and message broadcasting.
- `main.py` – Initializes the client and connects to the server.
- `Game.py` – Manages the overall game logic and switching between screens.
- `Menu.py` – Provides UI elements for creating and joining games.
- `TicTacToe.py` – Implements the Tic-Tac-Toe board and gameplay mechanics.
- `Board.py` – Abstract class defining the board interface.

## Future Improvements
- Add support for AI opponents.
- Implement a lobby system for better game room management.
- Improve UI with animations and sound effects.
