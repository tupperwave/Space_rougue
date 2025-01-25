import pgzrun
import random
import math

HEIGHT = 1000
WIDTH = 1200

class Player:
    def __init__(self, pos):
        self.actor = Actor('will', pos)
        self.velocidade = 0
        self.aceleracao = 0.15
        self.desaceleracao = 0.05
        self.velocidade_maxima = 6
        self.vidas = 5

    def draw(self):
        self.actor.draw()

    def update(self):
        self.movimentar()

    def movimentar(self):
        if keyboard.left:
            self.actor.angle += 3
        if keyboard.right:
            self.actor.angle -= 3
        if keyboard.up:
            self.velocidade = min(self.velocidade + self.aceleracao, self.velocidade_maxima)
        else:
            self.velocidade = max(self.velocidade - self.desaceleracao, 0)
        rad = math.radians(self.actor.angle + 180)
        self.actor.x += self.velocidade * math.sin(rad)
        self.actor.y += self.velocidade * math.cos(rad)
        self.actor.x = max(0, min(WIDTH, self.actor.x))
        self.actor.y = max(0, min(HEIGHT, self.actor.y))

class Enemy:
    def __init__(self, pos, angle):
        self.actor = Actor('enemy', pos)
        self.actor.angle = angle

    def draw(self):
        self.actor.draw()

    def update(self, player_pos):
        self.movimentar(player_pos)

    def movimentar(self, player_pos):
        angle_to_player = math.atan2(player_pos[1] - self.actor.y, player_pos[0] - self.actor.x)
        self.actor.angle = math.degrees(angle_to_player)
        rad = math.radians(self.actor.angle)
        self.actor.x += 1.5 * math.cos(angle_to_player)
        self.actor.y += 1.5 * math.sin(angle_to_player)

class Game:
    def __init__(self):
        self.player = Player((WIDTH // 2, HEIGHT - 100))
        self.inimigos = []
        self.asteroides = []
        self.tiros = []
        self.powerups = []
        self.highscore = 0
        self.tiros_inimigos = []
        self.explosoes = []
        self.pontuacao = 0
        self.menu_ativo = True
        self.musica_ativa = True
        self.jogo_pausado = False
        self.jogo_terminado = False
        self.background = Actor('background', (WIDTH // 2, HEIGHT // 2))
        self.explosion_frames = ['explosion1', 'explosion2', 'explosion3', 'explosion4']
        self.powerup_frames = ['powerup', 'powerup_blink']
        self.botao_jogar = Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        self.botao_musica = Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)
        self.botao_sair = Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
        self.botao_reiniciar = Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
        if self.musica_ativa:
            sounds.background.play(-1)
            sounds.background.set_volume(0.5)

    def draw(self):
        screen.clear()
        if self.menu_ativo:
            self.draw_menu()
        elif self.jogo_pausado:
            self.draw_pause()
        elif self.jogo_terminado:
            self.draw_game_over()
        else:
            self.draw_game()

    def draw_menu(self):
        screen.draw.text("SPACE ROGUELIKE", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=50, color="white")
        screen.draw.filled_rect(self.botao_jogar, "green")
        screen.draw.text("JOGAR", center=self.botao_jogar.center, fontsize=30, color="white")
        screen.draw.filled_rect(self.botao_musica, "blue")
        screen.draw.text("MÚSICA ON" if self.musica_ativa else "MÚSICA OFF", center=self.botao_musica.center, fontsize=30, color="white")
        screen.draw.filled_rect(self.botao_sair, "red")
        screen.draw.text("SAIR", center=self.botao_sair.center, fontsize=30, color="white")

    def draw_pause(self):
        screen.draw.text("JOGO PAUSADO", center=(WIDTH // 1, HEIGHT // 1), fontsize=50, color="yellow")
        screen.draw.filled_rect(self.botao_jogar, "green")
        screen.draw.text("CONTINUAR", center=self.botao_jogar.center, fontsize=30, color="white")
        screen.draw.filled_rect(self.botao_musica, "blue")
        screen.draw.text("MÚSICA ON" if self.musica_ativa else "MÚSICA OFF", center=self.botao_musica.center, fontsize=30, color="white")
        screen.draw.filled_rect(self.botao_sair, "red")
        screen.draw.text("SAIR", center=self.botao_sair.center, fontsize=30, color="white")

    def draw_game_over(self):
        screen.draw.text("FIM DE JOGO", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=50, color="red")
        screen.draw.text(f"Pontos: {self.pontuacao}", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=30, color="white")
        screen.draw.text(f"Highscore: {self.highscore}", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="white")
        screen.draw.filled_rect(self.botao_reiniciar, "green")
        screen.draw.text("REINICIAR", center=self.botao_reiniciar.center, fontsize=30, color="white")

    def draw_game(self):
        screen.draw.text(f"Pontos: {self.pontuacao}", (10, 10), color="white", fontsize=30)
        for i in range(self.player.vidas):
            screen.blit('heart', (10 + i * 40, 50))
        self.player.draw()
        for inimigo in self.inimigos:
            inimigo.draw()
        for asteroide in self.asteroides:
            asteroide.draw()
        for tiro in self.tiros:
            tiro.draw()
        for tiro_inimigo in self.tiros_inimigos:
            tiro_inimigo.draw()
        for explosao in self.explosoes:
            explosao["sprite"].draw()
        for powerup in self.powerups:
            powerup["sprite"].draw()

    def update(self):
        if self.menu_ativo or self.jogo_pausado or self.jogo_terminado:
            return
        self.player.update()
        self.atualizar_tiros()
        self.gerar_asteroides()
        self.atualizar_asteroides()
        self.gerar_inimigos()
        self.atualizar_inimigos()
        self.atualizar_explosoes()
        self.gerar_powerups()
        self.atualizar_powerups()

    def on_mouse_down(self, pos):
        if self.menu_ativo or self.jogo_pausado:
            if self.botao_jogar.collidepoint(pos):
                self.menu_ativo = False
                self.jogo_pausado = False
                music.stop()
            elif self.botao_musica.collidepoint(pos):
                self.musica_ativa = not self.musica_ativa
                if self.musica_ativa:
                    sounds.background.play(-1)
                    sounds.background.set_volume(0.5)
                else:
                    sounds.background.stop()
            elif self.botao_sair.collidepoint(pos):
                exit()
        elif self.jogo_terminado:
            if self.botao_reiniciar.collidepoint(pos):
                self.reset_game()

    def atualizar_tiros(self):
        for tiro in self.tiros[:]:
            rad = math.radians(tiro.angle + 180)
            tiro.x += 10 * math.sin(rad)
            tiro.y += 10 * math.cos(rad)
            if not (0 <= tiro.x <= WIDTH and 0 <= tiro.y <= HEIGHT):
                self.tiros.remove(tiro)

    def gerar_asteroides(self):
        if random.randint(1, 100) == 1:
            x = random.randint(0, WIDTH)
            asteroide = Actor('asteroid', (x, 0))
            self.asteroides.append(asteroide)

    def atualizar_asteroides(self):
        for asteroide in self.asteroides[:]:
            asteroide.y += 2
            if asteroide.y > HEIGHT:
                self.asteroides.remove(asteroide)
            if asteroide.colliderect(self.player.actor):
                sounds.hit2.play()
                self.ajustar_posicao(self.player.actor, asteroide)
            for inimigo in self.inimigos:
                if asteroide.colliderect(inimigo.actor):
                    sounds.hit2.play()
                    self.ajustar_posicao(inimigo.actor, asteroide)
            for tiros_inimigo in self.tiros_inimigos[:]:
                if asteroide.colliderect(tiros_inimigo):
                    self.tiros_inimigos.remove(tiros_inimigo)
            for tiro in self.tiros[:]:
                if asteroide.colliderect(tiro):
                    self.tiros.remove(tiro)
                    self.iniciar_explosao(tiro.pos)
                    sounds.explosion.play()
                    self.asteroides.remove(asteroide)
                    break

    def ajustar_posicao(self, obj, barreira):
        dx = obj.x - barreira.x
        dy = obj.y - barreira.y
        distancia = math.sqrt(dx**2 + dy**2)
        if distancia == 0:
            return
        overlap = (obj.width + barreira.width) / 2 - distancia
        obj.x += dx / distancia * overlap
        obj.y += dy / distancia * overlap

    def gerar_inimigos(self):
        if random.randint(1, 200) == 1:
            lado = random.choice(['top', 'bottom', 'left', 'right'])
            if lado == 'top':
                inimigo = Enemy((random.randint(0, WIDTH), 0), random.randint(0, 360))
            elif lado == 'bottom':
                inimigo = Enemy((random.randint(0, WIDTH), HEIGHT), random.randint(0, 360))
            elif lado == 'left':
                inimigo = Enemy((0, random.randint(0, HEIGHT)), random.randint(0, 360))
            elif lado == 'right':
                inimigo = Enemy((WIDTH, random.randint(0, HEIGHT)), random.randint(0, 360))
            self.inimigos.append(inimigo)

    def atualizar_inimigos(self):
        for inimigo in self.inimigos[:]:
            inimigo.update((self.player.actor.x, self.player.actor.y))
            if inimigo.actor.x < 0 or inimigo.actor.x > WIDTH or inimigo.actor.y < 0 or inimigo.actor.y > HEIGHT:
                self.inimigos.remove(inimigo)
            if random.randint(1, 50) == 1:
                tiro_inimigo = Actor('laserenemy', (inimigo.actor.x, inimigo.actor.y))
                tiro_inimigo.angle = inimigo.actor.angle
                self.tiros_inimigos.append(tiro_inimigo)
                sounds.laser5.play()
            if inimigo.actor.colliderect(self.player.actor):
                sounds.hit.play()
                self.iniciar_explosao(inimigo.actor.pos)
                self.inimigos.remove(inimigo)
                self.player.vidas -= 1
                if self.player.vidas == 0:
                    self.iniciar_explosao(self.player.actor.pos)
                    self.game_over()
        for tiro_inimigo in self.tiros_inimigos[:]:
            rad = math.radians(tiro_inimigo.angle)
            tiro_inimigo.x += 5 * math.cos(rad)
            tiro_inimigo.y += 5 * math.sin(rad)
            if tiro_inimigo.colliderect(self.player.actor):
                sounds.hit.play()
                self.tiros_inimigos.remove(tiro_inimigo)
                self.player.vidas -= 1
                if self.player.vidas == 0:
                    self.iniciar_explosao(self.player.actor.pos)
                    self.game_over()
            elif not (0 <= tiro_inimigo.x <= WIDTH and 0 <= tiro_inimigo.y <= HEIGHT):
                self.tiros_inimigos.remove(tiro_inimigo)
        for inimigo in self.inimigos[:]:
            for tiro in self.tiros[:]:
                if inimigo.actor.colliderect(tiro):
                    self.inimigos.remove(inimigo)
                    self.tiros.remove(tiro)
                    self.pontuacao += 2
                    self.iniciar_explosao(inimigo.actor.pos)
                    break
            if inimigo.actor.colliderect(self.player.actor):
                sounds.hit.play()
                self.iniciar_explosao(inimigo.actor.pos)
                self.inimigos.remove(inimigo)
                self.player.vidas -= 1
                if self.player.vidas == 0:
                    self.iniciar_explosao(self.player.actor.pos)
                    self.game_over()
        for tiro in self.tiros[:]:
            for tiro_inimigo in self.tiros_inimigos[:]:
                if tiro.colliderect(tiro_inimigo):
                    self.tiros.remove(tiro)
                    self.tiros_inimigos.remove(tiro_inimigo)
                    self.iniciar_explosao(tiro.pos)
                    sounds.explosion.play()
                    break

    def gerar_powerups(self):
        if random.randint(1, 2000) == 1:
            powerup = {
                "sprite": Actor('powerup', (random.randint(0, WIDTH), random.randint(0, HEIGHT))),
                "tempo": 0
            }
            self.powerups.append(powerup)

    def atualizar_powerups(self):
        for powerup in self.powerups[:]:
            powerup["tempo"] += 1
            if powerup["tempo"] > 300:
                if powerup["tempo"] % 30 < 15:
                    powerup["sprite"].image = 'powerup'
                else:
                    powerup["sprite"].image = 'powerup_blink'
            if powerup["tempo"] > 900:
                self.powerups.remove(powerup)
                continue
            if self.player.actor.colliderect(powerup["sprite"]):
                sounds.powerup.play()
                self.powerups.remove(powerup)
                self.player.vidas += 1

    def atualizar_explosoes(self):
        for explosao in self.explosoes[:]:
            explosao["tempo"] += 1
            if explosao["tempo"] % 5 == 0:
                explosao["indice"] += 1
                if explosao["indice"] < len(self.explosion_frames):
                    explosao["sprite"].image = self.explosion_frames[explosao["indice"]]
                else:
                    self.explosoes.remove(explosao)

    def on_key_down(self, key):
        if key == keys.ESCAPE:
            if self.menu_ativo:
                exit()
            else:
                self.jogo_pausado = not self.jogo_pausado
        if key == keys.SPACE and not self.menu_ativo and not self.jogo_pausado:
            rad = math.radians(self.player.actor.angle + 180)
            tiro = Actor('laser', (self.player.actor.x, self.player.actor.y))
            tiro.angle = self.player.actor.angle
            self.tiros.append(tiro)
            sounds.laser.play()

    def iniciar_explosao(self, pos):
        explosao = {"sprite": Actor(self.explosion_frames[0], pos), "indice": 0, "tempo": 0}
        self.explosoes.append(explosao)
        sounds.explosion.play()

    def reset_game(self):
        self.pontuacao = 0
        self.inimigos.clear()
        self.tiros.clear()
        self.explosoes.clear()
        self.asteroides.clear()
        self.tiros_inimigos.clear()
        self.powerups.clear()
        self.player.vidas = 5
        self.jogo_terminado = False
        self.player.velocidade = 0
        self.player.actor.pos = (WIDTH // 2, HEIGHT - 100)

    def game_over(self):
        self.jogo_terminado = True
        if self.pontuacao > self.highscore:
            self.highscore = self.pontuacao
            print("Novo highscore:", self.highscore)

game = Game()

def draw():
    game.draw()

def update():
    game.update()

def on_mouse_down(pos):
    game.on_mouse_down(pos)

def on_key_down(key):
    game.on_key_down(key)

pgzrun.go()