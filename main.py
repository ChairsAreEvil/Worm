import pygame, sys, random
from constants import *


class Worm():
    def __init__(self):
        self.body = [pygame.Vector2(6, 9), pygame.Vector2(5, 9), pygame.Vector2(4, 9)]
        self.direction = pygame.Vector2(1, 0)
        self.grow = False

    def draw(self, screen):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * CELL_SIZE, OFFSET + segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, "pink", segment_rect, 0, 7)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.grow == True:
            self.grow = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [pygame.Vector2(6, 9), pygame.Vector2(5, 9), pygame.Vector2(4, 9)]
        self.direction = pygame.Vector2(1, 0)



class Food():
    def __init__(self, worm_body):
        self.pos = self.generate_random_pos(worm_body)

    def draw(self, screen):
        food_rect = pygame.Rect(OFFSET + self.pos.x * CELL_SIZE, OFFSET + self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, "red", food_rect, 0, 7)

    def generate_random_cell(self):
        x = random.randint(0, NUMBER_OF_CELLS - 1)
        y = random.randint(0, NUMBER_OF_CELLS - 1)
        return pygame.Vector2(x, y)

    def generate_random_pos(self, worm_body):
        position = self.generate_random_cell()
        while position in worm_body:
            position = self.generate_random_cell()
        return position


class Game():
    def __init__(self):
        self.worm = Worm()
        self.food = Food(self.worm.body)
        self.state = "RUNNING"
        self.score = 0

    def draw(self, screen):
        self.worm.draw(screen)
        self.food.draw(screen)

    def update(self):
        if self.state == "RUNNING":
            self.worm.update()
            self.collide_with_food()
            self.collide_with_wall()
            self.collide_with_body()

    def collide_with_food(self):
        if self.worm.body[0] == self.food.pos:
            self.food.pos = self.food.generate_random_pos(self.worm.body)
            self.worm.grow = True
            self.score += 10

    def collide_with_wall(self):
        if self.worm.body[0].x == NUMBER_OF_CELLS or self.worm.body[0].x == -1:
            self.game_over()
        if self.worm.body[0].y == NUMBER_OF_CELLS or self.worm.body[0].y == -1:
            self.game_over()

    def collide_with_body(self):
        headless_body = self.worm.body[1:]
        if self.worm.body[0] in headless_body:
            self.game_over()

    def game_over(self):
        self.worm.reset()
        self.food.pos = self.food.generate_random_pos(self.worm.body)
        self.state = "STOPPED"
        self.score = 0




def main():
    pygame.init()

    title_font = pygame.font.Font(None, 60)
    score_font = pygame.font.Font(None, 40)

    clock = pygame.time.Clock()
    dt = 0.0

    pygame.display.set_caption("Worm")

    screen = pygame.display.set_mode((2*OFFSET + CELL_SIZE * NUMBER_OF_CELLS, 2*OFFSET + CELL_SIZE * NUMBER_OF_CELLS))

    game = Game()


    WORM_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(WORM_UPDATE, 200)


    running = True
    while running:
        for event in pygame.event.get():
            if game.state == "STOPPED":
                if event.type == pygame.KEYDOWN:
                    game.state = "RUNNING"
            if event.type == WORM_UPDATE:
                game.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        screen.fill("black")
        pygame.draw.rect(screen, "white", (OFFSET-5, OFFSET-5, CELL_SIZE*NUMBER_OF_CELLS+10, CELL_SIZE*NUMBER_OF_CELLS+10), 5)
        game.draw(screen)
        title_surface = title_font.render("Worm", True, "pink")
        screen.blit(title_surface, (OFFSET - 5, 20))
        score_surface = score_font.render(f"Score: {game.score}", True, "pink")
        screen.blit(score_surface, (OFFSET - 5, OFFSET + CELL_SIZE * NUMBER_OF_CELLS + 10))

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and game.worm.direction != pygame.Vector2(0, 1):
            game.worm.direction = pygame.Vector2(0, -1)
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and game.worm.direction != pygame.Vector2(0, -1):
            game.worm.direction = pygame.Vector2(0, 1)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and game.worm.direction != pygame.Vector2(1, 0):
            game.worm.direction = pygame.Vector2(-1, 0)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and game.worm.direction != pygame.Vector2(-1, 0):
            game.worm.direction = pygame.Vector2(1, 0)

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


        pygame.display.flip()

        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
