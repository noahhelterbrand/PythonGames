import pygame,sys,random
from pygame.locals import *


##IDEAS TO GET TO LATER:
#Have ball start at different position each time
#Change all variables with AI to player2 to make less confusing
#EASY/MEDIUM/HARD settings, that change the FPS.
#Custom win score.

FPS = 120
black,white,red,green,blue = (0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255)
def main():
    #creates fps counter, surface of entire game, and imports a font
    global fps_clock, display_surf,basic_font

    pygame.init()
    fps_clock = pygame.time.Clock()
    #sets display window to x = 500, y = 400
    display_surf = pygame.display.set_mode((500,400),0,32)
    #sets that font
    basic_font = pygame.font.Font('freesansbold.ttf',18)
    #Titles window
    pygame.display.set_caption("Pong")
    display_surf.fill(white)
    while True:
        #runs the game
        runGame()

def runGame():
    #holds up-down direction of the paddle
    direction = "None"
    AI_direction = "None"
    #creates coords and ball direction for paddles and ball
    paddleCoords = {'x':5,'y':175}
    AICoords = {'x':485, 'y':175}
    ballCoords = {'x':250,'y':200,'upDown':-2,'leftRight':5}
    #holds score
    player_score = 0
    AI_score = 0
    while True:
        for event in pygame.event.get():
            #checks if the user pressed the x in the top of the window
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #checks if a button was pressed
            if event.type == KEYDOWN:
                #sets the player direction to up
                if event.key == K_w:
                    direction = "up"
                #sets the player direction to down
                elif event.key == K_s:
                    direction = "down"
                #closes the game
                elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.key == K_UP:
                    AI_direction = "up"
                elif event.key == K_DOWN:
                    AI_direction = "down"
                if game_over and event.key == K_r:
                    return
            #checks if the key isn't pressed anymore
            if event.type == KEYUP:
                #resets player 2 direction to nothing
                if event.key == K_UP or event.key == K_DOWN:
                    AI_direction = "None"
                #resets player direction to nothing
                elif event.key == K_w or event.key == K_s:
                    direction = "None"
        #checks if the paddles hit boundries
        paddleCoords,AICoords,AI_direction,direction = checkBounds(paddleCoords,AICoords,AI_direction,direction)
        
        #moves player up or down
        if direction == "up":
            paddleCoords = {'x':paddleCoords['x'],'y':paddleCoords['y']-5}
        elif direction == "down":
            paddleCoords = {'x':paddleCoords['x'],'y':paddleCoords['y']+5}
        #moves player 2 up or down
        if AI_direction == "up":
            AICoords = {'x':AICoords['x'], 'y':AICoords['y'] - 5}
        elif AI_direction == "down":
            AICoords = {'x':AICoords['x'], 'y':AICoords['y'] + 5}

        #every frame, fills entire screen white, effectively erasing all movements
        display_surf.fill(white)
        #draws the line halfway down the game
        drawHalf()
        #Draws the player 1 and player 2 paddles
        drawPaddle(paddleCoords)
        drawPaddle(AICoords)
        #draws the ball movement, detecting whether it hit a paddle of a wall
        ballCoords,AI_score,player_score = drawBall(ballCoords,AICoords,paddleCoords,player_score,AI_score)
        #updates the score
        drawScore(player_score,AI_score)
        #game_over will become true is one of the scores reach 10
        game_over = checkScore(player_score,AI_score)
        #Updates all movement
        pygame.display.update()
        #goes onto next frame
        fps_clock.tick(FPS)

#makes sure paddles dont go off screen
def checkBounds(paddleCoords,AICoords,AI_direction,direction):
    if paddleCoords['y'] == 0:
        direction = "None"
        paddleCoords = {'x':5,'y':5}
    elif paddleCoords['y'] == 350:
        direction = "None"
        paddleCoords = {'x':5,'y':345}
    if AICoords['y'] == 0:
        AI_direction = "None"
        AICoords = {'x':485,'y':5}
    elif AICoords['y'] == 350:
        AI_direction = "None"
        AICoords = {'x':485,'y':345}
    return paddleCoords,AICoords,AI_direction,direction
    
#draws a paddle
def drawPaddle(paddleCoords):
    x = paddleCoords['x']
    y = paddleCoords['y']
    pygame.draw.rect(display_surf,black,(x,y,10,50))

#draws the line halfway down the screen
def drawHalf():
    pygame.draw.rect(display_surf,black,(249,0,2,400))


def drawAI(AI_direction,AICoords):
    if AICoords['y'] == 0:
        AI_direction = "down"
    elif AICoords['y'] == 200:
        AI_direction = "up"
    if AI_direction == "up":
        AICoords = {'x':AICoords['x'],'y':AICoords['y']-5}
    elif AI_direction == "down":
        AICoords = {'x':AICoords['x'],'y':AICoords['y']+5}

        
    AI_paddle = pygame.Rect(AICoords['x'],AICoords['y'],10,200)
    pygame.draw.rect(display_surf,black,AI_paddle)
    return AI_direction,AICoords

def drawBall(ballCoords,AICoords,paddleCoords,player_score,AI_score):
    #Check for bottom and top, make bounce
    if ballCoords['y'] <= 0 or ballCoords['y'] >= 400:
        ballCoords['upDown'] = ballCoords['upDown'] * -1
    #checks if hit AI paddle
    elif ballCoords['x']+10 >= 485 and ballCoords['x']+10 <= 500:
        if ballCoords['y'] >= AICoords['y'] and ballCoords['y'] <= AICoords['y']+50:
            ballCoords['leftRight'] = ballCoords['leftRight'] *-1
            #changes up down left right variables depending on where the paddle
            #they hit
            if ballCoords['y'] <= AICoords['y']+12:
                ballCoords['leftRight'] = -4
                ballCoords['upDown'] = -3
            elif ballCoords['y'] >= AICoords['y'] + 13 and ballCoords['y'] <= AICoords['y'] + 25:
                ballCoords['leftRight'] = -5
                ballCoords['upDown'] = -1
            elif ballCoords['y'] >= AICoords['y'] + 26 and ballCoords['y'] <= AICoords['y'] + 37:
                ballCoords['leftRight'] = -5
                ballCoords['upDown'] = 1
            elif ballCoords['y'] >= AICoords['y'] + 38 and ballCoords['y'] <= AICoords['y'] + 50:
                ballCoords['leftRight'] = -4
                ballCoords['upDown'] = 3
        else:
            player_score = player_score + 1
            ballCoords = {'x':250,'y':200,'upDown':-2,'leftRight':4}
    #checks if player hit it
    elif ballCoords['x'] >= -5 and ballCoords['x'] <= 10:
        if ballCoords['y'] >= paddleCoords['y'] and ballCoords['y'] <= paddleCoords['y']+50:
            ballCoords['leftRight'] = ballCoords['leftRight'] *-1
            if ballCoords['y'] <= paddleCoords['y']+12:
                ballCoords['leftRight'] = 4
                ballCoords['upDown'] = -3
            elif ballCoords['y'] >= paddleCoords['y'] + 13 and ballCoords['y'] <= paddleCoords['y'] + 25:
                ballCoords['leftRight'] = 5
                ballCoords['upDown'] = -1
            elif ballCoords['y'] >= paddleCoords['y'] + 26 and ballCoords['y'] <= paddleCoords['y'] + 37:
                ballCoords['leftRight'] = 5
                ballCoords['upDown'] = 1
            elif ballCoords['y'] >= paddleCoords['y'] + 38 and ballCoords['y'] <= paddleCoords['y'] + 50:
                ballCoords['leftRight'] = 4
                ballCoords['upDown'] = 3
        else:
            AI_score = AI_score + 1
            ballCoords = {'x':250,'y':200,'upDown':-2,'leftRight':-4}
    ballCoords['x'] = ballCoords['x'] + ballCoords['leftRight']
    ballCoords['y'] = ballCoords['y'] + ballCoords['upDown']
    pygame.draw.rect(display_surf, black, (ballCoords['x'],ballCoords['y'],10,10))
    return ballCoords,AI_score,player_score

def drawScore(player_score,AI_score):
    player_score_show = basic_font.render('Player 1 Score: {0}'.format(player_score),True,blue)
    player_score_rect = player_score_show.get_rect()
    player_score_rect.topleft = (50,10)
    display_surf.blit(player_score_show,player_score_rect)
    AI_score_show = basic_font.render('Player 2 Score: {0}'.format(AI_score),True,blue)
    AI_score_rect = AI_score_show.get_rect()
    AI_score_rect.topright = (450,10)
    display_surf.blit(AI_score_show,AI_score_rect)

def checkScore(player_score,AI_score):
    game_over = basic_font.render('Game Over',True,black)
    game_over_rect = game_over.get_rect()
    game_over_rect.midtop = (250,150)
    player_won = basic_font.render('Player 1 Wins!(r to restart)',True,black)
    player_won_rect = player_won.get_rect()
    player_won_rect.midtop = (250,200)
    AI_won = basic_font.render('Player 2 Wins!(r to restart)',True,black)
    AI_won_rect = AI_won.get_rect()
    AI_won_rect.midtop = (250,200)
    if player_score >= 10:
        display_surf.blit(game_over,game_over_rect)
        display_surf.blit(player_won,player_won_rect)
    elif AI_score >= 10:
        display_surf.blit(game_over,game_over_rect)
        display_surf.blit(AI_won,AI_won_rect)
    if player_score >= 10 or AI_score >= 10:
        return True
    return False
        

if __name__ == '__main__':
    main()
