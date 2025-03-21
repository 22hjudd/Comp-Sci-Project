#setup
import tkinter as tk #importing tkinter with the abbreviation tk for convinience
from tkinter import ttk #classes for themed widgets
import ttkbootstrap as ttkb #more useful tkinter, most used out of the tk libraries
import pygame #puts the physics on the screen
import sys #system specific parameters
import pymunk #does the physics
import pymunk.pygame_util #draw pymunk objects in pygame
from pymunk.vec2d import Vec2d #vectors and positioning, such as mouse pos
from typing import List #for lists/arrays
import math #maths


#main code


def menuProjectileButton_func(MWindow):
    MWindow.destroy() #close the menu

    def toMainMenuPButton_func():
        global Prun #destroy the projectiles window, used in a button func later
        Prun = False
    
    def createProjectile():
        global cannonBallBody, cannonBallProp
        vs = [(0, 0), (20, 0), (20, 20), (0, 20)] #corners of the cannon ball rectangle hitbox, relative to the centre. THESE VALUES MAY NEED CHANGING

        cannonBallBody = pymunk.Body(body_type = pymunk.Body.KINEMATIC) #(mass, inertia,) body type. Notes on body type at the bottom
        #                                                                for dynamic body
        cannonBallProp = pymunk.Poly(cannonBallBody, vs)
        cannonBallProp.collision_type = 1
        cannonBallProp.friction = 0.5 #notes on friction and elasticity values at the bottom
        cannonBallProp.elasticity = 0.5 #^ comment
        cannonBallProp.density = 0.1 #prop for properties
        
        Pspace.add(cannonBallBody, cannonBallProp) #add the body of the cannon ball to the space
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
            degrees = -math.degrees(cannonBody.angle)  # Convert radians to degrees, pymunk works in radians but pygame doesn't
            cannonRotation = pygame.transform.rotate(cannonImage, degrees)  # Rotate image
            cannonRect = cannonRotation.get_rect(center = (int(cannonBody.position.x), int(cannonBody.position.y)))
            PWindow.blit(cannonRotation, cannonRect)

    global PWindow

    pygame.init() #initiate pygame

    PWindow = pygame.display.set_mode((1200, 900), pygame.RESIZABLE) #window size, make window able to resize
    pygame.display.set_caption("Projectiles") #window title

    clock = pygame.time.Clock()

    #FIX THIS LATER
    destoryPWindow = ttkb.Button(master = PWindow,
                                text = 'Return to main menu',
                                command = toMainMenuPButton_func
                                )
    destoryPWindow.pack()

    def projectileLogic():
        global Pspace, cannonBallImage, cannonImage, cannonBallBody, cannonBallProp #globals required variables from other functions
        Pspace = pymunk.Space() #creates a space
        Pspace.gravity = (0, 10) #horizontal gravity, vertical gravity

        cannonBallImage = pygame.image.load('cannonBallImage.png') #load image
        cannonBallImage = pygame.transform.scale(cannonBallImage, (20, 20)) #scale it up in the x and y direction to be fitting size

        cannonImage = pygame.image.load('cannonImage.png')
        cannonImage = pygame.transform.scale(cannonImage, (150, 150))

        cannonBallBody, cannonBallProp = createProjectile() #use cannon ball body and properties to create the projectile
        cannonBody = createCannon(Pspace) #use cannon body to create the cannon in the space

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
                    Prun = False #pressing red x and escape closes the projectiles window
            
            keyPress = pygame.key.get_pressed()

            mousePoint = pymunk.pygame_util.from_pygame(Vec2d(*pygame.mouse.get_pos()), PWindow) #get the mouse position using vectors
            cannonBody.angle = (mousePoint - cannonBody.position).angle #calculate the angle of the cannon in relation to the mouse
            cannonBallDiff = Vec2d(-38, -20).rotated(cannonBody.angle) #change distance from the centre of the cannon
            cannonBallBody.position = cannonBody.position + cannonBallDiff #position the cannon ball by alligning with the cannon and then differntiating it from that point
            cannonBallBody.angle = cannonBody.angle #both rotate at the same time and angle

            PWindow.fill((124, 252, 0)) #colour
            drawProjectile(cannonBallBody) #draws the cannon ball on screen
            drawCannon(cannonBody) #draws the cannon on the screen
            Pspace.debug_draw(drawSetup) #draw the stuff
            fps = 60
            clock.tick(fps)
            Pspace.step(1/fps) #updates physics simulation loop every 1/fps (currently 1/60) seconds
            pygame.display.flip() #update entire display

    projectileLogic() #runs the main loop + some other stuff when menu button is clicked

    pygame.quit() #quit pygame
    menu()

#IDEAS FOR LATER
#Use a static body as the floor so it interacts better with hitboxes (THIS IS MOSTLY IMPLEMENTED NOW, COMPLICATED)
#Use horizontal gravity for aerodynamics
#Use a center gravity point for sun
#
#create a function that when press a button it returns to the menu, using similar code to
##make MWindow global, put all of the menu code into a function
##when button pressed, just run the menu code again
##dont forget MWindow.mainloop()
#
#make a seperate function for FLYING CANNON BALL
#125, 146

def menuAerodynamicButton_func():
    MWindow.destroy()

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
    menu()


def menuOrbitButton_func():
    MWindow.destroy()

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
    menu()


def menuOptionsButton_func():
    MWindow.destroy()

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
    menu()


def menu():
    global MWindow
    #setup, next 3 lines are backup window in case im stupid
    #window = tk.Tk() #create window
    #window.title('Menu') #name window
    #window.geometry('600x400') #window size
    MWindow = ttkb.Window(title = 'Menu',
                         themename = 'darkly', 
                         size = (600, 400)
                         ) #make a bootstrap window for more customisation

    #creating a grid
    MWindow.columnconfigure((0, 1), weight = 1)
    MWindow.rowconfigure((1, 2), weight = 1)

    titleLabel = ttkb.Label(master = MWindow,
                           text = 'Physics Scenario Simulator Menu',
                           font = 'Calibri 24 bold',
                           ) #creates heading
    titleLabel.grid(row = 0,
                   column = 0,
                   columnspan = 2,
                   pady = 20
                   ) #puts the heading on the grid
    
    menuProjectileButton = ttkb.Button(master = MWindow,
                                      text = 'Projectiles',
                                      command = menuProjectileButton_func,
                                      width = 15,
                                      bootstyle = 'success-outline'
                                      ) #Pressing button opens projectiles window, bootstyle outline creates the hover over change colour effect

    menuAerodynamicButton = ttkb.Button(master = MWindow,
                                       text = 'Aerodynamics (coming soon)',
                                       command = menuAerodynamicButton_func,
                                       width = 15,
                                       bootstyle = 'info-outline'
                                       )

    menuOrbitButton = ttkb.Button(master = MWindow,
                                 text = 'Orbit (coming soon)',
                                 command = menuOrbitButton_func,
                                 width = 15,
                                 bootstyle = 'light-outline'
                                 )

    menuOptionsButton = ttkb.Button(master = MWindow,
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
    MWindow.mainloop() #run the window

menu()

#notes on pymunk

#static body - body doesnt move but can be collided with
#dynamic body - can be moved by physics
#kinematic body - body that can be moved by the user, or other non-physical code

#friction and elasticity
#0 has no friction or bounce
#1 is a perfect bounce (no energy is lost)
#Between 1 and 0 energy is lost
#Greater than 1 energy is gained