#HopHacks Spring 2016 Project
#Rahul Yerrabelli, Benjamin Pikus, Dawei Geng
#February 5th, 2016 - February 7th, 2016

from graphics import * #used for GUI

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
    win = GraphWin("Hand Analysis", 325, 200) #("name of window", pixel width, pixel height)
    win.setBackground("light blue")
    win.setCoords(0,0, 100, 100) #make the window 100 by 100 in order to more easily set size/location of objects
    Title = Text(Point(50, 75), "Enter your name below:")
    Title.draw(win)

    input_name = Entry(Point(50,50), 20) #create an entry box where the user can input characters
    input_name.setText("") #Rahul Y, For testing purposes
    input_name.draw(win)

    bUseIMU = CheckBox(win,Point(34, 27), 29, 10, "Save Name",False) #toggle
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
        elif bUseIMU.clicked(p_clickin):
            bUseIMU.toggle()
    return ( port_name, bUseIMU.isChecked() )

def main():
    print "true3"
    setPortResults = startScreen() #do this before the main loop to avoid needing to re-enter the port name every time the user decides to play again

    #Create Graphics Window and instructions
    win = GraphWin("Hand Therapy Analysis", 750, 650) #("name of window", pixel width, pixel height)
    win.setBackground("ivory")
    win.setCoords(0,0, 100, 100) #make the window 100 by 100 in order to more easily set size/location of objects
    R1 = Rectangle(Point(5,98), Point(95, 43)) #Outline that helps break up the graphic window
    R1.setFill("white")
    R1.draw(win)
    winR1 = Rectangle(Point(5,39), Point(45,5))
    winR1.setFill("lavender")
    winR1.draw(win)
    R3 = Rectangle(Point(55,39), Point(95,5))
    R3.setFill("lavender")
    R3.draw(win)
    Title = Text(Point(50, 95), "Hand Therapy Exercise")
    Title.draw(win)
    print "true"
    loop = True
    while loop == True: #repeat this loop for as long as the "end" statment is not read
        clickmaster = win.checkMouse() #check last click
        if clickmaster != None and bQuit.clicked(clickmaster): #if Quit button is clicked: close the window and shut down the program
            casenum = -1 #tell other threads that they can close
            ser.write(b'q') #send 'q' to the Arduino in order to turn off all the lights
            win.close()
            ser.close()
            if (useIMU):
                serIMU.close()
            sys.exit()

main()
print "true2"