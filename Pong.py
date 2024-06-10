from turtle import bgcolor
import pygame, sys, random

class Menu:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 64)
        self.options = ['Start Game', 'Quit']
        self.selected_options = 0
        self.option_height = 100
        self.option_color = accent_color
    
    def draw_menu(self, screen):
        screen.fill(pygame.Color('#2F373F'))
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, self.option_color)
            text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + i*self.option_height))
            screen.blit(text, text_rect)
            if i == self.selected_options:
                pygame.draw.rect(screen, self.option_color, text_rect, 2)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_options = (self.selected_options - 1) % len(self.options)
                pygame.mixer.Sound.play(plob_sound)
            elif event.key == pygame.K_DOWN:
                self.selected_options = (self.selected_options + 1) % len(self.options)
                pygame.mixer.Sound.play(plob_sound)
            elif event.key == pygame.K_RETURN:
                pygame.mixer.Sound.play(score_sound)
                if self.selected_options == 0:  # Start Game
                    return "start"
                elif self.selected_options == 1:  # Quit
                    return "quit"

        return None

class Pause:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 64)
        self.options = ['Resume']
        self.selected_options = 0
        self.option_height = 100
        self.option_color = accent_color

    def draw_pause(self, screen):
        screen.fill(pygame.Color('#2F373F'))
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, self.option_color)
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + i * self.option_height))
            screen.blit(text, text_rect)
            if i == self.selected_option:
                pygame.draw.rect(screen, self.option_color, text_rect, 2)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                pygame.mixer.Sound.play(plob_sound)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                pygame.mixer.Sound.play(plob_sound)
            elif event.key == pygame.K_RETURN:
                pygame.mixer.Sound.play(score_sound)
                if self.selected_option == 0:  # Resume
                    return "resume"
                

        return None

class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(plob_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.pause_menu = Pause()
        self.paused = False

    def run_game(self):
        if not self.paused:

            # Drawing the game objects
            self.paddle_group.draw(screen)
            self.ball_group.draw(screen)

            # Updating the game objects
            self.paddle_group.update(self.ball_group)
            self.ball_group.update()
            self.update_score()
            self.draw_score()
        else:
            self.pause_menu.draw_pause(screen)

    def update_score(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            pygame.mixer.Sound.play(opponent_score_sound)
            self.ball_group.sprite.reset_ball()
            self.reset_paddles()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            pygame.mixer.Sound.play(score_sound)
            self.ball_group.sprite.reset_ball()
            self.reset_paddles()

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)


    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_menu.selected_option = 0

    def handle_pause_input(self, event):
        if self.paused:
            menu_result = self.pause_menu.handle_input(event)
            if menu_result == "resume":
                self.toggle_pause()
            elif menu_result == "main_menu":
                return "main_menu"

    def reset_paddles(self):
        for paddle in paddle_group:
            paddle.rect.centery = screen_height/2



# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')


# Global Variables
bg_color = pygame.Color('#2F373F')
accent_color = pygame.Color('papayawhip')
basic_font = pygame.font.Font('freesansbold.ttf', 32)
plob_sound = pygame.mixer.Sound("sounds/ball_hit.mp3")
score_sound = pygame.mixer.Sound("sounds/point_scored.mp3")
opponent_score_sound = pygame.mixer.Sound("sounds/point_lost.mp3")
middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)


# Game objects
player = Player('images/Paddle.png', screen_width - 20, screen_height / 2, 5)
opponent = Opponent('images/Paddle.png', 20, screen_width / 2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('images/Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)
menu = Menu()
menu_active = True


while True:
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input for the menu
            menu_result = menu.handle_input(event)
            if menu_result == "start":
                menu_active = False
                # Start the game
            elif menu_result == "quit":
                pygame.quit()
                sys.exit()
        menu.draw_menu(screen)
        pygame.display.flip()
        clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_manager.toggle_pause()
                
        game_manager.handle_pause_input(event)    

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed
                

    # Background Stuff
    screen.fill(bg_color)
    pygame.draw.rect(screen, accent_color, middle_strip)

    # Run the game
    game_manager.run_game()

    # Rendering
    pygame.display.flip()
    clock.tick(120)