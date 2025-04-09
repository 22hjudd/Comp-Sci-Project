#setup
import tkinter as tk #importing tkinter with the abbreviation tk for convenience
from tkinter import ttk #classes for themed widgets
import ttkbootstrap as ttkb #more useful tkinter, most used out of the tk libraries
import pygame #puts the physics on the screen
import pymunk #does the physics
import pymunk.pygame_util #draw pymunk objects in pygame
from pymunk.vec2d import Vec2d #vectors and positioning, such as mouse pos
import math #maths


#main code


#set global variable
darkMode = True #this is used in the options


def menuProjectileButton_func(MWindow):
    MWindow.destroy() #close the menu
    
    def createProjectile():
        global cannonBallBody, cannonBallProp

        cannonBallBody = pymunk.Body(body_type = pymunk.Body.KINEMATIC) #(mass, inertia,) body type. Notes on body type at the bottom
        #                                                                for dynamic body
        cannonBallProp = pymunk.Circle(cannonBallBody, 5) #body, radius
        cannonBallProp.collision_type = 1
        cannonBallProp.friction = 0.5 #notes on friction and elasticity values at the bottom
        cannonBallProp.elasticity = 0.5 #^ comment
        cannonBallProp.density = 0.1 #prop for properties

        PSpace.add(cannonBallBody, cannonBallProp) #add the body of the cannon ball to the space
        return cannonBallBody, cannonBallProp #makes it able to put on screen by returning
    
    def drawProjectile(cannonBallBody):
        if cannonBallBody: #get the cannon ball to pass into code
            cannonBallRect = cannonBallImage.get_rect(center = (int(cannonBallBody.position.x), int(cannonBallBody.position.y))) #make the cannon ball have a rectangle hitbox
            PWindow.blit(cannonBallImage, cannonBallRect) #put on screen
 
    def createCannon(PSpace):
        cannonBody = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        cannonBody.position = (60, 820)
        PSpace.add(cannonBody)
        return cannonBody
 
    def drawCannon(cannonBody):
        if cannonBody:
            degrees = -math.degrees(cannonBody.angle)  # Convert radians to degrees, pymunk works in radians but pygame doesn't
            cannonRotation = pygame.transform.rotate(cannonImage, degrees)  # Rotate image
            (cannonRect) = cannonRotation.get_rect(center = (int(cannonBody.position.x), int(cannonBody.position.y)))
            PWindow.blit(cannonRotation, cannonRect)

    def dealWithCollisions(arbiter, space, data): #space and data don't seem to do anything but are apparently required by pymunk's API
        cannonBallCollisionShape = arbiter.shapes[0] if arbiter.shapes[0].collision_type == 1 else arbiter.shapes[1]
        floorCollisionShape = arbiter.shapes[0] if arbiter.shapes[0].collision_type == 0 else arbiter.shapes[1]

        cannonBallCollisionShape.friction = 0.5
        floorCollisionShape.friction = 0.5

        #backup in case friction doesn't work. Subtle so it will slow down slowly if it doesn't
        cannonBallSpeed = cannonBallCollisionShape.body
        cannonBallSpeed.velocity = cannonBallSpeed.velocity * 0.8

 
    global PWindow, PSpace, cannonBallImage, cannonImage, cannonBallBody, cannonBallProp
 
    pygame.init() #initiate pygame

    PWindow = pygame.display.set_mode((1200, 900), pygame.RESIZABLE) #window size, make window able to resize
    pygame.display.set_caption("Projectiles") #window title
 
    clock = pygame.time.Clock()
 
    def projectileLogic():
        global PSpace, cannonBallImage, cannonImage, cannonBallBody, cannonBallProp #globals required variables from other functions
        PSpace = pymunk.Space() #creates a space
        inputGravity = float(input('Enter a gravity to be used in the simulation, in terms of Earth gravity (e.g. input of 1 meaning 9.81): '))
        finalGravity = inputGravity * 600 #since pymunk uses arbitrary values, this seemed about right from scientific estimates
        PSpace.gravity = (0, finalGravity) #horizontal gravity, vertical gravity

        cannonBallImage = pygame.image.load('cannonBallImage.png') #load image
        cannonBallImage = pygame.transform.scale(cannonBallImage, (20, 20)) #scale it up in the x and y direction to be fitting size
 
        cannonImage = pygame.image.load('cannonImage.png')
        cannonImage = pygame.transform.scale(cannonImage, (150, 150))

        cannonBallBody, cannonBallProp = createProjectile() #use cannon ball body and properties to create the projectile
        cannonBody = createCannon(PSpace) #use cannon body to create the cannon in the space

        floor = pymunk.Segment(PSpace.static_body, (0, 875), (2000, 875), 10) #add a static body to the space as a straight line across the screen, used as a floor. Interacts with projectiles
        floor.friction = 0.5
        floor.collision_type = 0
        PSpace.add(floor)

        cannonBallsInFlight = [] #list of all the cannonballs so the exisitng ones can still be on screen
        initialTime = 0 #start time

        collisionHandler = PSpace.add_collision_handler(0, 1) #collision handler deals with objects that have a collision type 0 and 1
        collisionHandler.post_solve = dealWithCollisions
 
        #Main loop
        Prun = True
        while Prun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key in [pygame.K_ESCAPE]):
                    Prun = False #pressing red x and escape closes the projectiles window
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #mouse pressed down
                    initialTime = pygame.time.get_ticks() #record the time when mouse first pressed down
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: #mouse released
                    finalTime = pygame.time.get_ticks() #record the time when mouse released

                    timeDiff = finalTime - initialTime #get the time diff by final - initial
                    
                    rateSpeedIncrease = max(min(timeDiff, 1000), 10) * 10 #min and max values of power so it doesn't go flying off the screen. Multiply by number so easy to change values
                    impulse = Vec2d.from_polar(rateSpeedIncrease, cannonBody.angle) #change in momentum, impulse vector, physics

                    cannonBallBody.body_type = pymunk.Body.DYNAMIC #makes cannonball body dyanmic from kinematic when set earlier so that it can be affected by physics
                    cannonBallBody.apply_impulse_at_world_point(impulse, cannonBallBody.position) #impulse set to cannonball pos
                    cannonBallsInFlight.append((cannonBallBody, cannonBallProp))
                    cannonBallBody, cannonBallProp = createProjectile()

 
            mousePoint = pymunk.pygame_util.from_pygame(Vec2d(*pygame.mouse.get_pos()), PWindow) #get the mouse position using vectors
            cannonBody.angle = (mousePoint - cannonBody.position).angle #calculate the angle of the cannon in relation to the mouse
            cannonBallDiff = Vec2d(-38, -20).rotated(cannonBody.angle) #change distance from the centre of the cannon
            cannonBallBody.position = cannonBody.position + cannonBallDiff #position the cannon ball by aligning with the cannon and then differentiating it from that point
            cannonBallBody.angle = cannonBody.angle #both rotate at the same time and angle
 
            PWindow.fill((124, 252, 0)) #colour
            drawProjectile(cannonBallBody) #draws the cannon ball on screen
            drawCannon(cannonBody) #draws the cannon on the screen
            for cBF, _ in cannonBallsInFlight:
                drawProjectile(cBF)

            #breaking up the line draw to give a target to aim at in red, think of it as a 2D classic red, white, red, white target, but just side on
            pygame.draw.line(PWindow, (255, 255, 255), (0, 875), (600, 875), 10) #white
            pygame.draw.line(PWindow, (255, 0, 0), (600, 875), (800, 875), 10) #red
            pygame.draw.line(PWindow, (255, 255, 255), (800, 875), (2000, 875), 10) #white

            fps = 60
            clock.tick(fps)
            PSpace.step(1/fps) #updates physics simulation loop every 1/fps (currently 1/60) seconds
            pygame.display.flip() #update entire display
 
    projectileLogic() #runs the main loop + some other stuff when menu button is clicked
 
    pygame.quit() #quit pygame

    menu()
 
def menuAerodynamicButton_func(MWindow):
    MWindow.destroy()

    def createAirParticles(ASpace, airParticlesPos):
        airParticlesBody = pymunk.Body(1, 10, body_type = pymunk.Body.DYNAMIC)
        airParticlesBody.position = airParticlesPos
        airParticlesProp = pymunk.Circle(airParticlesBody, 5) #body, radius
        ASpace.add(airParticlesBody, airParticlesProp)
        return airParticlesBody, airParticlesProp
    
    def drawAirParticles(airParticlesStore):
        for airParticleBody, _ in airParticlesStore:
            if airParticleBody:
                pygame.draw.circle(AWindow, 
                                  (255, 255, 255), 
                                  (int(airParticleBody.position.x), int(airParticleBody.position.y)),
                                  5
                                  ) #screen, colour, centre, radius

    def createAerodynamicObject(ASpace):
        aerodynamicObjectBody = pymunk.Body(body_type = pymunk.Body.STATIC)
        aerodynamicObjectBody.position = (600, 450)

        Avs = [] #ready for inputed vertice values

        NoV = int(input('How many verticies do you want your custom polygon to have? '))
        #NoV = Number of verticies

        for i in range (NoV):
            vsValues = input(f'Enter value for vertice v{i} in this format: (xvalue, yvalue). ') #Relative to the centre
            x, y = map(int, vsValues.strip('()').split(',')) #make string to int, strip the values of brackets and comma. Ask user to format like that to begin with so they understand what is happening
            Avs.append((x, y))


        #Avs = [(0, 0), (20, 0), (20, 20), (0, 20)] #this is a template as used earlier so I can work with it
        aerodynamicObjectProp = pymunk.Poly(aerodynamicObjectBody, Avs)
        ASpace.add(aerodynamicObjectBody, aerodynamicObjectProp)
        return aerodynamicObjectBody, aerodynamicObjectProp
    
    global colour
    colour = tuple(map(int, input('Enter a RGB value for the object, in this format: (R, G, B): ').strip('()').split(',')))

    def drawAerodynamicObject(aerodynamicObjectBody, aerodynamicObjectProp):
        if aerodynamicObjectBody:
            vertices = [aerodynamicObjectBody.local_to_world(v) for v in aerodynamicObjectProp.get_vertices()]
            pygame.draw.polygon(AWindow,
                               colour,
                               [(int(v.x), int(v.y)) for v in vertices]
                               )

    pygame.init()
    
    global AWindow, ASpace
    AWindow = pygame.display.set_mode((1200, 900), pygame.RESIZABLE)
    pygame.display.set_caption("Aerodynamics")

    ASpace = pymunk.Space()
    ASpace.gravity = (-50, 0) #use horizontal gravity this time as pulling (<--) this time
    
    aerodynamicObjectBody, aerodynamicObjectProp = createAerodynamicObject(ASpace)
    airParticlesStore = [] #store the airparticles in a list so they don't disappear when another is created

    clock = pygame.time.Clock()

    #Main loop
    Arun = True
    while Arun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key in [pygame.K_ESCAPE]):
                Arun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                airParticles = createAirParticles(ASpace, event.pos)
                airParticlesStore.append(airParticles)


        AWindow.fill((173, 216, 230))
        drawAirParticles(airParticlesStore)
        drawAerodynamicObject(aerodynamicObjectBody, aerodynamicObjectProp)
        fps = 60
        clock.tick(fps)
        ASpace.step(1/fps)
        pygame.display.flip()
 
    pygame.quit()
    menu()
    
    
def menuOrbitButton_func(MWindow):
    MWindow.destroy()
 
    pygame.init()
 
    orbitWindow = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    pygame.display.set_caption("Orbit")
 
    #Main loop
    Orrun = True
    while Orrun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key in [pygame.K_ESCAPE]):
                Orrun = False
 
        orbitWindow.fill((0, 0, 0))
        pygame.display.flip()
 
    pygame.quit()
    menu()
 
 
def menuOptionsButton_func(MWindow):
    #MWindow.destroy()
    def setOpWindowDarkMode(OpWindow):
        if darkMode:
            OpWindow.configure(background = 'black')
        else:
            OpWindow.configure(background = 'white')

    OpWindow = ttkb.Window(title = 'Options',
                          size = (600, 400)
                          )
    
    setOpWindowDarkMode(OpWindow)
    
    darkModeToggleVar = tk.BooleanVar(master = OpWindow, value = darkMode) #set dark mode to true, as the main menu starts in dark mode, sheilding eyes from unnecessary brightness
 
    def darkModeToggle_func():
        global darkMode
        darkMode = darkModeToggleVar.get()

        setOpWindowDarkMode(OpWindow)
        setMWindowDarkMode()
        
        OpWindow.update()
    
    def toMainMenuOpButton_func():
        OpWindow.destroy()
    
    darkModeToggle = ttk.Checkbutton(OpWindow,
                                    text = 'Dark Mode',
                                    variable = darkModeToggleVar,
                                    command = darkModeToggle_func
                                    )
    darkModeToggle.pack()

    toMainMenuOpButton = ttk.Button(OpWindow,
                                    text = 'Return to main menu',
                                    command = toMainMenuOpButton_func,
                                    )
    toMainMenuOpButton.pack()

    OpWindow.mainloop()
 
def setMWindowDarkMode():
    if darkMode:
        MWindow.configure(background = 'black')
    else:
        MWindow.configure(background = 'white')

def menu():
    global MWindow
    #setup, next 3 lines are backup window in case im stupid
    #window = tk.Tk() #create window
    #window.title('Menu') #name window
    #window.geometry('600x400') #window size

    MWindow = ttkb.Window(title = 'Menu',
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
                                      command = lambda: menuProjectileButton_func(MWindow),
                                      width = 15,
                                      bootstyle = 'success-outline'
                                      ) #Pressing button opens projectiles window, bootstyle outline creates the hover over change colour effect

    menuAerodynamicButton = ttkb.Button(master = MWindow,
                                       text = 'Aerodynamics',
                                       command = lambda: menuAerodynamicButton_func(MWindow),
                                       width = 15,
                                       bootstyle = 'info-outline'
                                       )
 
    menuOrbitButton = ttkb.Button(master = MWindow,
                                 text = 'Orbit (coming soon)',
                                 command = lambda: menuOrbitButton_func(MWindow),
                                 width = 15,
                                 bootstyle = 'danger-outline'
                                 )
 
    menuOptionsButton = ttkb.Button(master = MWindow,
                                   text = 'Options',
                                   command = lambda: menuOptionsButton_func(MWindow),
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
    
    setMWindowDarkMode()
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