import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)

# Display settings
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Alen')

# Game settings
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Define wall boundaries
wall_thickness = 10
wall_color = yellow

# Example walls (you can adjust these as needed)
wall1 = pygame.Rect(0, 0, dis_width, wall_thickness)  # Top wall
wall2 = pygame.Rect(0, 0, wall_thickness, dis_height)  # Left wall
wall3 = pygame.Rect(0, dis_height - wall_thickness, dis_width, wall_thickness)  # Bottom wall
wall4 = pygame.Rect(dis_width - wall_thickness, 0, wall_thickness, dis_height)  # Right wall

walls = [wall1, wall2, wall3, wall4]

# Load images
grass_texture = pygame.image.load('grass_texture.jpg')
game_over_bg = pygame.image.load("jungle.jpg")

# Scale game over background image
game_over_bg = pygame.transform.scale(game_over_bg, (dis_width, dis_height))

# Load and play background music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

munch_sound = pygame.mixer.Sound('munch_sound.mp3')
crash_sound = pygame.mixer.Sound('crash_sound.mp3')

# Define function to spawn apple away from walls
def spawn_apple():
    while True:
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        if not any(wall.collidepoint(foodx, foody) for wall in walls):
            return foodx, foody

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg1, msg2, color):
    mesg1 = font_style.render(msg1, True, color)
    mesg2 = font_style.render(msg2, True, color)
    dis.blit(mesg1, [dis_width / 2 - mesg1.get_width() / 2, dis_height / 2 - mesg1.get_height()])
    dis.blit(mesg2, [dis_width / 2 - mesg2.get_width() / 2, dis_height / 2 + mesg2.get_height()])

def is_collision(x, y):
    for wall in walls:
        if wall.colliderect(pygame.Rect(x, y, snake_block, snake_block)):
            return True
    return False

def gameLoop():
    game_over = False
    game_close = False

    # Set initial snake position away from walls
    x1 = dis_width / 2
    y1 = dis_height / 2

    while is_collision(x1, y1):
        x1 = random.randrange(0, dis_width - snake_block, snake_block)
        y1 = random.randrange(0, dis_height - snake_block, snake_block)

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = spawn_apple()

    while not game_over:

        while game_close == True:
            dis.blit(game_over_bg, (0, 0))
            message("Game Over!", "Press Q to quit or C to play again", white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            crash_sound.play()
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(green)  # Green background with grass texture

        # Draw grass texture
        for x in range(0, dis_width, grass_texture.get_width()):
            for y in range(0, dis_height, grass_texture.get_height()):
                dis.blit(grass_texture, (x, y))

        # Draw walls
        for wall in walls:
            pygame.draw.rect(dis, wall_color, wall)

        # Draw apple as a red rectangle
        pygame.draw.rect(dis, red, [foodx, foody, 15, 15])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                crash_sound.play()
                game_close = True

        our_snake(snake_block, snake_List)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            munch_sound.play()
            foodx, foody = spawn_apple()
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
