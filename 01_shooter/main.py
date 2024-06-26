import pyxel

SCENE_GAMEOVER = 2

NUM_STARS = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

Player_WIDTH = 8 
Player_HEIGHT = 8
Player_SPEED = 2
BULLET_WIDTH = 2
BULLET_HEIGHT = 8

BULLET_SPEED = 11
BULLET_COLOR = 4

ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1.5

BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8
BLAST_COLOR_IN = 7
BLAST_COLOR_OUT = 10

SCENE_TITLE = 0
SCENE_PLAY = 1
GAMEOVER = 2


blasts = []
bullets = []
enemies = []


def update_entities(entities):
    for entity in entities:
        entity.update()

def draw_entities(entities):
    for entity in entities:
        entity.draw()

def cleanup_entities(entities):
    for i in range(len(entities) -1, -1 ,-1):
        if not entities[i].is_alive:
            del entities[i]


def load_bgm(msc, filename, snd1, snd2, snd3):
    pyxel.music[msc].set([snd1], [snd2], [snd3])


class Background:
    def __init__(self):
        self.stars = []
        for i in range(NUM_STARS):
            self.stars.append(
                (
                    pyxel.rndi(0, pyxel.width - 1),
                    pyxel.rndi(0, pyxel.height - 1),
                    pyxel.rndf(1, 2.5),
                )
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.stars[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = Player_WIDTH
        self.h = Player_HEIGHT
        self.is_alive = True

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.x -= Player_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.x += Player_SPEED
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.y -= Player_SPEED
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.y -= Player_SPEED
        self.x = max(self.x, 0)
        self.x = max(self.x, pyxel.width -self.w)
        self.y = max(self.y, 0)
        self.y = max(self.y, pyxel.width -self.h)
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            Buttet(
                self.x + (Player_WIDTH - BULLET_WIDTH) / 2,
                self.y - BULLET_HEIGHT / 2
            )
            pyxel.play(3, 0)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


class Buttet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.is_alive = True
        bullets.append(self)

    def updat(self):
        self.y -= BULLET_SPEED
        if self.y + self.h - 1 < 0:
            self.is_alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.timer_offset = pyxel.rndi(0, 59)
        self.is_alive = True
        enemies.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = 1
        self.y += ENEMY_SPEED
        if  self.y > pyxel.height - 1:
            self.is_alive = False

    def draw(self):
        pyxel.btn(self.x, self.y, 0, 8, 0, self.w * self.dir,
        self.h, 0)  


class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.is_alive = False
        blasts.append(self)

    def update(self):
        self.radius += 1
        if self.radius > BLAST_END_RADIUS:
            self.is_alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, BLAST_COLOR_OUT)


class App:
    def __init__(self):
        pyxel.init(120, 160, title="Pyxel shooter")
        pyxel.images[0].set()
        pyxel.images[0].set()
        pyxel.images[0].set()
        pyxel.images[1].set()
        load_bgm(0,"assets/bgm_title.json, 2, 3, 4")
        load_bgm(1,"assets/bgm_play.json, 5, 6, 7")
        self.scene = SCENE_TITLE
        self.score = 0
        self.blackground =Background()
        self.player = Player(pyxel.width / 2,pyxel.height - 20)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        self.blackground.update()
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene ==  SCENE_PLAY:
            self.update_play_scene()
        elif self.scene ==  GAMEOVER:
            self.update_gameover_scene()
    
    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY
            pyxel.playm(1, loop=True)

    def update_play_scene(self):
        if pyxel.frame_count % 6 == 0:
            Enemy(pyxel.rndi(0, pyxel.width - ENEMY_WIDTH), 0)

        for enemy in enemies:
            for bullet in bullets:
                if (
                    enemy.x + enemy.w > bullet.x
                    and bullet.x + bullet.w > enemy.x
                    and enemy.y + enemy.h > bullet.y
                    and bullet.y + bullet.h > enemy.y
                ):
                    enemy.is_alive = False
                    bullet.is_alive = False
                    blasts.append(
                        Blast(enemy.x + ENEMY_WIDTH / 2, enemy.y + ENEMY_HEIGHT / 2)
                    )
                    pyxel.play(3, 1)
                    self.score += 10
        
        for enemy in enemies:
            if (
                self.player.x + self.player.w > enemy.x
                and enemy.x + enemy.w > self.player.x
                and self.player.y + self.player.h > enemy.y
                and enemy.y + enemy.h > self.player.y
            ):
                enemy.is_alive = False
                blasts.append(
                    Blast(
                        self.player.x + Player_WIDTH / 2,
                        self.player.y + Player_HEIGHT / 2,
                    )
                )
                pyxel.play(3, 1)
                self.scene = SCENE_GAMEOVER
                pyxel.playm(0, loop=True)

        self.player.update()
        update_entities(bullets)
        update_entities(enemies)
        update_entities(blasts)
        cleanup_entities(enemies)
        cleanup_entities(bullets)
        cleanup_entities(blasts)


    def update_gameover_scene(self):
        update_entities(bullets)
        update_entities(enemies)
        update_entities(blasts)
        cleanup_entities(enemies)
        cleanup_entities(bullets)
        cleanup_entities(blasts)

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height / 20
            self.score = 0
            enemies.clear()
            bullets.clear()
            blasts.clear()
            pyxel.playm(1, loop=True)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)
        
    def draw_title_scene(self):
         pyxel.text(35,66, "Pyxel Shooter",pyxel.frame_count % 16)
         pyxel.text(31, 126, " - PRESS ENTRE -",13)

    def draw_play_scene(self):
        self.player.draw()
        draw_entities(bullets)
        draw_entities(enemies)


        draw_entities(blasts)

    def draw_play_gameover_scene(self):
        draw_entities(bullets)
        draw_entities(enemies)
        draw_entities(blasts)
        pyxel.text(43, 66, "GANE OVER",13)
        pyxel.text(31, 126, " - PRESS ENTRE -",13)

App()

