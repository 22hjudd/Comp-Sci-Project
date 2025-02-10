import tkinter as tk #importing tkinter with the abbreviation tk for convinience
from tkinter import ttk #classes for themed widgets
import ttkbootstrap as ttkb
import pygame
import sys
import pymunk


#making the menu

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
    
    def createProjectile():
        cannonBall = pymunk.Body(10,
                                50,
                                body_type = pymunk.Body.DYNAMIC
                                ) #mass, inertia, body type, notes on body type at the bottom
        cannonBall.position = (300, 0) #put it at a place on the screen (CURRENTLY FOR TESTING)
        shape = pymunk.Circle(cannonBall) #makes cannon ball hitbox a circle
        Pspace.add(cannonBall, shape)
        return shape

    def drawProjectile():
        pass #placeholder until I watch more
        #https://www.pymunk.org/en/latest/tutorials.html
        #simulating physics in python 10:45

    pygame.init() #initiate pygame

    projectileWindow = pygame.display.set_mode((1200, 600), pygame.RESIZABLE) #display size
    pygame.display.set_caption("Projectiles") #window title

    def projectileLogic():
        global Pspace
        Pspace = pymunk.Space()
        Pspace.gravity = (0, 10)

        #Main loop
        Prun = True
        while Prun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Prun = False #pressing red x actually closes the projectiles window

            projectileWindow.fill((124, 252, 0)) #colour
            Pspace.step(1/50)
            pygame.display.flip() #update entire display

    projectileLogic()

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