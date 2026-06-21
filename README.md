# ♟️ Custom Chess Engine Core with AI Opposition

A modular, lightweight Chess Engine built from scratch in Python using **Pygame**. This project features a fully operational chess rules validation engine, real-time board evaluations based on positional tables, and an AI opponent powered by **Minimax algorithm alongside Alpha-Beta pruning**.

---

## 🚀 Features

* **Complete Chess Logic Core:** Handles complex rules including castling, en passant, pawn promotion, check/checkmate verification, and stalemates
* **Minimax AI Opponent:** A thinking adversary that evaluates positions up to 3 half-moves (plies) ahead to select optimal strategic lines
* **Alpha-Beta Pruning:** Optimizes the move-tree search by discarding paths mathematically proven to be worse than previously evaluated options
* **Positional Evaluation Tables (PST):** Pieces alter their internal worth dynamically depending on where they stand on the board (knights favor the center, pawns gain value as they approach promotion etc.).
* **Dynamic Value Overlay Mode:** A professional debugging tool that replaces graphical assets with raw internal piece values
* **a (somewhat) helpful control panel lol**
---

## 📁 Repository Structure

```text
├── assets/                  # Graphical icons for white and black chess pieces
├── ai.py                    # The AI logic (Minimax search, Alpha-Beta optimization)
├── main.py                  # Pygame UI rendering, move handling, and state machine
└── README.md                # Project documentation
```
## 🏁 Getting Started
(Download python 3.8 or higher)
```py
git clone [https://github.com/zarhouny/chess-engine.git](https://github.com/zarhouny/chess-engine.git)
```
Then:
```js
cd chess-engine
```
Install the pygame Library:
```css
pip install pygame
```
Finally:
```py
python main.py
```
And you're good to go.

