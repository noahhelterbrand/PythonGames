import pygame,sys,random,time
from pygame.locals import *

#IDEAS TO GET TO LATER:
#add points based on type of alien killed
#Add sound
#Aliens over barrier test by moving stuff around in main(barrier functions before alien
#move functions)
#Figure out how to restart the game by pressing r and also pause everything?
FPS = 30
black,white,red,green,blue = (0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255)

def main():
    global fps_clock, display_surf,basic_font

    pygame.init()
    #creates fps, display, and font
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((700,700),0,32)
    basic_font = pygame.font.Font('freesansbold.ttf',25)
    pygame.display.set_caption("Space Invaders")
    display_surf.fill(black)
    #runs space invaders
    runGame()
    #Asks if they want to play again
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
    #load all aliens and ships
    userImg = pygame.image.load('realHero.png')
    firstInvImg = pygame.image.load('smallInvader3.png')
    secondInvImg = pygame.image.load('medInvader.png')
    thirdInvImg = pygame.image.load('largeInvader.png')
    alien_images = [firstInvImg,secondInvImg,thirdInvImg]
    #start coords for ship
    startx,starty = 360,660
    userCoords = {'x':startx,'y':starty}
    #coords for each alien position in a row
    firstAlien = {'x':0,'y':100}
    secondAlien = {'x':0,'y':150}
    thirdAlien = {'x':0,'y':250}
    alienCoords = [firstAlien,secondAlien,thirdAlien]
    #initial direction of the ship
    direction = "None"
    bullet_fire = False
    #holds the position of each list
    bullet_list = []
    countdown = 0
    #create all the aliens o the screen
    first_aliens,second_aliens,third_aliens = drawAliens(alien_images,alienCoords)
    all_aliens = [first_aliens,second_aliens,third_aliens]
    #creates barriers
    barrier_list = createBarriers()
    alien_move_counter = 0
    #sets initial alien direction
    alien_direction = "right"
    move_down = False
    alien_bullets = []
    invulnerability_timer = 70
    lives = 3
    game_over = False
    score = 0
    while True:
        display_surf.fill(black)
        if game_over:
            return
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    direction = "left"
                elif event.key == K_RIGHT or event.key == K_d:
                    direction = "right"
                elif event.key == K_SPACE:
                    bullet_fire = True
            elif event.type == KEYUP:
                if event.key in (K_LEFT,K_a,K_RIGHT,K_d):
                    direction = "None"
                elif event.key == K_SPACE:
                    bullet_fire = False

        if bullet_fire and countdown == 0:
            bullet = {'x':userCoords['x']+25,'y':680}
            bullet_list.append(bullet)
            #Creates countdown
            countdown = 20
        for bullet in bullet_list:
            if bullet['y'] <= 0:
                bullet_list.remove(bullet)
            else:
                bullet['y'] -= 10
                pygame.draw.rect(display_surf,white,(bullet['x'],bullet['y'],5,10))
        if userCoords['x'] == -10:
            direction = "None"
            userCoords['x'] += 5
        elif userCoords['x'] == 650:
            direction = "None"
            userCoords['x'] -= 5
        if direction == "left":
            userCoords = {'x':userCoords['x'] - 5, 'y': userCoords['y']}
        elif direction == "right":
            userCoords = {'x':userCoords['x'] + 5, 'y': userCoords['y']}
        if countdown != 0:
            countdown -= 1

        display_surf.blit(userImg,(userCoords['x'],userCoords['y']))
        userRect = pygame.Rect(userCoords['x']+8,userCoords['y']+10,40,30)
        barrier_list = drawBarriers(barrier_list)
        alien_move_counter,alien_direction,move_down = moveAliens(all_aliens,alien_images,alien_move_counter,alien_direction,move_down)
        alien_bullets = alienFire(all_aliens,alien_bullets)
        if shipCollision(alien_bullets,userRect) and invulnerability_timer > 45:
            userCoords = {'x':startx,'y':starty}
            invulnerability_timer = 0
            lives -= 1
        if invulnerability_timer < 50:
            invulnerability_timer = invulnerability_timer + 1
            if invulnerability_timer %10 <= 5:
                pygame.draw.rect(display_surf,black,userRect)
        score = alienCollision(bullet_list,all_aliens,score)
        drawLives(lives)
        barrierCollision(barrier_list,bullet_list,alien_bullets)
        barrierHealth(barrier_list)
        checkHealth(barrier_list)
        drawScore(score)
        game_over = gameOver(lives,all_aliens)
        pygame.display.update()
        fps_clock.tick(FPS)

def drawAliens(alien_images,alienCoords):
    first_aliens = []
    second_aliens = []
    third_aliens = []
    #draws top aliens
    for i in range(11):
        #seperating so that the numbers become constant
        x = alienCoords[0]['x']
        y = alienCoords[0]['y']
        x2 = alienCoords[1]['x']
        y2 = alienCoords[1]['y']
        x3 = alienCoords[2]['x']
        y3 = alienCoords[2]['y']
        first_aliens.append({'x':x,'y':y})
        second_aliens.append({'x':x2,'y':y2})
        third_aliens.append({'x':x3,'y':y3})
        display_surf.blit(alien_images[0],(alienCoords[0]['x'],alienCoords[0]['y']))
        display_surf.blit(alien_images[1],(alienCoords[1]['x'],alienCoords[1]['y']))
        display_surf.blit(alien_images[2],(alienCoords[2]['x'],alienCoords[2]['y']))
        alienCoords[0]['x'] += 50
        alienCoords[1]['x'] += 50
        alienCoords[2]['x'] += 50
    #reset x coords
    for i in range(3):
        alienCoords[i]['x'] = 0
    alienCoords[1]['y'] += 50
    alienCoords[2]['y'] += 50
    #if aliens have secondary row, draws those
    for i in range(11):
        x2 = alienCoords[1]['x']
        y2 = alienCoords[1]['y']
        x3 = alienCoords[2]['x']
        y3 = alienCoords[2]['y']
        second_aliens.append({'x':x2,'y':y2})
        third_aliens.append({'x':x3,'y':y3})
        display_surf.blit(alien_images[1],(alienCoords[1]['x'],alienCoords[1]['y']))
        display_surf.blit(alien_images[2],(alienCoords[2]['x'],alienCoords[2]['y']))
        alienCoords[1]['x'] += 50
        alienCoords[2]['x'] += 50
    #resets coords
    for i in range(2):
        alienCoords[i+1]['x'] = 0
        alienCoords[i+1]['y'] -= 50
    return first_aliens,second_aliens,third_aliens

def moveAliens(all_aliens,alien_images,alien_move_counter,alien_direction,move_down):
    if alien_move_counter == 25:
        alien_move_counter = 0
        for aliens in all_aliens:
            for alien in aliens:
                if move_down:
                    alien['y'] += 50
                if alien_direction == "right":
                    alien['x'] += 10
                elif alien_direction == "left":
                    alien['x'] -= 10
        move_down = False
        for alien in all_aliens[0]:
                if alien['x'] >=650:
                    alien_direction = "left"
                    move_down = True
                elif alien['x'] <= 0:
                    alien_direction = "right"
                    move_down = True
    for alien in all_aliens[0]:
        display_surf.blit(alien_images[0],(alien['x'],alien['y']))
    for alien in all_aliens[1]:
        display_surf.blit(alien_images[1],(alien['x'],alien['y']))
    for alien in all_aliens[2]:
        display_surf.blit(alien_images[2],(alien['x'],alien['y']))
    alien_move_counter = alien_move_counter + 1
    return alien_move_counter,alien_direction,move_down

def alienFire(all_aliens,alien_bullets):
    for aliens in all_aliens:
        for alien in aliens:
            #10% chance alien fires
            x = random.randint(1,2500)
            if x == 5:
                bullet = {'x':alien['x']+25,'y':alien['y']+30}
                alien_bullets.append(bullet)
    for bullet in alien_bullets:
        if bullet['y'] >= 700:
            alien_bullets.remove(bullet)
        else:
            bullet['y'] += 10
            pygame.draw.rect(display_surf,white,(bullet['x'],bullet['y'],5,10))
    return alien_bullets

def shipCollision(alien_bullets,userRect):
    for bullet in alien_bullets:
        bullet_rect = pygame.Rect(bullet['x'],bullet['y'],5,10)
        if bullet_rect.colliderect(userRect):
            return True
    return False

def alienCollision(bullet_list,all_aliens,score):
    for aliens in all_aliens:
        for alien in aliens:
            alien_rect = pygame.Rect(alien['x'],alien['y'],45,45)
            for bullet in bullet_list:
                bullet_rect = pygame.Rect(bullet['x'],bullet['y'],5,10)
                if bullet_rect.colliderect(alien_rect):
                    if alien in all_aliens[2]:
                        score +=10
                    elif alien in all_aliens[1]:
                        score += 20
                    elif alien in all_aliens[0]:
                        score += 40
                    aliens.remove(alien)
                    bullet_list.remove(bullet)
    return score

def drawLives(lives):

    live_text = basic_font.render('LIVES: {0}'.format(lives),True,white)
    live_text_rect = live_text.get_rect()
    live_text_rect.midtop = (625,25)
    display_surf.blit(live_text,live_text_rect)

def createBarriers():
    barrier_list = []
    barrier_left = {'x':50,'y':575,"w":25,"h":50}
    barrier_right = {'x':125,'y':575,"w":25,"h":50}
    barrier_top = {'x':75,'y':575,"w":50,"h":25}
    health_show = 100
    for i in range(4):
        l_x = barrier_left['x']
        l_y = barrier_left['y']
        l_w = barrier_left['w']
        l_h = barrier_left['h']
        t_x = barrier_top['x']
        t_y = barrier_top['y']
        t_w = barrier_top['w']
        t_h = barrier_top['h']
        r_x = barrier_right['x']
        r_y = barrier_right['y']
        r_w = barrier_right['w']
        r_h = barrier_right['h']
        barrier_list.append([{'x':l_x,'y':l_y,'w':l_w,'h':l_h},{'x':t_x,'y':t_y,'w':t_w,'h':t_h},{'x':r_x,'y':r_y,'w':r_w,'h':r_h},{'health':15,'health_show':health_show}])
        health_show += 150
        barrier_left['x'] += 150
        barrier_right['x'] += 150
        barrier_top['x'] += 150
    barrier_left['x'] = 50
    barrier_right['x'] = 125
    barrier_top['x'] = 75
    return barrier_list

def drawBarriers(barrier_list):
    for barrier_pieces in barrier_list:
        for barrier_piece in barrier_pieces[:3]:
            barrier_part = pygame.Rect(barrier_piece['x'],barrier_piece['y'],barrier_piece['w'],barrier_piece['h'])
            pygame.draw.rect(display_surf,green,barrier_part)
    return barrier_list

def barrierCollision(barrier_list,bullet_list,alien_bullets):
    for barrier in barrier_list:
        for barrier_part in barrier[:3]:
            barrier_rect = pygame.Rect(barrier_part['x'],barrier_part['y'],barrier_part['w'],barrier_part['h'])
            for bullet in bullet_list:
                bullet_rect = pygame.Rect(bullet['x'],bullet['y'],5,10)
                if bullet_rect.colliderect(barrier_rect):
                    bullet_list.remove(bullet)
                    barrier[-1]['health'] -= 1
            for bullet in alien_bullets:
                bullet_rect = pygame.Rect(bullet['x'],bullet['y'],5,10)
                if bullet_rect.colliderect(barrier_rect):
                    alien_bullets.remove(bullet)
                    barrier[-1]['health'] -= 1


def barrierHealth(barrier_list):
    #shows barrier health
    for barrier_health in barrier_list:
        if barrier_health[-1]['health'] > 0:
            health_show = basic_font.render('{0}'.format(barrier_health[-1]['health']),True,blue)
            health_show_rect = health_show.get_rect()
            health_show_rect.midtop = (barrier_health[-1]['health_show'],575)
            display_surf.blit(health_show,health_show_rect)

def checkHealth(barrier_list):
    for barrier_health in barrier_list:
        if barrier_health[-1]['health'] <= 0:
            barrier_list.remove(barrier_health)

def drawScore(score):
    score_show = basic_font.render('SCORE: {0}'.format(score),True,white)
    score_show_rect = score_show.get_rect()
    score_show_rect.midtop = (75,25)
    display_surf.blit(score_show,score_show_rect)

def gameOver(lives,all_aliens):
    if lives == 0:
        game_over = basic_font.render('GAME OVER!',True,green)
        game_over_rect = game_over.get_rect()
        game_over_rect.midtop = (350,300)
        display_surf.blit(game_over,game_over_rect)
        return True
    elif all_aliens == [[],[],[]]:
        game_over = basic_font.render('YOU WIN!',True,green)
        game_over_rect = game_over.get_rect()
        game_over_rect.midtop = (350,300)
        display_surf.blit(game_over,game_over_rect)
        return True
    for aliens in all_aliens:
        for alien in aliens:
            if alien['y'] >= 675:
                game_over = basic_font.render('GAME OVER!',True,green)
                game_over_rect = game_over.get_rect()
                game_over_rect.midtop = (350,300)
                display_surf.blit(game_over,game_over_rect)
                return True
    return False

if __name__ == '__main__':
    main()
