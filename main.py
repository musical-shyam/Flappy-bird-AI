import pygame
import os
from sys import exit
import gamereqs
import population

pygame.init() # Initializes Pygame(set up the display, etc.)
clock = pygame.time.Clock() # Creates a clock object to control the frame rate
population = population.Population(100) # Creates a population of 100 players
font = pygame.font.Font('Roboto-Regular.ttf', 30)

def generate_pipes(): # Adds a new pipe to the list of pipes depending on the window width
    gamereqs.pipes.append(gamereqs.Pipes(gamereqs.WINDOW_WIDTH))
    
def quit_game(): # Quits the game properly if the user closes the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
def main():
    generationCount = 0
    pipes_spawn_time = 10 # Time between each pipe spawn
    while True:
        # Checks if the user has closed the window
        quit_game() 
        
        # Fills the window with a white background
        gamereqs.window.fill((255, 255, 255))
        
        # Spawns the ground
        gamereqs.ground.draw(gamereqs.window)
        
        # Spawns the pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1
        
        # Generation count output
        gen_count_label = font.render("Generation: " + str(generationCount),1,(0,0,0))
        gamereqs.window.blit(gen_count_label, (10, 510))


        for i in gamereqs.pipes:
            i.draw(gamereqs.window) # Draws the pipe on the window
            i.update() # Updates the pipe's position
            if i.off_screen: # Removes the pipe from the list if it is off the window
                gamereqs.pipes.remove(i)
                
        if not population.extinct(): # Checks if the population is extinct
            population.update_live_players() # Updates the live players
        else:
            gamereqs.pipes.clear()
            population.natural_selection() # Starts the natural selection process
            generationCount += 1

        clock.tick(60) # Sets the frame rate to 60 frames per second
        pygame.display.flip() # Updates the display 

main() # Calls the main function to start the game