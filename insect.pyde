# Add external libraries used for audio manipulation and playback
add_library('minim')
add_library('sound')
# Import libraries and tools needed for file handling and random number generation
import os
from random import randint

# Get the current working directory for file handling purposes
path = os.getcwd()
print(path)

# Initialize an audio player using the Minim library
player = Minim(this)

# Define a list of colors for the background, represented in RGBA format
bg_colors = [color(255), color(128,128,128), color(255, 0, 0), color(0, 255, 0)]  # white, grey, red, green
last_color_index = 0  # Keeps track of the last color index used for background


# Setup function to initialize the game environment
def setup():
    global game
    size(600, 600)  # Set the window size to 600x600 pixels
    game = GameLogic()
    game.setup()  # Call the setup method of the game logic class to initialize game objects
    

# Main drawing loop of environment
def draw():
    global mouseX, mouseY, mousePressed, last_color_index
    background(bg_colors[last_color_index])  # Set the background color from the list based on the current index
    game.draw()  # Call the draw method of the game logic to handle game rendering
    if mousePressed:
        game.check_hits(mouseX, mouseY)  # Check for mouse interactions
        #kill_sound.play()
    frameRate = 60  # Set the frame rate to 60 frames per second
    time = frameCount % frameRate
    if time % 60 == 0:  # Every second, change the background color
        print(time)
        last_color_index = (last_color_index + 1) % len(bg_colors)  # Cycle through the background color list

# Handle mouse pressed events
def mousePressed():
    if game.game_over:
        game.reset_game()  # If the game is over, allow restarting by resetting the game state

# Utility function to generate a non-zero random integer within a specified range
def get_non_zero_randint(min_val, max_val):
    result = 0
    while result == 0:  # Ensure that the result is not zero
        result = randint(min_val, max_val)
    return result

# Main class to handle game logic and state
class GameLogic:
    def __init__(self):
        # Initialize various game state variables
        self.game_over = False
        self.insects = []
        self.green_kills = 0
        self.high_score = 0
        self.score = 0
        self.innocent_kills = 0
        self.initial_growth_rate = 0.7
        self.growth_rate = self.initial_growth_rate  # Starting growth rate for insect spawning
        self.p = []
        self.center_x = 300  # X-coordinate for the center position
        self.center_y = 300  # Y-coordinate for the center position
        self.hit_decrement_active = False  # Flag to control decrementing the growth rate
        self.bg_sound = player.loadFile(path + "/data/bcsinging.mp3")
        # print("bcmusic.mp3")
        #self.bg_music=player.loadFile("bcmusic.mp3")
        #print("bcmusic.mp3")
        # self.insound=player.loadFile("correcthit.mp3")
        # print("correcthit.mp3")
        self.bg_sound.play()
        self.bg_sound.loop()
        self.bg_sound.rewind()
        

    def setup(self):
        # Load and resize images for different types of insects
        self.insect_leader_image = loadImage("insect_leader_image.png")
        self.insect_leader_image.resize(48, 20)
        self.normal_insect_image = loadImage("normal_insect_image.png")
        self.normal_insect_image.resize(38, 16)
        self.green_insect_image = loadImage("green_insect_image.png")
        self.green_insect_image.resize(34, 14)
        self.insect1 = InsectLeader(self, random(0, width), random(0, height), self.insect_leader_image)
        for _ in range(1):
            self.spawn_normal_insect()  # Spawn initial normal insects
        self.spawn_green_insect()  # Spawn an initial green insect


    def spawn_normal_insect(self):
        # Method to spawn a normal insect if the game is not over
        if not self.game_over:
            self.insects.append(NormalInsect(self, randint(0, width-1), randint(0, height-1), self.normal_insect_image))

    def spawn_green_insect(self):
        # Method to spawn a green insect if the game is not over
        if not self.game_over:
            self.insects.append(GreenInsect(self, randint(0, width-1), randint(0, height-1), self.green_insect_image))

    def draw(self):
        # Main drawing logic for the game
        if self.game_over:
            self.display_game_over()  # Display game over message
            self.display_restart_message()  # Display restart message
            self.gosound=player.loadFile(path + "/data/game_over.mp3")
            self.gosound.play()

        self.check_game_over()  # Check if  conditions are met
        if self.game_over:
            self.display_game_over()
            self.insect1.x, self.insect1.y = self.center_x, self.center_y  # Reset the position of the Insect Leader
        else:
            self.insect1.update()  # Update and display the Insect Leader
            self.insect1.display()

        for insect in self.insects[:]:  # Update and display all insects
            insect.update(self.game_over)
            insect.display()

        if not self.game_over:
            self.handle_game_logic()  # Handle game logic like spawning new insects

        self.display_game_info()  # Display current game information
        if not self.hit_decrement_active:
            self.increase_growth_rate()  # Increase growth rate if it's not being decremented

    def increase_growth_rate(self):
        # Method to incrementally increase the growth rate of insect spawning
        self.growth_rate += 0.005  # Increase by 0.005 each frame

    def display_game_over(self):
        # Display the game over screen
        background(255)  # Set background to white
        textSize(40)  # Set text size for the game over message
        fill(255, 0, 0)  # Set text color to red
        text("GAME OVER", 190, 300)  # Display the "GAME OVER" message at position (80, 200)
        self.display_restart_message()
        textSize(13)  # Set text size for the high score
        fill(255, 0, 0)  # Set text color to red
        text("HIGH SCORE: %d" % self.high_score, 10, height - 15)  # Display the high score at the bottom left

    def handle_game_logic(self):
        # Main game logic for spawning insects
        if not self.game_over:
            if random(1) < 0.04 * self.growth_rate:
                self.spawn_normal_insect()  # Spawn normal insects based on the growth rate
            if random(1) < 0.03:
                self.spawn_green_insect()  # Occasionally spawn a green insect

    def display_game_info(self):
        # Display current game statistics
        textSize(13)  # Set text size for game info
        fill(0)  # Set text color to black
        text("INSECT COUNT = " + str(len(self.insects)), 10, 20)  # Display the current count of insects
        text("SCORE = " + str(self.score), 500, 20)  # Display the current score
        text("INNOCENT KILLS = " + str(self.innocent_kills), 10, 40)  # Display the number of innocent kills
    

    def check_game_over(self):
        # Check conditions to determine if the game should be over
        if self.innocent_kills >= 5 or len(self.insects) >= 500:
            if self.innocent_kills > 5:
                self.innocent_kills = 5  # Cap innocent kills at 5
            self.game_over = True
            if self.high_score < self.score:
                self.high_score = self.score  # Update the high score if the current score is higher
            self.growth_rate = 0  # Stop spawning insects

    def check_hits(self, x, y):
        # Check if insects are hit by the mouse click
        self.insound=player.loadFile(path + "/data/correcthit.mp3") #block game but works
        if self.insect1.is_hit(x, y):
            self.insound.play()
            print("correcthit.mp3")
            self.score += 1  # Increment score for hitting the Insect Leader
            if self.growth_rate > self.initial_growth_rate:
                self.growth_rate -= 0.01  # Decrement the growth rate on hit, but not below the initial rate
                self.hit_decrement_active = True
            if self.growth_rate <= self.initial_growth_rate:
                self.growth_rate = self.initial_growth_rate
                self.hit_decrement_active = False  # Reset the decrement flag if growth rate reaches initial rate

        for insect in self.insects[:]:  # Check each insect for a hit
            if isinstance(insect, GreenInsect) and dist(x, y, insect.x, insect.y) < 25:
                insect.kill()  # Kill the GreenInsect if it's close enough to the click position

    def display_restart_message(self):
        # Display the message to restart the game
        textSize(16)  # Set text size for the restart message
        fill(150)  # Set text color to gray
        text("Click on the board to play again", 180, 330)  # Display the restart message at position (80, 250)

    def reset_game(self):
        # Reset the game to its initial state
        self.insects = []  # Clear all insects
        self.game_over = False
        self.score = 0
        self.innocent_kills = 0
        self.growth_rate = self.initial_growth_rate  # Reset the growth rate
        self.hit_decrement_active = False  # Reset the hit decrement flag
        self.setup()  # Reinitialize the game setup



# InsectLeader class manages the behavior of the main target insect in the game
class InsectLeader:
    def __init__(self, game_logic, startX, startY, insect_leader_image):
        # Initialization with game logic, starting position, and image
        self.game_logic = game_logic
        self.x = startX
        self.y = startY
        self.img = insect_leader_image
        self.base_speed = 2  # Base speed of the insect
        # Initial random speed in x and y directions, ensuring non-zero values
        self.dx = get_non_zero_randint(-self.base_speed, self.base_speed)
        self.dy = get_non_zero_randint(-self.base_speed, self.base_speed)
        self.speed_increment = 0.0009  # Incremental speed increase per frame
        #self.insound=player.loadFile("correcthit.mp3") #should work
        #print("correcthit.mp3")
    

    def update(self):
        # Update method called every frame, handles movement and speed increase
        if not self.game_logic.game_over:
            self.change_direction()  # Potentially change direction
            self.fly()  # Move based on current speed
            self.increase_speed()  # Gradually increase speed over time

    def display(self):
        # Visual representation of the Insect Leader
        if dist(mouseX, mouseY, self.x, self.y) < 25:
            # If the mouse is near the insect, draw a yellow halo
            fill(255, 255, 0, 127)
            ellipse(self.x, self.y, 50, 50)
        # Draw the insect image at its current position
        image(self.img, self.x - self.img.width / 2, self.y - self.img.height / 2)

    def fly(self):
        # Update position based on speed and direction
        self.x += self.dx
        self.y += self.dy
        self.wrap_around()  # Handle wrapping around the screen edges

    def increase_speed(self):
        # Increase the speed of the insect continuously
        angle = atan2(self.dy, self.dx)  # Calculate current movement angle
        speed = sqrt(self.dx**2 + self.dy**2) + self.speed_increment  # Calculate new speed
        self.speed_increment += 0.0001  # Increase the increment itself over time
    
        # Apply the new speed in the direction of current motion
        self.dx = speed * cos(angle)
        self.dy = speed * sin(angle)
    
        # Ensure that the new speed components are not zero
        if self.dx == 0:
            self.dx = 0.1 if self.dx >= 0 else -0.1
        if self.dy == 0:
            self.dy = 0.1 if self.dy >= 0 else -0.1
    def change_direction(self):
        # Randomly change direction with a 10% chance each frame
        if random(1) < 0.1:
            self.dx = get_non_zero_randint(-self.base_speed, self.base_speed)
            self.dy = get_non_zero_randint(-self.base_speed, self.base_speed)

    def wrap_around(self):
        # Handle wrapping around the screen edges to create a seamless play area
        if self.x < 0:
            self.x = 600
        elif self.x > 600:
            self.x = 0
        if self.y < 0:
            self.y = 600
        elif self.y > 600:
            self.y = 0

    def is_hit(self, x, y):
        # Check if the insect is hit by a click within a specific radius
        #self.insound.play() should work
        #print("correcthit.mp3")
        return dist(x, y, self.x, self.y) < 25  # Check distance from the click to the insect
    

# NormalInsect class manages the behavior of normal enemies in the game
class NormalInsect:
    def __init__(self, game_logic, startX, startY, insect_image):
        # Initialize with game logic, starting position, and image
        self.game_logic = game_logic
        self.x = startX
        self.y = startY
        self.img = insect_image
        self.alive = True  # State to track if the insect is alive

    def fall(self):
        # Method to handle the insect falling when the game is over
        if self.game_logic.game_over:
            self.y += 5  # Move down by 5 units

    def move(self):
        # Randomly move the insect within a small range around its current position
        self.x += random(-2, 2)
        self.y += random(-2, 2)
        self.wrap_around()  # Wrap around screen edges

    def wrap_around(self):
        # Handle wrapping around the screen edges
        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height

    def update(self, game_over):
        # Update method called every frame, decides whether to move or fall based on game state
        if game_over:
            self.fall()  # Fall if the game is over
        else:
            self.move()  # Move normally otherwise

    def display(self):
        # Display the insect image at its current position
        image(self.img, self.x, self.y)

# GreenInsect class manages a special type of insect, which is "Innocent" that moves faster and should not be hit
class GreenInsect:
    def __init__(self, game_logic, startX, startY, insect_image):
        # Initialize with game logic, starting position, and image
        self.game_logic = game_logic
        self.x = startX
        self.y = startY
        self.img = insect_image
        self.alive = True
        self.speed_multiplier = 3  # Increased speed for added challenge
        self.insound=player.loadFile(path + "/data/wronghit.mp3")
        print("wronghit.mp3")

    def move(self):
        # Move the insect randomly within a larger range due to increased speed
        if not self.alive:
            return  # Do not move if the insect is not alive
        self.x += randint(-self.speed_multiplier, self.speed_multiplier)
        self.y += randint(-self.speed_multiplier, self.speed_multiplier)
        self.wrap_around()  # Handle screen wrapping

    def wrap_around(self):
        # Handle wrapping around the screen edges
        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height

    def is_mouse_near(self):
        # Check if the mouse is near this insect
        return dist(self.x, self.y, mouseX, mouseY) < 25  # Calculate distance to the mouse

    def display(self):
        # Visual representation of the Green Insect, including a red halo if the mouse is near
        if self.alive and not self.game_logic.game_over:
            if self.is_mouse_near():
                stroke(255, 0, 0)
                fill(255, 0, 0, 127)  # Red color with transparency indicates danger
                ellipse(self.x, self.y, 50, 50)
        image(self.img, self.x - self.img.width / 2, self.y - self.img.height / 2)

    def update(self, game_over):
        # Update method called every frame, decides whether to move or fall based on game state
        if game_over:
            self.fall()  # Fall if the game is over
        else:
            self.move()  # Move normally otherwise

    def fall(self):
        # Handle falling when the game is over
        if self.game_logic.game_over:
            self.y += 5

    def kill(self):
        # Handle the logic when this insect is incorrectly hit
        if self.game_logic.score >= 5:
            self.game_logic.score -= 10  # Penalize by reducing score
        else:
            self.game_logic.score = 0
        self.game_logic.innocent_kills += 1  # Increment innocent kills count
        self.insound.play()
        self.alive = False  # Mark insect as dead
        self.game_logic.insects.remove(self)  # Remove this insect from the game list
