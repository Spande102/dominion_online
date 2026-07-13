# Dominion - Online Multiplayer Edition

A Python-based web implementation of the classic deck-building card game **Dominion**, with online multiplayer support.

## Features

### Core Gameplay
- **Text-based interface** for interactive gameplay
- **Base Dominion set** included (1st & 2nd editions)
- **Dominion Prosperity expansion** support with Platinum and Colony cards
- **Manual or random kingdom selection** for varied game experiences
- **Dynamic kingdom pile scaling** based on number of players

### Multiplayer
- **Online multiplayer support** for playing with friends remotely
- **Scalable game rules** that automatically adjust for multiple players
- Real-time game state synchronization

## Getting Started

### Installation
```bash
git clone https://github.com/Spande102/dominion_project.git
cd dominion_project
git checkout online-multiplayer
```

### Requirements
- Python 3.7+

### Running the Game
```bash
python dominion.py
```

## Game Setup

When starting a game, you can:
1. **Select kingdoms manually** - Choose specific card sets for your game
2. **Generate random kingdoms** - Let the game choose for you
3. **Set player count** - The game will automatically scale piles appropriately

## Card Sets Available

- **Base Dominion (1st Edition)** - Original cards
- **Base Dominion (2nd Edition)** - Revised rules and card balancing
- **Dominion Prosperity** - Platinum and Colony cards

## Development

This branch focuses on multiplayer functionality. Key areas include:
- Online player connection and session management
- Real-time game state synchronization
- Turn management across multiple clients

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

See the repository for license details.
