# Snake Arena

> retro snake game with pathfinding AI and unnecessary engineering decisions

A modern arcade-style Snake game built using Python and Pygame.

This project started as a small recreation of the classic Snake game and slowly turned into a full AI-vs-player arena with:
- pathfinding
- flood-fill survival logic
- animated UI
- customizable gameplay
- smoother rendering
- executable packaging

---

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet">

# Overview

Snake Arena is built around one simple idea:

What if Snake had:
- modern UI polish
- aggressive AI
- survival logic
- smoother gameplay
- arcade-style presentation

The result is a competitive Snake game where the opponent actively evaluates space and attempts to survive instead of moving randomly.

---

# Features

## Intelligent AI Snake

The AI:
- searches paths using BFS
- evaluates survivable space using flood fill
- avoids dead ends
- reroutes dynamically
- uses wall wrapping strategically

It behaves more like a survival bot than a scripted enemy.

---

## Gameplay Improvements

Compared to traditional Snake clones:
- smoother movement timing
- cleaner collision handling
- responsive controls
- proper pause system
- polished HUD
- dynamic pacing
- animated food pulse
- improved rendering

---

## Visual Design

The game uses:
- dark retro grid styling
- neon-inspired HUD
- rounded UI panels
- animated food rendering
- cleaner snake rendering
- modernized menus

---

# Difficulty Modes

Available modes:
- Easy
- Medium
- Hard
- Expert

Difficulty changes:
- movement speed
- AI aggression
- reaction pacing

Expert mode becomes significantly more competitive.

---

# Match System

Timed arena matches allow:
- short sessions
- survival runs
- high-score attempts
- long AI battles

---

# Algorithms Used

## BFS Pathfinding

Used for:
- shortest route search
- AI navigation

---

## Flood Fill

Used for:
- survivability checks
- trap detection
- movement scoring

---

## Dynamic Decision Scoring

The AI evaluates:
- reachable space
- food distance
- survival probability

instead of blindly chasing food.

---

# Tech Stack

```txt id="5a8yec"
Python
Pygame
BFS Pathfinding
Flood Fill Logic
PyInstaller
````
# Project Structure

```txt
SnakeArena/
│
├── snake_01.py
├── README.md
├── assets/
├── dist/
└── build/
```

---

# Running the Game

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/snake-arena.git
```

---

## 2. Enter Project Folder

```bash
cd snake-arena
```

---

## 3. Install Dependencies

```bash
pip install pygame
```

---

## 4. Run Game

```bash
python snake_01.py
```

---

# Building the EXE

## Install PyInstaller

```bash
pip install pyinstaller
```

---

## Build Executable

```bash
pyinstaller --onefile --windowed snake_01.py
```

---

# EXE Output

Generated executable will appear inside:

```txt
dist/
```

Example:

```txt
dist/snake_01.exe
```

---

# Optional Custom Icon

```bash
pyinstaller --onefile --windowed --icon=icon.ico snake.py
```

---

# Windows Defender Warning

Windows may display a security warning because the executable is unsigned.

This is common for independent desktop applications.

Click:

```txt
More Info → Run Anyway
```

---

# Recent Updates

Recently added:
- improved food spawning
- centered food indicator
- safer wall handling
- cleaner color selection UI
- smoother food scaling
- more natural code structure
- smarter AI behavior

---

# Future Plans

Planned additions:
- particle effects
- sound system
- powerups
- screen shake
- online leaderboard
- replay mode
- local PvP
- procedural arenas
- adaptive AI personalities

---

# Contributing

Feel free to:
- fork the project
- optimize the AI
- redesign systems
- improve visuals
- add mechanics

Pull requests are welcome.

---

# License

MIT License

---

# Upcoming

New EXE build will be shared soon.

---

# Screenshots

Screenshots and gameplay previews will be added soon.

---

# Final Note

The AI wraps through walls.

You do not.
