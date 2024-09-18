import pygame

WIDTH = 800
HEIGHT = 640

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

running = True

sky_blue = (142, 202, 230)
blue_green = (33, 158, 188)
prussian_blue = (2, 48, 71)
selective_yellow = (255, 183, 3)
ut_orange = (251, 133, 0)
white = (255, 255, 255)
black = (0, 0, 0)

pong = pygame.mixer.Sound('Assets/audio/jingles_SAX04.ogg') # colocando sons
ping = pygame.mixer.Sound('Assets/audio/jingles_SAX05.ogg')
point = pygame.mixer.Sound('Assets/audio/jingles_SAX16.ogg')
win = pygame.mixer.Sound('Assets/audio/game_over.ogg')
start = pygame.mixer.Sound('Assets/audio/new game.ogg')

letraP = pygame.image.load('assets/image/letter_P.png')  # escolhi colocar só letras pela didatica de colocar imagens no jogo
letraO = pygame.image.load('assets/image/letter_O.png')
letraN = pygame.image.load('assets/image/letter_N.png')
letraG = pygame.image.load('assets/image/letter_G.png')

letraP = pygame.transform.scale(letraP, (50, 50)) # mudando tamanho das letras
letraO = pygame.transform.scale(letraO, (50, 50))
letraN = pygame.transform.scale(letraN, (50, 50))
letraG = pygame.transform.scale(letraG, (50, 50))

score_font = pygame.font.SysFont("couriernew", 50) # escolhendo a fonte

maxvel = 1 # velocidade da bola
rect_x, rect_y, rect_w, rect_h = 10, int(HEIGHT / 2) - 50, 50, 100 #criando player esquerdo
rect2_x, rect2_y, rect2_w, rect2_h = (WIDTH - 60), int(HEIGHT / 2) - 50, 50, 100 #criando player direito
circle_x, circle_y, circle_w, x_vel, y_vel = (800 // 2 - 2), (640 // 2), 7, maxvel, 0 #criando a bola

# score
left_score = 0
right_score = 0
winning_score = 10
start.play()

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and rect_y >= 0:
        rect_y -= 1

    if keys[pygame.K_s] and rect_y <= HEIGHT - 100:
        rect_y += 1

    if keys[pygame.K_UP] and rect2_y >= 0:
        rect2_y -= 1

    if keys[pygame.K_DOWN] and rect2_y <= HEIGHT - 100:
        rect2_y += 1

    screen.fill(prussian_blue)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(screen, white, (WIDTH // 2 - 5, i, 5, HEIGHT // 40))

    pygame.draw.rect(screen, white, (rect_x, rect_y, rect_w, rect_h))

    pygame.draw.rect(screen, white, (rect2_x, rect2_y, rect2_w, rect2_h))

    pygame.draw.circle(screen, white, (circle_x, circle_y), circle_w)

    circle_x = circle_x + x_vel  #movendo bola
    circle_y = circle_y + y_vel  #movendo bola
    if circle_y + circle_w > HEIGHT:  #kikando a bola cima e baixo
        y_vel *= -1
    elif circle_y - circle_w <= 0:
        y_vel *= -1

    if x_vel < 0:  # mecanica de rebater com logica de aceleração e mudança de direção
        if circle_y >= rect_y and circle_y <= rect_y + rect_h:  #esquerda
            if circle_x - circle_w <= rect_x + rect_w:
                x_vel *= -1

                middle_y = rect_y + rect_h / 2
                difference_in_y = middle_y - circle_y
                reduction_factor = (rect_h / 2) / maxvel
                yvelcalc = difference_in_y / reduction_factor
                y_vel = -1 * yvelcalc
                ping.play()
    else:
        if circle_y >= rect2_y and circle_y <= rect2_y + rect2_h:  #direita
            if circle_x + circle_w >= rect2_x:
                x_vel *= -1

                middle_y = rect2_y + rect2_h / 2
                difference_in_y = middle_y - circle_y
                reduction_factor = (rect2_h / 2) / maxvel
                yvelcalc = difference_in_y / reduction_factor
                y_vel = -1 * yvelcalc
                pong.play()

    if circle_x < 0:  #ponto lado direito
        right_score += 1
        point.play()
        circle_x, circle_y = WIDTH // 2, HEIGHT // 2  # Reset da posição da bola
        x_vel, y_vel = maxvel, 0  # Reset velocidade
        pygame.time.delay(200)
    elif circle_x > WIDTH:  #ponto lado esquerdo
        left_score += 1
        point.play()
        circle_x, circle_y = WIDTH // 2, HEIGHT // 2  # Reset da posição da bola
        x_vel, y_vel = -maxvel, 0  # Reset velocidade
        pygame.time.delay(200)

    left_score_text = score_font.render(f"{left_score}", True, selective_yellow)
    right_score_text = score_font.render(f"{right_score}", True, selective_yellow)

    screen.blit(left_score_text, (WIDTH // 4, 20))
    screen.blit(right_score_text, (3 * WIDTH // 4, 20))

    won = False

    if left_score >= winning_score:
        won = True
        win_text = "Left Player Won!"
    elif right_score >= winning_score:
        won = True
        win_text = "Right Player Won!"

    if won:
        win.play()
        text = score_font.render(win_text, 1, selective_yellow)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)

        left_score = 0 #reset
        right_score = 0
        circle_x, circle_y = WIDTH // 2, HEIGHT // 2
        rect_x, rect_y = 10, int(HEIGHT / 2) - 50
        rect2_x, rect2_y = (WIDTH - 60), int(HEIGHT / 2) - 50
        start.play()

        # Exibir as imagens
        screen.fill(prussian_blue)
        screen.blit(letraP, (WIDTH // 4 - 50, HEIGHT // 2 - letraP.get_width() //2))
        screen.blit(letraO, (WIDTH // 4 + 100, HEIGHT // 2 - letraP.get_width() //2))
        screen.blit(letraN, (WIDTH // 2 + 50, HEIGHT // 2 - letraP.get_width() //2))
        screen.blit(letraG, (WIDTH // 2 + 200, HEIGHT // 2 - letraP.get_width() //2))
        pygame.display.update()
        pygame.time.delay(2000)

    #clock.tick(60)
    pygame.display.flip()  # é a função que é chamada para atualizar a tela.
