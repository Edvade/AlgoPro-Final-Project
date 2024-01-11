# Modules
import random
import pygame
from Classes import Button 

# Initializing Pygame
pygame.init()
    
# Pygame Setup
WIDTH = 1000
HEIGHT = 600
window = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Scream Topgun')
font = pygame.font.Font('pixeltype.ttf', 20)
fps = 60
timer = pygame.time.Clock()

# Jet Attributes
x_level = 100
y_level = 300
Jet = pygame.transform.scale(pygame.image.load('jet.png'), (80, 80))

# Map Attributes
new_map = True
map_rects = []
rect_width = 10
total_rects = WIDTH // rect_width
map_speed = 2
background = pygame.image.load("Map.png").convert()


# Flying Attributes
spacer = 10
flying = False
y_speed = 0
gravity = 0.3

# Scores
score = 0
high_score = 0
active = True


# Generating New Rectangles
def generate_new():
    global y_level
    rects = []
    top_height = random.randint(0, 300)
    y_level = top_height + 150
    for i in range(total_rects):
        top_height = random.randint(top_height - spacer, top_height + spacer)
        if top_height < 0:
            top_height = 0
        elif top_height > 300:
            top_height = 300
        top_rect = pygame.draw.rect(window, 'brown', [i * rect_width, 0, rect_width, top_height])
        bot_rect = pygame.draw.rect(window, 'brown', [i * rect_width, top_height + 300, rect_width, HEIGHT])
        rects.append(top_rect)
        rects.append(bot_rect)
    return rects

# Drawing the Rectangles
def draw_map(rects):
    for i in range(len(rects)):
        pygame.draw.rect(window, 'brown', rects[i])
    pygame.draw.rect(window, 'black', [0, 0, WIDTH, HEIGHT], 12)

# Drawing the Player
def draw_player():

    player = pygame.draw.circle(window, 'black', (x_level, y_level), 10)
    window.blit(Jet, (x_level - 40, y_level - 30))
    return player

# Adjusting the y_coordinate when flying, gravity included
def move_player(y_pos, speed, fly):
    if fly:
        speed += gravity
    else:
        speed -= gravity
    y_pos -= speed
    return y_pos, speed

# Moving the map to the left as the Jet moves
def move_rects(rects):
    global score
    for i in range(len(rects)):
        rects[i] = (rects[i][0] - map_speed, rects[i][1], rect_width, rects[i][3])
        if rects[i][0] + rect_width < 0:
            rects.pop(1)
            rects.pop(0)
            top_height = random.randint(rects[-2][3] - spacer, rects[-2][3] + spacer)
            if top_height < 0:
                top_height = 0
            elif top_height > 300:
                top_height = 300
            rects.append((rects[-2][0] + rect_width, 0, rect_width, top_height))
            rects.append((rects[-2][0] + rect_width, top_height + 300, rect_width, HEIGHT))
            score += 1
    return rects

# Collision
def check_collision(rects, circle, act):
    for i in range(len(rects)):
        if circle.colliderect(rects[i]):
            act = False
    return act

# Start Screen
start_game_btn = pygame.image.load('start_btn.png').convert_alpha()
start_game_btn_x = WIDTH // 2 - start_game_btn.get_width() // 2
start_game_btn_y = HEIGHT // 2 - start_game_btn.get_height() // 2
start_game_button = Button(start_game_btn_x, start_game_btn_y, start_game_btn, 1)

welcome_font = pygame.font.Font('pixeltype.ttf', 40)
welcome_text = 'WELCOME TO SCREAM TOPGUN!'
welcome_text_width, welcome_text_height = welcome_font.size(welcome_text)
welcome_text_x = WIDTH // 2 - welcome_text_width // 2
welcome_text_y = 200

# Start Screen Loop
start_screen = True
while start_screen:
    window.fill(('brown'))
    
    # Draw UI elements for the start screen
    window.blit(welcome_font.render(welcome_text, True, 'white'), (welcome_text_x, welcome_text_y))
    start_game_button.draw(window)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_game_button.draw(window):
                start_screen = False

# Main Loop
run = True
while run:
    window.fill('black')
    timer.tick(fps)
    if new_map:
        map_rects = generate_new()
        new_map = False
    draw_map(map_rects)
    player_circle = draw_player()
    if active:
        y_level, y_speed = move_player(y_level, y_speed, flying)
        map_rects = move_rects(map_rects)
    active = check_collision(map_rects, player_circle, active)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flying = True
            if event.key == pygame.K_RETURN:
                if not active:
                    new_map = True
                    active = True
                    y_speed = 0
                    map_speed = 2
                    if score > high_score:
                        high_score = score
                    score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flying = False
    map_speed = 2 + score//50
    spacer = 10 + score//100

    window.blit(font.render(f'Score: {score}', True, 'White'), (20, 15))
    window.blit(font.render(f'High Score: {high_score}', True, 'White'), (875, 15))
    if not active:
        window.blit(font.render('Press Enter to Restart', True, 'White'), (400, 565))
    pygame.display.flip()
    pygame.display.update()
pygame.quit()

