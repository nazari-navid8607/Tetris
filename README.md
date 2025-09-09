# Tetris

## Challenges & Solutions
I set out to build a Tetris game and started by breaking down the components I’d need. One of the trickiest parts was rotation. I initially tried a mathematical approach using this formula:

```python
# rotation, 90 degrees clockwise
x = 2
y = 3
new_x, new_y = y, -x
```
It worked in theory, but in practice, rotating near the edges caused blocks to go through walls and crash the game. Although I could’ve patched it, I decided to switch to a JSON-based system for defining block shapes and rotations. That turned out to be a great decision—not only did it fix several bugs, but I also learned JSON from scratch during this project, which was super fun!  

Using JSON also opens up future possibilities: I could easily add new block types like 5-piece or even 3-piece shapes to make the game more exciting.  

For handling landed blocks and the floor, I used a nested list to represent the game board filled with ```None``` values. When a block touches the floor or another block, it gets saved into the board and freezes in place.  

Another cool part of this project was practicing Object-Oriented Programming (OOP). I’m still new to it, but this was a great hands-on way to learn and apply OOP concepts.  

I’d love to improve this game further by adding features like multiplayer, score tracking, ratings, and new block designs. There’s a lot more I want to explore!  
By the way, I'm getting better at writing Markdown :)

## How to use
clone this repo and open it's directory
```terminal
git clone https://github.com/nazari-navid8607/Tetris.git
cd Tetris
```
and then, run the app:  
```terminal
python tetris.py
```
or in some linux distros or mac
```terminal
python3 tetris.py
```

## ScreenShot
</br>
<img width="604" height="761" alt="Screenshot From 2025-09-10 00-50-40" src="https://github.com/user-attachments/assets/c6a20b7c-949d-4ff3-8918-c0d47e4cad16" />
