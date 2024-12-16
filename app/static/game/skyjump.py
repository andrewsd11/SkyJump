import pygame
import random
import sys

# Receber o ID da fase como argumento de linha de comando
fase_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1  # Padrão: fase 1

# Inicializar o pygame
pygame.init()

# Configurações da tela
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Sky Jump - Fase {fase_id}")  # Adiciona o número da fase no título

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)  # Azul para o foguete

# Configurações do jogador
player = {
    'x': 200,
    'y': 500,
    'width': 40,
    'height': 40,
    'color': ORANGE,
    'velocity_y': -10,
    'jump_force': -10,
    'gravity': 0.5
}

platforms = []
is_game_over = False
score = 0
last_platform_y = player['y']  # Para rastrear a última posição em Y para pontuação
is_gravity_reduced = False

# Criar plataformas iniciais
for i in range(8):
    platforms.append({
        'x': random.randint(0, 300),
        'y': i * 75,
        'width': 100,
        'height': 20,
        'has_umbrella': random.random() < 0.1 if fase_id >= 2 else False,  # 10% de chance para o guarda-chuva
        'has_rocket': random.random() < 0.05 if fase_id == 3 else False  # 5% de chance para o foguete na fase 3
    })

def draw_player():
    pygame.draw.rect(screen, player['color'], (player['x'], player['y'], player['width'], player['height']))

def draw_platforms():
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, (platform['x'], platform['y'], platform['width'], platform['height']))
        if platform['has_umbrella']:
            pygame.draw.circle(screen, RED, (platform['x'] + platform['width'] // 2, platform['y'] + platform['height'] // 2), 10)
        if platform['has_rocket']:
            pygame.draw.circle(screen, BLUE, (platform['x'] + platform['width'] // 2, platform['y'] + platform['height'] // 2), 10)

def update_player():
    global is_gravity_reduced, score, last_platform_y
    
    player['y'] += player['velocity_y']
    player['velocity_y'] += player['gravity']
    
    if player['y'] + player['height'] > HEIGHT:
        game_over()
    
    for platform in platforms:
        if (player['y'] + player['height'] >= platform['y'] and
            player['y'] + player['height'] <= platform['y'] + platform['height'] and
            player['x'] + player['width'] >= platform['x'] and
            player['x'] <= platform['x'] + platform['width'] and
            player['velocity_y'] >= 0):
            player['velocity_y'] = player['jump_force']
            if platform['has_umbrella']:
                activate_umbrella()
            if platform['has_rocket']:
                activate_rocket()
    
    # Pontuar ao subir plataformas
    if player['y'] < last_platform_y:
        score += (last_platform_y - player['y']) // 75 * 10  # 10 pontos para cada plataforma passada
        last_platform_y = player['y']

def activate_umbrella():
    global is_gravity_reduced
    if not is_gravity_reduced:
        is_gravity_reduced = True
        player['gravity'] = 0.2
        pygame.time.set_timer(pygame.USEREVENT, 4000)

def activate_rocket():
    player['velocity_y'] = -30  # Impulso maior para o "super pulo"

def update_platforms():
    if player['y'] < 300:
        for platform in platforms:
            platform['y'] += 3
            if platform['y'] > HEIGHT:
                platform['y'] = 0
                platform['x'] = random.randint(0, 300)
                platform['has_umbrella'] = random.random() < 0.1 if fase_id >= 2 else False  # 10% de chance de ter o guarda-chuva
                platform['has_rocket'] = random.random() < 0.05 if fase_id == 3 else False  # 5% de chance de ter o foguete

def game_over():
    global is_game_over
    is_game_over = True

def draw_score():
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def main():
    global is_game_over
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:  # Restaura a gravidade após 4 segundos
                player['gravity'] = 0.5
                is_gravity_reduced = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player['x'] -= 5
        if keys[pygame.K_RIGHT]:
            player['x'] += 5

        if not is_game_over:
            update_player()
            update_platforms()

        screen.fill(BLACK)
        draw_player()
        draw_platforms()
        draw_score()
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
