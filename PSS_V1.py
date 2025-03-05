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
                       text = 'Physics Scenario Simulator Menu',
                       font = 'Calibri 24 bold',
                       ) #creates heading
titleLabel.grid(row = 0,
               column = 0,
               columnspan = 2,
               pady = 20
               ) #puts the heading on the grid

#WHY DID I PICK THE HARDEST TO DO FIRST
def menuProjectileButton_func():
    Mwindow.destroy() #close the menu
    
    def createProjectile():
        global cannonBallBody, cannonBallProp
        vs = [(20, 0), (0, 20), (20, 20), (0, 20)] #corners of the cannon ball rectangle hitbox. these values may need changing

        cannonBallBody = pymunk.Body(body_type = pymunk.Body.KINEMATIC) #(mass, inertia,) body type, notes on body type at the bottom
        
        cannonBallProp = pymunk.Poly(cannonBallBody, vs)
        cannonBallProp.collision_type = 1
        cannonBallProp.friction = 0.5 #notes on friction and elasticity values at the bottom
        cannonBallProp.elasticity = 0.5 #^^^
        cannonBallProp.density = 0.1 #prop for properties
        
        Pspace.add(cannonBallBody) #temp i think
        return cannonBallBody, cannonBallProp #makes it able to put on screen by returning

    def drawProjectile(cannonBallProp):
        if cannonBallProp: #get the cannon ball to pass into code
            cannonBallRect = cannonBallImage.get_rect(center = (int(cannonBallProp.position.x), int(cannonBallProp.position.y))) #make the cannon ball have a rectangle hitbox
            PWindow.blit(cannonBallImage, cannonBallRect) #put on screen

    def createCannon(Pspace):
        cannonBody = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        cannonBody.position = (60, 820)
        Pspace.add(cannonBody)
        return cannonBody

    def drawCannon(cannonBody):
        if cannonBody:
            cannonRect = cannonImage.get_rect(center = (int(cannonBody.position.x), int(cannonBody.position.y)))
            PWindow.blit(cannonImage, cannonRect)

    pygame.init() #initiate pygame

    PWindow = pygame.display.set_mode((1200, 900), pygame.RESIZABLE) #display size
    pygame.display.set_caption("Projectiles") #window title

    clock = pygame.time.Clock()

    def projectileLogic():
        global Pspace, cannonBallImage, cannonImage, cannonBallBody, cannonBallProp #globals required variables from other functions
        Pspace = pymunk.Space() #creates a space
        Pspace.gravity = (0, 10) #horizontal gravity, vertical gravity

        cannonBallImage = pygame.image.load('cannonBallImage.png')
        cannonBallImage = pygame.transform.scale(cannonBallImage, (20, 20))

        cannonImage = pygame.image.load('cannonImage.png')
        cannonImage = pygame.transform.scale(cannonImage, (150, 150))

        cannonBallBody, cannonBallProp = createProjectile()
        cannonBody = createCannon(Pspace)

        drawSetup = pymunk.pygame_util.DrawOptions(PWindow) #sets up drawing stuff on the screen

        static: List[pymunk.Shape] = [pymunk.Segment(Pspace.static_body,
                                                    (0, 875),
                                                    (2000, 875), 
                                                    10)
                                                    ] #the floor
        Pspace.add(*static) #add all of static list to space. Other things may be added to this list further in development

        #Main loop
        Prun = True
        while Prun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key in [pygame.K_ESCAPE]):
                    Prun = False #pressing red x actually closes the projectiles window
            
            keyPress = pygame.key.get_pressed()

            mousePoint = pymunk.pygame_util.from_pygame(Vec2d(*pygame.mouse.get_pos()), PWindow) #get the mouse position using vectors
            cannonBody.angle = (mousePoint - cannonBody.position).angle #calculate the angle of the cannon in relation to the mouse
            cannonBallBody.position = cannonBody.position + Vec2d.from_polar(cannonBallProp.radius + 40, cannonBody.angle) #adding the position to the vector (length, angle)
            cannonBallBody.angle = cannonBody.angle
            #cannon rotation needs work
            #cannon ball body needs to be same angle of rotation but further forward

            PWindow.fill((124, 252, 0)) #colour
            drawProjectile(cannonBallBody) #draws the cannon ball on screen
            drawCannon(cannonBody) #draws the cannon on the screen
            Pspace.debug_draw(drawSetup) #draw the stuff
            fps = 60
            clock.tick(fps)
            Pspace.step(1/fps) #updates physics simulation loop every 1/fps seconds
            pygame.display.flip() #update entire display

    projectileLogic() #runs the main loop + some other stuff when menu button is clicked

    pygame.quit() #quit pygame
    sys.exit() #quit sys

#IDEAS FOR LATER
#Use a static body as the floor so it interacts better with hitboxes (THIS IS MOSTLY IMPLEMENTED NOW, COMPLICATED)
#Use horizontal gravity for aerodynamics
#Use a center gravity point for sun
#
#create a function that when press a button it returns to the menu, using similar code to
##make Mwindow global, put all of the menu code into a function
##when button pressed, just run the menu code again
##dont forget Mwindow.mainloop()
#
#make a seperate function for FLYING CANNON BALL
#125, 146

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

#friction and elasticity
#0 has no friction or bounce
#1 is a perfect bounce (no energy is lost)
#Between 1 and 0 energy is lost
#Greater than 1 energy is gained