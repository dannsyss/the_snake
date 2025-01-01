import pygame
from random import randint

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        super().__init__(self.randomize_position(), APPLE_COLOR)

    def randomize_position(self):
        """Случайная позиция яблока."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__(
            (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE),
            SNAKE_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction and (
            self.direction[0] + self.next_direction[0] != 0
            or self.direction[1] + self.next_direction[1] != 0
        ):
            self.direction = self.next_direction

    def move(self):
        """Перемещает змейку."""
        head_x, head_y = self.get_head_position()
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if new_head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        self.__init__()

    def grow(self):
        """Увеличивает длину змейки."""
        self.length += 1

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.position = apple.randomize_position()

        apple.draw()
        snake.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
