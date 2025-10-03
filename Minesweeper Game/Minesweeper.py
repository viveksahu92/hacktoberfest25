import random


SIZE = 5   # Grid size (5x5)
MINES = 5  # Number of mines


grid = [["." for _ in range(SIZE)] for _ in range(SIZE)]
mines = random.sample(range(SIZE * SIZE), MINES)


for m in mines:
    r, c = divmod(m, SIZE)
    grid[r][c] = "M"


def count_mines(r, c):
    if grid[r][c] == "M":
        return "M"
    count = 0
    for i in range(r-1, r+2):
        for j in range(c-1, c+2):
            if 0 <= i < SIZE and 0 <= j < SIZE and grid[i][j] == "M":
                count += 1
    return str(count)


revealed = [["." for _ in range(SIZE)] for _ in range(SIZE)]
while True:
    
    for row in revealed:
        print(" ".join(row))
    
    
    try:
        r, c = map(int, input("Enter row and col (0-based): ").split())
    except:
        print("❌ Invalid input, try again.")
        continue
    
    if grid[r][c] == "M":
        print("💥 BOOM! You hit a mine. Game Over.")
        break
    else:
        revealed[r][c] = count_mines(r, c)
    
    
    safe_cells = SIZE*SIZE - MINES
    revealed_count = sum(cell != "." for row in revealed for cell in row)
    if revealed_count == safe_cells:
        print("🏆 You win! All safe cells revealed.")
        break
