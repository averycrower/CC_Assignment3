import time, os, random

# Settings
WIDTH = os.get_terminal_size()[0] - 1
DELAY = 0.2
HEART_INTERIOR = '*'  # Changed heart fill to '*'
MIN_HEART_SIZE = 2
MAX_HEART_SIZE = 4
HEART_PROBABILITY = 0.001
GHOST_PROBABILITY = 0.0005  # Probability of a ghost appearing

# Clear the screen at the start
os.system('cls || clear')

# Ghost ASCII Art
GHOST = [
    "  .-.  ",
    " (o o) ",
    " | O | ",
    " '~~~' "
]

def get_ghost():
    """Returns a dictionary representing the ghost's pixels."""
    return {(x, y): GHOST[y][x] for y in range(len(GHOST)) for x in range(len(GHOST[0])) if GHOST[y][x] != ' '}

# Heart ASCII Generation
def get_heart(size):
    img = {}  # keys are (x, y), values are 'X'

    for x in range(size, size * 2):
        img[(x, 0)] = '_'  # left top of heart
        img[(size * 3 + x, 0)] = '_'  # right top of heart

    for i in range(size):
        img[(size - 1 - i, i + 1)] = '/'  # left side of left side top
        img[(size - 1 - i + (size * 3), i + 1)] = '/'  #left side of right side top
        img[(size * 2 + i, i + 1)] = '\\'  # right side of left side top
        img[(size * 2 + i + (size * 3), i + 1)] = '\\'  # right side of right side top

    for i in range(size * 3):
        img[(i, i + size + 1)] = '\\'  # left side bottom slant of heart
        img[(size * 6 - i - 1, i + size + 1)] = '/'  # right side bottom slant of heart

    # Interior of heart:
    for i in range(size):
        for j in range(size):
            img[(size + i, j + 1)] = HEART_INTERIOR  # left side top
            img[(size * 4 + i, j + 1)] = HEART_INTERIOR  # right side top
   
        for j in range(i):
            img[(i, size - j)] = HEART_INTERIOR
            img[(size * 2 + (size - i - 1), size - j)] = HEART_INTERIOR 
            img[(size * 3 + i, size - j)] = HEART_INTERIOR
            img[(size * 5 + (size - i - 1), size - j)] = HEART_INTERIOR 

    for j in range(size * 3):
        for i in range(size * 3 - 1 - j):
            img[((size * 3) - i - 1, j + size + 1)] = HEART_INTERIOR
            img[((size * 3) + i, j + size + 1)] = HEART_INTERIOR

    return img

# Normalize Image Coordinates
def normalize_img(img):
    normalized = {}
    if len(img) == 0:
        return {}

    x, y = next(iter(img.keys()))
    minx = maxx = x
    miny = maxy = y

    for x, y in img.keys():
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y

    for x, y in img.keys():
        normalized[(x - minx, y - miny)] = img[(x, y)]

    return normalized, maxx + 1, maxy + 1

# Print ASCII Image
def print_img(img, maxx, maxy):
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x, y) in img:
                print(img[(x, y)], end='')
            else:
                print(' ', end='')
        print()

# Skull Template
SKULL_TEMPLATE = [
    r'|  ______  | (_)  (_) ', 
    r'| /      \ |          ', 
    r' / _    _ \ \   ^^   /', 
    r'| (_)  (_) | VVVVVVVV ', 
    r'|          |  \____/  ', 
    r' \   ^^   /   ______  ', 
    '  VVVVVVVV   /      \\ ', 
    '   \\____/   / _    _ \\'] 

SKULL_TEMPLATE_HEIGHT = len(SKULL_TEMPLATE)
SKULL_TEMPLATE_WIDTH = len(SKULL_TEMPLATE[0])

# Repeat Skulls Based on Terminal Width
SKULL_X_REPEAT = WIDTH // SKULL_TEMPLATE_WIDTH
next_rows = []
step = 0

# Main Animation Loop
try:    
    while True:
        # Add skull rows
        while len(next_rows) < (MAX_HEART_SIZE * 4 + 1):
            next_rows.append(list(SKULL_TEMPLATE[step % SKULL_TEMPLATE_HEIGHT] * SKULL_X_REPEAT))
            next_rows[-1].extend(' ' * (WIDTH - len(next_rows[-1])))
            step += 1

        # Add Random Hearts
        for x in range(WIDTH - (MAX_HEART_SIZE * 7)):
            if random.random() < HEART_PROBABILITY:
                heart_size = random.randint(MIN_HEART_SIZE, MAX_HEART_SIZE)
                img, maxx, maxy = normalize_img(get_heart(heart_size))
                for ix in range(maxx + 1):
                    for iy in range(maxy + 1):
                        if (ix, iy) in img:
                            next_rows[iy][ix + x] = img[(ix, iy)]

        # Add Random Ghosts
        for x in range(WIDTH - 10):  # Avoid placing ghosts too close to the edge
            if random.random() < GHOST_PROBABILITY:
                ghost_img = get_ghost()
                maxx = len(GHOST[0]) - 1
                maxy = len(GHOST) - 1
                for ix in range(maxx + 1):
                    for iy in range(maxy + 1):
                        if (ix, iy) in ghost_img:
                            next_rows[iy][ix + x] = ghost_img[(ix, iy)]

        # Print Scroll Effect
        row = next_rows[0]
        del next_rows[0]
        print(''.join(row))
        if step % 9 == 0:  # Print 9 rows at a time before pause
            time.sleep(DELAY)

except KeyboardInterrupt:
    print('Skulls, Hearts, and Ghosts by Al Sweigart & Modified by You')
