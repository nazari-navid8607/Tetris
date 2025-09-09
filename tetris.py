import json
import tkinter
from random import choice

with open("blocks.json") as f:
    data = json.load(f)

# ======== settings =======
SIZE = 45
ROWS = 20
COLUMNS = 16
SPEED = 400  # ms
# ========================

root = tkinter.Tk()
root.title("🅣🅔🅣🅡🅘🅢")
canvas = tkinter.Canvas(root, height=ROWS*SIZE, width=COLUMNS*SIZE)
canvas.pack()

for i in range(ROWS):
    canvas.create_line(0, i*SIZE, COLUMNS*SIZE, i*SIZE)
for i in range(COLUMNS):
    canvas.create_line(i*SIZE, 0, i*SIZE, ROWS*SIZE)

table = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

# game control
game_over = False
_loop_id = None

class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.rotation = 0
        self.coords = [c[:] for c in data["types"][kind][0]]
        self.color = data["colors"][f"color{kind[-1]}"]
        self.x = COLUMNS // 2 - 2
        self.y = 0
        self.ids = []
        self.draw()

    def draw(self):
        for id in self.ids:
            try:
                canvas.delete(id)
            except tkinter.TclError:
                return
        self.ids.clear()
        for cx, cy in self.coords:
            x1 = (self.x + cx) * SIZE
            y1 = (self.y + cy) * SIZE
            x2 = x1 + SIZE
            y2 = y1 + SIZE
            self.ids.append(canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline="#111"))

    def can_move(self, dx, dy):
        for cx, cy in self.coords:
            nx = self.x + cx + dx
            ny = self.y + cy + dy
            if nx < 0 or nx >= COLUMNS or ny >= ROWS:
                return False
            if ny >= 0 and table[ny][nx] is not None:
                return False
        return True

    def move(self, dx, dy):
        if game_over:
            return False
        if self.can_move(dx, dy):
            self.x += dx
            self.y += dy
            self.draw()
            return True
        return False

    def rotate(self):
        if game_over:
            return
        new_rot = (self.rotation + 1) % 4
        new_coords = data["types"][self.kind][new_rot]
        for cx, cy in new_coords:
            nx = self.x + cx
            ny = self.y + cy
            if nx < 0 or nx >= COLUMNS or ny >= ROWS:
                return
            if ny >= 0 and table[ny][nx] is not None:
                return
        self.rotation = new_rot
        self.coords = [c[:] for c in new_coords]
        self.draw()

    def freeze(self):
        for cx, cy in self.coords:
            nx = self.x + cx
            ny = self.y + cy
            if 0 <= ny < ROWS:
                table[ny][nx] = self.color
        for id in self.ids:
            try:
                canvas.delete(id)
            except tkinter.TclError:
                pass
        self.ids.clear()
        check_lines()


def check_lines():
    global table
    new_table = []
    cleared = 0
    for row in table:
        if all(cell is not None for cell in row):
            cleared += 1
        else:
            new_table.append(row)
    while len(new_table) < ROWS:
        new_table.insert(0, [None for _ in range(COLUMNS)])
    table = new_table
    redraw_table()


def redraw_table():
    try:
        canvas.delete("frozen")
    except tkinter.TclError:
        return
    for y in range(ROWS):
        for x in range(COLUMNS):
            if table[y][x] is not None:
                x1, y1 = x*SIZE, y*SIZE
                x2, y2 = x1+SIZE, y1+SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill=table[y][x], outline="#111", tags="frozen")

current = None

def new_piece():
    global current, game_over, _loop_id
    kind = choice(list(data["types"]))
    current = Piece(kind)
    if not current.can_move(0,0):
        game_over = True
        if _loop_id is not None:
            try:
                root.after_cancel(_loop_id)
            except Exception:
                pass
        try:
            root.unbind("<Key>")
        except Exception:
            pass
        try:
            canvas.destroy()
        except Exception:
            pass
        label = tkinter.Label(root, text="Game Over", font=("", 90))
        label.pack()
        root.after(1500, root.destroy)
        return

def game_loop():
    global current, _loop_id
    if game_over:
        return
    if current is None:
        new_piece()
        if game_over:
            return
    if not current.move(0, 1):
        current.freeze()
        new_piece()
        if game_over:
            return
    _loop_id = root.after(SPEED, game_loop)

def key(event):
    if game_over:
        return
    if current is None:
        return
    if event.keysym == "Left":
        current.move(-1, 0)
    elif event.keysym == "Right":
        current.move(1, 0)
    elif event.keysym == "Down":
        current.move(0, 1)
    elif event.keysym == "Up":
        current.rotate()

root.bind("<Key>", key)

new_piece()
_loop_id = root.after(SPEED, game_loop)
root.mainloop()
