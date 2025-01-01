from random import choice
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position):
        self.position = position

    def draw(self):
        """Метод для отрисовки объекта."""
        raise NotImplementedError("Дочерние классы должны реализовать "
                                  "этот метод.")


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализация змейки с начальной позицией и направлением."""
        super().__init__((GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.grow = False

    def update(self):
        """Обновление позиции змейки на основе текущего направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head_x = self.positions[0][0] + self.direction[0]
        new_head_y = self.positions[0][1] + self.direction[1]
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def handle_keys(self):
        """Обработка нажатий клавиш для изменения направления."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def grow_snake(self):
        """Увеличение длины змейки."""
        self.grow = True

    def check_collision_with_tail(self):
        """Проверка столкновения головы змейки с её хвостом."""
        return self.positions[0] in self.positions[1:]


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализация яблока с случайной позицией."""
        super().__init__((choice(range(GRID_WIDTH)),
                          choice(range(GRID_HEIGHT))))

    def spawn(self):
        """Перемещение яблока на новую случайную позицию."""
        self.position = (choice(range(GRID_WIDTH)), choice(range(GRID_HEIGHT)))

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, APPLE_COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Основная функция игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        snake.handle_keys()
        snake.update()

        # Проверка на столкновение с яблоком
        if snake.positions[0] == apple.position:
            snake.grow_snake()
            apple.spawn()

        # Проверка на столкновение с хвостом
        if snake.check_collision_with_tail():
            print("Game Over! You collided with your tail.")
            pygame.quit()
            raise SystemExit

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
