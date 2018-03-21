import pygame,sys,random,math
from pygame.locals import *

FPS = 30
black,white,red,green,blue = (0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255)

def main():
    global fps_clock,display_surf,basic_font

    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((800,600),0,32)
    basic_font = pygame.font.Font('freesansbold.ttf',18)
    pygame.display.set_caption("Asteroids")
    display_surf.fill(black)
    runGame()
    again = input("Would you like to play again? ").title()
    while again != "Yes" and again != "No":
        print("That isn't a valid input.")
        again = input("Would you like to play again? ").title()
    if again == "Yes":
        main()
    else:
        print("Thanks for playing!")
        pygame.quit()
        sys.exit()
    

def runGame():
    asteroid_img_list = [pygame.image.load('asteroid.png'),pygame.image.load('asteroid1.png'),pygame.image.load('asteroid2.png')]
    userShip = {'x':400,'y':300,'degrees':90,'speed':0}
    createShip(userShip)
    turn_left = False
    turn_right = False
    move_up = False
    fire = False
    bullet_list = []
    asteroid_list = []
    bullet_countdown = 0
    lives = 3
    score = 0
    invulnerability_timer = 0
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif game_over:
                return
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    turn_left = True
                if event.key == K_RIGHT:
                    turn_right = True
                if event.key == K_UP:
                    move_up = True
                if event.key == K_SPACE:
                    fire = True
            elif event.type == KEYUP:
                if event.key == K_UP:
                    move_up = False
                if event.key == K_LEFT:
                    turn_left = None
                if event.key == K_RIGHT:
                    turn_right = None
                if event.key == K_SPACE:
                    fire = False
        if turn_left:
            userShip['degrees'] -= 5
        elif turn_right:
            userShip['degrees'] += 5
        if move_up:
            if userShip['speed'] > -16:
                userShip['speed']-=0.25
        elif not move_up:
            if userShip['speed'] < 0:
                userShip['speed'] +=0.25
        userShip['x'] = userShip['speed'] * math.cos(math.radians(userShip['degrees']))+userShip['x']
        userShip['y'] = userShip['speed'] * math.cos(math.radians(90-userShip['degrees']))+userShip['y']
        display_surf.fill(black)
        if fire and bullet_countdown == 0:
            fireBullet(userShip,bullet_list)
            bullet_countdown = 20
        if bullet_countdown > 0:
            bullet_countdown -= 1
        createAsteroids(asteroid_img_list,asteroid_list)
        moveAsteroids(asteroid_list)
        shiftPosition(userShip)
        trackBullets(bullet_list)
        createShip(userShip)
        score = asteroidHit(asteroid_list,asteroid_img_list,bullet_list,score)
        if shipHit(asteroid_list,asteroid_img_list,userShip) and invulnerability_timer == 0:
            userShip = {'x':400,'y':300,'degrees':90,'speed':0}
            lives -= 1
            invulnerability_timer = 70
        if invulnerability_timer > 0:
            invulnerability_timer -= 1
            if invulnerability_timer %10 <= 5:
                pygame.draw.rect(display_surf,black,getCollisionBox(userShip))
        showLives(lives)
        showScore(score)
        if lives == 0:
            gameOverShow()
            game_over = True
        pygame.display.update()
        fps_clock.tick(FPS)

def createShip(userShip):
    #draws left line
    left_x = userShip['x'] + math.cos(math.radians(userShip['degrees']+25)) * 34
    left_y = userShip['y'] + math.sin(math.radians(userShip['degrees']+25)) * 34
    pygame.draw.line(display_surf,white,(userShip['x'],userShip['y']),(left_x,left_y),1)
    #draws right line
    right_x = userShip['x'] + math.cos(math.radians(userShip['degrees']-25)) * 34
    right_y = userShip['y'] + math.sin(math.radians(userShip['degrees']-25)) * 34
    pygame.draw.line(display_surf,white,(userShip['x'],userShip['y']),(right_x,right_y),1)
    #draws bot line
    pygame.draw.line(display_surf,white,(left_x,left_y),(right_x,right_y))

def fireBullet(userShip,bullet_list):
    bul_x = userShip['x']
    bul_y = userShip['y']
    bul_deg = userShip['degrees']
    bullet = {'x':bul_x,'y':bul_y,'speed':15,'degrees':bul_deg,'life':0}
    bullet_list.append(bullet)

def trackBullets(bullet_list):
    for bullet in bullet_list:
        bullet['x'] = bullet['speed'] * math.cos(math.radians(180 - bullet['degrees']))+bullet['x']
        bullet['y'] = bullet['speed'] * math.cos(math.radians(270 - bullet['degrees']))+bullet['y']
        pygame.draw.rect(display_surf,white,(bullet['x'],bullet['y'],2,5))
        shiftPosition(bullet)
        bullet['life'] += 1
        if bullet['life'] >= 50:
            bullet_list.remove(bullet)

def shiftPosition(thing):
    if thing['x'] < -25:
        thing['x'] = 825
    elif thing['x'] > 825:
        thing['x'] = -25
    elif thing['y'] < 0:
        thing['y'] = 625
    elif thing['y'] > 625:
        thing['y'] = 0

def showLives(lives):
    lives_show = basic_font.render('LIVES: {0}'.format(lives),True,white)
    lives_show_rect = lives_show.get_rect()
    lives_show_rect.midtop = (725,25)
    display_surf.blit(lives_show,lives_show_rect)

def showScore(score):
    score_show = basic_font.render('SCORE: {0}'.format(score),True,white)
    score_show_rect = score_show.get_rect()
    score_show_rect.midtop = (75,25)
    display_surf.blit(score_show,score_show_rect)

def getCollisionBox(userShip):
    if userShip['degrees'] > 360:
        userShip['degrees'] -= 360
    if userShip['degrees'] < 0:
        userShip['degrees'] += 360
    if userShip['degrees'] < 65 and userShip['degrees'] >= 25:
        user_box = pygame.Rect(userShip['x'],userShip['y'],35,35)
    elif userShip['degrees'] >= 65 and userShip['degrees'] < 105:
        user_box = pygame.Rect(userShip['x']-15,userShip['y'],35,35)
    elif userShip['degrees'] >= 105 and userShip['degrees'] < 155:
        user_box = pygame.Rect(userShip['x']-30,userShip['y'],35,35)
    elif userShip['degrees'] >= 155 and userShip['degrees'] < 205:
        user_box = pygame.Rect(userShip['x']-30,userShip['y']-15,35,35)
    elif userShip['degrees'] >= 205 and userShip['degrees'] < 245:
        user_box = pygame.Rect(userShip['x']-30,userShip['y']-30,35,35)
    elif userShip['degrees'] >= 245 and userShip['degrees'] < 295:
        user_box = pygame.Rect(userShip['x']-15,userShip['y']-30,35,35)
    elif userShip['degrees'] >= 295 and userShip['degrees'] < 345:
        user_box = pygame.Rect(userShip['x'],userShip['y']-30,35,35)
    elif (userShip['degrees'] >= 345 and userShip['degrees'] <= 360) or (userShip['degrees'] >= 0 and userShip['degrees'] < 25):
        user_box = pygame.Rect(userShip['x'],userShip['y']-15,35,35)
    return user_box

def getBulletBox(bullet):
    bullet_box = pygame.Rect(bullet['x'],bullet['y'],2,5)
    pygame.draw.rect(display_surf,green,bullet_box)
    return bullet_box

def createAsteroids(asteroid_img_list,asteroid_list):
    if len(asteroid_list) < 5:
        chosen_asteroid = asteroid_img_list[random.randint(0,2)]
        asteroidCoords = {'x':random.randint(0,800),'y':random.randint(0,600),'upDown':random.randint(-5,5),'leftRight':random.randint(-5,5),'picture':chosen_asteroid}
        display_surf.blit(chosen_asteroid,(asteroidCoords['x'],asteroidCoords['y']))
        asteroid_list.append(asteroidCoords)

def moveAsteroids(asteroid_list):
    for asteroid in asteroid_list:
        asteroid['y'] += asteroid['upDown']
        asteroid['x'] += asteroid['leftRight']
        shiftPosition(asteroid)
        display_surf.blit(asteroid['picture'],(asteroid['x'],asteroid['y']))

def getAsteroidBox(asteroid, asteroid_img_list):
    if asteroid['picture'] == asteroid_img_list[0]:           
        asteroid['rect'] = pygame.Rect(asteroid['x']+50,asteroid['y']+25,60,80)
    elif asteroid['picture'] == asteroid_img_list[1]:
        asteroid['rect'] = pygame.Rect(asteroid['x'],asteroid['y']+10,80,50)
    elif asteroid['picture'] == asteroid_img_list[2]:
        asteroid['rect'] = pygame.Rect(asteroid['x']+15,asteroid['y']+10,60,70)
    return asteroid['rect']

def asteroidHit(asteroid_list,asteroid_img_list,bullet_list,score):
    for asteroid in asteroid_list:
        asteroid['rect'] = getAsteroidBox(asteroid,asteroid_img_list)
        for bullet in bullet_list:
            bullet_rect = getBulletBox(bullet)
            if bullet_rect.colliderect(asteroid['rect']):
                asteroid_list.remove(asteroid)
                bullet_list.remove(bullet)
                score += 50
    return score

def shipHit(asteroid_list,asteroid_img_list,userShip):
    for asteroid in asteroid_list:
        asteroid['rect'] = getAsteroidBox(asteroid,asteroid_img_list)
        ship_box = getCollisionBox(userShip)
        if asteroid['rect'].colliderect(ship_box):
            asteroid_list.remove(asteroid)
            return True
    return False

def gameOverShow():
    game_over = basic_font.render('Game Over', True, green)
    game_over_rect = game_over.get_rect()
    game_over_rect.midtop = (350,400)
    display_surf.blit(game_over,game_over_rect)
    
        
        
        
        
        
    
    

if __name__ == '__main__':
    main()
