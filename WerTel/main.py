import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
FPS = 60

# Цвета
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (139, 69, 19)
STONE_GRAY = (128, 128, 128)
PLAYER_COLOR = (255, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WerTel")
clock = pygame.time.Clock()

# Класс игрока
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE - 10, BLOCK_SIZE - 10)
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.on_ground = False

    def move(self, keys, world):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        # Гравитация
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        # Движение по X
        self.rect.x += dx
        self.check_collision(world, 'x')

        # Движение по Y
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collision(world, 'y')

        # Границы экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def check_collision(self, world, axis):
        for block in world.blocks:
            if self.rect.colliderect(block['rect']):
                if axis == 'x':
                    if self.rect.centerx < block['rect'].centerx:
                        self.rect.right = block['rect'].left
                    else:
                        self.rect.left = block['rect'].right
                elif axis == 'y':
                    if self.vel_y > 0:
                        self.rect.bottom = block['rect'].top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.top = block['rect'].bottom
                        self.vel_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)

# Класс мира
class World:
    def __init__(self):
        self.blocks = []
        self.generate()

    def generate(self):
        # Простая генерация ландшафта
        ground_level = SCREEN_HEIGHT // 2
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            height_variation = random.randint(-1, 1) * BLOCK_SIZE
            current_ground = ground_level + height_variation
            
            # Трава
            self.blocks.append({
                'rect': pygame.Rect(x, current_ground, BLOCK_SIZE, BLOCK_SIZE),
                'type': 'grass'
            })
            
            # Земля под травой
            for y in range(current_ground + BLOCK_SIZE, SCREEN_HEIGHT, BLOCK_SIZE):
                block_type = 'stone' if y > current_ground + BLOCK_SIZE * 3 else 'dirt'
                self.blocks.append({
                    'rect': pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE),
                    'type': block_type
                })

    def draw(self, surface):
        for block in self.blocks:
            if block['type'] == 'grass':
                color = GRASS_GREEN
            elif block['type'] == 'dirt':
                color = DIRT_BROWN
            else:
                color = STONE_GRAY
            pygame.draw.rect(surface, color, block['rect'])
            pygame.draw.rect(surface, (0, 0, 0), block['rect'], 1)  # Обводка

    def handle_click(self, pos, button):
        # Разрушение/установка блоков по клику
        for i, block in enumerate(self.blocks):
            if block['rect'].collidepoint(pos):
                if button == 1:  # Левая кнопка - разрушить
                    self.blocks.pop(i)
                    return
                elif button == 3:  # Правая кнопка - установить блок (упрощено)
                    pass
                break

# Основной цикл игры
def main():
    world = World()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                world.handle_click(pygame.mouse.get_pos(), event.button)
        
        keys = pygame.key.get_pressed()
        player.move(keys, world)
        
        # Отрисовка
        screen.fill(SKY_BLUE)
        world.draw(screen)
        player.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
