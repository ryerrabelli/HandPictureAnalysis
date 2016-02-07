#HopHacks Spring 2016 Project
#Rahul Yerrabelli, Benjamin Pikus, Dawei Geng
#February 5th, 2016 - February 7th, 2016

from graphics import * #used for GUI
import cv2
import random
from math import *
import time
import thread
from test import *

#Button class with pre-determined functions
class Button:

    #general description of rectangular button
    def __init__(self, win, center, width, height, label): #(*name of graphic window*, Point(#,#) of center, "button label")
        #pre-set values from Button class
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = rect = Rectangle(p1,p2)
        self.setOriginalFill()
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        "Returns true if button p is inside"
        try:
            return (self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)
        except AttributeError:
            print("Error: Attribute error found in button clicked")
            return False

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.active = False

    #color of the button is set to orange when clicked
    def setFillOrange(self):
        "set the color of the button to orange"
        self.rect.setFill('orange')

    def setFillGrey(self):
        "set the color of the button to grey"
        self.rect.setFill('grey')

    #Button is set to its default color
    def setOriginalFill(self):
        self.rect.setFill('Bisque')

class CheckBox:

    #general description of rectangular checkbix
    def __init__(self, win, center, width, height, label, initialValue): #(*name of graphic window*, Point(#,#) of center, "checkbox label")
        #pre-set values from CheckBox class
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = rect = Rectangle(p1,p2)
        self.setOriginalFill()
        self.rect.draw(win)
        #if you just want to the text to be centered at the center of the CheckBox, put simply write Text(center, label)
        #However the following compensates for the square box on the left side that is used for checking
        inset = height/5 #how far the box's edges are spaced from the button edges (not including the right side of box)
        self.label = Text(Point( (self.xmin+(self.ymax-inset)-(self.ymin+inset)+self.xmax)/2, y), label)
        self.label.draw(win)

        chckP1 = Point(self.xmin+inset, self.ymin+inset)
        chckP2 = Point(self.xmin+(self.ymax-inset)-(self.ymin+inset),self.ymax-inset)
        # width/height of box is equal to (self.ymax-inset)-(self.ymin+inset) = self.ymax-self.ymin-2*inset
        # box is a square

        self.chckRect = Rectangle(chckP1,chckP2)
        self.chckRect.draw(win)

        self.value = initialValue
        if self.value:
            self.setChecked()
        else:
            self.setUnchecked()
        self.deactivate()

    def clicked(self, p):
        "Returns true if button p is inside"
        try:
            return (self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)
        except AttributeError:
            print("Error: Attribute error found in button clicked")
            return False

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.active = False

    def setChecked(self):
        self.value = True
        self.chckRect.setFill('green')

    def setUnchecked(self):
        self.value = False
        self.chckRect.setFill('red')

    def isChecked(self):
        return self.value

    def toggle(self):
        if self.isChecked():
            self.setUnchecked()
        else:
            self.setChecked()

    def setFillGrey(self):
        "set the color of the button to grey"
        self.rect.setFill('grey')

    #Button is set to its default color
    def setOriginalFill(self):
        self.rect.setFill('Bisque')

class Player:
    def __init__(self, win, center):
        i = 2
        self.center = center
        self.rect = Rectangle(Point(10,45),Point(13,48))
        self.rect.setFill("green")
        #self.rect.draw(win)
        self.image = Image(Point(10,50), "Decorational/hoppingsnowman.gif")#make center 10,46 if square
        self.image.draw(win)
        self.width = 3
        self.height = 5


    def getCenter(self):
#        return self.rect.get
        return self.image.getAnchor()
        #Center()

    def move(self, dx, dy):
    #        self.rect.move(dx,dy)
        self.image.move(dx,dy)

    def getP1(self):
        p = Point(self.getCenter().getX() + self.width, self.getCenter().getY() + self.height )
        print "XY"
        print str(p.getX())
        print str(p.getY())
        return p
        #return self.rect.getP1()

    def getP2(self):
        #return self.rect.getP2()
        p = Point(self.getCenter().getX() - self.width, self.getCenter().getY() - self.height )
        print "XY"
        print str(p.getX())
        print str(p.getY())
        return p
        #return Point(self.getCenter().getX() - self.image.getWidth(), self.getCenter().getY() - self.image.getHeight() )


class Enemy:
    def __init__(self, win, player):
        global  bEasyMode
        global lives
        center = Point(20,80)
        rand = random.random()
        if rand < 0.5:
            #vertical
            y=100
            x=random.random()*100
        elif rand <0.75:
            #left, height 45 to 100
            x=0
            y = ceil(random.random()*55)

        else:
            #right, height 45 to 100
            x=100
            y = 48+ ceil(random.random()*55)

        center = Point(x,y)


        self.xCenter = center.getX()
        self.yCenter = center.getY()
        self.circle = Circle(center,1)
        if lives > 1:
            self.circle.setFill("white")
        else:
            self.circle.setFill("red")

        self.circle.draw(win)

        if bEasyMode.isChecked():
            hyp = 5.0
            #yVel = random.random()* hyp
            #xVel = sqrt(pow(hyp,2)-pow(yVel,2))
            x0 = (random.random()-0.5)*20+50 #50
            y0 = 46
            yVel = hyp/sqrt(1+pow( (x-x0)/(fabs(y-y0)+0.001),2))
            xVel = hyp/sqrt(1+pow( (y-y0)/(fabs(x-x0)+0.001),2))
        else:
            hyp = 5.0
            x0 = player.getCenter().getX()
            y0 = player.getCenter().getY()
            yVel = hyp/sqrt(1+pow( (x-x0)/(fabs(y-y0)+0.001),2))
            xVel = hyp/sqrt(1+pow( (y-y0)/(fabs(x-x0)+0.001),2))


        if x < 50:
            xVel = abs(xVel)
        else:
            xVel = -1*abs(xVel)
        yVel = -1*abs(yVel)
        self.xVel = xVel
        self.yVel =  yVel
        self.alive = True

    def travel(self, timeDif):
        if self.alive == False:
            print "Error. Enemy is already dead"
        self.circle.move(self.xVel*timeDif,self.yVel*timeDif)
        if self.circle.getCenter().getX() <= 0.0 or self.circle.getCenter().getX() >= 100.0 or self.circle.getCenter().getY() >= 100.0:
            self.alive = False
            self.circle.undraw()
        elif self.circle.getCenter().getY() <= 0.0:
            self.alive = False
        #self.alive = False


    def isAlive(self):
        return self.alive



#input a GraphWin object
def getMouse(window):
    if window.isClosed():
        exitProgram(window)
    else:
        return window.getMouse()

def exitProgram(window):
    window.close()
    sys.exit()

def startScreen(): #This function allows the user to input the port name of the serial connection to the Arduino board
    #The function returns the port name which is needed later in this code to create the serial connection to the Arduino Board in order to send instructions to the Arduino board and receive results
    global  bEasyMode
    win = GraphWin("Hand Analysis", 325, 200) #("name of window", pixel width, pixel height)
    win.setBackground("light blue")
    win.setCoords(0,0, 100, 100) #make the window 100 by 100 in order to more easily set size/location of objects
    Title = Text(Point(50, 75), "Enter your name below:")
    Title.draw(win)

    input_name = Entry(Point(50,50), 20) #create an entry box where the user can input characters
    input_name = Entry(Point(50,50), 20) #create an entry box where the user can input characters
    input_name.setText("") #Rahul Y, For testing purposes
    input_name.draw(win)

    bEasyMode = CheckBox(win,Point(34, 27), 29, 10, "Easy",False) #toggle
    bHelp = Button(win, Point(66, 27), 29,10, "Help") #button the user should press in order to pull up instructions about how to install port settings
    binstall = Button(win, Point(50, 10), 25,12, "Start") #button the user should press after writing port name


    clickinstall = False #initialize the click to false so that the following look repeats until the "set port" button is pressed

    helpWin = None
    while clickinstall == False:
        p_clickin = getMouse(win) #wait to get mouse click
        if isinstance(helpWin,GraphWin):
            helpWin.close()

        if binstall.clicked(p_clickin): #if "set port" was clicked then return the value input by the user and close the window
            port_name = input_name.getText()
            binstall.setFillOrange()
            clickinstall = True
            win.close()
        elif bHelp.clicked(p_clickin): #if the "Help" button was pressed than open the instructions
            wordDocName = 'Install_help.docx'
            if (os.path.isfile(wordDocName)):
                bHelp.setFillOrange()
                os.startfile(wordDocName) #Open file with instructions
            else:
                helpWin = GraphWin("Help Window ", 200, 50) #("name of window", pixel width, pixel height)
                helpWin.setBackground("light gray")
                helpWin.setCoords(0,0, 100, 100) #make the window 100 by 100 in order to more easily set size/location of objects
                helpText = Text(Point(50, 50), "Please find and open the\nWord Document called\n\"Install_help.docx\" ")
                helpText.draw(helpWin)
        elif bEasyMode.clicked(p_clickin):
            bEasyMode.toggle()
    return ( port_name, bEasyMode.isChecked() )

def convertToPBM(filePath, extension):
    origFile = open(filePath+extension,'r')
    PBMFile = open(filePath+".pbm",'w+')
    PBMFile.write("P1\n6 10\n")
    for line in origFile:
        PBMFile.write(line.replace(","," "))


def main():
    global loopNumber
    global bEasyMode
    global lives
    global shielded
    global liveTitle

    print "true3"
    setPortResults = startScreen() #do this before the main loop to avoid needing to re-enter the port name every time the user decides to play again

    #Create Graphics Window and instructions
    win = GraphWin("Hand Therapy Analysis", 750, 650) #("name of window", pixel width, pixel height)
    #win.setBackground("ivory")
    win.setCoords(0,0, 100, 100) #make the window 100 by 100 in order to more easily set size/location of objects
    myImage = Image(Point(20,40), "MARBLES.PPM")
   # myImage.se
    myImage.draw(win)

    R1 = Rectangle(Point(5,98), Point(95, 43)) #Outline that helps break up the graphic window
    R1.setFill("black")
    R1.draw(win)

    winR1 = Rectangle(Point(5,39), Point(45,5)) #Left one
    winR1.setFill("lavender")
    winR1.draw(win)
    R3 = Rectangle(Point(55,39), Point(95,5)) #Right one
    R3.setFill("lavender")
    R3.draw(win)

    liveTitle = Text(Point(50,36), "Lives: 3")
    liveTitle.draw(win)

    Title = Text(Point(50, 95), "Hand Therapy Exercises")
    Title.draw(win)
    Title2 = Text(Point(25, 36), "Exercise:")
    Title2.draw(win)
    Title3 = Text(Point(75, 36), "Exercise:")
    Title3.draw(win)
    print "true"

    player = Player(win, Point(10,45))

    bQuit = Button(win, Point(50, 7), 6, 3, "Quit") #Quit button
    bQuit.setFillGrey()

    enemies = []
    enemies.append( Enemy(win, player) )

    thread.start_new_thread(gitMotion, ())

    epoch = time.time()
    loop = True
    while loop == True: #repeat this loop for as long as the "end" statment is not read
        clickmaster = win.checkMouse() #check last click
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        movePlayer(player,0.005)
        for anEnemy in enemies:
            anEnemy.travel(0.005)

        print "motion"
        print motion

        #player.move(0.01,0)
        if clickmaster != None:
            player.move(5,0)
        if clickmaster != None and bQuit.clicked(clickmaster): #if Quit button is clicked: close the window and shut down the program
            casenum = -1 #tell other threads that they can close
            win.close()
            sys.exit()
        enemies = [anEnemy for anEnemy in enemies if anEnemy.isAlive()]
        for anEnemy in enemies:
            if time.time() > shielded and haveCollided(player,anEnemy):
                print "collided"
                lives -= 1
                shielded = time.time()+3 #second invicibility

                if lives < 1:
                    exitProgram(win)
        if bEasyMode.isChecked() or time.time() < epoch + 10.0:
            if len(enemies) < 1:
                enemies.append( Enemy(win, player) )
        elif len(enemies) < 2:
            enemies.append( Enemy(win, player) )

loopNumber = 0

def haveCollided(player, anEnemy):
    enCen = anEnemy.circle.getCenter()
    enRad = anEnemy.circle.getRadius()
    plaCen = player.getCenter()
    plW = fabs(player.getP1().getX()-player.getP2().getX())
    plH = fabs(player.getP1().getY()-player.getP2().getY())
    heightWithin = False
    widthWithin = False
    if (enCen.getY() >= plaCen.getY() and enCen.getY() - enRad < plaCen.getY() + 0.5*plH): #enemy on top
        heightWithin = True
    elif enCen.getY() <= plaCen.getY() and enCen.getY() + enRad > plaCen.getY() - 0.5*plH: #player on top
        heightWithin = True

    if (enCen.getX() >= plaCen.getX() and enCen.getX() - enRad < plaCen.getX() + 0.5*plW): #enemy on right
        widthWithin = True
    elif enCen.getX() <= plaCen.getX() and enCen.getX() + enRad > plaCen.getX() - 0.5*plW: #player on right
        widthWithin = True

    return widthWithin and heightWithin #returns boolean. Doesn't take into account the diagonals


def movePlayer(player, displ):
    if player.getCenter().getX()+displ < 5:
        player.move(95-player.getCenter().getX(), 0)
    elif player.getCenter().getX()+displ > 95:
        player.move(player.getCenter().getX() -185, 0)
    else:
        player.move(displ,0)
def elevatePlayer(player, displ):
    if player.getCenter().getY()+displ < 48:
        player.move(0,95-player.getCenter().getY())
    elif player.getCenter().getY()+displ > 95:
        player.move(0,player.getCenter().getY() -142)
    else:
        player.move(0,displ)

shielded = 0
lives = 3
liveTitle = -1 #should be the textbox
bEasyMode = 0
#convertToPBM("65", ".txt")
main()
print "true2"