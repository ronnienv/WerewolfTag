#! /usr/bin/env python

import os
import random
import pygame
import Player
import time

##############################

# randomly selects a player to be it at the start of the game
# the "it" player number is the random number + 1
def choose_it(players):
    it_player = random.randint(0, len(players)-1)
    players[it_player].becomes_it()

#############################

def select_winner(players):
    winner_score = 0
    winner_player = 0
    for player in players:
        if player.getScore > winner_score:
            winner_player = player
    
    return winner_player

############################

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Play Tag!")
screen = pygame.display.set_mode((640, 440))

mode = 0

borders = [pygame.Rect(0,0, 640, 1), pygame.Rect(0,0, 1, 440), pygame.Rect(639,0, 1, 440), pygame.Rect(0,439, 640, 1)]

players = []
player1 = Player.Player(100, 100, 1, players) # Create the player
player2 = Player.Player(200, 200, 2, players)
player3 = Player.Player(300, 300, 3, players)

myfont = pygame.font.SysFont("monospace", 16)

running = True
FRAMERATE = 60
clock = pygame.time.Clock()

controls = {pygame.K_LEFT : (-2,0, player1), pygame.K_RIGHT : (2,0, player1), pygame.K_UP : (0,-2, player1), pygame.K_DOWN : (0,2, player1)} # player 1 controls
controls.update({pygame.K_a : (-2,0, player2), pygame.K_d : (2,0, player2), pygame.K_w : (0,-2, player2), pygame.K_s : (0,2, player2)}) # player 2 controls
controls.update({pygame.K_b : (-2,0, player3), pygame.K_m : (2,0, player3), pygame.K_j : (0,-2, player3), pygame.K_n : (0,2, player3)})

############ MAIN GAME LOOP ##########################

choose_it(players)

while running:

    key = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    #start screen
    if mode == 0:
        title = myfont.render("Werewolf Tag", 1, (255,255,255))
        instructions = myfont.render("Press SPACE to Start", 1, (255,255,255))
        screen.blit(title, (240, 10))
        screen.blit(instructions, (210, 210))

        if key[pygame.K_SPACE]:
            mode = 1
            now = time.time()

    #actual game
    if mode == 1:
        time_up = now + 60
        if time.time() >= time_up:
            mode = 2

        clock.tick(FRAMERATE)
        
        # Move the player if an arrow key is pressed
        
        for pressed in controls:
            if key[pressed]:
                instruction = controls.get(pressed)
                moving_player = instruction[2]

                # used to know what instruction players are currently going to see if they can be pushed
                # instruction[2].current_dir = (instruction[0], instruction[1])

                #if the player has an attribute check if they can still move
                if len(moving_player.attributes) > 0:
                    for attribute in moving_player.attributes:
                        if attribute != "transforming":
                            moving_player.move(instruction[0], instruction[1], borders, players)
                else:
                    moving_player.move(instruction[0], instruction[1], borders, players)

        # Draw the scene
        screen.fill((0, 0, 0))

        #check to see if any player is still transforming
        for player in players:
            for attribute in player.attributes:
                if attribute == "transforming":
                    if time.time() >= player.transform_complete:
                        player.finish_transform()

                    #randomly tested modulo numbers were used for the animation
                    elif player.transform_counter %18 == 1:
                        player.color = (255, 255, 255)
                    elif player.transform_counter %6 == 1:
                        player.color = (255, 0, 0)

                    #counter used to determine which transformation animation should be shown
                    player.transform_counter += 1

            player.draw_player(screen)
       
        disclaimertext = myfont.render("Player 1 score: {0}".format(player1.getScore()) , 1, (255,255,255))
        disclaimertext2 = myfont.render("Player 2 score: {0}".format(player2.getScore()) , 1, (255,255,255))
        disclaimertext4 = myfont.render("Player 3 score: {0}".format(player3.getScore()) , 1, (255,255,255))
        disclaimertext3 = myfont.render("Time left: {0}".format(round(time_up-time.time(), 2)) , 1, (255,255,255))
        screen.blit(disclaimertext, (16, 400))
        screen.blit(disclaimertext2, (16, 410))
        screen.blit(disclaimertext4, (16, 420))
        screen.blit(disclaimertext3, (200, 10))

    #once the time is up!
    if mode == 2:
        backgroundColor = (0,0,0)
        screen.fill(backgroundColor)

        time_up = myfont.render("Time's Up!", 1, (255,255,255))
        winner = select_winner(players)
        winner_text = myfont.render("The winner is: Player " + str(winner.playerNumber), 1, (255,255,255))
        restart_text = myfont.render("Press Space to Restart", 1, (255,255,255))

        screen.blit(time_up, (240, 10))
        screen.blit(winner_text, (210, 210))
        screen.blit(restart_text, (210, 220))

        if key[pygame.K_SPACE]:
            mode = 1
            now = time.time()

    pygame.display.flip()
    
