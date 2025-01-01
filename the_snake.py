import pygame
import random

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position):
        self.position = position

    def draw(self):
        """Метод для отрисовки объекта."""
        raise NotImplementedError("Дочерние классы должны реализовать этот метод.")


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        super().__init__((GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.grow = False
        self.body_color = SNAKE_COLOR

    def update(self):
        """Обновление позиции змейки на основе текущего направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head_x = self.positions[0][0] + self.direction[0]
        new_head_y = self.positions[0][1] + self.direction[1]
        new_head = (new_head_x, new_head_y)

        # Проверка на выход за границы
        if (new_head_x < 0 or new_head_x >= GRID_WIDTH or
                new_head_y < 0 or new_head_y >= GRID_HEIGHT):
            print("Game Over! You hit the wall.")
            pygame.quit()
            raise SystemExit

        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
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

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до начального состояния."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.grow = False

    def update_direction(self, new_direction):
        """Обновление направления змейки."""
        if new_direction in (UP, DOWN, LEFT, RIGHT):
            self.next_direction = new_direction


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, snake):
        super().__init__((0, 0))  # Инициализация позиции
        self.snake = snake
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Перемещение яблока на позицию, не пересекающуюся со змеёй."""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in self.snake.positions:
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple(snake)

    while True:
        clock.tick(10)  # Установите скорость игры
        snake.handle_keys()
        snake.update()

        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow_snake()
            apple.randomize_position()

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
