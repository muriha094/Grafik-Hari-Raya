import pygame
import random
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Selamat Hari Raya Idul Adha")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("arial", 40, bold=True)
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(100)]
colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 255), (255, 165, 0), (255, 255, 255)]
alpha_title = 0
lanterns = [(150, 100), (WIDTH // 2, 120), (650, 100)]

# Partikel kembang api
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 60
        self.color = color
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.life -= 1
        self.size = max(1, self.size - 0.05)

    def draw(self, surface):
        if self.life > 0:
            alpha = max(0, int(255 * (self.life / 60)))
            surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color + (alpha,), (self.size, self.size), int(self.size))
            surface.blit(surf, (self.x, self.y))

# Gambar tanah berumput
def draw_ground():
    grass_height = 80
    ground_y = HEIGHT - grass_height
    pygame.draw.rect(screen, (34, 139, 34), (0, ground_y, WIDTH, grass_height))  # hijau rumput


# Masjid realistis
def draw_mosque(frame):
    base_y = HEIGHT - 80

    # Dinding utama
    pygame.draw.rect(screen, (210, 210, 230), (150, base_y - 100, 500, 100))

    # Pintu utama
    pygame.draw.rect(screen, (80, 80, 120), (375, base_y - 60, 50, 60))

    # Kubah utama
    pygame.draw.circle(screen, (100, 100, 160), (400, base_y - 100), 70)

    # Kubah kecil kiri-kanan
    pygame.draw.circle(screen, (100, 100, 160), (220, base_y - 60), 30)
    pygame.draw.circle(screen, (100, 100, 160), (580, base_y - 60), 30)

    # Menara kiri-kanan
    for mx in (120, 660):
        pygame.draw.rect(screen, (160, 160, 200), (mx, base_y - 160, 20, 160))
        pygame.draw.circle(screen, (100, 100, 160), (mx + 10, base_y - 160), 15)
        for i in range(3):
            pygame.draw.rect(screen, (255, 255, 255), (mx + 5, base_y - 140 + i * 30, 10, 10))

# Bulan sabit realistis
def draw_realistic_crescent(surface, x, y, radius, frame):
    moon_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(moon_surface, (255, 255, 200), (radius, radius), radius)
    offset = int(4 + math.sin(frame * 0.04) * 4)
    pygame.draw.circle(moon_surface, (0, 0, 0, 0), (radius + offset, radius), radius - 6)
    surface.blit(moon_surface, (x, y))

# Lentera islami
def draw_islamic_lantern(surface, x, y, swing_offset):
    pygame.draw.line(surface, (255, 255, 255), (x, y - 20), (x, y), 2)
    body_rect = pygame.Rect(x - 10 + swing_offset, y, 20, 40)
    pygame.draw.rect(surface, (255, 215, 0), body_rect, border_radius=5)
    pygame.draw.circle(surface, (255, 255, 150), (x + swing_offset, y + 10), 3)
    pygame.draw.circle(surface, (255, 255, 150), (x + swing_offset, y + 20), 3)
    pygame.draw.circle(surface, (255, 255, 150), (x + swing_offset, y + 30), 3)
    pygame.draw.polygon(surface, (200, 170, 0), [(x - 12 + swing_offset, y), (x + 12 + swing_offset, y), (x + swing_offset, y - 10)])
    pygame.draw.rect(surface, (200, 170, 0), (x - 12 + swing_offset, y + 40, 24, 4))

# Kembang api
fireworks = []
def spawn_firework():
    x = random.randint(150, WIDTH - 150)
    y = random.randint(100, HEIGHT // 2)
    color = random.choice(colors)
    for _ in range(60):
        fireworks.append(Particle(x, y, color))

# Variabel animasi
spawn_timer = 0
frame_count = 0

# Main loop
running = True
while running:
    # Latar belakang
    for y_pos in range(HEIGHT):
        color = (0, 0, min(70 + y_pos // 10, 255))
        pygame.draw.line(screen, color, (0, y_pos), (WIDTH, y_pos))

    # Bintang
    for x_star, y_star, r_star in stars:
        brightness = random.randint(180, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x_star, y_star), r_star)

    # Teks ucapan
    if alpha_title < 255:
        alpha_title += 3
    text_surface = font_title.render("Selamat Hari Raya Idul Adha", True, (255, 255, 255))
    text_surface.set_alpha(alpha_title)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 40))

    # Bulan sabit
    draw_realistic_crescent(screen, WIDTH - 130, 50, 40, frame_count)

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kembang api
    for p in fireworks[:]:
        p.update()
        p.draw(screen)
        if p.life <= 0:
            fireworks.remove(p)
    if spawn_timer > 50:
        spawn_firework()
        spawn_timer = 0

    # Gambar tanah berumput
    draw_ground()  # tanah berumput


    # Masjid
    draw_mosque(frame_count)

    # Lentera
    for lx, ly in lanterns:
        offset = int(math.sin(frame_count * 0.05 + lx * 0.01) * 5)
        draw_islamic_lantern(screen, lx, ly, offset)

    pygame.display.flip()
    clock.tick(60)
    spawn_timer += 1
    frame_count += 1

pygame.quit()
sys.exit()
