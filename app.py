import pygame
import math
import sys

# Pygame Setup
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Skeletal Dragon Cursor")
clock = pygame.time.Clock()

# Segment class jo dragon ki bones ko control karegi
class Segment:
    def __init__(self, x, y, length, size):
        self.x = x
        self.y = y
        self.length = length
        self.size = size
        self.angle = 0

    def update(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.atan2(dy, dx)
        
        # Bones ko aage khinchne ka Inverse Kinematics logic
        self.x = target_x - math.cos(self.angle) * self.length
        self.y = target_y - math.sin(self.angle) * self.length

    def draw_bone(self, surface):
        # Perpendicular angles rib cage (pankhudi) banane ke liye
        perp_angle1 = self.angle + math.pi / 2
        perp_angle2 = self.angle - math.pi / 2

        # Spine Point (Reeth ki haddi)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 2)

        if self.size > 2:
            # Ribs ke dono corners nikalna
            r1_x = self.x + math.cos(perp_angle1) * self.size
            r1_y = self.y + math.sin(perp_angle1) * self.size
            r2_x = self.x + math.cos(perp_angle2) * self.size
            r2_y = self.y + math.sin(perp_angle2) * self.size

            # Agla point jahan haddi judti hai
            tip_x = self.x + math.cos(self.angle) * self.length
            tip_y = self.y + math.sin(self.angle) * self.length

            # Rib lines draw karna
            pygame.draw.line(surface, (230, 230, 230), (int(self.x), int(self.y)), (int(r1_x), int(r1_y)), 2)
            pygame.draw.line(surface, (230, 230, 230), (int(self.x), int(self.y)), (int(r2_x), int(r2_y)), 2)
            
            # Cage look ke liye corners ko aage jodna
            pygame.draw.line(surface, (180, 180, 180), (int(r1_x), int(r1_y)), (int(tip_x), int(tip_y)), i=1)
            pygame.draw.line(surface, (180, 180, 180), (int(r2_x), int(r2_y)), (int(tip_x), int(tip_y)), i=1)
        else:
            # Tail (Ponchh) ki patli single line
            tip_x = self.x + math.cos(self.angle) * self.length
            tip_y = self.y + math.sin(self.angle) * self.length
            pygame.draw.line(surface, (230, 230, 230), (int(self.x), int(self.y)), (int(tip_x), int(tip_y)), 2)

# Pair (Limbs) draw karne wala function
def draw_leg(surface, start_x, start_y, angle, side, phase):
    leg_angle = angle + (side * math.pi / 2.5) + math.sin(phase) * 0.2
    
    # Joint 1
    joint_x = start_x + math.cos(leg_angle) * 25
    joint_y = start_y + math.sin(leg_angle) * 25
    
    # Claw (Panja)
    claw_angle = leg_angle + (side * 0.5)
    claw_x = joint_x + math.cos(claw_angle) * 15
    claw_y = joint_y + math.sin(claw_angle) * 15
    
    pygame.draw.line(surface, (200, 200, 200), (int(start_x), int(start_y)), (int(joint_x), int(joint_y)), 3)
    pygame.draw.line(surface, (200, 200, 200), (int(joint_x), int(joint_y)), (int(claw_x), int(claw_y)), 2)

# Dragon Initial Structure
segments = []
num_segments = 35
segment_length = 15

# Initial mouse positions
mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2

for i in range(num_segments):
    # Center mota hoga aur dono sides patli honi chahiye transitions ke liye
    size = math.sin((i / num_segments) * math.pi) * 22
    if i < 5:
        size = 12 + i * 2  # Neck section
    segments.append(Segment(mouse_x, mouse_y, segment_length, size))

animation_frame = 0

# Trail surface setup taaki video jaisa halka peeche shadow chhoote
trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.set_alpha(70) # Trail effect intensity
trail_surface.fill((17, 17, 17))

# Main Game Loop
while True:
    animation_frame += 1
    
    # Event Check (Window close karne ke liye)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get Current Mouse Position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Background black trail chadhana
    screen.blit(trail_surface, (0, 0))

    # Target points update system
    target_x = mouse_x
    target_y = mouse_y

    # Head (Sar) segment drawing logic
    head_angle = segments[0].angle
    pygame.draw.circle(screen, (255, 255, 255), (int(target_x), int(target_y)), 7)
    
    # Head Jaws / Horns lines
    h1_x = target_x + math.cos(head_angle + 2.5) * 15
    h1_y = target_y + math.sin(head_angle + 2.5) * 15
    h2_x = target_x + math.cos(head_angle - 2.5) * 15
    h2_y = target_y + math.sin(head_angle - 2.5) * 15
    pygame.draw.line(screen, (255, 255, 255), (int(target_x), int(target_y)), (int(h1_x), int(h1_y)), 2)
    pygame.draw.line(screen, (255, 255, 255), (int(target_x), int(target_y)), (int(h2_x), int(h2_y)), 2)

    # Poori body update aur draw loop
    for i in range(len(segments)):
        segments[i].update(target_x, target_y)
        segments[i].draw_bone(screen)
        
        # Sahi segments par legs lagana
        if i == 7: # Front legs
            draw_leg(screen, segments[i].x, segments[i].y, segments[i].angle, 1, animation_frame * 0.1)
            draw_leg(screen, segments[i].x, segments[i].y, segments[i].angle, -1, animation_frame * 0.1)
        if i == 18: # Back legs
            draw_leg(screen, segments[i].x, segments[i].y, segments[i].angle, 1, animation_frame * 0.1 + math.pi)
            draw_leg(screen, segments[i].x, segments[i].y, segments[i].angle, -1, animation_frame * 0.1 + math.pi)

        # Agla segment pichle segment ke piche chalega
        target_x = segments[i].x
        target_y = segments[i].y

    pygame.display.flip()
    clock.tick(60) # 60 FPS Super smooth speed
                         
