#setup
import tkinter as tk #importing tkinter with the abbreviation tk for convinience
from tkinter import ttk #classes for themed widgets
import ttkbootstrap as ttkb #more useful tkinter
import pygame #puts the physics on the screen
import sys #system specific parameters
import pymunk #does the physics
import pymunk.pygame_util #draw pymunk objects in pygame
from pymunk.vec2d import Vec2d #vectors
from typing import List #for lists/arrays


#main code

#setup, next 3 lines are backup window in case im stupid
#window = tk.Tk() #create window
#window.title('Menu') #name window
#window.geometry('600x400') #window size
Mwindow = ttkb.Window(title = 'Menu',
                      themename = 'darkly', 
                      size = (600, 400)
                     ) #make a bootstrap window for more customisation

#creating a grid
Mwindow.columnconfigure((0, 1), weight = 1)
Mwindow.rowconfigure((1, 2), weight = 1)

titleLabel = ttkb.Label(master = Mwindow,
                       text = 'Menu',
                       font = 'Calibri 24 bold',
                       ) #creates heading
titleLabel.grid(row = 0,
               column = 0,
               columnspan = 2,
               pady = 20
               ) #puts the heading on the grid


def menuProjectileButton_func():
    Mwindow.destroy() #close the menu
    
    def createProjectile(Pspace):
        cannonBall = pymunk.Body(body_type = pymunk.Body.KINEMATIC) #(mass, inertia,) body type, notes on body type at the bottom
        cannonBall.position = (115, 810)
        Pspace.add(cannonBall) #adds to space
        return cannonBall

    def drawProjectile(cannonBall):
        if cannonBall:
            cannonBallRect = cannonBallImage.get_rect(center = (int(cannonBall.position.x), int(cannonBall.position.y)))
            projectileWindow.blit(cannonBallImage, cannonBallRect)

    def createCannon(Pspace):
        cannonBody = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        cannonBody.position = (50, 830)
        Pspace.add(cannonBody)
        return cannonBody

    def drawCannon(cannonBody):
        if cannonBody:
            cannonRect = cannonImage.get_rect(center = (int(cannonBody.position.x), int(cannonBody.position.y)))
            projectileWindow.blit(cannonImage, cannonRect)

    pygame.init() #initiate pygame

    projectileWindow = pygame.display.set_mode((1200, 900), pygame.RESIZABLE) #display size
    pygame.display.set_caption("Projectiles") #window title

    clock = pygame.time.Clock()

    def projectileLogic():
        global Pspace, cannonBallImage, cannonImage #globals required variables from other functions
        Pspace = pymunk.Space() #creates a space
        Pspace.gravity = (0, 10) #horizontal gravity, vertical gravity

        cannonBallImage = pygame.image.load('cannonBallImage.png')
        cannonBallImage = pygame.transform.scale(cannonBallImage, (40, 40))

        cannonImage = pygame.image.load('cannonImage.png')
        cannonImage = pygame.transform.scale(cannonImage, (100, 100))

        cannonBall = createProjectile(Pspace)
        cannonBody = createCannon(Pspace)

        drawSetup = pymunk.pygame_util.DrawOptions(projectileWindow) #sets up drawing stuff on the screen

        static: List[pymunk.Shape] = [pymunk.Segment(Pspace.static_body, (0, 875), (2000, 875), 10)] #the floor
        Pspace.add(*static) #add floor to space

        #Main loop
        Prun = True
        while Prun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Prun = False #pressing red x actually closes the projectiles window

            projectileWindow.fill((124, 252, 0)) #colour
            drawProjectile(cannonBall) #draws the cannon ball on screen
            drawCannon(cannonBody)
            Pspace.debug_draw(drawSetup) #draw the stuff
            fps = 60
            clock.tick(fps)
            Pspace.step(1/fps) #updates physics simulation loop every 1/fps seconds
            pygame.display.flip() #update entire display

    projectileLogic() #runs the main loop + some other stuff when menu button is clicked

    pygame.quit() #quit pygame
    sys.exit() #quit sys

#IDEAS
#Use a static body as the floor so it interacts better with hitboxes
#Use horizontal gravity for aerodynamics
#create a function that when press a button it returns to the menu, using similar code to
#make Mwindow global, put all of the menu code into a function
#when button pressed, just run the menu code again
#dont forget Mwindow.mainloop()

def menuAerodynamicButton_func():
    Mwindow.destroy()

    pygame.init()

    aerodynamicWindow = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Aerodynamics")

    #Main loop
    Arun = True
    while Arun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Arun = False

        aerodynamicWindow.fill((173, 216, 230))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def menuOrbitButton_func():
    Mwindow.destroy()

    pygame.init()

    orbitWindow = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Orbit")

    #Main loop
    Orrun = True
    while Orrun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Orrun = False

        orbitWindow.fill((0, 0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def menuOptionsButton_func():
    Mwindow.destroy()

    pygame.init()

    optionsWindow = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Options")

    #Main loop
    Oprun = True
    while Oprun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Oprun = False

        optionsWindow.fill((232, 191, 40))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


menuProjectileButton = ttkb.Button(master = Mwindow,
                                  text = 'Projectiles',
                                  command = menuProjectileButton_func,
                                  width = 15,
                                  bootstyle = 'success-outline'
                                  ) #Pressing button opens projectiles window, bootstyle outline creates the hover over change colour effect

menuAerodynamicButton = ttkb.Button(master = Mwindow,
                                   text = 'Aerodynamics (coming soon)',
                                   command = menuAerodynamicButton_func,
                                   width = 15,
                                   bootstyle = 'info-outline'
                                   )

menuOrbitButton = ttkb.Button(master = Mwindow,
                             text = 'Orbit (coming soon)',
                             command = menuOrbitButton_func,
                             width = 15,
                             bootstyle = 'light-outline'
                             )

menuOptionsButton = ttkb.Button(master = Mwindow,
                               text = 'Options (coming soon)',
                               command = menuOptionsButton_func,
                               width = 15,
                               bootstyle = 'warning-outline'
                               )

menuProjectileButton.grid(row = 1,
                         column = 0,
                         sticky = "nsew",
                         padx = 20,
                         pady = 20
                         ) #puts the button into a grid (Arne (funny liverpool joke)) slot

menuAerodynamicButton.grid(row = 1,
                          column = 1,
                          sticky = "nsew",
                          padx = 20,
                          pady = 20
                          )

menuOrbitButton.grid(row = 2,
                    column = 0,
                    sticky = "nsew",
                    padx = 20,
                    pady = 20
                    )

menuOptionsButton.grid(row = 2,
                      column = 1,
                      sticky = "nsew",
                      padx = 20,
                      pady = 20
                      )


#run the menu
Mwindow.mainloop() #run the window

#notes on pymunk
#static body - body doesnt move but can be collided with
#dynamic body - can be moved by physics
#kinematic body - body that can be moved by the user, or other non-physical code