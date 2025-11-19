import pygame
import tkinter as tk
import cv2
import mediapipe as mp
import threading

# Player class to handle the player
class Player:
    def __init__(self, x, y):
        self.img_right = []
        self.img_left = []
        self.index = 0
        self.counter = 0
        self.left_counter = 0  # Separate counter for left animation to control speed

        # Load and transform images once
        self._load_images()

        # Set the initial image (frame)
        self.image = self.img_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.gravity = 0.75
        self.fall_speed = 0
        self.jump_speed = -15
        self.is_jumping = False
        self.is_on_ground = False
        self.facing_right = True

    def _load_images(self):
        """Helper method to load and transform player images."""
        for num in range(1, 5):
            hero_img = pygame.image.load(f"img/guy{num}.png")
            hero_img = pygame.transform.smoothscale(hero_img, (50, 100))
            self.img_right.append(hero_img)
            self.img_left.append(pygame.transform.flip(hero_img, True, False))

    def update(self, platforms, screen_width, screen_height, gesture=None):
        if gesture == "move_left":
            self.rect.x -= self.speed
            self.facing_right = False
            self.left_counter += 1
            if self.left_counter >= 1.2:
                self.index = (self.index + 1) % len(self.img_left)
                self.left_counter = 0
            self.image = self.img_left[self.index]

        if gesture == "move_right":
            self.rect.x += self.speed
            self.facing_right = True
            self.counter += 1
            if self.counter >= 10:
                self.index = (self.index + 1) % len(self.img_right)
                self.counter = 0
            self.image = self.img_right[self.index]

        if gesture == "jump" and not self.is_jumping and self.is_on_ground:
            self.fall_speed = self.jump_speed
            self.is_jumping = True
            self.is_on_ground = False

        self.rect.left = max(0, min(self.rect.left, screen_width - self.rect.width))
        self.fall_speed += self.gravity
        self.rect.y += self.fall_speed

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.fall_speed = 0

        self.is_on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.fall_speed >= 0:
                self.rect.bottom = platform.rect.top
                self.fall_speed = 0
                self.is_jumping = False
                self.is_on_ground = True

        screen.blit(self.image, self.rect)

    def check_collision(self, enemies):
        """Optimized collision check using sprite collision."""
        return pygame.sprite.spritecollideany(self, enemies)

# Platform class for testing collision
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

# World class to handle the world data and drawing blocks
class World:
    def __init__(self, data):
        self.dirt_img = pygame.image.load("img/dirt.png")
        self.dirt_img = pygame.transform.smoothscale(self.dirt_img, (60, 60))  # Resize to fit the new screen
        self.grass_img = pygame.image.load("img/grass.png")
        self.grass_img = pygame.transform.smoothscale(self.grass_img, (60, 60))
        self.enemy_img = pygame.image.load("img/blob.png")
        self.enemy_img = pygame.transform.smoothscale(self.enemy_img, (60, 60))  # Resize enemies accordingly
        self.world_data = data
        self.platforms = self.create_platforms()
        self.exit = self.create_exit()

    def create_platforms(self):
        platforms = []
        self.enemies = []

        for row_index, row in enumerate(self.world_data):
            for col_index, tile in enumerate(row):
                if tile == 1:  # Dirt block
                    platforms.append(Platform(col_index * 60, row_index * 60, 60, 60))
                elif tile == 2:  # Grass block
                    platforms.append(Platform(col_index * 60, row_index * 60, 60, 60))
                elif tile == 3:  # Enemy position (place an enemy here)
                    enemy = Enemy(col_index * 61, row_index * 61)
                    self.enemies.append(enemy)
        return platforms

    def create_exit(self):
        exit_group = pygame.sprite.Group()
        for row_index, row in enumerate(self.world_data):
            for col_index, tile in enumerate(row):
                if tile == 4:  # If world data contains '4', place the exit here
                    exit_obj = Exit(col_index * 60, row_index * 60)
                    exit_group.add(exit_obj)
        return exit_group

    def draw(self, screen):
        for row_index, row in enumerate(self.world_data):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    screen.blit(self.dirt_img, (col_index * 60, row_index * 60))
                elif tile == 2:
                    screen.blit(self.grass_img, (col_index * 60, row_index * 60))

# Enemy class for basic enemy movement
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.image = pygame.transform.smoothscale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        # Move the enemy back and forth
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

# Exit class
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/exit.png')
        self.image = pygame.transform.smoothscale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

# Function to check if player reaches the exit (win condition)
def check_exit_collision(player, exit_group):
    return pygame.sprite.spritecollideany(player, exit_group)

# Function to create a game-over screen using Tkinter
def game_over_screen():
    def close_game_window():
        root.quit()  # Close the Tkinter window

    root = tk.Tk()
    root.title("Game Over")
    root.geometry("400x400")
    root.configure(background="#99d9ea")

    label = tk.Label(root, text="Game Over", fg="#ffffff", font=("Arial", 40), background="#bc4c14")
    label.pack(pady=10, padx=10)

    root.mainloop()

# Function to create a win screen using Tkinter
def win_screen():
    root = tk.Tk()
    root.title("You Win!")
    root.geometry("400x400")
    root.configure(background="#99d9ea")

    label = tk.Label(root, text="You Won!", fg="#ffffff", font=("Arial", 40), background="#bc4c14")
    label.pack(pady=10, padx=10)

    root.mainloop()

# Initialize pygame
pygame.init()

# Screen dimensions set to 1080x720
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Load sky and sun images once
sky_img = pygame.image.load("img/sky.png")
sky_img = pygame.transform.smoothscale(sky_img, (screen_width, screen_height))
sun_img = pygame.image.load("img/sun.png")
sun_img = pygame.transform.smoothscale(sun_img, (50, 50))

# World data
world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

# Game restart function
def restart_game():
    global hero, world, enemies, running
    hero = Player(50, screen_height - 150)
    world = World(world_data)
    enemies = pygame.sprite.Group()
    enemies.add(*world.enemies)
    run_game_loop()

#hand gesture controls
class HandGestureController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to initialize camera.")
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.frame_skip_counter = 0

    def get_gesture(self):
        self.frame_skip_counter += 1
        if self.frame_skip_counter % 3 != 0:
            return None
        
        success, img = self.cap.read()
        if not success:
            print("Failed to capture frame")
            return None

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist_x = hand_landmarks.landmark[0].x
                index_tip_y = hand_landmarks.landmark[8].y
                index_pip_y = hand_landmarks.landmark[6].y
                pinky_root_x = hand_landmarks.landmark[17].x
                thumb_root_x = hand_landmarks.landmark[5].x

                # Detect gestures
                if wrist_x < pinky_root_x:
                    print("Gesture detected: move_left")
                    return "move_left"
                elif wrist_x > thumb_root_x:
                    print("Gesture detected: move_right")
                    return "move_right"
                elif index_tip_y < index_pip_y:
                    print("Gesture detected: jump")
                    return "jump"

        return None

    def release(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

# Main game loop
def run_game_loop():
    global running
    running = True
    Clock = pygame.time.Clock()
    fps = 60

    gesture_controller = HandGestureController()

    while running:
        Clock.tick(fps)

        gesture = gesture_controller.get_gesture()
        print(f"{gesture}")

        if hero.check_collision(enemies):
            game_over_screen()
            running = False

        if check_exit_collision(hero, world.exit):
            win_screen()
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(sky_img, (0, 0))
        screen.blit(sun_img, (200, 50))
        world.draw(screen)
        hero.update(world.platforms, screen_width, screen_height, gesture)
        enemies.update()

        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)

        world.exit.update()
        for exit_obj in world.exit:
            screen.blit(exit_obj.image, exit_obj.rect)

        pygame.display.update()

    pygame.quit()

# Initialize the game
restart_game()
