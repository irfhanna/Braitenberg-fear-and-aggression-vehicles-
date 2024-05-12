import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braitenberg Vehicles: Fear and Aggression")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create a light source (as an area)
light_source = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 20, 20)

class Vehicle:
    def __init__(self, color, label):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.color = color
        self.label = label
        self.angle = random.uniform(0, 2 * math.pi)
        self.vl = 2
        self.vr = 2
        self.sensor_length = 20
        self.trajectory = [(self.x, self.y)]

    def update(self):
        # Sensor positions (right and left of the vehicle's front)
        sensor1_x = self.x + self.sensor_length * math.cos(self.angle + math.pi / 4)  # Right sensor
        sensor1_y = self.y - self.sensor_length * math.sin(self.angle + math.pi / 4)
        sensor2_x = self.x + self.sensor_length * math.cos(self.angle - math.pi / 4)  # Left sensor
        sensor2_y = self.y - self.sensor_length * math.sin(self.angle - math.pi / 4)

        # Calculate distances to light source
        distance_to_light1 = math.sqrt((light_source.centerx - sensor1_x)**2 + (light_source.centery - sensor1_y)**2)  # Right sensor
        distance_to_light2 = math.sqrt((light_source.centerx - sensor2_x)**2 + (light_source.centery - sensor2_y)**2)  # Left sensor

        # Adjust vl and vr based on the behavior
        if self.color == RED:  # Fear behavior
            self.vl = max(0.5, 0.5+ 0.01 * distance_to_light2)  # Left sensor affects left velocity
            self.vr = max(0.5, 0.5 + 0.01 * distance_to_light1)  # Right sensor affects right velocity
           
        elif self.color == GREEN:  # Aggression behavior
            self.vl = max(0.5, 0.5 + 1 / (0.01*distance_to_light1))  # Right sensor affects left velocity
            self.vr = max(0.5, 0.5 + 1 / (0.01*distance_to_light2))  # Left sensor affects right velocity

        # Compute the average speed and change in angle
        speed = (self.vl + self.vr) / 2
        if self.color == RED:  # Fear behavior
            delta_angle = (self.vr - self.vl) / 30
        elif self.color == GREEN:
            delta_angle = (self.vl - self.vr) * 0.5

        # Update angle and position
        self.angle += delta_angle
        self.x += speed * math.cos(self.angle)
        self.y -= speed * math.sin(self.angle)

        # Handle toroidal wrapping
        self.x %= WIDTH
        self.y %= HEIGHT
        
        # Update trajectory
        self.trajectory.append((self.x, self.y))

    def draw(self):
        # Draw the vehicle body (circle)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
        
        # Draw sensors (black lines)
        sensor1_x = self.x + self.sensor_length * math.cos(self.angle + math.pi / 4)  # Right sensor
        sensor1_y = self.y - self.sensor_length * math.sin(self.angle + math.pi / 4)
        sensor2_x = self.x + self.sensor_length * math.cos(self.angle - math.pi / 4)  # Left sensor
        sensor2_y = self.y - self.sensor_length * math.sin(self.angle - math.pi / 4)
        pygame.draw.line(screen, BLACK, (self.x, self.y), (sensor1_x, sensor1_y), 2)  # Right sensor
        pygame.draw.line(screen, BLACK, (self.x, self.y), (sensor2_x, sensor2_y), 2)  # Left sensor
        
        # Draw label
        font = pygame.font.SysFont(None, 24)
        label_text = font.render(self.label, True, BLACK)
        screen.blit(label_text, (self.x - 10, self.y - 30))
        
        # Draw trajectory
        #for i in range(1, len(self.trajectory)):
             #pygame.draw.line(screen, self.color, self.trajectory[i - 1], self.trajectory[i], 2)

def main():
    # Create two vehicles
    vehicle1 = Vehicle(RED, "2a")  # Fear vehicle
    vehicle2 = Vehicle(GREEN, "2b")  # Aggression vehicle

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        vehicle1.update()
        vehicle2.update()

        # Clear the screen
        screen.fill(WHITE)

        # Draw light source
        pygame.draw.rect(screen, YELLOW, light_source)

        # Draw vehicles
        vehicle1.draw()
        vehicle2.draw()

        # Update the display
        pygame.display.flip()

        # Limit frames per second
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
