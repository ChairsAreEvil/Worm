import pygame, sys, random, os
from constants import *


# --- high score helpers ---
def load_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except ValueError:
        return 0
    
def save_high_score(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except OSError:
        pass

def draw_menu(screen, title_font, score_font, high_score):
    screen.fill("black")
    title_surface = title_font.render("Worm", True, "pink")
    screen.blit(title_surface, (OFFSET - 5, 20))

    start_prompt_surface = score_font.render("Press SPACE to play", True, "pink")
    screen.blit(start_prompt_surface, (OFFSET, 200))

    exit_prompt_surface = score_font.render("Press ESC to exit", True, "pink")
    screen.blit(exit_prompt_surface, (OFFSET, 250))

    high_score_surface = score_font.render(f"High Score: {high_score}", True, "pink")
    screen.blit(high_score_surface, (OFFSET + 545, 40))#(OFFSET, 300))


class Worm():
    def __init__(self):
        self.body = [pygame.Vector2(6, 9)]#, pygame.Vector2(5, 9), pygame.Vector2(4, 9)]
        self.direction = pygame.Vector2(1, 0)
        self.next_direction = self.direction
        self.grow = False
        self.super_grow = False

    def draw(self, screen):
        index = 0
        for segment in self.body:
            if index == 0:
                segment_rect = (OFFSET + segment.x * CELL_SIZE, OFFSET + segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, "pink2", segment_rect, 0, 7)
            elif len(self.body) >=8 and index != 0 and index % (len(self.body)//4) == 0:
                segment_rect = (OFFSET + segment.x * CELL_SIZE, OFFSET + segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, "pink4", segment_rect, 0, 7)
            else:
                segment_rect = (OFFSET + segment.x * CELL_SIZE, OFFSET + segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, "pink", segment_rect, 0, 7)
            index += 1

    def update(self):
        self.direction = self.next_direction
        self.body.insert(0, self.body[0] + self.direction)
        if self.grow == True:
            if self.super_grow == True:
                self.super_grow = False
            else:
                self.grow = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [pygame.Vector2(6, 9)]#, pygame.Vector2(5, 9), pygame.Vector2(4, 9)]
        self.next_direction = pygame.Vector2(1, 0)

    def wander(self):
        up = pygame.Vector2(0, -1)
        down = pygame.Vector2(0, 1)
        left = pygame.Vector2(-1, 0)
        right = pygame.Vector2(1, 0)

        if self.direction == up: # Currently Moving Up
            valid_dirs = self.valid_directions([up, up, up, left, right])
            self.next_direction = random.choice(valid_dirs)

        elif self.direction == down: # Currently Moving Down
            valid_dirs = self.valid_directions([down, down, down, left, right])
            self.next_direction = random.choice(valid_dirs)

        elif self.direction == left: # Currently Moving Left
            valid_dirs = self.valid_directions([left, left, left, up, down])
            self.next_direction = random.choice(valid_dirs)

        elif self.direction == right: # Currently Moving Right
            valid_dirs = self.valid_directions([right, right, right, up, down])
            self.next_direction = random.choice(valid_dirs)

    def is_valid_direction(self, direction):
        next_pos = self.body[0] + direction

        if next_pos.x == NUMBER_OF_CELLS or next_pos.x == -1:
            return False
        if next_pos.y == NUMBER_OF_CELLS or next_pos.y == -1:
            return False

        return True

    def valid_directions(self, directions):
        valid_dirs = [dir for dir in directions if self.is_valid_direction(dir)]
        return valid_dirs



class Food():
    def __init__(self, worm_body):
        self.pos = self.generate_random_pos(worm_body)
        self.is_super = False

    def draw(self, screen):
        #food_rect = pygame.Rect(OFFSET + self.pos.x * CELL_SIZE, OFFSET + self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE) # --- if food is rounded square
        food_rect = pygame.Rect(OFFSET + self.pos.x * CELL_SIZE + 5 , OFFSET + self.pos.y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10) # --- if food is circle
        if self.is_super:
            #pygame.draw.rect(screen, "green", food_rect, 0, 7) # --- makes food rounded square
            pygame.draw.rect(screen, GREEN, food_rect, 0, 15) # --- makes food circle
        else:
            #pygame.draw.rect(screen, "red", food_rect, 0, 7) # --- makes food rounded square
            pygame.draw.rect(screen, RED, food_rect, 0, 15) # --- makes food circle

    def generate_random_cell(self):
        x = random.randint(0, NUMBER_OF_CELLS - 1)
        y = random.randint(0, NUMBER_OF_CELLS - 1)
        if random.randint(0, 100) < 20:
            self.is_super = True
        else:
            self.is_super = False
        return pygame.Vector2(x, y)

    def generate_random_pos(self, worm_body):
        position = self.generate_random_cell()
        while position in worm_body:
            position = self.generate_random_cell()
        return position


class Game():
    def __init__(self, high_score):
        self.worm = Worm()
        self.food = Food(self.worm.body)
        self.state = "RUNNING"
        self.score = 0
        self.high_score = high_score

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
            super_food = self.food.is_super
            self.food.pos = self.food.generate_random_pos(self.worm.body)
            self.worm.grow = True
            if super_food:
                self.worm.super_grow = True
                self.score += 10
            self.score += 10

    def collide_with_wall(self):
        if self.worm.body[0].x == NUMBER_OF_CELLS or self.worm.body[0].x == -1:
            self.game_over()
        if self.worm.body[0].y == NUMBER_OF_CELLS or self.worm.body[0].y == -1:
            self.game_over()

    # --- original body collision ---
    #def collide_with_body(self):
    #    headless_body = self.worm.body[1:]
    #    if self.worm.body[0] in headless_body:
    #        self.game_over()

    # --- new body slicing on collision ---
    def collide_with_body(self):
        headless_body = self.worm.body[1:]
        i = 0
        if self.worm.body[0] in headless_body:
            for segment in headless_body:
                if headless_body[i] == self.worm.body[0]:
                    lost = self.worm.body[i + 1:]
                    self.worm.body = self.worm.body[:i + 1]
                    self.score -= len(lost) * 10
                i += 1

    def game_over(self):
        self.worm.reset()
        self.food.pos = self.food.generate_random_pos(self.worm.body)
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)
        self.state = "STOPPED"
        self.score = 0




def main():
    pygame.init()

    title_font = pygame.font.Font(None, 60)
    score_font = pygame.font.Font(None, 40)

    app_state = "MENU"

    clock = pygame.time.Clock()
    dt = 0.0

    high_score = load_high_score()

    pygame.display.set_caption("Worm")

    screen = pygame.display.set_mode((2*OFFSET + CELL_SIZE * NUMBER_OF_CELLS, 2*OFFSET + CELL_SIZE * NUMBER_OF_CELLS))

    game = Game(high_score)

    menu_worm = Worm()
    menu_worm.body = [pygame.Vector2(6, 9), pygame.Vector2(5, 9), pygame.Vector2(4, 9)]

    WORM_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(WORM_UPDATE, 200)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if app_state == "MENU":
                if event.type == WORM_UPDATE:
                    menu_worm.wander()
                    menu_worm.update()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    app_state = "PLAYING"
                    game = Game(high_score)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif app_state == "PLAYING":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    app_state = "MENU"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game.worm.reset()
                    game.score = 0
                    game.state = "STOPPED"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if game.state == "STOPPED":
                        game.state = "RUNNING"
                    elif game.state == "RUNNING":
                        game.state = "STOPPED"

                if game.state == "STOPPED":
                    if event.type == pygame.KEYDOWN and event.key not in (pygame.K_ESCAPE, pygame.K_p, pygame.K_r):
                        game.state = "RUNNING"

                if event.type == WORM_UPDATE:
                    game.update()

        if app_state == "MENU":
            draw_menu(screen, title_font, score_font, high_score)
            menu_worm.draw(screen)
        else:
            screen.fill("black")
            pygame.draw.rect(screen, "white", (OFFSET-5, OFFSET-5, CELL_SIZE*NUMBER_OF_CELLS+10, CELL_SIZE*NUMBER_OF_CELLS+10), 5)
            game.draw(screen)

            title_surface = title_font.render("Worm", True, "pink")
            screen.blit(title_surface, (OFFSET - 5, 20))

            score_surface = score_font.render(f"Score: {game.score}", True, "pink")
            screen.blit(score_surface, (OFFSET - 5, OFFSET + CELL_SIZE * NUMBER_OF_CELLS + 10))

            high_score_surface = score_font.render(f"High Score: {game.high_score}", True, "pink")
            screen.blit(high_score_surface, (OFFSET + 545, 40))

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and game.worm.direction != pygame.Vector2(0, 1):
            game.worm.next_direction = pygame.Vector2(0, -1)
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and game.worm.direction != pygame.Vector2(0, -1):
            game.worm.next_direction = pygame.Vector2(0, 1)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and game.worm.direction != pygame.Vector2(1, 0):
            game.worm.next_direction = pygame.Vector2(-1, 0)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and game.worm.direction != pygame.Vector2(-1, 0):
            game.worm.next_direction = pygame.Vector2(1, 0)


        pygame.display.flip()

        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
