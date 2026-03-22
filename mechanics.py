from __future__ import annotations

import random


class Entity:
    def __init__(self, x, y, redline, redlineDrag, drag):
        self.x = x
        self.y = y
        self.redline = redline
        self.redlineDrag = redlineDrag
        self.drag = drag
        self.vx = random.randint(0, 10)
        self.vy = random.randint(0, 10)
        self.speed = (self.vx**2 + self.vy ** 2)**0.5
    def updatePos(self):
        self.vx += random.randint(-2,2)
        self.vy += random.randint(-2,2)
        self.speed = (self.vx**2 + self.vy ** 2)**0.5
        if self.speed >= self.redline:
            self.vx *= (1-self.redlineDrag)
            self.vy *= (1 - self.redlineDrag)
        else:
            self.vx *= (1 - self.drag)
            self.vy *= (1 - self.drag)
        self.x += self.vx
        self.y += self.vy

class FoodParticle(Entity):
    def __init__(self, x, y):
        super().__init__(x,y, 0, 0.9, 0.7)

class Antibiotic(Entity):
    def __init__(self, x, y):
        super().__init__(x,y, 50, 0.3, 0.05)

class Bacteria(Entity):
    def __init__(self, x, y, redline, redlineDrag, drag):
        super().__init__(x,y, redline, redlineDrag, drag)
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.a = random.randint(0, 100)
        self.infected = False
        self.phageData = None
        self.energy = 5000
    def phageCollision(self, phage:Phage):
        if (((phage.x-self.x)**2 + (phage.y- self.y)**2)**0.5) <= 12:
            if ((phage.r-self.r)**2 + (phage.g-self.g)**2 + (phage.b-self.b)**2 )**0.5 < random.randint(0,200):
                self.infected = True
                self.phageData = (phage.r,phage.g,phage.b)
                return True
        return False
    def foodCollision(self, food: FoodParticle):
        if (((food.x-self.x)**2 + (food.y- self.y)**2)**0.5) <= 12:
            self.energy += 2000
            return True
        else:
            return False

    def antibioticCollision(self, antb: Antibiotic):
        if (((antb.x - self.x) ** 2 + (antb.y - self.y) ** 2) ** 0.5) <= 20:
            if random.randint(0,100) >= self.a:
                return True
        return False
    def update(self):
        super().updatePos()
        self.energy -= (1.5 + self.a/100)

class Phage(Entity):
    def __init__(self, x, y, redline, redlineDrag, drag):
        super().__init__(x,y, redline, redlineDrag, drag)
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.energy = 1000
    def update(self):
        super().updatePos()
        self.energy -= random.randint(0,3)