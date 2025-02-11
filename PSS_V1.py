import tkinter as tk #importing tkinter with the abbreviation tk for convinience
from tkinter import ttk #classes for themed widgets
import ttkbootstrap as ttkb
import pygame
import sys
import pymunk


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
        cannonBall = pymunk.Body(10,
                                50,
                                body_type = pymunk.Body.DYNAMIC
                                ) #mass, inertia, body type, notes on body type at the bottom
        cannonBall.position = (300, 0) #put it at a place on the screen (CURRENTLY FOR TESTING)
        cannonBallCircle = pymunk.Circle(cannonBall, 5) #makes cannon ball hitbox a circle
        Pspace.add(cannonBall, cannonBallCircle) #adds to space
        return cannonBallCircle

    def drawProjectile(cannonBalls):
        for CB in cannonBalls:
            posX = int(CB.body.position.x) #x pos of cannon ball
            posY = int(CB.body.position.y) #y pos of cannon ball
            pygame.draw.circle(projectileWindow,
                              (0,0,0), 
                              (posX, posY),
                              20) #window, colour, position, size
        #https://www.pymunk.org/en/latest/tutorials.html

    pygame.init() #initiate pygame

    projectileWindow = pygame.display.set_mode((1200, 600), pygame.RESIZABLE) #display size
    pygame.display.set_caption("Projectiles") #window title

    def projectileLogic():
        global Pspace, cannonBalls #globals required variables from other functions
        Pspace = pymunk.Space() #creates a space
        Pspace.gravity = (0, 10) #horizontal gravity, vertical gravity
        cannonBalls = [] #empty list for cannon balls
        cannonBalls.append(createProjectile(Pspace)) #appends the creation of the projectile to the list, and puts it in space

        #Main loop
        Prun = True
        while Prun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Prun = False #pressing red x actually closes the projectiles window

            projectileWindow.fill((124, 252, 0)) #colour
            drawProjectile(cannonBalls) #draws the cannon ball on screen
            Pspace.step(1/50) #updates physics simulation loop every 0.02 seconds
            pygame.display.flip() #update entire display

    projectileLogic() #runs the main loop + some other stuff when menu button is clicked

    pygame.quit() #quit pygame
    sys.exit() #quit sys


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
                                   text = 'Aerodynamics',
                                   command = menuAerodynamicButton_func,
                                   width = 15,
                                   bootstyle = 'info-outline'
                                   )

menuOrbitButton = ttkb.Button(master = Mwindow,
                             text = 'Orbit',
                             command = menuOrbitButton_func,
                             width = 15,
                             bootstyle = 'light-outline'
                             )

menuOptionsButton = ttkb.Button(master = Mwindow,
                               text = 'Options',
                               command = menuOptionsButton_func,
                               width = 15,
                               bootstyle = 'warning-outline'
                               )

menuProjectileButton.grid(row = 1,
                         column = 0,
                         sticky = "nsew",
                         padx = 20,
                         pady = 20
                         ) #puts the button into a grid (Arne) slot

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