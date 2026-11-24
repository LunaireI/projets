import pyxel as px
import random 
from typing import Literal

allien_type = Literal["standard", "boosted", "boss"]

BonusType = Literal["invisible", "auto-shot", "super-shot", "damage_multiplicateur"]

class EltGraphique:
    def __init__(self, x: float, y: float, dx: float, dy: float, image: int, height: int, width: int, u: int, v: int):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.img = image
        self.height = height
        self.width = width
        self.u = u
        self.v = v

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        px.blt(int(self.x), int(self.y), self.img, self.u, self.v, self.width, self.height)

    def collision(self, other: 'EltGraphique') -> bool:
        return not ( 
                (other.x >= self.x + self.width)   
                or (other.x + other.width <= self.x)  
                or (other.y >= self.y + self.height) 
                or (other.y + other.height <= self.y) 
        )

class Vaisseau(EltGraphique):
    def __init__(self, x: float, y: float, dx: float, dy: float, image: int, height: int, width: int, u: int, v: int):
        super().__init__(x, y, dx, dy, image, height, width, u, v)
        self.missiles: list[Missile] = []
        self.bonus: list[Bonus] = []

    def update(self):
        self.x += self.dx
        self.y += self.dy
        for e in self.bonus:
            if e.duration > 0:
                e.duration -= 1
            else:
                self.bonus.remove(e)
        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.y > 0]

    def obtainBonus(self, bonus: 'Bonus'):
        self.bonus.append(bonus)

    def tirer(self):
        self.missiles.append(Missile(self.x+3, self.y-2, 0, -1, self.img, 4, 1, 18, 50))      

    def draw_all(self):
        self.draw()
        # draw all missiles
        for m in self.missiles:
            m.draw()
        # draw all bonus
        for i in range(len(self.bonus)):
            b = self.bonus[i]
            if b.type == "invisible":
                px.blt(int(self.x-4+(5*i)), int(self.y+9), 0, 73, 49, 4, 5)
           

class Enemie(EltGraphique):
    def __init__(self, x: float, y: float, dx: float, dy: float, image: int, height: int, width: int, u: int, v: int, level: int = 1, health: int = 1):
        super().__init__(x, y, dx, dy, image, height, width, u, v)
        self.missiles: list[EltGraphique] = []
        self.level = level
        self.health = health
        self.current_healt = health
    def update(self):
        self.x += self.dx
        self.y += self.dy
        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.y > m.height]
    def tirer(self):
        if (self.level == 1 or self.level == 2):
            self.missiles.append(Missile(self.x+3, self.y+2, 0, 1, self.img, 4, 1, 20, 50))
        elif (self.level == 3):
            self.missiles.append(Missile(self.x+3, self.y+2, 0, 1, self.img, 4, 1, 22, 50))
        else:
            self.missiles.append(Missile(self.x+3, self.y+2, 0, 1, self.img, 4, 1, 20, 50))


    def draw_hp(self):
        if self.current_healt != 0:
            px.rect(self.x+2, self.y-3 , self.health, 1, px.COLOR_RED)
            px.rect(self.x+2, self.y-3 , self.current_healt, 1, px.COLOR_GREEN)

    def draw_all(self):
        self.draw()
        self.draw_hp()
        for m in self.missiles:
            m.draw()


class Missile(EltGraphique):
    def __init__(self, x: float, y: float, dx: float, dy: float, image: int, height: int, width: int, u: int, v: int):
        super().__init__(x, y, dx, dy, image, height, width, u, v)

class Bonus(EltGraphique):
    def __init__(self, x: float, y: float, dx: float, dy: float, image: int, height: int, width: int, u: int, v: int, type: BonusType, duration = 600):
        super().__init__(x, y, dx, dy, image, height, width, u, v)
        self.type: BonusType = type
        self.duration: int = duration
    def update(self):
        self.x += self.dx
        self.y += self.dy

ennemies_type = {
    "standard": {"dx": 0, "dy": 0, "image": 0, "height": 8, "width": 8, "u": 24, "v": 8, "level": 1, "health": 1},
    "boosted": {"dx": 0, "dy": 0, "image": 0, "height": 8, "width": 6, "u": 33, "v": 8, "level": 2, "health": 2},
    "boss": {"dx": 0, "dy": 0, "image": 0, "height": 13, "width": 10, "u": 59, "v": 25, "level": 3, "health": 5}
}

def create_ennemie(type_nom: allien_type, x: int, y: int) -> Enemie:
    type = ennemies_type[type_nom]
    return Enemie(x, y, type["dx"], type["dy"], type["image"], type["height"], type["width"], type["u"], type["v"], type["level"], type["health"])

class Game:
    def __init__(self, score: int = 0, level: int = 0) -> None:
        self.score = score
        self.vaisseau: Vaisseau = Vaisseau(px.width//2, px.height//2 + 40, 0, 0, 0, 8, 8, 0, 8)
        self.bonus: list[Bonus] = []
        self.ennemies: list[Enemie] = ennemies_level[level]
        self.cooldown = 0
        self.level = 0
        self.level_max_reached = False
        self.game_over = False

    def update(self):

        if self.game_over:
            px.cls(0)
            self.__init__()
        
        if self.level_max_reached:
            px.cls(0)
            return

        # Variables
        if (self.cooldown > 0):
            self.cooldown -= 1

        # Mouvement Vaisseau Joueur
        if px.btn(px.KEY_RIGHT):
            self.vaisseau.dx = 1
            self.vaisseau.dy = 0	
        elif px.btn(px.KEY_LEFT):
            self.vaisseau.dx = -1
            self.vaisseau.dy = 0

        if not px.btn(px.KEY_RIGHT) and not px.btn(px.KEY_LEFT): 
            self.vaisseau.dx = 0

        # Comportement
        # If lose
        isInvinsible = len([b for b in self.vaisseau.bonus if b.type == "invisible"]) != 0
        for e in self.ennemies:
            for m in e.missiles:
                if self.vaisseau.collision(m): 
                    if not isInvinsible:
                        self.game_over = True
                        print("lose")
                    else:
                        e.missiles.remove(m)
                        
        # If win level
        if len(self.ennemies) == 0 and len(ennemies_level)-1 > self.level:
            self.level += 1
            self.ennemies = ennemies_level[self.level]
        # if level max reached
        if len(self.ennemies) == 0 and len(ennemies_level)-1 == self.level:
            self.level_max_reached = True
            print("win")
        # destroy enemy
        for m in self.vaisseau.missiles:
            for e in self.ennemies:
                if m.collision(e) and e.current_healt == 1: # enemy dead
                    self.score += e.level # score add
                    self.ennemies.remove(e) # remove enemy
                    self.vaisseau.missiles.remove(m) # remove the missile having killed the enemy
                    rd = random.randint(1, 10)
                    if rd == 1:
                        self.bonus.append(Bonus(e.x, e.y, 0, 1.5, 0, 5, 5, 73, 49, "invisible")) # fait spawn un bonus aléatoirement, luck = 1/10
                    break
                elif m.collision(e):
                    e.current_healt -= 1
                    self.vaisseau.missiles.remove(m)
                    break
                for me in e.missiles: # destroy missile when shoot enemy missile
                    if m.collision(me) and e.level != 3:
                        e.missiles.remove(me)
                        self.vaisseau.missiles.remove(m)
                        break
                    elif m.collision(me):
                        self.vaisseau.missiles.remove(m)
                        break
        for e in self.bonus:
            if self.vaisseau.collision(e):
                self.bonus.remove(e)
                if len(self.bonus) < 3:
                    self.vaisseau.bonus.append(e)
        # CD tirer
        if px.btnp(px.KEY_SPACE) and self.cooldown == 0:
            self.vaisseau.tirer()
            self.cooldown = 5
        # enemy shoot
        if len(self.ennemies) > 0 and px.frame_count % 15 == 0: # shoot every 15 frames
                suite = 1.2 ** self.level 
                luckTir = 10 * suite + (1 + self.level/10)
                for e in self.ennemies:
                    if random.randint(0, 100) < luckTir:
                        e.tirer()
        # update vaiseau
        if (px.frame_count%5):
            self.vaisseau.update()
        # update tout les enemies
        for e in self.ennemies:
            e.update()
        # update tout les bonus
        for e in self.bonus:
            e.update()

    def draw(self):
        px.cls(0) # draw black screen
        px.text(0, 0, str(self.score), 13) # write score
        self.vaisseau.draw_all()
        # draw all enemy
        for e in self.ennemies:
            e.draw_all()
        # draw all bonus
        for e in self.bonus:
            e.draw()
ennemies_level: list[list[Enemie]] = [
    [create_ennemie("standard", 20, 15), create_ennemie("standard", 40, 15), create_ennemie("standard", 60, 15), create_ennemie("standard", 80, 15), create_ennemie("standard", 100, 15)],
    [create_ennemie("standard", 20, 15), create_ennemie("boosted", 40, 15), create_ennemie("standard", 60, 15), create_ennemie("boosted", 80, 15), create_ennemie("standard", 100, 15)],
    [create_ennemie("boosted", 20, 15), create_ennemie("boosted", 40, 15), create_ennemie("boosted", 60, 15), create_ennemie("boosted", 80, 15), create_ennemie("boosted", 100, 15)],
    [
        create_ennemie("boosted", 20, 15), create_ennemie("boosted", 40, 15), create_ennemie("boosted", 60, 15), create_ennemie("boosted", 80, 15), create_ennemie("boosted", 100, 15),
        create_ennemie("standard", 30, 30), create_ennemie("standard", 50, 30), create_ennemie("standard", 70, 30), create_ennemie("standard", 90, 30)
    ],
    [create_ennemie("boosted", 20, 15), create_ennemie("boosted", 40, 15), create_ennemie("boss", 60, 15), create_ennemie("boosted", 80, 15), create_ennemie("boosted", 100, 15)],
    [create_ennemie("boosted", 20, 15), create_ennemie("boss", 40, 15), create_ennemie("boss", 60, 15), create_ennemie("boss", 80, 15), create_ennemie("boosted", 100, 15)],
    [
        create_ennemie("boosted", 20, 15), create_ennemie("boss", 40, 15), create_ennemie("boss", 60, 15), create_ennemie("boss", 80, 15), create_ennemie("boosted", 100, 15),
        create_ennemie("boosted", 50, 30), create_ennemie("boosted", 70, 30)
    ],
]

if __name__ == "__main__":
    px.init(120, 120, title="Pixel", fps=60)
    appli = Game()
    px.load("2.pyxres") 
    px.run(appli.update, appli.draw)

