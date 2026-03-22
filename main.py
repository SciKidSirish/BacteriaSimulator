import pygame
import sys
from mechanics import *
import random
# --- Config ---
WIDTH, HEIGHT = 2000, 1000
FPS = 60

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Window")
clock = pygame.time.Clock()
#bacteria = Entity(WIDTH //2, HEIGHT // 2, 5, 0.8, 0.3 )

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Game State ---
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
bacteriaList = [Bacteria(random.randint(0, WIDTH), random.randint(0, HEIGHT), 5, 0.8, 0.3 )]
phageList = [Phage(random.randint(0, WIDTH), random.randint(0, HEIGHT), 20, 0.8, 0.2 )]
foodList = []
antbList = []
for i in range(50):
    foodList.append(FoodParticle(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

# --- Functions ---
def update():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        bacteriaList.append(Bacteria(random.randint(0, WIDTH), random.randint(0, HEIGHT), 5, 0.8, 0.3 ))
    if keys[pygame.K_s]:
        if len(bacteriaList) > 1:
            bacteriaList.pop(0)
    if keys[pygame.K_d]:
        phageList.append(Phage(random.randint(0, WIDTH), random.randint(0, HEIGHT), 20, 0.8, 0.2 ))
    if keys[pygame.K_f] or (random.randint(0,20) == 0):
        foodList.append(FoodParticle(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    if keys[pygame.K_p]:
        antbList.append(Antibiotic(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    if keys[pygame.K_a]:
        if len(phageList) > 1:
            phageList.pop(0)
    if keys[pygame.K_v]:
        if len(foodList) > 1:
            foodList.pop(0)
    if keys[pygame.K_l]:
        if len(antbList) > 1:
            antbList.pop(0)
    cntrBacr = 0
    sumA = 0
    for bacteria in bacteriaList:
        sumA += bacteria.a
        for j in range(0, len(foodList)):
            if bacteria.foodCollision(foodList[j]):
                foodList.pop(j)
                break
        for j in range(0, len(phageList)):
            if bacteria.phageCollision(phageList[j]):
                phageList.pop(j)
                break
        bacteria.update()
        antbd = False
        for j in range(0, len(antbList)):
            if bacteria.antibioticCollision(antbList[j]):
                antbList.pop(j)
                antbd = True
                break
        if bacteriaList[cntrBacr].energy <= 0 or antbd:
            bacteriaList.pop(cntrBacr)
        else:
            cntrBacr += 1
    for bacteria in bacteriaList:
        if bacteria.energy +random.randint(0,1000) >= 7500:
            childBact = Bacteria(bacteria.x, bacteria.y, 5, 0.8, 0.3 )
            childBact.a = max(0, min(100,bacteria.a + random.randint(-70,70)))
            childBact.r = max(0, min(255,bacteria.r + random.randint(-70,70)))
            childBact.g = max(0, min(255,bacteria.g + random.randint(-70, 70)))
            childBact.b = max(0, min(255,bacteria.b + random.randint(-70, 70)))
            bacteria.energy -= 500

            bacteriaList.append(childBact)
            print("daughter bacterium made")
        if bacteria.infected:
            for k in range(3):
                tempPhage= Phage(bacteria.x, bacteria.y, 20, 0.8, 0.2 )
                tempPhage.r = max(0, min(255, bacteria.phageData[0] + random.randint(-20, 20)))
                tempPhage.g = max(0, min(255, bacteria.phageData[1] + random.randint(-20, 20)))
                tempPhage.b = max(0, min(255, bacteria.phageData[2] + random.randint(-20, 20)))
                phageList.append(tempPhage)
            bacteria.energy = -1000
    cntr =0
    for phage in phageList:
        if phage.energy <=0:
            phageList.pop(cntr)
        else:
            cntr +=1

    try:
        print(f"resistance: {sumA//len(bacteriaList)} bacteria: {len(bacteriaList)} phages: {len(phageList)} antibiotics: {len(antbList)} food: {len(foodList)}")
    except ZeroDivisionError:
        print("no bacteria")


    for phage in phageList:
        phage.update()
    for food in foodList:
        food.updatePos()
    for antb in antbList:
        antb.updatePos()


def draw():
    screen.fill(BLACK)
    for bacteria in bacteriaList:
        pygame.draw.circle(screen, (bacteria.r, bacteria.g, bacteria.b), (bacteria.x, bacteria.y), 6.0)
    for phage in phageList:
        pygame.draw.rect(screen, (phage.r, phage.g, phage.b), (phage.x, phage.y, 5,5))
    for food in foodList:
        pygame.draw.circle(screen, WHITE, (food.x, food.y), 3.0)
    for antb in antbList:
        pygame.draw.circle(screen, (255,0,0), (antb.x, antb.y), 3.0)
    pygame.display.flip()


# --- Main Loop ---
def main():
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # delta time (seconds)
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # --- Update ---
        update()
        # --- Draw ---
        draw()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()